#!/usr/bin/env python3
"""
detect.py - un pannello di cinque controlli che misura quanto una bozza sembra
scritta da una macchina.

Cos'è:  cinque euristiche locali modellate sui segnali che i rilevatori di IA
pubblici misurano davvero: variazione nella lunghezza delle frasi, concretezza,
vocabolario di repertorio, impronta tipografica e voce. Ogni punteggio è
calcolato sul tuo computer, dal solo testo. Non viene caricato niente.

Cosa NON è:  GPTZero, Originality, Copyleaks, Winston o Turnitin. Non chiama
le loro API e non può promettere il loro verdetto. Trova le cose su cui si
basano tutti, ed è per questo che sistemarle tende a spostare anche i loro
numeri; ma l'unica affermazione onesta è quella di questa riga.

Ogni controllo restituisce un punteggio UMANO da 0 a 100. Più alto è meglio.

Lingua: rilevata da sola (italiano o inglese); forzala con --lang it|en.
In italiano il controllo VOCE non conta le contrazioni (che non esistono) ma i
segnali di parlato: "cioè", "tipo", "insomma", "boh", le persone verbali
(ho, hai, abbiamo, sei...), domande ed esclamazioni.

Uso
  python3 detect.py bozza.txt
  pbpaste | python3 detect.py -
  python3 detect.py bozza.txt --json
  python3 detect.py prima.txt dopo.txt      # confronto tra due bozze
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

LETTERE = "A-Za-zÀ-ÖØ-öø-ÿ"
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(rf"[{LETTERE}'’]+")
CONTRACTIONS = re.compile(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", re.IGNORECASE)
PRONOUNS_EN = re.compile(r"\b(i|me|my|mine|we|us|our|you|your)\b", re.IGNORECASE)
# In italiano il soggetto si sottintende: la persona sta nel verbo. Si contano
# pronomi, possessivi e le forme verbali di prima e seconda persona più comuni.
PRONOUNS_IT = re.compile(
    r"\b(?:io|me|mi|mio|mia|miei|mie|noi|ci|ce|nostr[oaie]|tu|te|ti|tuo|tua|tuoi|tue|"
    r"voi|vi|ve|vostr[oaie]|ho|hai|abbiamo|avete|sei|siamo|siete|posso|puoi|possiamo|"
    r"potete|devo|devi|dobbiamo|dovete|voglio|vuoi|vogliamo|volete|so|sai|sappiamo|"
    r"sapete|faccio|fai|facciamo|fate|vado|vai|andiamo|andate|sto|stai|stiamo|state|"
    r"dico|dici|diciamo|dite)\b", re.IGNORECASE)
# Segnali di italiano parlato. Un testo generato non dice quasi mai "boh".
PARLATO_IT = re.compile(
    r"\b(?:cioè|cioe|tipo|insomma|boh|beh|mah|ecco|dai|mica|magari|comunque|"
    r"praticamente|tra l'altro|un sacco|ok|okay|ehm|guarda|senti|figurati|"
    r"pazzesco|no\?|vero\?|giusto\?)", re.IGNORECASE)
NUMBERS = re.compile(r"\b\d[\d,.]*%?\b|[$€]\s?\d|\d\s?€")
# Numeri detti a parole: in un copione si scrive "dieci volte", non "10 volte".
# Mancano apposta "uno", "sei" (quasi sempre "tu sei") e "mezzo".
SPOKEN_NUM = re.compile(
    r"\b(?:two|three|four|five|seven|eight|nine|ten|twelve|fifteen|twenty|thirty|"
    r"fifty|hundred|thousand|million|due|tre|quattro|cinque|sette|otto|nove|dieci|"
    r"undici|dodici|quindici|venti|trenta|quaranta|cinquanta|sessanta|cento|mille|"
    r"\w{2,}mila|\w{2,}cento|milioni|metà)\b", re.IGNORECASE)
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-ZÀ-ÖØ-Þ][a-zà-öø-ÿ]{2,}\b", re.MULTILINE)

IT_FUNC = {"il", "lo", "la", "gli", "le", "un", "una", "di", "del", "della", "che",
           "non", "è", "e", "per", "con", "sono", "ho", "hai", "ha", "mi", "ti",
           "si", "ma", "come", "più", "questo", "questa", "nel", "nella", "alla",
           "al", "se", "anche", "tuo", "tua", "perché", "cosa", "quando", "ci",
           "l", "c", "da", "in"}
EN_FUNC = {"the", "and", "of", "to", "is", "you", "that", "it", "for", "with",
           "i", "my", "your", "this", "but", "not", "are", "was", "be", "have",
           "what", "how", "on", "at", "do", "just", "a", "an", "in"}


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Porta value su 0-100, dove `human` -> 100 e `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def lingua(text, forced="auto"):
    if forced in ("it", "en"):
        return forced
    it = en = 0
    for w in words(text):
        for p in re.split(r"['’]", w.lower()):
            it += p in IT_FUNC
            en += p in EN_FUNC
    return "en" if en > it else "it"


def check_burstiness(text):
    """Le persone variano molto la lunghezza delle frasi. I modelli scrivono uniforme."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "troppo corto per giudicare"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variazione {cv:.2f} su {len(lens)} frasi (meglio 0,55+)"


