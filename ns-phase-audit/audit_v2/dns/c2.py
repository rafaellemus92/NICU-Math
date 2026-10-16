"""C2: symmetry Z(T,phi) = Z(T,-phi), N=24, phi=0.5, T=2, plus explicit check of the
map F[u](x) = R u(R x + b), R = diag(-1,-1,1), b = (0,0,pi), on fields at t=0 and t=T."""
import sys
import numpy as np
sys.path.insert(0, '.')
from ns import NS

N, phi, T, dt = 24, 0.5, 2.0, 0.005
m = NS(N, 1.0 / 28.0)
g = m.g
nst = int(round(T / dt))

def F(u):
    """F[u](x) = R u(Rx+b) on the grid: x_i -> -x_i, y_j -> -y_j, z_l -> z_l + pi."""
    i = (-np.arange(N)) % N
    l = (np.arange(N) + N // 2) % N
    v = u[:, i][:, :, i][:, :, :, l]
    return v * np.array([-1.0, -1.0, 1.0])[:, None, None, None]

up0, um0 = m.init_family(phi), m.init_family(-phi)
print('t=0: max|F[u_phi] - u_-phi| =', np.abs(F(g.inv(up0)) - g.inv(um0)).max())
up, tp, Ep, Zp = m.run(up0, dt, nst)
um, tm, Em, Zm = m.run(um0, dt, nst)
print(f'Z(2, +0.5) = {Zp[-1]:.15f}')
print(f'Z(2, -0.5) = {Zm[-1]:.15f}')
print(f'difference = {Zp[-1]-Zm[-1]:.3e}; max over all steps |Z(t,+)-Z(t,-)| = {np.abs(Zp-Zm).max():.3e}; '
      f'max |E(t,+)-E(t,-)| = {np.abs(Ep-Em).max():.3e}')
print('t=2: max|F[u(T;phi)] - u(T;-phi)| =', np.abs(F(g.inv(up)) - g.inv(um)).max(),
      ' (max|u| =', np.abs(g.inv(up)).max(), ')')
# Control: the map is NOT trivial -- u(T;phi) and u(T;-phi) differ as fields
print('control: max|u(T;phi) - u(T;-phi)| =', np.abs(g.inv(up) - g.inv(um)).max())
# Control 2: another reflection candidate that should NOT map the family to itself
X, Y, Z = np.broadcast_arrays(g.X, g.Y, g.Z)
