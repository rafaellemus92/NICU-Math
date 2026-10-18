"""RESULTS.md 'Relative Z difference' column (vs 64^3) recomputed from the DNS report's
independent fixed-dt RK4 runs (dns/c1_N*_dt0.005.json)."""
import json, csv
W = ".."
P = "../../periodic_ns_lab_v2"
d = {N: {round(r["phi"], 3): r for r in json.load(open(f"{W}/dns/c1_N{N}_dt0.005.json"))} for N in (32, 48, 64)}
pk = list(csv.DictReader(open(f"{P}/results/spatial_comparison.csv")))
print("columns:", list(pk[0].keys()))
for r in pk:
    ph = round(float(r['phase']), 3); T = int(float(r['time'])); N = int(r['n'])
    key = f"Z{T}"
    zN, z64 = d[N][ph][key], d[64][ph][key]
    rel = abs(zN - z64) / abs(z64)
    pkrel = float(r['relative_Z_difference'])
    print(f"phi={ph:.3f} T={T} N={N}: DNS relZ={rel:.4e}  package={pkrel:.4e}  ratio={rel/pkrel:.4f}")
