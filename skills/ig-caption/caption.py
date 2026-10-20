#!/usr/bin/env python3
"""
caption.py - controlla una didascalia Instagram e mostra esattamente cosa vede
il feed prima del "... altro".

Instagram mostra circa 125 caratteri di didascalia nel feed e nasconde il resto
dietro un tocco. Quasi ogni didascalia che non funziona si rompe lì: l'hook è
nella terza frase, la prima riga è un saluto, o tutto si apre con un hashtag.
Lo script stampa la finestra visibile in un riquadro, così la leggi come la
legge uno sconosciuto che scorre, poi fa i nove controlli che vale la pena fare.

Il taglio a 125 caratteri è un'approssimazione. Il numero vero cambia con il
telefono, la dimensione del carattere e dove cadono gli a capo, ed è proprio
per questo che serve un margine e non una didascalia studiata per finire a 125.
Cambialo con --truncate se vuoi provarne uno più stretto.

Le richieste all'azione si riconoscono in italiano e in inglese:
"Commenta SCHEDA", "Scrivimi CRESCITA", "Scrivi ACQUA nei commenti",
"scrivimi in DM", "salvalo", "link in bio", "comment KEYWORD", "DM me"...

Uso
  python3 caption.py didascalia.txt
  python3 caption.py didascalia.txt --keywords "tutor dsa vicenza,metodo di studio"
  pbpaste | python3 caption.py -
  python3 caption.py didascalia.txt --json
"""

import argparse
import json
import re
import sys
import textwrap

LIMIT = 2200             # Limite massimo di Instagram per una didascalia.
TRUNCATE = 125           # Più o meno dove il feed taglia con "... altro".
HASHTAG_LIMIT = 5        # Il tetto di Instagram per post o reel dal 18 dicembre
                         # 2025 (prima erano 30). Annunciato dall'account
                         # @Creators: usare meno hashtag (fino a 5) e più mirati
                         # al posto di tanti generici può migliorare sia il
                         # rendimento dei contenuti sia l'esperienza delle persone.

HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[A-Za-z0-9_.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:com|co|io|net|org|ai|app|it|eu|info|shop|store)\b(?:/\S*)?",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
CONCRETE_RE = re.compile(
    r"[$€]\s?\d|\b\d[\d,.]*\b|(?<!^)(?<![.!?]\s)\b[A-ZÀ-ÖØ-Þ][a-zà-öø-ÿ]{2,}\b",
    re.MULTILINE)
# Numeri detti a parole ("quattro domande"), che contano come una cifra.
SPOKEN_NUM = re.compile(
    r"\b(?:two|three|four|five|seven|eight|nine|ten|twenty|hundred|thousand|"
    r"due|tre|quattro|cinque|sette|otto|nove|dieci|dodici|quindici|venti|trenta|"
    r"quaranta|cinquanta|cento|mille|\w{2,}mila|\w{2,}cento|milioni|metà)\b", re.IGNORECASE)

