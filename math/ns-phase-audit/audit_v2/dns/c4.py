"""C4: local maximiser of Z(2, phi) on [0.85, 1.10].
Method A: golden-section search (tol 1e-7 in phi) + parabolic fit on final bracket.
Method B: Newton iteration phi <- phi - Z_phi/Z_phiphi using the tangent equations."""
import sys, time, json
import numpy as np
sys.path.insert(0, '.')
from ns import NS, NSTangent

D = './'
N = int(sys.argv[1])
methods = sys.argv[2] if len(sys.argv) > 2 else 'golden,newton'
T, dt = 2.0, 0.005
nst = int(round(T / dt))
m = NS(N, 1.0 / 28.0)
out = dict(N=N, K=m.g.K)
cache = {}
def Z2(phi):
    if phi not in cache:
        uh = m.init_family(phi)
        for _ in range(nst):
            uh = m.step(uh, dt)
        cache[phi] = m.g.enstrophy(uh)
    return cache[phi]

if 'golden' in methods:
    t0 = time.time()
    a, b = 0.85, 1.10
    r = (np.sqrt(5) - 1) / 2
    c, d = b - r * (b - a), a + r * (b - a)
    fc, fd = Z2(c), Z2(d)
    nev = 2
    while b - a > 1e-7:
        if fc > fd:      # maximise
            b, d, fd = d, c, fc
            c = b - r * (b - a); fc = Z2(c)
        else:
            a, c, fc = c, d, fd
            d = a + r * (b - a); fd = Z2(d)
        nev += 1
    xg = 0.5 * (a + b)
    # parabolic fit over 5 well-spaced points around xg (robust to roundoff)
    hs = np.array([-0.02, -0.01, 0.0, 0.01, 0.02])
    zs = np.array([Z2(xg + h) for h in hs])
    cf = np.polyfit(hs, zs, 4)
    # maximise the quartic near 0 via Newton
    p1, p2 = np.polyder(cf), np.polyder(cf, 2)
    s = 0.0
    for _ in range(50):
        s -= np.polyval(p1, s) / np.polyval(p2, s)
    el = time.time() - t0
    out.update(golden_phi=xg, golden_Z=Z2(xg), golden_evals=nev, quartic_phi=xg + s,
               quartic_Z=np.polyval(cf, s), quartic_curv=np.polyval(p2, s), sec_golden=el)
    print(f'N={N} K={m.g.K}: golden-section phi*={xg:.9f} Z(2,phi*)={Z2(xg):.12f} ({nev} evals, {el:.0f}s); '
          f'quartic fit (h=0.01) phi*={xg+s:.9f} Z={np.polyval(cf, s):.12f} Z_phiphi={np.polyval(p2, s):.6f}', flush=True)
    for phi in [0.85, 0.9, 0.95, 0.970409, 0.971073, 0.971073032, 1.0, 1.05, 1.10]:
        print(f'   Z(2, {phi}) = {Z2(phi):.12f}', flush=True)
        out[f'Z2_{phi}'] = Z2(phi)

if 'newton' in methods:
    t0 = time.time()
    mt = NSTangent(N, 1.0 / 28.0)
    phi = 0.97
    hist = []
    for it in range(6):
        Y = mt.init_aug(phi)
        for _ in range(nst):
            Y = mt.step(Y, dt)
        z0, z1, z2 = mt.zderivs(Y)
        hist.append((phi, z0, z1, z2))
        print(f'   Newton it {it}: phi={phi:.12f} Z={z0:.12f} Z_phi={z1:+.3e} Z_phiphi={z2:.6f}', flush=True)
        if abs(z1 / z2) < 1e-12:
            break
        phi = phi - z1 / z2
    el = time.time() - t0
    out.update(newton=hist, newton_phi=hist[-1][0], newton_Z=hist[-1][1], sec_newton=el)
    print(f'N={N} K={m.g.K}: Newton(tangent) phi*={hist[-1][0]:.10f} Z(2,phi*)={hist[-1][1]:.12f} '
          f'Z_phiphi={hist[-1][3]:.6f} ({el:.0f}s)', flush=True)
with open(D + f'c4_N{N}_{methods.replace(",", "_")}.json', 'w') as f:
    json.dump(out, f, indent=1)
