#!/usr/bin/env python3
"""
hookscore.py - dà un punteggio alla prima riga di un Reel sulle cinque cose che
gli hook forti hanno in comune, e mette in classifica un gruppo di hook.

Cos'è:  cinque euristiche locali, calcolate sul tuo computer dal solo testo.
Misurano proprietà che gli hook che tengono l'attenzione tendono ad avere:
una durata che si dice in meno di tre secondi, un elemento concreto, qualcosa
in gioco, il contenuto all'inizio e non alla fine, uno spettatore a cui parlare.

Cosa NON è:  un predittore di visualizzazioni. La versione originale (inglese)
è stata provata su 74 hook reali, trascritti dai primi tre secondi degli otto
video migliori e degli otto peggiori di cinque canali. Distinguere un hook vero
da uno scritto apposta male le riesce bene: AUC 0,83, e 9 hook "cattivi" su 10
sono finiti sotto la mediana di quelli veri. Distinguere i successi di un
creator dai suoi flop non le riesce quasi per niente: AUC 0,56, dove 0,50 è
lanciare una moneta. I lessici italiani sono stati aggiunti a mano e NON sono
stati rivalidati su un campione italiano.

Quindi usala per quello che misura bene. Trova saluti, preamboli, hook senza
niente di concreto e hook che ci mettono cinque secondi a essere detti. Non ti
dirà quale di due hook decenti andrà più lontano, e nessuno strumento che legge
testo può farlo: lo decidono la faccia, il montaggio, l'audio e a chi Instagram
lo mostra. Fidati più del grafico di permanenza che di questo script.

Ogni controllo restituisce un valore da 0 a 100. Più alto è meglio.

Lingua: rilevata da sola (italiano o inglese); forzala con --lang it|en.
Per l'italiano la durata si stima in sillabe al secondo (default 5,8), perché
le parole al minuto sovrastimano: "di", "il", "un" si dicono in un attimo.

Uso
  python3 hookscore.py hooks.txt              # un hook per riga, in classifica
  python3 hookscore.py --hook "Ho perso 3 clienti in un mese per un form rotto."
  pbpaste | python3 hookscore.py -
  python3 hookscore.py hooks.txt --json
  python3 hookscore.py hooks.txt --lang it --sps 6.2
"""

import argparse
import json
import re
import statistics
import sys
import unicodedata

LETTERE = "A-Za-zÀ-ÖØ-öø-ÿ"
WORD_RE = re.compile(rf"[{LETTERE}0-9$€%'’-]+")
NUMBER_RE = re.compile(
    r"[$€]\s?\d[\d.,]*"                                   # soldi, con il simbolo prima
    r"|\b\d[\d.,]*\s?"                                    # una cifra, con o
    r"(?:%|€|k\b|x\b|euro\b|hrs?\b|hours?\b|mins?\b|minutes?\b"   # senza unità
    r"|days?\b|weeks?\b|months?\b|years?\b"
    r"|ore\b|ora\b|minut[oi]\b|second[oi]\b|giorn[oi]\b|settiman[ae]\b"
    r"|mes[ei]\b|ann[oi]\b|anni\b|mila\b)?",
    re.IGNORECASE)
PROPER_RE = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-ZÀ-ÖØ-Þ][a-zà-öø-ÿ]{2,}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

