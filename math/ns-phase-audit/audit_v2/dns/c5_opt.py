"""C5 refinement: continuous maximiser phi*(T) of Z(T, phi) on [0, pi] for given T values,
by Newton iteration with the tangent (first/second variation) equations."""
import sys, time
import numpy as np
sys.path.insert(0, '.')
from ns import NSTangent

N = int(sys.argv[1])
pairs = [tuple(float(v) for v in s.split(':')) for s in sys.argv[2].split(',')]  # T:phi0
dt = 0.005
mt = NSTangent(N, 1.0 / 28.0)
for T, phi in pairs:
    t0 = time.time()
    nst = int(round(T / dt))
    for it in range(8):
        Y = mt.init_aug(phi)
        for _ in range(nst):
            Y = mt.step(Y, dt)
        z0, z1, z2 = mt.zderivs(Y)
        step = -z1 / z2
        if z2 > 0:                    # not a maximum: take a bounded ascent step instead
            step = 0.1 * np.sign(z1)
        print(f'   N={N} T={T} it={it} phi={phi:.10f} Z={z0:.12f} Z_phi={z1:+.3e} Z_phiphi={z2:+.6f}', flush=True)
        if abs(z1 / z2) < 1e-11:
            break
        phi += step
    print(f'N={N} K={mt.g.K} T={T}: phi*={phi:.9f} Z*={z0:.12f} Z_phiphi={z2:+.6f} [{time.time()-t0:.0f}s]', flush=True)
