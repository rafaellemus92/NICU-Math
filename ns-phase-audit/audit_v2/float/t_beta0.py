"""T4 / P1: beta = 0.
(a) Laurent tables with beta=0 (N=28, M=32, nmax=12) at nu=0, 1/28, 1/7 (unit
    alpha,gamma,delta) and at a generic tuple (alpha,gamma,delta,nu)=(0.83,1.29,0.71,0.05):
    max |c_{n,m}| over |m|>=2 vs the m=0,1 entries.
(b) Mechanism: the computed U_n (spectral) with beta=0 are checked to be
    z-independent (no k_z != 0 content), U_n,1 = alpha (-nu)^n/n! sin y,
    U_n,2 = 0, U_n,3 supported on k_x = +-1 only, and U_n,3 is linear
    (superposition) in the u3 data (gamma, p, q)."""
import math, numpy as np
from nsseries import Grid, phi_scan, series, laurent
g = Grid(28)
nmax = 12
for (al, ga, de, nu) in [(1, 1, 1, 0.0), (1, 1, 1, 1/28), (1, 1, 1, 1/7), (0.83, 1.29, 0.71, 0.05)]:
    Z, c, mm, _ = phi_scan(32, nmax, g, alpha=al, beta=0.0, gamma=ga, delta=de, nu=nu)
    big = max(abs(c[n, i]) for n in range(nmax + 1) for i, m in enumerate(mm) if abs(m) >= 2)
    where = max(((abs(c[n, i]), n, m) for n in range(nmax + 1) for i, m in enumerate(mm) if abs(m) >= 2))
    m1 = [abs(laurent(c, mm, n, 1)) for n in range(nmax + 1)]
    m0 = [abs(laurent(c, mm, n, 0)) for n in range(nmax + 1)]
    print(f"beta=0, alpha={al} gamma={ga} delta={de} nu={nu:.5f}: max_{{n<=12,|m|>=2}} |c_nm| = {big:.2e} (at n={where[1]}, m={where[2]})")
    print("    |c_n0| =", " ".join(f"{x:.2e}" for x in m0))
    print("    |c_n1| =", " ".join(f"{x:.2e}" for x in m1))
# (b) field structure
al, ga, nu = 0.83, 1.29, 0.05
p, q = 0.71 * np.exp(0.9j), 0.71 * np.exp(-0.9j)
r = series(al, 0.0, ga, p, q, nu, nmax, g, diag=True)
Uh = r["Uh"]
N3 = g.N ** 3
Kx, Ky, Kz = g.Kint
worst = dict(kz=0, u1=0, u2=0, kx=0, lin=0)
rg = series(0, 0.0, ga, 0, 0, nu, nmax, g, diag=True)["Uh"]
rp = series(0, 0.0, 0, p, 0, nu, nmax, g, diag=True)["Uh"]
rq = series(0, 0.0, 0, 0, q, nu, nmax, g, diag=True)["Uh"]
ra = series(al, 0.0, 0, 0, 0, nu, nmax, g, diag=True)["Uh"]
sc = max(np.abs(Uh[n] / N3).max() for n in range(nmax + 1))  # absolute scale: max over all orders
for n in range(nmax + 1):
    U = Uh[n] / N3
    worst["kz"] = max(worst["kz"], np.abs(U[:, Kz != 0]).max() / sc)
    ref = np.zeros_like(U[0]); ref[0, 1, 0] = al * (-nu) ** n / math.factorial(n) / 2j; ref[0, -1, 0] = -ref[0, 1, 0]
    worst["u1"] = max(worst["u1"], np.abs(U[0] - ref).max() / sc)
    worst["u2"] = max(worst["u2"], np.abs(U[1]).max() / sc)
    worst["kx"] = max(worst["kx"], np.abs(U[2][np.abs(Kx) != 1]).max() / sc)
    # u3 linearity: u3[alpha; gamma,p,q] = u3[alpha;gamma,0,0] + u3[alpha;0,p,0] + u3[alpha;0,0,q]  (alpha fixed => linear advection operator)
    # (series is not linear in alpha, so compare at fixed alpha)
for n in range(nmax + 1):
    pass
r_g = series(al, 0.0, ga, 0, 0, nu, nmax, g, diag=True)["Uh"]
r_p = series(al, 0.0, 0, p, 0, nu, nmax, g, diag=True)["Uh"]
r_q = series(al, 0.0, 0, 0, q, nu, nmax, g, diag=True)["Uh"]
for n in range(nmax + 1):
    lhs = Uh[n][2]
    rhs = r_g[n][2] + r_p[n][2] + r_q[n][2]
    worst["lin"] = max(worst["lin"], np.abs(lhs - rhs).max() / N3 / sc)
    # k_x content of the p-driven part: only k_x=+1
r_p_kx = max(np.abs((r_p[n][2] / N3)[Kx != 1]).max() for n in range(nmax + 1))
r_q_kx = max(np.abs((r_q[n][2] / N3)[Kx != -1]).max() for n in range(nmax + 1))
print("\nfield-structure check with beta=0 (max abs Fourier-coefficient defect over n<=12, divided by max_n max|U_n| = %.3f):" % sc)
print("  (min over n of max|U_n| = %.2e)" % min(np.abs(Uh[n] / N3).max() for n in range(nmax + 1)))
print("  content at k_z != 0                      :", f"{worst['kz']:.1e}")
print("  |U_n,1 - alpha(-nu)^n/n! sin y|           :", f"{worst['u1']:.1e}")
print("  |U_n,2|                                   :", f"{worst['u2']:.1e}")
print("  U_n,3 content at |k_x| != 1               :", f"{worst['kx']:.1e}")
print("  superposition defect of u3 in (gamma,p,q) :", f"{worst['lin']:.1e}")
print("  p-driven u3 content at k_x != +1 (abs)    :", f"{r_p_kx:.1e};  q-driven at k_x != -1: {r_q_kx:.1e}")