# Gli hook parlati dicono i numeri a voce. "Zero euro" e "ventimila" sono
# concreti quanto "0 €" e "20.000 €", e contare solo le cifre li perdeva.
# "one"/"uno" e "first"/"primo" mancano apposta: sono riempitivi molto più
# spesso che quantità. "sei" manca perché quasi sempre è "tu sei", e "mezzo"
# perché quasi sempre è "in mezzo".
SPOKEN_NUMBERS = {
    # inglese
    "zero", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "fifteen", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million",
    "billion", "dozen", "half", "twice", "triple",
    # italiano
    "due", "tre", "quattro", "cinque", "sette", "otto", "nove", "dieci",
    "undici", "dodici", "tredici", "quattordici", "quindici", "sedici",
    "diciassette", "diciotto", "diciannove", "venti", "trenta", "quaranta",
    "cinquanta", "sessanta", "settanta", "ottanta", "novanta", "cento",
    "mille", "mila", "milione", "milioni", "miliardo", "miliardi", "dozzina",
    "metà", "meta", "doppio", "triplo", "decina", "centinaia", "migliaia",
}
# "duemila", "trecento", "ventimila": i composti si riconoscono dalla coda.
SPOKEN_NUMBER_RE = re.compile(r"^\w{2,}(?:mila|cento)$")
MONEY_WORDS = {
    "dollars", "dollar", "bucks", "grand", "percent", "cents",
    "millionaire", "billionaire", "revenue", "profit", "salary", "rent",
    "euro", "centesimi", "percento", "fatturato", "stipendio", "affitto",
    "guadagno", "guadagnato", "guadagni", "profitto", "incasso", "incassato",
    "milionario", "prezzo", "preventivo", "fattura",
}

# Parole che mettono qualcosa in gioco. Un hook senza nessuna di queste è
# un'affermazione; un hook con una è un motivo per continuare a guardare.
STAKES = {
    # inglese
    "stop", "never", "wrong", "mistake", "mistakes", "lost", "lose", "losing",
    "cost", "costs", "broke", "broken", "failed", "failure", "fail", "nobody",
    "no", "not", "don't", "dont", "doesn't", "didn't", "can't", "won't",
    "quit", "quitting", "fired", "deleted", "delete", "killed", "kills", "kill",
    "replaced", "replaces", "cut", "beat", "free", "paid", "charged", "hired",
    "saved", "first",
    "banned", "illegal", "worst", "hate", "hated", "wasted", "waste", "scam",
    "lie", "lied", "lying", "truth", "secret", "hidden", "stole", "stolen",
    "before", "until", "instead", "but", "except", "unless", "problem",
    "risk", "danger", "warning", "regret", "wish", "should", "shouldn't",
    "still", "already", "only", "without", "versus", "vs", "actually",
    # italiano
    "basta", "smetti", "smettila", "smettete", "fermati", "mai", "sbagliato",
    "sbagliata", "sbagliati", "sbagliate", "sbagli", "sbagliando", "errore",
    "errori", "perso", "persa", "persi", "perse", "perdere", "perdi", "perdendo",
    "perderai", "costa", "costato", "costata", "costo", "costi", "rotto",
    "rotta", "fallito", "fallita", "fallimento", "nessuno", "nessuna", "non",
    "né", "licenziato", "cancellato", "eliminato", "eliminare", "sostituito",
    "sostituisce", "tagliato", "battuto", "gratis", "gratuito", "gratuita",
    "pagato", "pagare", "pagavo", "risparmiato", "risparmiare", "primo",
    "prima", "vietato", "illegale", "peggiore", "peggio", "odio", "odiato",
    "sprecato", "sprecati", "spreco", "truffa", "bugia", "bugie", "mentito",
    "verità", "segreto", "nascosto", "rubato", "finché", "invece", "ma",
    "però", "tranne", "problema", "rischio", "rischi", "pericolo", "attenzione",
    "rimpianto", "dovresti", "dovreste", "ancora", "già", "solo", "soltanto",
    "senza", "contro", "davvero", "realtà", "paura", "ansia", "colpa",
    "fatica", "difficile", "ritardo", "tardi", "troppo",
}

