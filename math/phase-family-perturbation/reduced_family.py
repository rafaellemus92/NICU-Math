"""The family u0 = (a sin y, 0, c cos x - d cos(x+y+phi)) with nothing depending on z.

U(y,t) = a e^{-nu t} sin y exactly; w = Re[wh(y,t) e^{ix}] with
    wh_t + i U wh = nu (wh_yy - wh),   wh(y,0) = c - d e^{i(y+phi)}.
Averages:  <w^2> = <|wh|^2>_y / 2,  <w_x^2> = <|wh|^2>_y / 2,  <w_y^2> = <|wh_y|^2>_y / 2,
vorticity (w_y, -w_x, -U'), so
    E = a^2 e^{-2 nu t}/4 + <|wh|^2>_y/4,
    Z = a^2 e^{-2 nu t}/4 + <|wh|^2 + |wh_y|^2>_y/4,
    S = -<U' w_x w_y> = -(a e^{-nu t}/2) Re <cos y . conj(i wh) . wh_y>_y   (w_x = Re[i wh e^{ix}]).
Checks: (1) inviscid closed form Z = (a^2+c^2+2d^2)/4 + acd t cos(phi)/4 + a^2 t^2 (c^2+d^2)/8;
(2) with nu = 1/28, the phi-harmonics of E, Z, S above the first vanish to rounding;
(3) the cos(phi) part of E is O(nu).
Spectral in y (M modes), RK4 in time; stdlib + numpy.
"""
import numpy as np, sys

def run(a, c, d, phi, nu, T, M=64, dt=1e-3):
    y = 2*np.pi*np.arange(M)/M
    k = np.fft.fftfreq(M)*M
    wh = c - d*np.exp(1j*(y+phi))
    def rhs(t, wh):
        U = a*np.exp(-nu*t)*np.sin(y)
        whh = np.fft.fft(wh)
        diff = np.fft.ifft(-(k**2+1)*whh)
        return -1j*U*wh + nu*diff
    n = int(round(T/dt)); t = 0.0
    for _ in range(n):
        k1 = rhs(t, wh); k2 = rhs(t+dt/2, wh+dt/2*k1); k3 = rhs(t+dt/2, wh+dt/2*k2); k4 = rhs(t+dt, wh+dt*k3)
        wh = wh + dt/6*(k1+2*k2+2*k3+k4); t += dt
    whh = np.fft.fft(wh)
    why = np.fft.ifft(1j*k*whh)
    Ua = a*np.exp(-nu*t)
    E = Ua**2/4 + np.mean(np.abs(wh)**2)/4
    Z = Ua**2/4 + np.mean(np.abs(wh)**2 + np.abs(why)**2)/4
    S = -(Ua/2)*np.mean(np.cos(y)*np.real(np.conj(1j*wh)*why))
    return E, Z, S

def harmonics(vals, phis, m=4):
    """Fourier coefficients in phi: returns {0: A, 1: (cos, sin), 2: ...}."""
    out = {}
    for j in range(m+1):
        cj = np.mean(vals*np.cos(j*phis))*(1 if j == 0 else 2)
        sj = np.mean(vals*np.sin(j*phis))*2
        out[j] = (cj, sj)
    return out

if __name__ == "__main__":
    a, c, d = 1.0, 1.0, 1.0
    phis = 2*np.pi*np.arange(16)/16
    # (1) inviscid closed form at several t
    print("(1) inviscid, a=c=d=1: max |Z_numeric - Z_formula| over 16 phases")
    for T in (0.5, 1.0, 2.0):
        Zs = np.array([run(a, c, d, p, 0.0, T, M=96, dt=5e-4)[1] for p in phis])
        Zf = (a*a+c*c+2*d*d)/4 + a*c*d*T*np.cos(phis)/4 + a*a*T*T*(c*c+d*d)/8
        print(f"   t={T}: {np.max(np.abs(Zs-Zf)):.1e}   (Z ranges {Zs.min():.6f}..{Zs.max():.6f})")
    # also a non-unit amplitude set
    a2, c2, d2 = 0.7, 1.3, 0.4
    Zs = np.array([run(a2, c2, d2, p, 0.0, 1.0, M=96, dt=5e-4)[1] for p in phis])
    Zf = (a2*a2+c2*c2+2*d2*d2)/4 + a2*c2*d2*1.0*np.cos(phis)/4 + a2*a2*1.0*(c2*c2+d2*d2)/8
    print(f"   a,c,d=0.7,1.3,0.4 t=1: {np.max(np.abs(Zs-Zf)):.1e}")
    # (2) nu = 1/28: harmonic content of E, Z, S at t = 0.5 and 2
    nu = 1/28
    for T in (0.5, 2.0):
        res = np.array([run(a, c, d, p, nu, T, M=96, dt=5e-4) for p in phis])
        for name, col in (("E", 0), ("Z", 1), ("S", 2)):
            h = harmonics(res[:, col], phis)
            print(f"(2) nu=1/28 t={T} {name}: A={h[0][0]:+.9f} B1cos={h[1][0]:+.9f} B1sin={h[1][1]:+.1e} |cos2|={abs(h[2][0]):.1e} |cos3|={abs(h[3][0]):.1e} |cos4|={abs(h[4][0]):.1e}")
    # (3) cos(phi) part of E scales with nu
    print("(3) E's cos(phi) coefficient at t=1 for nu = 1/28, 1/56, 1/112:")
    for nu in (1/28, 1/56, 1/112):
        Es = np.array([run(a, c, d, p, nu, 1.0, M=96, dt=5e-4)[0] for p in phis])
        print(f"   nu={nu:.5f}: B_E = {harmonics(Es, phis)[1][0]:+.6e}  ratio to nu: {harmonics(Es, phis)[1][0]/nu:+.5f}")
