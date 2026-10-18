"""C5: phase sweep phi_j = j*pi/M, j=0..M (M=16 -> 17 points on [0,pi]; Z is even in phi so
[0,pi] covers the circle), N=24, record Z at T=1,2,3,4 (+ every 0.05), report argmax per T
(grid value and 3-point parabolic refinement)."""
import sys, time, json
import numpy as np
sys.path.insert(0, '.')
from ns import NS

D = './'
N = int(sys.argv[1]) if len(sys.argv) > 1 else 24
M = int(sys.argv[2]) if len(sys.argv) > 2 else 16
dt, Tend = 0.005, 4.0
nst = int(round(Tend / dt))
m = NS(N, 1.0 / 28.0)
phis = np.pi * np.arange(M + 1) / M
Zt = []
t0 = time.time()
for phi in phis:
    uh = m.init_family(phi)
    _, ts, Es, Z = m.run(uh, dt, nst, every=10)
    Zt.append(Z)
Zt = np.array(Zt)               # (M+1, len(ts))
el = time.time() - t0
print(f'N={N} K={m.g.K} sweep M={M} ({M+1} phases) in {el:.0f}s')
res = {}
hdr = 'phi        ' + ' '.join(f'Z(T={T:.0f})      ' for T in [1, 2, 3, 4])
print(hdr)
iT = {T: int(round(T / 0.05)) for T in [1, 2, 3, 4]}
for j, phi in enumerate(phis):
    print(f'{phi:.6f}  ' + ' '.join(f'{Zt[j, iT[T]]:.10f}' for T in [1, 2, 3, 4]))
for T in [1, 2, 3, 4]:
    col = Zt[:, iT[T]]
    j = int(np.argmax(col))
    # parabolic refinement using neighbours (use evenness/periodicity at the ends)
    def val(i):
        if i < 0:
            return col[-i]          # Z(-phi) = Z(phi)
        if i > M:
            return col[2 * M - i]   # Z(pi + d) = Z(-pi - d) = Z(pi - d)
        return col[i]
    a, b, c = val(j - 1), val(j), val(j + 1)
    off = 0.5 * (a - c) / (a - 2 * b + c)
    hstep = np.pi / M
    res[T] = dict(grid_phi=phis[j], grid_Z=col[j], parab_phi=phis[j] + off * hstep, parab_Z=b - 0.25 * (a - c) * off)
    print(f'T={T}: best grid phase {phis[j]:.6f} (= {j}pi/{M}) Z={col[j]:.10f}; parabolic {phis[j]+off*hstep:.4f} '
          f'(Z~{b-0.25*(a-c)*off:.8f}); worst grid phase {phis[np.argmin(col)]:.6f} Z={col.min():.8f}')
# drift curve: best phase vs T every 0.25 (grid + parabolic)
print('best-phase drift (every 0.25):')
for T in np.arange(0.25, 4.0001, 0.25):
    i = int(round(T / 0.05)); col = Zt[:, i]; j = int(np.argmax(col))
    def val(k):
        if k < 0: return col[-k]
        if k > M: return col[2 * M - k]
        return col[k]
    a, b, c = val(j - 1), val(j), val(j + 1)
    off = 0.5 * (a - c) / (a - 2 * b + c) if (a - 2 * b + c) != 0 else 0.0
    print(f'  T={T:.2f}: grid {phis[j]:.4f}  parabolic {phis[j]+off*np.pi/M:.4f}  Zmax={col[j]:.8f}')
np.savez(D + f'c5_N{N}_M{M}.npz', phis=phis, t=ts, Z=Zt)
with open(D + f'c5_N{N}_M{M}.json', 'w') as f:
    json.dump({str(k): v for k, v in res.items()}, f, indent=1)
