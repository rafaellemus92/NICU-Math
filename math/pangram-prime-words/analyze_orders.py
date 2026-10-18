"""Aggregate results/order_scan/*.json: which digit assignments admit a
perfect pangram of prime words (English clusters, base 26), and what
distinguishes them.  A letter can end a prime word iff its digit is coprime
to 26 (odd and not 13)."""
import glob, json
from collections import Counter
from clusters import CODAS, VOWELS
recs = [json.load(open(f)) for f in sorted(glob.glob("results/order_scan/*.json"))]
rnd = [r for r in recs if r["name"].startswith("random_")]
named = [r for r in recs if not r["name"].startswith("random_")]
coda_finals = Counter(c[-1] for c in CODAS if c)          # how many English codas end in each letter
def features(r):
    fin = set(r["final_letters"])
    return {"odd_vowels": sum(v in fin for v in VOWELS),
            "usable_codas": sum(n for ch, n in coda_finals.items() if ch in fin),
            "pinned": "".join(ch for ch in "jqvxz" if ch not in fin)}
print(f"random assignments: {len(rnd)}, with a solution: {sum(1 for r in rnd if r['witness'])} "
      f"({100*sum(1 for r in rnd if r['witness'])/max(1,len(rnd)):.0f}%)")
print("\nby number of vowels that can end a word (digit coprime to 26):")
for k in range(7):
    grp = [r for r in rnd if features(r)["odd_vowels"] == k]
    if grp:
        print(f"  {k} vowels: {len(grp):3d} assignments, {sum(1 for r in grp if r['witness']):3d} with solutions")
print("\nby number of English codas whose final letter can end a prime word (of 174):")
for lo, hi in ((0, 40), (40, 70), (70, 100), (100, 130), (130, 175)):
    grp = [r for r in rnd if lo <= features(r)["usable_codas"] < hi]
    if grp:
        print(f"  {lo:3d}-{hi-1:3d}: {len(grp):3d} assignments, {sum(1 for r in grp if r['witness']):3d} with solutions")
print("\nnamed assignments:")
for r in named:
    f = features(r)
    print(f"  {r['name']:14s} final letters {r['final_letters']} | vowels {f['odd_vowels']} | usable codas {f['usable_codas']:3d} | "
          f"prime words {r['n_prime']:,} | {'count ' + format(r['count'], ',') if 'count' in r else ('solution' if r['witness'] else 'NONE')}")
    if r.get("witness"):
        print("      ", r["witness"])
a = [r for r in named if r["name"] == "alphabetical"]
if a:
    f = features(a[0]); print(f"\nalphabetical: usable codas {f['usable_codas']} of 174, pinned letters {f['pinned']}")
