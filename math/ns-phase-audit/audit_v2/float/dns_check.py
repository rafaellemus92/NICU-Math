"""Independent validation of the recurrence: direct RK4 pseudo-spectral DNS
(2/3-dealiased, N=48) of the same initial value problem, compared with the
partial sums sum_{n<=12} Z_n t^n from the recurrence (phi=0.7, nu=1/28 and
phi=2.1, nu=1/7, unit amplitudes)."""
import numpy as np
from nsseries import Grid, series, initial_hat, curl_hat, project, cross, FFT, IFFT, AX
def dns(phi, nu, T, dt, N=48):
    g = Grid(N)
    Uh = initial_hat(g, 1, 1, 1, np.exp(1j * phi), np.exp(-1j * phi))
    dealias = (np.abs(g.Kint).max(0) < N / 3)
    def rhs(Uh):
        u = IFFT(Uh, axes=AX); w = IFFT(curl_hat(g.K, Uh), axes=AX)
        Nh = FFT(cross(u, w), axes=AX) * dealias
        return project(g.K, g.K2inv, Nh) - nu * g.K2 * Uh
    def Z(Uh):
        Wh = curl_hat(g.K, Uh) / N ** 3
        return 0.5 * (np.abs(Wh) ** 2).sum()
    out = {0.0: Z(Uh)}
    t = 0.0; nsteps = int(round(T / dt))
    for s in range(nsteps):
        k1 = rhs(Uh); k2 = rhs(Uh + dt / 2 * k1); k3 = rhs(Uh + dt / 2 * k2); k4 = rhs(Uh + dt * k3)
        Uh = Uh + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t = (s + 1) * dt
        if abs(t / 0.05 - round(t / 0.05)) < 1e-9:
            out[round(t, 6)] = Z(Uh)
    return out
for phi, nu in [(0.7, 1/28), (2.1, 1/7)]:
    Zc = series(1, 1, 1, np.exp(1j * phi), np.exp(-1j * phi), nu, 12, Grid(28))["Z"].real
    for dt in [0.01, 0.005]:
        res = dns(phi, nu, 0.2, dt)
        for t, z in res.items():
            if t == 0: continue
            ser = sum(Zc[n] * t ** n for n in range(13))
            print(f"phi={phi} nu={nu:.4f} dt={dt}: t={t:.2f}  Z_DNS={z:.15f}  Z_series(n<=12)={ser:.15f}  diff={z-ser:+.2e}")
