#!/usr/bin/env python3
"""
swipe.py - mette in classifica i reel che hai raccolto in base a quanto hanno
superato il proprio account, dà un nome alla formula dell'hook e scrive lo
swipe file.

Questo script esiste per correggere un errore: le visualizzazioni da sole non
sono una prova. Un account da 2.000.000 di follower che fa 400.000
visualizzazioni ha avuto una giornata tranquilla. Un account da 4.000 follower
che fa 400.000 visualizzazioni ha trovato qualcosa. La classifica si basa sul
multiplo rispetto alla mediana dell'account stesso, l'unica versione di "è
andato virale" che ti dice qualcosa che puoi copiare.

L'input è un file separato da tabulazioni che compili mentre guardi, un reel
per riga, con una riga d'intestazione che nomina le colonne (in inglese o in
italiano):

    account   followers   median   views    hook
    account   follower    mediana  visualizzazioni   hook

`median`/`mediana` è la mediana delle visualizzazioni recenti dell'account,
ed è la base migliore. Se hai solo i follower, lascia fuori la mediana e lo
script lo dice. `hook` è la prima riga del reel, detta o a schermo, con le
parole di chi l'ha scritta.

Le formule vengono da ../ig-reel/hooks.json e si riconoscono in italiano e in
inglese. Riconoscerle è un aiuto, non una sentenza: leggi sempre a mano le
righe "non classificato", è lì che si nasconde una formula che ancora non hai.

Uso
  python3 swipe.py raccolti.tsv
  python3 swipe.py raccolti.tsv --out swipe.md
  python3 swipe.py raccolti.tsv --json
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(HERE, "..", "ig-reel", "hooks.json")
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9$€%'’-]+")
NON_CLASSIFICATO = "non classificato"

# Intestazioni accettate, in inglese e in italiano.
ALIAS = {
    "account": "account", "profilo": "account", "handle": "account",
    "followers": "followers", "follower": "followers", "seguaci": "followers",
    "median": "median", "mediana": "median",
    "views": "views", "visualizzazioni": "views", "views reel": "views", "vista": "views",
    "hook": "hook", "apertura": "hook", "prima riga": "hook",
}

try:                                              # facoltativo: valuta anche gli hook
    sys.path.insert(0, os.path.join(HERE, "..", "ig-reel"))
    from hookscore import run as score_hook       # noqa: E402
except Exception:                                 # ig-viral copiato da solo
    score_hook = None


def load_formulas(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        return None
    by_id = {h["id"]: h for h in d["hooks"]}
    order = d.get("classify_order") or sorted(by_id)
    return [(by_id[i]["id"], by_id[i]["name"],
             re.compile(by_id[i]["match"], re.IGNORECASE)) for i in order if i in by_id]


def classify(hook, formulas):
    if not formulas:
        return None, NON_CLASSIFICATO
    for fid, name, pattern in formulas:
        if pattern.search(hook):
            return fid, name
    return None, NON_CLASSIFICATO


def numero(cella):
    """'13,4K' -> 13400;  '2.344' -> 2344;  '1.2M' -> 1200000."""
    c = (cella or "").strip().lower().replace(" ", "")
    m = re.match(r"^([\d.,]+)([km]|mila|mln)?$", c)
    if not m:
        digits = re.sub(r"[^\d]", "", c)
        return int(digits) if digits else None
    num, suf = m.groups()
    if suf:
        val = float(num.replace(",", "."))
        return int(val * (1000 if suf in ("k", "mila") else 1_000_000))
    return int(re.sub(r"[^\d]", "", num) or 0) or None


def read_rows(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    head = [ALIAS.get(c.strip().lower(), c.strip().lower()) for c in lines[0].split("\t")]
    if "views" in head and "hook" in head:
        cols, body = head, lines[1:]
    else:
        cols, body = ["account", "followers", "views", "hook"], lines
    rows = []
    for line in body:
        cells = line.split("\t")
        if len(cells) < len(cols):
            cells += [""] * (len(cols) - len(cells))
        r = dict(zip(cols, [c.strip() for c in cells]))
        r["views"] = numero(r.get("views", "")) or 0
        for k in ("followers", "median"):
            r[k] = numero(r.get(k, ""))
        if r["views"] and r.get("hook"):
            rows.append(r)
    return rows


def analyse(rows, formulas):
    used_median = any(r.get("median") for r in rows)
    for r in rows:
        base = r.get("median") or r.get("followers") or 0
        r["baseline"] = base
        r["outlier"] = round(r["views"] / base, 2) if base else None
        r["formula_id"], r["formula"] = classify(r["hook"], formulas)
        r["words"] = len(WORD_RE.findall(r["hook"]))
        if score_hook:
            _, overall, verdict, _ = score_hook(r["hook"])
            r["hook_score"], r["hook_verdict"] = round(overall, 1), verdict
        else:
            r["hook_score"], r["hook_verdict"] = None, None
    ranked = sorted(rows, key=lambda r: -(r["outlier"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def med(items, key):
        vals = [i[key] for i in items if i.get(key) is not None]
        return round(statistics.median(vals), 1) if vals else None

    counts, counts_bottom = {}, {}
    for r in top:
        counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    for r in bottom:
        counts_bottom[r["formula"]] = counts_bottom.get(r["formula"], 0) + 1
    return {
        "baseline": "mediana dell'account" if used_median else "numero di follower",
        "n": len(ranked),
        "accounts": len({r.get("account", "") for r in ranked}),
        "reels": ranked,
        "top_formulas": sorted(counts.items(), key=lambda kv: -kv[1]),
        "bottom_formulas": counts_bottom,
        "top_hook_score": med(top, "hook_score"),
        "bottom_hook_score": med(bottom, "hook_score"),
        "top_words": med(top, "words"),
        "bottom_words": med(bottom, "words"),
        "unclassified": sum(1 for r in ranked if r["formula"] == NON_CLASSIFICATO),
    }


def render(a, out=sys.stdout):
    head = (f"SWIPE FILE  ·  {a['n']} reel  ·  {a['accounts']} account  ·  "
            f"base: {a['baseline']}")
    print("\n" + head, file=out)
    print("=" * max(len(head), 78), file=out)
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "   ?"
        score = f"{r['hook_score']:.0f}" if r["hook_score"] is not None else " -"
        fid = f"#{r['formula_id']:<2}" if r["formula_id"] else "-  "
        views = f"{r['views']:,}".replace(",", ".")
        print(f"  {mult:>7}  hook {score:>3}  {fid} {r['formula'][:22]:<22} "
              f"{r.get('account', '')[:16]:<16} {views:>9}", file=out)
        print(f"           \"{r['hook'][:96]}\"", file=out)
    print("-" * max(len(head), 78), file=out)
    print("COSA FUNZIONA IN QUESTO GRUPPO", file=out)
    if a["top_formulas"]:
        print("  terzo più alto per multiplo:  "
              + ", ".join(f"{n} x{c} (in basso x{a['bottom_formulas'].get(n, 0)})"
                          for n, c in a["top_formulas"][:4]), file=out)
    if a["top_hook_score"] is not None:
        print(f"  punteggio hook mediano:       in alto {a['top_hook_score']:.0f}  "
              f"contro in basso {a['bottom_hook_score']:.0f}", file=out)
    print(f"  lunghezza hook mediana:       in alto {a['top_words']:g} parole  "
          f"contro in basso {a['bottom_words']:g} parole", file=out)
    print(f"  non classificati:             {a['unclassified']} su {a['n']}. Leggili a mano: "
          "è lì che si nasconde una formula che ancora non hai.", file=out)
    print("\n  Un gruppo raccolto a mano è un indizio, non una prova. Dodici reel non ti "
          "dicono\n  niente; quaranta su sei account ti dicono qualcosa. Raccogline altri "
          "prima di crederci.\n", file=out)


def to_markdown(a):
    lines = ["# Swipe file", "",
             f"{a['n']} reel su {a['accounts']} account. "
             f"In classifica per multiplo sulla {a['baseline']}.", ""]
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "?"
        lines += [f"## {mult}  {r['formula']}  ({r.get('account', '')})",
                  f"- visualizzazioni: {r['views']:,}  base: {r['baseline']:,}".replace(",", "."),
                  f"- punteggio hook: {r['hook_score']}  parole: {r['words']}",
                  f"- hook: \"{r['hook']}\"", ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Classifica i reel raccolti per multiplo sulla mediana.")
    ap.add_argument("input", nargs="?", default="-", help="file TSV, oppure - per stdin")
    ap.add_argument("--hooks", default=HOOKS, help="percorso di ig-reel/hooks.json")
    ap.add_argument("--out", help="scrive anche lo swipe file in markdown qui")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = read_rows(args.input)
    if not rows:
        print("nessuna riga utilizzabile. Serve un file separato da tabulazioni con almeno "
              "visualizzazioni e hook.", file=sys.stderr)
        sys.exit(2)
    formulas = load_formulas(args.hooks)
    a = analyse(rows, formulas)
    if not formulas:
        print("nota: hooks.json non trovato, le formule non hanno nome. Usa --hooks.",
              file=sys.stderr)
    if score_hook is None:
        print("nota: hookscore.py non importabile, punteggi degli hook saltati.", file=sys.stderr)

    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    if args.out:
        path = os.path.expanduser(args.out)
        cartella = os.path.dirname(path)
        if cartella:                             # "swipe.md" da solo non ha cartella
            os.makedirs(cartella, exist_ok=True)
        open(path, "w", encoding="utf-8").write(to_markdown(a))
        print(f"scritto {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
