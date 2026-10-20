#!/usr/bin/env python3
"""
humanize.py - toglie l'impronta della macchina da una bozza.

Tre passate, in quest'ordine:

  1. INVISIBILI    cancella o normalizza i caratteri che una tastiera umana non
                   produce mai: zero-width joiner, word joiner, trattini morbidi,
                   BOM, caratteri tag Unicode, spazi rigidi e stretti. Sopravvivono
                   al copia-incolla e sono il segno più meccanico di un testo
                   generato.
  2. TIPOGRAFIA    trattino lungo -> virgola, trattino medio -> trattino,
                   virgolette tipografiche (anche « ») -> dritte, puntini di
                   sospensione -> tre punti, pallino -> trattino.
  3. LESSICO       sostituisce il lessico di repertorio di slop.json con parole
                   semplici, mantenendo maiuscole e minuscole e lasciando
                   intatti i link. Usa solo le voci della lingua del testo
                   (rilevata da sola, o --lang it|en), così "innovative"
                   italiano non diventa "new".

I tic strutturali ("non è solo X, è Y", triadi, muri di hashtag) vengono
SEGNALATI, mai riscritti in automatico: cambiare la forma di una frase
richiede giudizio, quindi è un lavoro per chi scrive, non per una regex.

Uso
  python3 humanize.py bozza.txt
  python3 humanize.py bozza.txt --report
  pbpaste | python3 humanize.py - --report
  python3 humanize.py bozza.txt --json
  python3 humanize.py bozza.txt -o pulita.txt
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
AZIONI = {"delete": "eliminato", "space": "sostituito con uno spazio"}

IT_FUNC = {"il", "lo", "la", "gli", "le", "un", "una", "di", "del", "della", "che",
           "non", "è", "e", "per", "con", "sono", "ho", "hai", "ha", "mi", "ti",
           "si", "ma", "come", "più", "questo", "questa", "nel", "nella", "alla",
           "al", "se", "anche", "tuo", "tua", "perché", "cosa", "quando", "ci",
           "l", "c", "da", "in"}
EN_FUNC = {"the", "and", "of", "to", "is", "you", "that", "it", "for", "with",
           "i", "my", "your", "this", "but", "not", "are", "was", "be", "have",
           "what", "how", "on", "at", "do", "just", "a", "an", "in"}


def lingua(text, forced="auto"):
    if forced in ("it", "en"):
        return forced
    it = en = 0
    for w in re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ'’]+", text):
        for p in re.split(r"['’]", w.lower()):
            it += p in IT_FUNC
            en += p in EN_FUNC
    return "en" if en > it else "it"


def voci(lex, lang):
    """Le voci del lessico per questa lingua (senza campo lang: valgono sempre)."""
    return [e for e in lex["phrases"] + lex["words"] if e.get("lang", lang) == lang]


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    """'U+200B' -> 0x200B;  'U+E0000-U+E007F' -> (inizio, fine)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    """Sostituisce i link con dei segnaposto, così nessuna passata li riscrive."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    """Cancella o trasforma in spazio i caratteri invisibili. Restituisce (testo, occorrenze)."""
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": entry["action"]})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Ogni altro carattere Cf (di formato) è invisibile per definizione.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "altri caratteri di formato invisibili", "count": len(stray),
                     "action": "delete"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n,
                     "to": entry["to"].strip() or "(spazio)"})
        if ch == "—":
            # " parola — parola " e "parola—parola" diventano entrambi virgola + spazio.
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)      # 5–10  -> 5-10
            text = re.sub(r"\s+–\s+", ", ", text)            # usato come trattino lungo
            text = text.replace("–", "-")
        elif ch in "«»":
            # «parola» e « parola » diventano "parola".
            text = re.sub(r"«\s*", '"', text) if ch == "«" else re.sub(r"\s*»", '"', text)
        else:
            text = text.replace(ch, entry["to"])
    # Una virgola inserita prima di altra punteggiatura si legge male.
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def _lex_pattern(find):
    # (?<!\w)/(?!\w) al posto di \b: alcune voci iniziano o finiscono con
    # punteggiatura ("cosa aspetti?") o cifre ("a 360 gradi").
    return re.compile(r"(?<!\w)" + re.escape(find).replace(r"\ ", r"\s+") + r"(?!\w)",
                      re.IGNORECASE)


def pass_lexical(text, lex, lang):
    """Sostituisce parole ed espressioni di repertorio. Prima le più lunghe."""
    hits = []
    entries = sorted(voci(lex, lang), key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        find = entry["find"]
        pattern = _lex_pattern(find)
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": find, "replace": entry["replace"] or "(eliminato)",
                     "count": len(found), "family": entry["family"]})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    # Pulizia dopo le cancellazioni. Togliere una frase intera lascia
    # punteggiatura orfana ("sistema. ." o una riga che inizia con una virgola),
    # e si legge peggio del testo di partenza.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:]+[ \t]*)+", "", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)       # lo spazio lasciato da una
                                                      # cancellazione. I rientri più
                                                      # profondi sono voluti.
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)      # un trattino lungo diventato
                                                      # virgola, poi la frase dopo è sparita
    text = text.replace("...", "\x00ELL\x00")          # protegge i veri puntini
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = re.sub(r"\.\s*[!?]+(?=\s|$)", ".", text)  # "aspettiamo.!" dopo una cancellazione
    text = text.replace("\x00ELL\x00", "...")
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Un trattino lungo diventato virgola, seguito da un connettivo, lascia una
    # frase incollata ("è importante, anche, è la prova"). La si chiude col punto.
    text = re.sub(r",\s*(also|so|still|basically|in the end|anche|quindi|comunque|"
                  r"praticamente|alla fine|inoltre)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    # Anche l'uniformità della lunghezza delle frasi è strutturale.
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "name": f"Frasi tutte della stessa lunghezza (variazione {cv:.2f})",
                "count": len(lens),
                "fix": "Spezza una frase a metà. Lasciane correre un'altra. Le macchine scrivono uniforme.",
            })
    return flags


def restore_capitals(original, text):
    """Cancellare un'apertura lascia la parola dopo in minuscolo.

    Si sistema solo per chi scrive le frasi con la maiuscola: una voce tutta in
    minuscolo è uno stile, non un difetto, e sovrascriverla sarebbe proprio il
    genere di cosa che questo script esiste per evitare.
    """
    starts = re.findall(r"(?:^|[.!?]\s+|\n)\s*([A-Za-zÀ-ÖØ-öø-ÿ])", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    return re.sub(r"(?:^|(?<=[.!?] )|(?<=[.!?]\n)|(?<=\n))\s*([a-zà-öø-ÿ])",
                  lambda m: m.group(0)[:-1] + m.group(1).upper(), text)


def humanize(text, lex, lang="auto"):
    lang = lingua(text, lang)
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex, lang)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "structures": scan_structures(text, lex),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + sum(h["count"] for h in report["lexical"])

    head("RAPPORTO HUMANIZE")
    print(f"{total} artefatti della macchina rimossi, "
          f"{len(report['structures'])} tic strutturali da riscrivere a mano", file=out)

    if report["invisible"]:
        head("1. CARATTERI INVISIBILI")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {AZIONI.get(h['action'], h['action'])}",
                  file=out)
    if report["typographic"]:
        head("2. TIPOGRAFIA")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. LESSICO DI REPERTORIO")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["structures"]:
        head("4. TIC STRUTTURALI  (non corretti in automatico, riscrivili tu)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("PULITO")
        print("  Niente da togliere.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Toglie l'impronta della macchina da una bozza.")
    ap.add_argument("input", nargs="?", default="-", help="file, oppure - per stdin")
    ap.add_argument("-o", "--out", help="scrive qui il testo pulito invece che su stdout")
    ap.add_argument("--report", action="store_true", help="stampa cosa è cambiato, su stderr")
    ap.add_argument("--json", action="store_true", help="emette {text, report} in JSON")
    ap.add_argument("--lexicon", default=LEX, help="percorso di slop.json")
    ap.add_argument("--lang", default="auto", choices=["auto", "it", "en"],
                    help="lingua del testo (default: rilevata)")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex, args.lang)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"scritto {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
