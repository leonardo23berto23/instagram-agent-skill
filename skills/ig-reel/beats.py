#!/usr/bin/env python3
"""
beats.py - trasforma il copione di un Reel in una scaletta con i tempi, prima
di registrarlo.

Stima quanto ci vuole a dire ogni riga, le mette in fila con i timecode e
segnala le quattro cose che ammazzano un Reel al montaggio: un hook che va
oltre i tre secondi, un passaggio abbastanza lungo da far andare via chi
guarda, una serie di righe senza niente di concreto, e una durata totale che
non corrisponde a quella che volevi.

I tempi sono una stima, non un sostituto della registrazione, ma bastano per
pianificare il montaggio.
  - Italiano: si contano le sillabe (default 5,8 al secondo). Le parole al
    minuto sovrastimano l'italiano, pieno di parole brevi come "di", "il", "un".
  - Inglese: si contano le parole (default 165 al minuto), come l'originale.
Tarali sulla tua voce: leggi un copione ad alta voce, cronometra, e passa
--sps (italiano) o --wpm (inglese). La maggior parte delle persone in camera
sta tra 5,5 e 7 sillabe al secondo.

Lingua: rilevata da sola; forzala con --lang it|en.

Uso
  python3 beats.py copione.txt
  python3 beats.py copione.txt --target 30
  python3 beats.py copione.txt --sps 6.3 --target 45
  python3 beats.py script.txt --lang en --wpm 185
  pbpaste | python3 beats.py -
  python3 beats.py copione.txt --json
"""

import argparse
import json
import re
import sys
import unicodedata

LETTERE = "A-Za-zÀ-ÖØ-öø-ÿ"
WORD_RE = re.compile(rf"[{LETTERE}0-9$€%'’-]+")
SENT_RE = re.compile(r"[^.!?]+[.!?]*")
CONCRETE_RE = re.compile(
    r"[$€]\s?\d|\b\d[\d,.]*\b|(?<!^)(?<![.!?]\s)\b[A-ZÀ-ÖØ-Þ][a-zà-öø-ÿ]{2,}\b",
    re.MULTILINE)
SPOKEN_NUMBERS = {
    "zero", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "fifteen", "twenty", "thirty", "forty", "fifty",
    "hundred", "thousand", "million", "half", "twice",
    "due", "tre", "quattro", "cinque", "sette", "otto", "nove", "dieci",
    "undici", "dodici", "quindici", "venti", "trenta", "quaranta", "cinquanta",
    "sessanta", "settanta", "ottanta", "novanta", "cento", "mille", "mila",
    "milione", "milioni", "metà", "doppio", "triplo", "euro",
}
SPOKEN_NUMBER_RE = re.compile(r"^\w{2,}(?:mila|cento)$")
STOPWORDS = {
    # inglese
    "the", "a", "an", "and", "or", "but", "if", "of", "to", "in", "on", "for",
    "with", "that", "this", "it", "is", "are", "was", "were", "be", "been",
    "you", "your", "i", "my", "me", "we", "our", "they", "them", "he", "she",
    "so", "just", "not", "no", "do", "did", "does", "have", "has", "had",
    "will", "can", "at", "as", "by", "from", "out", "up", "off", "one", "all",
    # italiano
    "il", "lo", "la", "i", "gli", "le", "l", "un", "uno", "una", "di", "da",
    "con", "su", "per", "tra", "fra", "e", "ed", "o", "ma", "se", "che", "non",
    "è", "sono", "ho", "hai", "ha", "abbiamo", "mi", "ti", "ci", "vi", "si",
    "ne", "del", "della", "dei", "delle", "dello", "degli", "al", "alla",
    "ai", "alle", "nel", "nella", "nei", "nelle", "sul", "sulla", "questo",
    "questa", "questi", "queste", "quello", "quella", "tuo", "tua", "tuoi",
    "tue", "mio", "mia", "come", "più", "anche", "poi", "già", "così", "solo",
    "quando", "cosa", "chi", "io", "tu", "noi", "voi", "lui", "lei", "loro",
    "c", "era", "sei", "fa", "fare", "uno", "ogni", "molto", "tutto", "tutti",
}
IT_FUNC = {"il", "lo", "la", "gli", "le", "un", "una", "di", "del", "della", "che",
           "non", "è", "e", "per", "con", "sono", "ho", "hai", "ha", "mi", "ti",
           "si", "ma", "come", "più", "questo", "questa", "nel", "nella", "alla",
           "al", "se", "anche", "tuo", "tua", "perché", "cosa", "quando", "ci",
           "l", "c", "da", "in"}
