"""Measured growth of the perturbation v = u_b - u_0 (phi = 0, nu = 1/28, N = 24):
    y(t) = ||grad v||^2 / ||grad v(0)||^2  and  ||v||^2 / ||v(0)||^2,
to compare with the Gronwall factors Phi(t) and exp(2 I1(t)) of the explicit bound.
Run: python3 perturbation_growth.py b T dt
"""
import sys, json, numpy as np
from full_family_dns import make_solver, family

b, T, dt = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
N, nu = 24, 1/28
project, step, _ = make_solver(N, nu, dt)
k1 = np.fft.fftfreq(N) * N
kx, ky, kz = np.meshgrid(k1, k1, k1, indexing="ij")
k2 = kx ** 2 + ky ** 2 + kz ** 2
ub = project(np.array([np.fft.fftn(c) for c in family(N, 1.0, b, 1.0, 1.0, 0.0)]))
u0 = project(np.array([np.fft.fftn(c) for c in family(N, 1.0, 0.0, 1.0, 1.0, 0.0)]))
def norms(vh):
    return float(np.sum(np.abs(vh) ** 2)) / N ** 6 * (2 * np.pi) ** 3, float(np.sum(k2 * np.abs(vh) ** 2)) / N ** 6 * (2 * np.pi) ** 3
l20, h10 = norms(ub - u0)
print(f"b={b}: ||v(0)||^2 = {l20:.6f} (exact b^2 (2pi)^3/2 = {b*b*(2*np.pi)**3/2:.6f}), ||grad v(0)||^2 = {h10:.6f}")
rows = []
nsteps = int(round(T / dt)); every = int(round(0.5 / dt))
for n in range(nsteps + 1):
    if n % every == 0:
        l2, h1 = norms(ub - u0)
        rows.append((n * dt, l2 / l20, h1 / h10))
        print(f"  t={n*dt:5.1f}  ||v||^2/||v0||^2 = {l2/l20:8.4f}   ||grad v||^2/||grad v0||^2 = {h1/h10:8.4f}", flush=True)
    if n < nsteps:
        ub, u0 = step(ub), step(u0)
peak = max(rows, key=lambda r: r[2])
print(f"peak enstrophy amplification {peak[2]:.4f} at t = {peak[0]:.1f};  peak energy amplification {max(r[1] for r in rows):.4f}")
json.dump(dict(b=b, rows=rows), open(f"perturbation_growth_b{b}.json", "w"))
