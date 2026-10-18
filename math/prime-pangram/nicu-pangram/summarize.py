"""Print the lattice tables (markdown) from results/b_lattice/*.json."""
import glob, json, re, sys
rows = {}
for f in glob.glob("results/b_lattice/*.json"):
    r = json.load(open(f))
    rows[r["regime"]] = r
def key(n):
    m = re.match(r"([RF])\((\d),(\d)\)", n); return (m.group(1), int(m.group(2)) + int(m.group(3)), int(m.group(2)))
def fmt(c):
    return "0" if c == 0 else f"{c:,} ≈ {c:.3g}".replace("e+", " × 10^")
for fam in ("R", "F"):
    print(f"\n### family {fam}")
    if fam == "R":
        print("| regime | prime words | packing feasible | min non-English clusters | exact number of solutions | witness |")
        print("|---|---|---|---|---|---|")
    else:
        print("| regime | prime words | exact number of solutions | witness |")
        print("|---|---|---|---|")
    for n in sorted([n for n in rows if n.startswith(fam)], key=key):
        r = rows[n]
        w = " ".join(x[0].upper() for x in r["witness"]) if "witness" in r else "—"
        cnt = fmt(r["count"]) if "count" in r else "pending"
        if fam == "R":
            mf = r.get("min_foreign_clusters"); mf = "—" if mf is None else str(mf)
            pk = r.get("packing_feasible"); pk = "n/a" if pk is None else ("yes" if pk else "no (⇒ 0)")
            print(f"| {n} | {r['n_prime']:,} | {pk} | {mf} | {cnt} | {w} |")
        else:
            print(f"| {n} | {r['n_prime']:,} | {cnt} | {w} |")
