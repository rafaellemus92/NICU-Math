"""C3: sign change of d2Z/dphi2 (T, phi=0) near T=1.76-1.77.
Method A: symmetric finite differences D(T,h) = 2 (Z(T,h) - Z(T,0))/h^2 (Z even in phi),
          h = 0.04, 0.02 (and 0.01), Richardson D_R = (4 D(h/2) - D(h))/3.
Method B: tangent (first+second variation) equations integrated with the same RK4.
Z recorded at every step (dt=0.005 -> every 0.005) on [1.70, 1.85]; zero crossing by
cubic (4-point Lagrange) interpolation of the bracketing samples."""
import sys, time, json
import numpy as np
sys.path.insert(0, '.')
from ns import NS, NSTangent

D = './'
N = int(sys.argv[1])
dt = float(sys.argv[2]) if len(sys.argv) > 2 else 0.005
do_tangent = (len(sys.argv) <= 3) or sys.argv[3] != 'notan'
Tend = 1.85
nst = int(round(Tend / dt))
rec = int(round(0.005 / dt))
m = NS(N, 1.0 / 28.0)

def crossing(t, y):
    """first sign change of y on grid t; cubic Lagrange interpolation + bisection."""
    idx = np.where(np.sign(y[:-1]) != np.sign(y[1:]))[0]
    outs = []
    for i in idx:
        j0 = max(0, min(len(t) - 4, i - 1))
        tt, yy = t[j0:j0 + 4], y[j0:j0 + 4]
        def P(s):
            tot = 0.0
            for a in range(4):
                L = 1.0
                for b in range(4):
                    if b != a:
                        L *= (s - tt[b]) / (tt[a] - tt[b])
                tot += yy[a] * L
            return tot
        lo, hi = t[i], t[i + 1]
        flo = P(lo)
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            fm = P(mid)
            if np.sign(fm) == np.sign(flo):
                lo, flo = mid, fm
            else:
                hi = mid
        lin = t[i] - y[i] * (t[i + 1] - t[i]) / (y[i + 1] - y[i])
        outs.append((0.5 * (lo + hi), lin))
    return outs

Zs = {}
t0 = time.time()
for h in [0.0, 0.01, 0.02, 0.04]:
    uh = m.init_family(h)
    _, ts, Es, Z = m.run(uh, dt, nst, every=rec)
    Zs[h] = Z
tFD = time.time() - t0
sel = ts >= 1.70 - 1e-9
T = ts[sel]
Dh = {h: 2.0 * (Zs[h][sel] - Zs[0.0][sel]) / h ** 2 for h in [0.01, 0.02, 0.04]}
DR = (4 * Dh[0.02] - Dh[0.04]) / 3.0          # Richardson from h=0.04,0.02
DR2 = (4 * Dh[0.01] - Dh[0.02]) / 3.0         # Richardson from h=0.02,0.01
DRR = (16 * DR2 - DR) / 15.0                   # second-level Richardson
out = dict(N=N, K=m.g.K, dt=dt, sec_fd=tFD)
print(f'N={N} K={m.g.K} dt={dt}  FD runs: {tFD:.1f}s')
for name, arr in [('D(h=0.04)', Dh[0.04]), ('D(h=0.02)', Dh[0.02]), ('D(h=0.01)', Dh[0.01]),
                  ('Rich(0.04,0.02)', DR), ('Rich(0.02,0.01)', DR2), ('Rich2', DRR)]:
    c = crossing(T, arr)
    out[name] = c
    print(f'  {name:16s} crossings (cubic, linear): ' + ', '.join(f'({a:.6f}, {b:.6f})' for a, b in c))
# print table around crossing
for k in range(len(T)):
    if 1.745 <= T[k] <= 1.785:
        print(f'   T={T[k]:.3f} Z0={Zs[0.0][sel][k]:.12f} D04={Dh[0.04][k]:+.6e} D02={Dh[0.02][k]:+.6e} '
              f'D01={Dh[0.01][k]:+.6e} DR={DR[k]:+.6e}')
if do_tangent:
    t0 = time.time()
    mt = NSTangent(N, 1.0 / 28.0)
    Y = mt.init_aug(0.0)
    tt, Z0t, Z1t, Z2t = [0.0], [], [], []
    z = mt.zderivs(Y); Z0t.append(z[0]); Z1t.append(z[1]); Z2t.append(z[2])
    for n in range(1, nst + 1):
        Y = mt.step(Y, dt)
        if n % rec == 0:
            tt.append(n * dt)
            z = mt.zderivs(Y); Z0t.append(z[0]); Z1t.append(z[1]); Z2t.append(z[2])
    tt, Z0t, Z1t, Z2t = map(np.array, (tt, Z0t, Z1t, Z2t))
    tTan = time.time() - t0
    s2 = tt >= 1.70 - 1e-9
    c = crossing(tt[s2], Z2t[s2])
    out['tangent'] = c
    out['sec_tan'] = tTan
    print(f'  tangent: crossings (cubic, linear): ' + ', '.join(f'({a:.6f}, {b:.6f})' for a, b in c) +
          f'   [{tTan:.1f}s]; max|Z_tan - Z_FD(0)| = {np.abs(Z0t - Zs[0.0]).max():.2e}; '
          f'max|dZ/dphi(phi=0)| = {np.abs(Z1t).max():.2e}')
    print(f'  max|tangent - Rich(0.04,0.02)| on [1.70,1.85] = {np.abs(Z2t[s2]-DR).max():.2e}; '
          f'max|tangent - Rich2| = {np.abs(Z2t[s2]-DRR).max():.2e}')
    for k in range(len(tt)):
        if abs(tt[k] - 1.76) < 1e-9 or abs(tt[k] - 1.765) < 1e-9 or abs(tt[k] - 1.77) < 1e-9 or abs(tt[k] - 1.0) < 1e-9 or abs(tt[k]-1.85)<1e-9:
            print(f'   tangent T={tt[k]:.3f}: Z={Z0t[k]:.12f} Z_phiphi={Z2t[k]:+.10e}')
    np.savez(D + f'c3_tan_N{N}_dt{dt}.npz', t=tt, Z=Z0t, Z1=Z1t, Z2=Z2t)
np.savez(D + f'c3_fd_N{N}_dt{dt}.npz', t=ts, **{f'Z_{h}': Zs[h] for h in Zs})
with open(D + f'c3_N{N}_dt{dt}.json', 'w') as f:
    json.dump(out, f, indent=1)
