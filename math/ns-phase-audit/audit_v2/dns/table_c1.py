import json, glob
D = './'
pkg = {0.0: (2.229748776, 1.806838777, 2.2407, 2.20), 0.971073032: (2.255276393, 1.954808208, 2.3446, 2.55),
       2.159844949: (2.128147203, 2.058295070, 2.3394, 2.90)}
rows = []
for f in sorted(glob.glob(D + 'c1_N*_dt*.json')):
    rows += json.load(open(f))
rows.sort(key=lambda r: (r['phi'], r['N'], -r['dt']))
for r in rows:
    p = pkg[round(r['phi'], 9)]
    print(f"phi={r['phi']:.9f} N={r['N']:3d} K={r['K']:2d} dt={r['dt']:.4f}  Z(2)={r['Z2']:.10f} (pkg-ours {p[0]-r['Z2']:+.1e})  "
          f"Z(4)={r['Z4']:.10f} (pkg-ours {p[1]-r['Z4']:+.1e})  peak {r['peak_sampled']:.6f}@{r['t_peak_sampled']:.2f}  "
          f"[{r['sec']:.0f}s]")
for N in sorted(set(r['N'] for r in rows)):
    sub = [r for r in rows if r['N'] == N and r['dt'] == 0.005]
    if len(sub) == 3:
        b2 = max(sub, key=lambda r: r['Z2'])['phi']; b4 = max(sub, key=lambda r: r['Z4'])['phi']
        print(f'N={N}: best at t=2 -> phi={b2}, best at t=4 -> phi={b4}')