# La parola chiave da commentare va scritta in MAIUSCOLO: è così che la si
# riconosce, e così la riconosce anche chi legge.
PAROLA = r"[\"«“']?[A-ZÀ-Ý0-9]{3,}\b"
ASKS = [
    (re.compile(r"(?i:\bcomment(?:a|ate)?\s+(?:the word |la parola |qui |sotto )?)" + PAROLA
                + r"|(?i:\bscriv(?:i|ete)(?:mi|ci)?\s+(?:la parola |qui |sotto )?)" + PAROLA
                + r"|(?i:\b(?:lascia|lasciate)\s+(?:la parola |un )?)" + PAROLA + r"(?i:\s+nei commenti)"),
     "commenta una parola chiave"),
    (re.compile(r"(?i)\b(?:dm|message) me\b|\bscriv(?:i|ete)(?:mi|ci) (?:in |un )?(?:dm|direct|privato|messaggio)\b"
                r"|\bmanda(?:mi|teci|ci|temi)? un (?:dm|messaggio|direct)\b|\bin direct\b"),
     "scrivimi in DM"),
    (re.compile(r"(?i)\bsave (?:this|it)\b|\bsalva(?:lo|la|telo|tela|te)?\b(?! [a-z]+ (?:vita|pelle))"),
     "salva"),
    (re.compile(r"(?i)\bshare (?:this|it)\b|\bcondividi(?:lo|la|telo)?\b|\bmanda(?:lo|la|telo) a\b"
                r"|\bgira(?:lo|la|telo) a\b"),
     "condividi"),
    (re.compile(r"(?i)\bfollow (?:me|for)\b|\bseguimi\b|\bseguici\b|\bsegui(?:teci|temi)?\b(?= per)"),
     "segui"),
    (re.compile(r"(?i)\blink in (?:my )?bio\b|\blink nella bio\b"),
     "link in bio"),
    (re.compile(r"(?i)\b(?:swipe|tap) (?:through|left|right|for|to)\b|\bscorri\b|\bsfoglia\b"),
     "scorri"),
    (re.compile(r"(?i)\btell me\b|\bwhat would you\b|\bwhich one\b|\bdimmi\b|\bditemi\b|\braccontami\b"
                r"|\braccontateci\b|\bfammi sapere\b|\bfatemi sapere\b|\btu (?:cosa|come)\b[^?\n]{0,40}\?"
                r"|\bquale (?:scegli|preferisci)\b"),
     "rispondi a una domanda"),
    (re.compile(r"(?i)\bprenota(?:te)?\b|\bchiama(?:ci|teci)?\b|\bvieni a trovarci\b|\bpassa(?:te)? a trovarci\b"),
     "prenota o vieni"),
]

FILLER_TAGS = {"#viral", "#fyp", "#explore", "#explorepage", "#foryou", "#foryoupage",
               "#trending", "#instagood", "#love", "#follow", "#like4like", "#reels",
               "#reelsinstagram", "#viralreels", "#instadaily",
               "#perte", "#neiperte", "#virale", "#seguimi", "#followme", "#instaitalia",
               "#italia", "#reelsitalia", "#tendenze", "#esplora", "#likeforlike",
               "#photooftheday", "#picoftheday"}


