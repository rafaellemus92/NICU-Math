"""C1: Z(2), Z(4), sampled peak (0.05 sampling) for three phases at given N (and dt)."""
import sys, time, json
import numpy as np
sys.path.insert(0, '.')
from ns import NS

D = './'
N = int(sys.argv[1])
dt = float(sys.argv[2]) if len(sys.argv) > 2 else 0.005
phis = [float(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else [0.0, 0.971073032, 2.159844949]
T = 4.0
m = NS(N, 1.0 / 28.0)
nst = int(round(T / dt))
every_005 = int(round(0.05 / dt))
res = []
for phi in phis:
    t0 = time.time()
    uh = m.init_family(phi)
    uh, ts, Es, Zs = m.run(uh, dt, nst, every=1)
    el = time.time() - t0
    i2, i4 = int(round(2.0 / dt)), int(round(4.0 / dt))
    samp = np.arange(0, nst + 1, every_005)
    j = samp[np.argmax(Zs[samp])]
    # refined peak from per-step data (parabola through 3 points around per-step max)
    jj = int(np.argmax(Zs))
    a, b, c = Zs[jj - 1], Zs[jj], Zs[jj + 1]
    off = 0.5 * (a - c) / (a - 2 * b + c)
    tpk = (jj + off) * dt
    zpk = b - 0.25 * (a - c) * off
    r = dict(N=N, K=m.g.K, dt=dt, phi=phi, Z2=Zs[i2], Z4=Zs[i4], E2=Es[i2], E4=Es[i4],
             peak_sampled=Zs[j], t_peak_sampled=ts[j], peak_refined=zpk, t_peak_refined=tpk, sec=el)
    res.append(r)
    print(f"N={N} K={m.g.K} dt={dt} phi={phi:.9f}: Z(2)={Zs[i2]:.10f} Z(4)={Zs[i4]:.10f} "
          f"sampled peak {Zs[j]:.6f} at t={ts[j]:.2f}; refined peak {zpk:.8f} at t={tpk:.4f}; "
          f"E(2)={Es[i2]:.10f} E(4)={Es[i4]:.10f} [{el:.1f}s]", flush=True)
    np.savez(D + f'c1_N{N}_dt{dt}_phi{phi:.6f}.npz', t=ts, E=Es, Z=Zs)
with open(D + f'c1_N{N}_dt{dt}.json', 'w') as f:
    json.dump(res, f, indent=1)