# Aperture che spendono il primo secondo per non dire niente.
WEAK_OPENERS = [
    # inglese
    "so", "ok", "okay", "hey", "hi", "hello", "guys", "yo", "alright",
    "welcome", "today", "basically", "honestly", "look", "listen", "um",
    "just", "let", "lets", "let's", "i wanted", "i want", "one of",
    "have you", "did you", "do you", "are you", "in this", "in today",
    "the thing", "a lot", "there is", "there are", "this is", "it is",
    "as a", "when it", "if you've", "you know",
    # italiano
    "allora", "dunque", "bene", "ciao", "ehi", "ehilà", "salve", "ragazzi",
    "buongiorno", "buonasera", "benvenuti", "benvenute", "bentornati",
    "eccoci", "oggi", "praticamente", "sinceramente", "ascoltate", "ascolta",
    "ehm", "uhm", "volevo", "vorrei", "voglio parlarvi", "voglio parlarti",
    "uno dei", "una delle", "avete mai", "vi siete", "in questo", "nel video",
    "la cosa", "c'è", "ci sono", "questo è", "questa è", "è importante",
    "quando si", "come sapete", "come sai", "sapete", "parliamo",
]

# Imperativi che si guadagnano la prima posizione.
IMPERATIVES = {
    "stop", "steal", "copy", "delete", "try", "watch", "read", "save",
    "use", "build", "make", "write", "send", "take", "start", "quit",
    "never", "always", "don't", "dont", "do", "put", "run", "check",
    "smetti", "smettila", "smettete", "basta", "fermati", "ruba", "rubate",
    "copia", "copiate", "cancella", "elimina", "prova", "provate", "guarda",
    "guardate", "leggi", "salva", "salvate", "usa", "usate", "costruisci",
    "fai", "fate", "scrivi", "scrivete", "manda", "mandate", "prendi",
    "inizia", "comincia", "mai", "sempre", "non", "metti", "togli",
    "controlla", "evita", "dimentica", "lascia", "commenta", "segna",
}

DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:stop scrolling|don'?t scroll|smetti di scorrere|"
                r"non scorrere|non scrollare|aspetta[,.]? non scorrere)"),
     "Apre con \"non scorrere\". Chiedere attenzione dimostra che non te la sei guadagnata."),
    (re.compile(r"(?i)\b(?:in (?:this|today'?s) (?:video|reel)|i'?m going to show you|"
                r"i'?ll show you how|in questo (?:video|reel)|nel (?:video|reel) di oggi|"
                r"oggi (?:ti|vi) (?:mostro|parlo|faccio vedere|spiego)|"
                r"(?:ti|vi) faccio vedere come|voglio parlar(?:vi|ti) di)\b"),
     "Preambolo da video. Cancellalo e apri direttamente sul punto."),
    (re.compile(r"(?i)^\s*(?:hey |hi |what'?s up |welcome |ciao\b|ehi\b|ehilà\b|salve\b|"
                r"buongiorno\b|buonasera\b|benvenut[ie]\b|bentornat[ie]\b)"),
     "Saluto. Nessuno è venuto nel feed per farsi salutare."),
    (HASHTAG_RE,
     "Hashtag nell'hook. Gli hashtag vanno in fondo alla didascalia, se proprio."),
    (EMOJI_RE,
     "Emoji nell'hook. Il testo a schermo, alla dimensione di un hook, ha spazio "
     "per parole o per un'emoji, non per entrambe."),
]

# Parole funzione per capire la lingua senza dipendenze.
IT_FUNC = {"il", "lo", "la", "gli", "le", "un", "una", "uno", "di", "del", "della",
           "che", "non", "è", "e", "per", "con", "sono", "ho", "hai", "ha", "mi",
           "ti", "si", "ma", "come", "più", "questo", "questa", "nel", "nella",
           "alla", "al", "se", "anche", "tuo", "tua", "perché", "cosa", "quando",
           "dei", "delle", "ci", "vi", "l", "un'", "c", "sei", "da", "in"}
EN_FUNC = {"the", "and", "of", "to", "is", "you", "that", "it", "for", "with",
           "i", "my", "your", "this", "but", "not", "are", "was", "be", "have",
           "what", "how", "on", "at", "do", "don't", "just", "a", "an", "in"}

SPS_IT = 5.8             # sillabe al secondo, italiano parlato in camera
WPS_EN = 2.75            # parole al secondo, inglese (~165 al minuto)


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    # "18.000 €" e "$18,000" si dicono come una parola sola, quindi qui sono
    # una parola sola. Si tolgono i separatori delle migliaia tra cifre.
    return WORD_RE.findall(re.sub(r"(?<=\d)[.,](?=\d{3}\b)", "", text))


