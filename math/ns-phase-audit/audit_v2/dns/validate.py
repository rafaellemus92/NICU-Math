"""Validation of ns.py: divergence, energy identity, exact solutions, dZ/dt(0), dt-convergence,
convective-vs-rotational nonlinear term, Z/E at t=0."""
import time, sys
import numpy as np
sys.path.insert(0, '.')
from ns import NS, Grid

nu = 1.0 / 28.0
out = []
def p(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    out.append(s)

N = 24
m = NS(N, nu)
g = m.g
p(f'N={N} K={g.K}')

# 1. initial E, Z, divergence; dZ/dt(0) vs cos(phi)/4 - 7nu/2
for phi in [0.0, 0.5, 0.971073032, np.pi / 2, 2.159844949, np.pi]:
    uh = m.init_family(phi)
    # check initial field is reproduced exactly by the retained modes
    X, Y, Z = np.broadcast_arrays(g.X, g.Y, g.Z)
    u_ex = np.stack([np.sin(Y), np.sin(Z), np.cos(X) - np.cos(X + Y + phi)])
    err_ic = np.abs(g.inv(uh) - u_ex).max()
    E0, Z0 = g.energy(uh), g.enstrophy(uh)
    r = m.rhs(uh)
    dZdt = float((g.w * g.k2 * (uh.conj() * r).real.sum(axis=0)).sum())
    dEdt = g.inner(uh, r)
    nl = m.nonlin(uh)
    dEdt_nl = g.inner(uh, nl)
    p(f'phi={phi:.9f} E0={E0:.15f} Z0={Z0:.15f} |div|max={np.abs(g.div_h(uh)).max():.2e} '
      f'IC err={err_ic:.2e} dZ/dt(0)={dZdt:.15f} exact={np.cos(phi)/4 - 7*nu/2:.15f} '
      f'diff={dZdt-(np.cos(phi)/4-7*nu/2):.2e} dE/dt+2nuZ={dEdt+2*nu*Z0:.2e} <u.N>={dEdt_nl:.2e} '
      f'palin={g.palin(uh):.12f}')

# 2. convective form vs rotational form (projected), on a random retained div-free field and on IC
rng = np.random.default_rng(1)
def convective(uh):
    u = g.inv(uh)
    gradu = [g.inv(1j * g.kvec[j] * uh) for j in range(3)]   # d_j u_i, list over j of (3,...)
    c = sum(u[j] * gradu[j] for j in range(3))                 # (u.grad) u
    return -g.proj(g.fwd(c))
for name, uh in [('IC phi=0.7', m.init_family(0.7)),
                 ('random', g.proj(g.fwd(rng.standard_normal((3, N, N, N)))))]:
    a, b = m.nonlin(uh), convective(uh)
    p(f'{name}: max|rot - conv| = {np.abs(a-b).max():.2e} (max|rot|={np.abs(a).max():.2e}); '
      f'<u.N> = {g.inner(uh, a):.2e}; div N = {np.abs(g.div_h(a)).max():.2e}')

# 3. exact decaying solutions
def run_exact(name, u0fun, decay_rate, T=2.0, dt=0.005):
    X, Y, Z = np.broadcast_arrays(g.X, g.Y, g.Z)
    u0 = u0fun(X, Y, Z)
    uh = g.fwd(u0) * g.mask
    nst = int(round(T / dt))
    for _ in range(nst):
        uh = m.step(uh, dt)
    uex = u0 * np.exp(-decay_rate * T)
    err = np.abs(g.inv(uh) - uex).max()
    p(f'exact {name}: T={T} max|u-u_exact|={err:.2e} (|u_exact|max={np.abs(uex).max():.3f}), div={np.abs(g.div_h(uh)).max():.2e}')

# 2D Taylor-Green: nonlinear term is a pure gradient -> exact decay exp(-2 nu t)
run_exact('Taylor-Green 2D (k^2=2)', lambda X, Y, Z: np.stack([np.sin(X) * np.cos(Y), -np.cos(X) * np.sin(Y), 0 * X]), 2 * nu)
# Taylor-Green with higher wavenumber, rotated plane (y,z), k^2 = 2*9
run_exact('TG (y,z) k=3', lambda X, Y, Z: np.stack([0 * X, np.sin(3*Y) * np.cos(3*Z), -np.cos(3*Y) * np.sin(3*Z)]), 18 * nu)
# ABC Beltrami (curl u = u): u x omega = 0, exact decay exp(-nu t)
A, B, C = 1.0, 0.7, 0.4
run_exact('ABC Beltrami', lambda X, Y, Z: np.stack([A*np.sin(Z)+C*np.cos(Y), B*np.sin(X)+A*np.cos(Z), C*np.sin(Y)+B*np.cos(X)]), nu)
# Beltrami mixing three |k|^2=2 waves: helical waves with curl u = sqrt2 u
s2 = np.sqrt(2.0)
def belt2(X, Y, Z):
    # each term: helical wave with k=(1,1,0),(0,1,1),(1,0,1), eigenvalue +sqrt2 of curl
    def hw(kv, th, X, Y, Z):
        kv = np.array(kv, float); kh = kv / np.linalg.norm(kv)
        e1 = np.cross(kh, [0.3, -0.5, 0.8]); e1 /= np.linalg.norm(e1); e2 = np.cross(kh, e1)
        ph = kv[0]*X + kv[1]*Y + kv[2]*Z + th
        return np.stack([e1[i]*np.cos(ph) - e2[i]*np.sin(ph) for i in range(3)])
    return hw((1,1,0),0.3,X,Y,Z) + 0.8*hw((0,1,1),1.1,X,Y,Z) + 0.6*hw((1,0,1),2.0,X,Y,Z)
X, Y, Z = np.broadcast_arrays(g.X, g.Y, g.Z)
bh = g.fwd(belt2(X, Y, Z)) * g.mask
cb = g.curl_h(bh)
lam = np.sqrt(2.0)
p(f'Beltrami2 check: max|curl u - sqrt2 u| = {np.abs(cb - lam*bh).max():.2e} or -sqrt2: {np.abs(cb + lam*bh).max():.2e}')
run_exact('Beltrami |k|^2=2 mixture', belt2, 2 * nu)

# 4. energy identity along a trajectory (phi=0.5): dE/dt=-2nuZ instantaneous, and integrated
uh = m.init_family(0.5)
dt = 0.005
Elist, Zlist, inst = [g.energy(uh)], [g.enstrophy(uh)], []
for n in range(1, 801):
    uh = m.step(uh, dt)
    Elist.append(g.energy(uh)); Zlist.append(g.enstrophy(uh))
    if n % 200 == 0:
        r = m.rhs(uh)
        inst.append((n*dt, g.inner(uh, r) + 2*nu*g.enstrophy(uh), np.abs(g.div_h(uh)).max()))
Elist, Zlist = np.array(Elist), np.array(Zlist)
# Simpson integral of Z
h = dt
I = h/3*(Zlist[0] + Zlist[-1] + 4*Zlist[1:-1:2].sum() + 2*Zlist[2:-1:2].sum())
p(f'energy budget phi=0.5, T=4: E(T)={Elist[-1]:.12f}, E(0)-2nu*int Z = {Elist[0]-2*nu*I:.12f}, diff={Elist[-1]-(Elist[0]-2*nu*I):.2e}')
for t, r, d in inst:
    p(f'  t={t:.1f}: dE/dt + 2 nu Z = {r:.2e}, max|div| = {d:.2e}')

# 5. dt convergence of Z(2) at phi=0.971073032, N=24
for phi in [0.971073032]:
    vals = {}
    for dt in [0.02, 0.01, 0.005, 0.0025]:
        uh = m.init_family(phi)
        for _ in range(int(round(2.0/dt))):
            uh = m.step(uh, dt)
        vals[dt] = g.enstrophy(uh)
        p(f'dt={dt}: Z(2)={vals[dt]:.13f}')
    d1 = vals[0.02]-vals[0.01]; d2 = vals[0.01]-vals[0.005]; d3 = vals[0.005]-vals[0.0025]
    p(f'diffs: {d1:.3e} {d2:.3e} {d3:.3e}; ratios {d1/d2:.2f} {d2/d3:.2f}; Richardson-est error at dt=0.005: {d3*16/15:.2e}')

open('./validate.out', 'w').write('\n'.join(out) + '\n')
