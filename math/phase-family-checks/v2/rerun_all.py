"""Re-run the session's b^2 checks with strict dealiasing K=(N-1)//3 and 16 phases at long times. Writes v2/results.json."""
import numpy as np, json, time, sys; sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent)); from ns3d import NS
nu = 1/28; out = {}; t0 = time.time()
# (1) T=1 scaling, N=32, dt=0.01, 8 phases
M = 8; phis = np.arange(M)*2*np.pi/M; ns = NS(32, nu, 0.01); rows = {}
for b in (0.0, 0.05, 0.1, 0.2, 0.4):
    vals = np.array([ns.run(1, b, 1, 1, p, [1.0])[1.0] for p in phis]); h = np.fft.rfft(vals, axis=0)/M
    rows[b] = {'A0': h[0].real.tolist(), 'A1': (2*h[1].real).tolist(), 'A2': (2*h[2].real).tolist(), 'A3': (2*h[3].real).tolist(),
               'max_sin': float(np.abs(h[1:4].imag).max()*2)}
out['T1_N32_8phases'] = rows; print("T=1 done", round(time.time()-t0), "s", flush=True)
# (2) long time, N=24, dt=0.02, 16 phases, b=0.1 and 0.2, checkpoints 1,2,4,8
M = 16; phis = np.arange(M)*2*np.pi/M; ns = NS(24, nu, 0.02); cps = [1, 2, 4, 8]; rows = {}
for b in (0.1, 0.2):
    res = [ns.run(1, b, 1, 1, p, cps) for p in phis]; rows[b] = {}
    for T in cps:
        vals = np.array([r[T] for r in res]); h = np.fft.rfft(vals, axis=0)/M
        rows[b][T] = {'A0': h[0].real.tolist(), 'A1': (2*h[1].real).tolist(), 'A2': (2*h[2].real).tolist(), 'A3': (2*h[3].real).tolist(), 'A4': (2*h[4].real).tolist()}
    print("long-time b", b, "done", round(time.time()-t0), "s", flush=True)
out['long_N24_16phases'] = rows
json.dump(out, open(__import__('pathlib').Path(__file__).resolve().parent / 'results.json', 'w'), indent=1)
print("T=1  c2(Z)/b^2:", {b: (r['A2'][1]/b**2 if b else r['A2'][1]) for b, r in out['T1_N32_8phases'].items()})
print("T=1  c2(S)/b^2:", {b: (r['A2'][2]/b**2 if b else r['A2'][2]) for b, r in out['T1_N32_8phases'].items()})
for b, rr in out['long_N24_16phases'].items():
    print(f"b={b}: c2(Z)/b^2 by T:", {T: round(r['A2'][1]/b**2, 4) for T, r in rr.items()}, " c2(S)/b^2:", {T: round(r['A2'][2]/b**2, 4) for T, r in rr.items()})
print("total", round(time.time()-t0), "s")