def visible_window(text, cut):
    """Cosa mostra il feed. Instagram taglia a metà parola, quindi anche qui."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  COSA MOSTRA IL FEED", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... altro" if truncated else "(la didascalia ci sta tutta)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    text = text.rstrip()
    stripped = text.strip()
    chars = len(stripped)
    lines = [l for l in stripped.split("\n")]
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = [name for pattern, name in ASKS if pattern.search(stripped)]
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("LUNGHEZZA", "ERRORE" if chars > LIMIT else "OK",
        f"{chars} / {LIMIT} caratteri" + (f", {chars - LIMIT} oltre il limite"
                                          if chars > LIMIT else ""))

    if not first_line:
        add("PRIMA RIGA", "ERRORE", "la didascalia si apre con una riga vuota")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("PRIMA RIGA", "ERRORE",
            "si apre con un hashtag o una menzione, cioè sprecando l'unica posizione che vale una frase")
    elif re.match(r"(?i)^\W*(?:ciao|buongiorno|buonasera|salve|ehi|hey|hi|hello)\b", first_line):
        add("PRIMA RIGA", "ATTENZIONE", "si apre con un saluto: nessuno scorre il feed per farsi salutare")
    elif len(first_line) > cut:
        add("PRIMA RIGA", "ATTENZIONE",
            f"{len(first_line)} caratteri, quindi viene tagliata a {cut} a metà pensiero. "
            "Va bene se il taglio crea attesa, male se cade in mezzo a una subordinata")
    else:
        add("PRIMA RIGA", "OK", f"{len(first_line)} caratteri, si legge intera")

    nconc = len(CONCRETE_RE.findall(window)) + len(SPOKEN_NUM.findall(window))
    add("HOOK CONCRETO", "OK" if nconc else "ATTENZIONE",
        (f"{nconc} numero o nome" if nconc == 1 else f"{nconc} numeri o nomi")
        + " nella parte visibile"
        + ("" if nconc else " - niente di verificabile prima del tocco"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAG", "ERRORE", f"{len(tags)} hashtag, oltre il tetto di {HASHTAG_LIMIT} di Instagram. "
                                 "Quelli dopo il quinto non contano e il blocco sembra vecchio")
    elif len(tags) == HASHTAG_LIMIT and filler:
        add("HASHTAG", "ATTENZIONE", f"{len(tags)} hashtag, al tetto, e "
                                     f"{len(filler)} generici. Usa i cinque per gli argomenti")
    elif filler:
        add("HASHTAG", "ATTENZIONE", f"{len(tags)} hashtag, {len(filler)} generici "
                                     f"({', '.join(filler[:3])}). Quelli non descrivono niente")
    else:
        add("HASHTAG", "OK", f"{len(tags)} hashtag" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("POSIZIONE TAG", "OK", "nessun hashtag da posizionare")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"(?!\w)", window) for t in tags):
        add("POSIZIONE TAG", "ATTENZIONE", "un hashtag è nella parte visibile, "
                                           "e spreca spazio del feed per un'etichetta")
    else:
        add("POSIZIONE TAG", "OK", "gli hashtag sono sotto il taglio")

    add("LINK", "ATTENZIONE" if links else "OK",
        f"{len(links)} link nella didascalia, e le didascalie non sono cliccabili. "
        f"Spostalo in bio o in DM" if links else "nessun link morto nel testo")

    if len(asks) == 1:
        add("UNA RICHIESTA", "OK", f"una sola richiesta: {asks[0]}")
    elif not asks:
        add("UNA RICHIESTA", "ATTENZIONE", "nessuna richiesta. Decidi a cosa serve questo post")
    else:
        add("UNA RICHIESTA", "ATTENZIONE", f"{len(asks)} richieste ({', '.join(asks)}). "
                                           "Due richieste valgono quanto nessuna")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJI", "ATTENZIONE" if density > 4 else "OK",
        f"{len(emoji)} emoji, {density:.1f} ogni 100 caratteri"
        + (" - sembrano decorazione" if density > 4 else ""))

    if keywords:
        low = stripped.lower()
        found = [k for k in keywords if k.lower() in low]
        missing = [k for k in keywords if k.lower() not in low]
        in_window = [k for k in found if k.lower() in window.lower()]
        status = "OK" if not missing else ("ATTENZIONE" if found else "ERRORE")
        add("TERMINI DI RICERCA", status,
            f"{len(found)}/{len(keywords)} presenti"
            + (f", {len(in_window)} nella parte visibile" if found else "")
            + (f". Mancano: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "ERRORE")
    warns = sum(1 for c in checks if c["status"] == "ATTENZIONE")
    verdict = "DA SISTEMARE" if fails else ("DA RIVEDERE" if warns else "PRONTA")

    return {
        "characters": chars, "limit": LIMIT, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


def render(a, out=sys.stdout):
    head = (f"CONTROLLO DIDASCALIA  ·  {a['characters']} / {a['limit']} caratteri  ·  "
            f"{len(a['hashtags'])} hashtag  ·  {len(a['asks'])} "
            + ("richiesta" if len(a['asks']) == 1 else "richieste"))
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<10} {c['check']:<19} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  VERDETTO  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Controlla una didascalia Instagram.")
    ap.add_argument("input", nargs="?", default="-", help="file della didascalia, oppure - per stdin")
    ap.add_argument("--truncate", type=int, default=TRUNCATE,
                    help=f"caratteri mostrati prima di '... altro' (default {TRUNCATE})")
    ap.add_argument("--keywords", default="",
                    help="termini per cui vuoi essere trovato, separati da virgola")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "PRONTA" else 1)


if __name__ == "__main__":
    main()