def check_specificity(text):
    """Numeri, nomi e cose concrete. Il testo di repertorio è astratto."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "troppo corto per giudicare"
    per100 = 100 / len(w)
    hits = (len(NUMBERS.findall(text)) + len(SPOKEN_NUM.findall(text))
            + len(set(PROPER.findall(text))))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, f"{hits} elementi concreti, {density:.1f} ogni 100 parole (meglio 4+)"


def _lex_pattern(find):
    return re.compile(r"(?<!\w)" + re.escape(find).replace(r"\ ", r"\s+") + r"(?!\w)",
                      re.IGNORECASE)


def check_slop(text, lex, lang):
    """Densità di vocabolario di repertorio rispetto al lessico."""
    w = words(text)
    if not w:
        return 50.0, "vuoto"
    hits, found = 0, []
    resto = text
    voci = [e for e in lex["phrases"] + lex["words"] if e.get("lang", lang) == lang]
    # Prima le voci più lunghe, e ogni occorrenza si conta una volta sola:
    # "con passione e dedizione" non vale anche come "con passione".
    for entry in sorted(voci, key=lambda e: len(e["find"]), reverse=True):
        pat = _lex_pattern(entry["find"])
        n = len(pat.findall(resto))
        if n:
            hits += n
            found.append(entry["find"])
            resto = pat.sub(" ", resto)
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} termini di repertorio, {density:.1f} ogni 100 parole"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Caratteri che la tastiera di un telefono non produce."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”«»")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisibili, {em} trattini lunghi, {curly} virgolette tipografiche, "
              f"{ellip} puntini di sospensione, {nbsp} spazi rigidi")
    return score, detail


def check_voice(text, lex, lang):
    """Registro parlato, persona, e le forme a cui i modelli tornano sempre."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "troppo corto per giudicare"
    per100 = 100 / len(w)
    if lang == "it":
        spoken = (len(PARLATO_IT.findall(text))
                  + text.count("?") * 0.5 + text.count("!") * 0.5) * per100
        person = len(PRONOUNS_IT.findall(text)) * per100
        spoken_label = "segnali di parlato"
        spoken_human = 2.5
        person_human = 10.0
    else:
        spoken = len(CONTRACTIONS.findall(text)) * per100
        person = len(PRONOUNS_EN.findall(text)) * per100
        spoken_label = "contrazioni"
        spoken_human = 3.0
        person_human = 8.0
    tells = 0
    names = []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(spoken, human=spoken_human, machine=0.0) * 0.35
             + scale(person, human=person_human, machine=1.0) * 0.35
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("elenchi-uniformi")
    detail = (f"{spoken:.1f} {spoken_label}, {person:.1f} marcatori di persona "
              f"ogni 100 parole, {tells} tic strutturali")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["VARIAZIONE", "CONCRETEZZA", "REPERTORIO", "IMPRONTA", "VOCE"]


def run(text, lex, lang="auto"):
    lang = lingua(text, lang)
    results = {}
    results["VARIAZIONE"] = check_burstiness(text)
    results["CONCRETEZZA"] = check_specificity(text)
    results["REPERTORIO"] = check_slop(text, lex, lang)
    results["IMPRONTA"] = check_fingerprint(text)
    results["VOCE"] = check_voice(text, lex, lang)
    scores = [results[c][0] for c in CHECKS]
    # Il controllo più debole trascina il verdetto: a un rilevatore basta un segnale.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "PASSA" if overall >= 70 and min(scores) >= 55 else (
        "DA RIVEDERE" if overall >= 50 else "SEGNALATO")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "PANNELLO RILEVAMENTO IA" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'UMANO':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "PASSA":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Segnale più debole: {weakest}. Parti da quello.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Misura quanto una bozza sembra scritta da una macchina.")
    ap.add_argument("input", nargs="?", default="-", help="file, oppure - per stdin")
    ap.add_argument("compare", nargs="?", help="secondo file, per il confronto prima/dopo")
    ap.add_argument("--lang", default="auto", choices=["auto", "it", "en"],
                    help="lingua del testo (default: rilevata)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    args = ap.parse_args()

    lex = json.load(open(args.lexicon, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex, args.lang)
        payload.append({
            "source": name,
            "lang": lingua(text, args.lang),
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex, args.lang)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
              f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "PASSA" else 1)


if __name__ == "__main__":
    main()