EN_FUNC = {"the", "and", "of", "to", "is", "you", "that", "it", "for", "with",
           "i", "my", "your", "this", "but", "not", "are", "was", "be", "have",
           "what", "how", "on", "at", "do", "just", "a", "an", "in"}

HOOK_WINDOW = 3.0        # secondi. Oltre, il pollice ha già deciso.
MAX_BEAT = 4.0           # secondi su un'idea sola senza che cambi niente a schermo.
ABSTRACT_RUN = 3         # passaggi di fila senza niente di verificabile.
SPS_IT = 5.8
WPM_EN = 165


def words(text):
    # "18.000 €" si dice come una parola sola, quindi qui è una parola sola.
    return WORD_RE.findall(re.sub(r"(?<=\d)[.,](?=\d{3}\b)", "", text))


def parts(token):
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


class Ritmo:
    """Converte un testo in secondi, nella lingua giusta."""

    def __init__(self, lang, sps=SPS_IT, wpm=WPM_EN):
        self.lang, self.sps, self.wps = lang, sps, wpm / 60.0

    def secondi(self, text):
        w = words(text)
        if self.lang == "it":
            return sum(sillabe(x) for x in w) / self.sps
        return len(w) / self.wps

    def parole_in(self, secs, campione):
        """Quante parole stanno in `secs` secondi, al ritmo medio del copione."""
        w = words(campione)
        if not w:
            return 0
        per_parola = self.secondi(campione) / len(w)
        return int(secs / per_parola) if per_parola else 0

    def etichetta(self):
        return (f"{self.sps:g} sillabe/s" if self.lang == "it"
                else f"{self.wps * 60:g} parole/min")


def pretty(token, lang="it"):
    """Rimette il separatore delle migliaia per la visualizzazione."""
    return re.sub(r"(\d)(?=(\d{3})+$)", r"\1." if lang == "it" else r"\1,", token)


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}"


def concreti(text):
    n = len(CONCRETE_RE.findall(text))
    for w in words(text):
        p = parts(w)[-1]
        if p in SPOKEN_NUMBERS or SPOKEN_NUMBER_RE.match(p):
            n += 1
    return n


