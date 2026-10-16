"""Markdown table of the base-dependence experiment from results/base_scan/base_*.json."""
import glob, json, math
rows = {}
for f in glob.glob("results/base_scan/base_*.json"):
    r = json.load(open(f)); rows[r["base"]] = r
rows[26] = {"base": 26, "n_prime": 16243, "count": 0, "witness": None, "admissible_final_letters": "acegikoqsuwy"}
def factor(n):
    f, p = [], 2
    while p * p <= n:
        while n % p == 0: f.append(p); n //= p
        p += 1
    if n > 1: f.append(n)
    return "·".join(map(str, f))
print("| base b | b | b−1 | final letters coprime to b (words of ≥ 2 letters) | word count | prime words | perfect pangrams | witness |")
print("|---|---|---|---|---|---|---|---|")
for b in sorted(rows):
    r = rows[b]
    parity = "odd (3 or 5)" if (b - 1) % 2 == 0 else "3..6"
    w = r.get("witness") or "—"
    print(f"| {b} | {factor(b)} | {factor(b-1)} | {r['admissible_final_letters']} ({len(r['admissible_final_letters'])}) | {parity} | {r['n_prime']:,} | **{r['count']:,}** | {w} |")