def parts(token):
    """'l'errore' -> ['l', 'errore'];  'don't' resta com'è più i pezzi."""
    t = token.lower().strip("'’-")
    bits = [b for b in re.split(r"['’]", t) if b]
    return [t] + bits if len(bits) > 1 else [t]


def lingua(text, forced="auto"):
    if forced in ("it", "en"):
        return forced
    it = en = 0
    for w in words(text):
        for p in parts(w):
            it += p in IT_FUNC
            en += p in EN_FUNC
    return "en" if en > it else "it"


def _senza_accenti(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def sillabe(token):
    """Stima delle sillabe di una parola italiana. Approssimata, e va bene così."""
    t = _senza_accenti(token.lower())
    cifre = re.sub(r"\D", "", t)
    if cifre:
        n = len(cifre)
        s = {1: 2, 2: 3, 3: 4, 4: 5}.get(n, n + 1)
        if "€" in token or "$" in token:
            s += 2
        if "%" in token:
            s += 3
        return s
    gruppi = re.findall(r"[aeiouy]+", t)
    return max(1, sum(1 if len(g) < 3 else 2 for g in gruppi))


def secondi(text, lang, sps=SPS_IT, wps=WPS_EN):
    w = words(text)
    if lang == "it":
        return sum(sillabe(x) for x in w) / sps
    return len(w) / wps


def is_spoken_number(tok):
    return tok in SPOKEN_NUMBERS or bool(SPOKEN_NUMBER_RE.match(tok))


def check_length(text, lang, sps):
    """Un hook deve arrivare prima che il pollice si muova. Circa due secondi."""
    w = words(text)
    n = len(w)
    secs = secondi(text, lang, sps)
    # Il punteggio ragiona in "parole equivalenti" a 2,75 al secondo, così le
    # due lingue hanno la stessa scala: 5-12 equivale a ~1,8-4,4 secondi.
    eq = secs * WPS_EN
    chars = len(text.strip())
    if 5 <= eq <= 12:
        score = 100.0
    elif eq < 5:
        score = clamp(100 - (5 - eq) * 20)
    else:
        score = clamp(100 - (eq - 12) * 11)
    if chars > 60:                       # due righe di testo grande a schermo
        score -= 12
    return clamp(score), f"{n} parole, {chars} caratteri, ~{secs:.1f}s a voce (ideale 2-4s)"


def check_specificity(text, lang):
    """Una cosa concreta batte tre astratte."""
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    propers = set(PROPER_RE.findall(text))
    low = [p for w in words(text) for p in parts(w)[-1:]]
    spoken = [w for w in low if is_spoken_number(w) or w in MONEY_WORDS]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    lab = "elemento concreto" if hits == 1 else "elementi concreti"
    return score, (f"{hits} {lab}" + (f": {found}" if found else
                   " - nessun numero, nessun nome, niente di verificabile"))


def check_stakes(text, lang):
    """Tensione, costo, negazione. Qualcosa che lo spettatore potrebbe perdere."""
    hits = []
    for w in words(text):
        for p in parts(w):
            if p in STAKES:
                hits.append(p)
                break
    markers = sorted(set(hits))
    if re.search(r"[$€]\s?\d|\d\s?(?:€|euro\b)", text, re.IGNORECASE):
        markers.append("un prezzo")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    lab = "segnale di tensione" if n == 1 else "segnali di tensione"
    detail = f"{n} {lab}" + (f": {', '.join(markers[:4])}" if markers else
                                           " - in questa riga non c'è niente in gioco")
    return clamp(score), detail


def check_frontload(text, lang):
    """La parola interessante non può stare in nona posizione."""
    w = words(text)
    if not w:
        return 0.0, "vuoto"
    low = [x.lower().strip("'’") for x in w]
    opener = " ".join(low[:2])
    penalty = 0
    hit_opener = None
    for weak in WEAK_OPENERS:
        if opener.startswith(weak) or low[0] == weak:
            penalty, hit_opener = 30, weak
            break
    payload = None
    for i, token in enumerate(low):
        pz = parts(token)
        if (any(p in STAKES or is_spoken_number(p) or p in MONEY_WORDS for p in pz)
                or NUMBER_RE.match(w[i]) or (i and PROPER_RE.match(w[i]))):
            payload = i
            break
    if payload is None:
        base = 30.0
        where = "nessuna parola-chiave in tutta la riga"
    elif payload <= 3:
        base = 100.0
        where = f"parola-chiave alla posizione {payload + 1}"
    elif payload <= 6:
        base = 70.0
        where = f"parola-chiave alla posizione {payload + 1}, si può anticipare"
    else:
        base = 40.0
        where = f"parola-chiave alla posizione {payload + 1}, troppo tardi"
    detail = where + (f"; apertura debole \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


IT_SECONDA = re.compile(
    r"\b(?:tu|ti|te|tuo|tua|tuoi|tue|voi|vi|ve|vostr[oaie]|hai|sei|puoi|devi|"
    r"vuoi|sai|fai|stai|avete|siete|potete|dovete|volete|sapete|fate|state)\b")
IT_PRIMA = re.compile(r"\b(?:io|mi|me|mio|mia|miei|mie|noi|ci|ce|nostr[oaie]|ho|abbiamo)\b")


def check_address(text, lang):
    """Rivolto a uno spettatore, o sospeso nel vuoto."""
    low = text.lower()
    w = [x.lower().strip("'’") for x in words(text)]
    if (re.search(r"\b(you|your|you're|youre|yourself)\b", low)
            or IT_SECONDA.search(low)):
        return 100.0, "parla allo spettatore"
    if w and parts(w[0])[-1] in IMPERATIVES:
        return 90.0, f"apre con un imperativo (\"{w[0]}\")"
    if re.search(r"\b(i|my|me|we|our)\b", low) or IT_PRIMA.search(low):
        return 70.0, "prima persona, nessuno spettatore chiamato in causa"
    return 35.0, "terza persona, non c'è nessuno nella stanza"


CHECKS = ["DURATA", "CONCRETEZZA", "TENSIONE", "ATTACCO", "DESTINATARIO"]


def run(text, lang="auto", sps=SPS_IT):
    lang = lingua(text, lang)
    results = {
        "DURATA": check_length(text, lang, sps),
        "CONCRETEZZA": check_specificity(text, lang),
        "TENSIONE": check_stakes(text, lang),
        "ATTACCO": check_frontload(text, lang),
        "DESTINATARIO": check_address(text, lang),
    }
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # La proprietà più debole fa da tetto, come in detect.py: ne basta una
    # sbagliata perché il pollice continui a scorrere.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "FORTE" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "DEBOLE")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nPUNTEGGIO HOOK", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'TOTALE':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    for f in flags:
        print(f"\n  BLOCCANTE  {f}", file=out)
    if verdict != "FORTE":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Proprietà più debole: {weakest}. Sistema quella e rilancia.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nCLASSIFICA HOOK\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<7} {hook}", file=out)
        print(f"        più debole: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})",
              file=out)
        for f in r["flags"]:
            print(f"        bloccante: {f}", file=out)
    print("\nGira il primo. Se il primo è sotto 50, nessuno di questi è l'hook.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Punteggio di un hook da Reel su cinque proprietà.")
    ap.add_argument("input", nargs="?", default="-", help="file con un hook per riga, oppure -")
    ap.add_argument("--hook", help="valuta un solo hook passato da riga di comando")
    ap.add_argument("--lang", default="auto", choices=["auto", "it", "en"],
                    help="lingua del testo (default: rilevata)")
    ap.add_argument("--sps", type=float, default=SPS_IT,
                    help=f"sillabe al secondo per l'italiano (default {SPS_IT})")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("niente da valutare", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line, args.lang, args.sps)
        payload.append({
            "hook": line,
            "lang": lingua(line, args.lang),
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0], args.lang, args.sps)
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
