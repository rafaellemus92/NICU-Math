"""Diagnostic variant: integrating-factor RK4 (viscous term exact) and an explicit
dt-variant driver, to see how the time-integrator choice affects Z(T) at the 1e-9 level."""
import sys
import numpy as np
sys.path.insert(0, '.')
from ns import NS


class NSIF(NS):
    def step(self, uh, dt):
        if getattr(self, '_dt', None) != dt:
            self._dt = dt
            self.E1 = np.exp(-self.visc * dt)
            self.E2 = np.exp(-self.visc * dt / 2)
        N_, E1, E2 = self.nonlin, self.E1, self.E2
        k1 = N_(uh)
        k2 = N_(E2 * (uh + 0.5 * dt * k1))
        k3 = N_(E2 * uh + 0.5 * dt * k2)
        k4 = N_(E1 * uh + dt * E2 * k3)
        return E1 * uh + (dt / 6.0) * (E1 * k1 + 2 * E2 * (k2 + k3) + k4)


if __name__ == '__main__':
    import time
    N = int(sys.argv[1]); dt = float(sys.argv[2]); scheme = sys.argv[3]
    phis = [float(x) for x in sys.argv[4].split(',')]
    T = float(sys.argv[5]) if len(sys.argv) > 5 else 4.0
    m = (NSIF if scheme == 'if' else NS)(N, 1.0 / 28.0)
    for phi in phis:
        t0 = time.time()
        uh = m.init_family(phi)
        _, ts, Es, Zs = m.run(uh, dt, int(round(T / dt)), every=1)
        i2 = int(round(2.0 / dt))
        s = f'scheme={scheme} N={N} K={m.g.K} dt={dt} phi={phi:.9f}: Z(2)={Zs[i2]:.12f}'
        if T >= 4.0:
            s += f' Z(4)={Zs[int(round(4.0/dt))]:.12f}'
        print(s + f' [{time.time()-t0:.0f}s]', flush=True)