def split_beats(raw, ritmo):
    """Una riga è un passaggio, a meno che sia troppo lunga per esserlo."""
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if ritmo.secondi(line) <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        # Paragrafo lungo: spezzalo a fine frase così i tempi hanno senso.
        parts_ = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts_:
            candidate = (buf + " " + part).strip()
            if buf and ritmo.secondi(candidate) > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, wpm=WPM_EN, target=None, sps=SPS_IT, lang="auto"):
    lang = lingua(raw, lang)
    ritmo = Ritmo(lang, sps, wpm)
    beats = split_beats(raw, ritmo)
    if not beats:
        return None

    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        dur = ritmo.secondi(text)
        rows.append({
            "n": i + 1,
            "start": round(clock, 2),
            "dur": round(dur, 2),
            "words": len(words(text)),
            "text": text,
            "concrete": concreti(text),
            "label": "",
            "flags": [],
        })
        clock += dur
    total = clock

    # Etichetta le posizioni attorno a cui un Reel è costruito davvero.
    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "HOOK"
    rows[-1]["label"] = "CTA" if rows[-1]["label"] != "HOOK" else "HOOK/CTA"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "METÀ"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"l'hook dura {rows[0]['dur']:.1f}s, oltre i {HOOK_WINDOW:.0f}s")
        notes.append(f"Il passaggio 1 si dice in {rows[0]['dur']:.1f}s. Taglialo a circa "
                     f"{ritmo.parole_in(HOOK_WINDOW, rows[0]['text'])} parole, o l'hook arriva "
                     "dopo che la decisione è già stata presa.")
    if rows[0]["concrete"] == 0:
        notes.append("Il passaggio 1 non ha né un numero né un nome. Gli hook senza niente "
                     "di verificabile sono quelli che vengono scrollati.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{r['dur']:.1f}s su un solo passaggio")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        lab = "Passaggio" if len(long_beats) == 1 else "Passaggi"
        notes.append(f"{lab} {', '.join(map(str, long_beats))} oltre {MAX_BEAT:.0f}s. "
                     "Spezza la riga o cambia quello che c'è a schermo a metà. "
                     "Un'inquadratura ferma è il punto in cui la gente se ne va.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"Passaggi {start}-{r['n']} senza niente di concreto. "
                             "Metti un numero, un nome o un prezzo in uno dei tre.")
        else:
            run, start = 0, None

    # L'ultima riga riporta alla prima?
    def chiave(text):
        out = set()
        for w in words(text):
            p = parts(w)[-1]
            if p not in STOPWORDS and len(p) > 1:
                out.add(p)
        return out

    loop = sorted(pretty(w, lang) for w in chiave(rows[0]["text"]) & chiave(rows[-1]["text"]))
    if loop:
        notes.append(f"Loop: l'ultimo passaggio riprende \"{', '.join(loop[:3])}\" dall'hook. "
                     "La seconda visione è reach gratis.")
    else:
        notes.append("Nessun loop. L'ultimo passaggio non ha parole in comune con l'hook, "
                     "quindi il video finisce piatto. Ripetere una parola del passaggio 1 è "
                     "la seconda visione più economica che puoi ottenere.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"Durata in linea ({total:.1f}s contro {target:g}s).")
        elif delta > 0:
            notes.append(f"{delta:.1f}s oltre l'obiettivo. Taglia circa "
                         f"{ritmo.parole_in(delta, raw)} parole.")
        else:
            notes.append(f"{-delta:.1f}s sotto l'obiettivo. Aggiungi circa "
                         f"{ritmo.parole_in(-delta, raw)} parole, oppure giralo più corto. "
                         "Più corto di solito è giusto.")

    return {
        "lang": lang, "ritmo": ritmo.etichetta(),
        "wpm": wpm, "sps": sps, "target": target,
        "total_seconds": round(total, 2),
        "total_words": sum(r["words"] for r in rows),
        "beats": rows,
        "notes": notes,
    }


def render(a, out=sys.stdout):
    head = (f"SCALETTA  ·  {a['total_words']} parole  ·  ~{a['total_seconds']:.1f}s "
            f"a {a['ritmo']}" + (f"  ·  obiettivo {a['target']:g}s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<8}" if r["label"] else " " * 8
        print(f"  {tc(r['start'])}  {r['dur']:4.1f}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<8}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Scaletta con i tempi per il copione di un Reel.")
    ap.add_argument("input", nargs="?", default="-", help="file del copione, oppure - per stdin")
    ap.add_argument("--sps", type=float, default=SPS_IT,
                    help=f"sillabe al secondo, italiano (default {SPS_IT})")
    ap.add_argument("--wpm", type=float, default=WPM_EN,
                    help=f"parole al minuto, inglese (default {WPM_EN})")
    ap.add_argument("--lang", default="auto", choices=["auto", "it", "en"],
                    help="lingua del copione (default: rilevata)")
    ap.add_argument("--target", type=float, help="durata obiettivo in secondi")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, wpm=args.wpm, target=args.target, sps=args.sps, lang=args.lang)
    if not a:
        print("copione vuoto", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
