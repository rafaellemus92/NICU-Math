import sys, numpy as np
sys.path.insert(0, '../../periodic_ns_lab_v2')
from ns_solver import PeriodicNS, fft, ifft, cross

def rand_retained(s, seed=3):
    rng = np.random.default_rng(seed)
    return s.project(fft(rng.normal(size=(3, s.n, s.n, s.n))))

def embed(a, nlo, nhi):
    freq = np.rint(np.fft.fftfreq(nlo)*nlo).astype(int); idx = freq % nhi
    out = np.zeros((3, nhi, nhi, nhi), complex)
    for c in range(3): out[c][np.ix_(idx, idx, idx)] = a[c]
    return out

def restrict(a, nhi, nlo):
    freq = np.rint(np.fft.fftfreq(nlo)*nlo).astype(int); idx = freq % nhi
    return np.stack([a[c][np.ix_(idx, idx, idx)] for c in range(3)])

print("== kmax per n:", {n: PeriodicNS(n).kmax for n in (16, 24, 32, 48, 64)}, " 3K<n:", all(3*PeriodicNS(n).kmax < n for n in (16,24,32,48,64)))
# 1. dealiasing exactness: N=24 Galerkin nonlinearity vs alias-free N=64 evaluation of the same retained field
s24, s64 = PeriodicNS(24), PeriodicNS(64)
a = rand_retained(s24)
nl24 = s24.nonlinear(a)
nl64 = s64.nonlinear(embed(a, 24, 64))
exact_on_24 = restrict(nl64, 64, 24) * s24.mask
print("1. dealiasing: max|N_24 - P_K N_exact| =", np.max(np.abs(nl24 - exact_on_24)), " scale", np.max(np.abs(nl24)))
# counterexample: K=8 (3K=N=24) contaminates retained modes
s_bad = PeriodicNS(24); s_bad.kmax = 8; s_bad.mask = np.max(np.abs(s_bad.k), axis=0) <= 8
ab = rand_retained(s_bad)
nlb = s_bad.nonlinear(ab)
ex = restrict(s64.nonlinear(embed(ab, 24, 64)), 64, 24) * s_bad.mask
print("   counterexample K=8 on N=24 (3K=N): max error =", np.max(np.abs(nlb - ex)))
# 2. Hermitian symmetry, zero mean, divergence after evolution
s = PeriodicNS(24); u = s.initial(phase=0.97)
for _ in range(50): u = s.step(u, 0.01)
neg = np.stack([np.roll(np.flip(c, axis=(0, 1, 2)), 1, axis=(0, 1, 2)) for c in u])  # u(-k)
print("2. Hermitian max|u(-k)-conj u(k)| =", np.max(np.abs(neg - u.conj())), " mean:", np.max(np.abs(u[:, 0, 0, 0])),
      " max|k.u|:", np.max(np.abs(np.sum(s.k*u, axis=0))), " outside mask:", np.max(np.abs(u*(~s.mask))),
      " imag(ifft):", np.max(np.abs(ifft(u).imag)))
# 3. Equivariance of the Galerkin RHS under F[u](x)=R u(Rx+b), R=diag(-1,-1,1), b=(0,0,pi) (exact grid map for even n)
def Fmap(uh):
    up = ifft(uh).real; n = up.shape[-1]
    ind = (-np.arange(n)) % n; zind = (np.arange(n)+n//2) % n
    v = up[:, ind][:, :, ind][:, :, :, zind].copy(); v[0:2] *= -1
    return fft(v)
a = rand_retained(s, 11)
print("3. equivariance max|F[rhs(a)] - rhs(F[a])| =", np.max(np.abs(Fmap(s.rhs(a)) - s.rhs(Fmap(a)))),
      " |F[u_phi]-u_-phi| =", np.max(np.abs(Fmap(s.initial(phase=0.6)) - s.initial(phase=-0.6))))
# 4. Shell flux sign: d/dt E(|k|^2<=m) = -Pi(m) - 2 nu sum_{<=m} k^2 E(k)
u = s.initial(phase=0.0)
for _ in range(100): u = s.step(u, 0.01)
rows = s.shell_rows(u, 1.0)
h = 1e-4
up = s.step(u, h); um = s.step(u, -h) if False else None
# centered difference using forward and a backward step done as RK4 with negative dt is disallowed; use forward 2-point Richardson
u1 = s.step(u, h); u2 = s.step(u1, h)
def Ele(v, m):
    p = np.sum(np.abs(v)**2, axis=0); return 0.5*np.sum(p[s.mask & (s.k2 <= m)])
def Dle(v, m):
    p = np.sum(np.abs(v)**2, axis=0); return np.sum((s.k2*p)[s.mask & (s.k2 <= m)])
worst = 0
for r in rows[:-1]:
    m = r['k_squared']
    dE = (-3*Ele(u, m) + 4*Ele(u1, m) - Ele(u2, m))/(2*h)
    pred = -r['energy_flux_out'] - s.nu*Dle(u, m)
    worst = max(worst, abs(dE - pred))
print("4. shell budget dE_<=m/dt + Pi(m) + nu*D_<=m max residual =", worst, "; Pi(m) at m=1,2,3,6:",
      [round(r['energy_flux_out'], 6) for r in rows if r['k_squared'] in (1, 2, 3, 6)], "; last Pi:", rows[-1]['energy_flux_out'])
# 5. production viscosity and energy identity
print("5. default nu:", PeriodicNS(24).nu, "== 1/28:", PeriodicNS(24).nu == 1/28)
