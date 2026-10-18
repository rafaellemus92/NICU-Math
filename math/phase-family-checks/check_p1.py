"""Independent check of the beta=0 restricted-family claims.

Family: u0 = (a sin y, 0, c cos x - d cos(x+y+phi)) on [0,2pi]^3, viscosity nu >= 0.
Claims: (1) inviscid  Z(t,phi) = (a^2+c^2+2d^2)/4 + a c d t cos(phi)/4 + a^2 t^2 (c^2+d^2)/8,
            with Z = (1/2) * torus average of |omega|^2;
        (2) for nu >= 0, E(t,.) and Z(t,.) are A + B cos(phi): no sin(phi), no |m|>=2 harmonics.
Three checks: A quadrature of the exact inviscid solution; B the 1D complex-amplitude
reduction with viscosity; C a full 3D pseudo-spectral Navier-Stokes run compared with B.
"""
import numpy as np, time
rng = np.random.default_rng(1)

# ---------- A: inviscid exact solution, quadrature ----------
def Z_formula(a, c, d, t, phi):
    return (a*a + c*c + 2*d*d)/4 + a*c*d*t*np.cos(phi)/4 + a*a*t*t*(c*c + d*d)/8

def Z_inviscid_quadrature(a, c, d, t, phi, N=256):
    x = np.arange(N)*2*np.pi/N; y = x.copy()
    X, Y = np.meshgrid(x, y, indexing='ij')
    th = X - a*t*np.sin(Y)
    psi = th + Y + phi
    wx = -c*np.sin(th) + d*np.sin(psi)
    wy = a*t*c*np.cos(Y)*np.sin(th) + d*(1 - a*t*np.cos(Y))*np.sin(psi)
    om2 = wx**2 + wy**2 + (a*np.cos(Y))**2
    return 0.5*om2.mean()

print("A. inviscid formula vs quadrature of the exact transported solution")
worst = 0.0
for _ in range(20):
    a, c, d = rng.uniform(-2, 2, 3); t = rng.uniform(0, 4); phi = rng.uniform(0, 2*np.pi)
    err = abs(Z_formula(a, c, d, t, phi) - Z_inviscid_quadrature(a, c, d, t, phi))
    worst = max(worst, err)
print(f"   max |formula - quadrature| over 20 random (a,c,d,t,phi): {worst:.2e}")

# ---------- B: viscous reduction, 1D complex amplitude in Fourier-y ----------
# w(x,y,t) = Re(e^{ix} W(y,t)),  W_t + i a e^{-nu t} sin(y) W = nu (W_yy - W)
# Fourier in y: What_k' = -nu (k^2+1) What_k - (a e^{-nu t}/2) (What_{k-1} - What_{k+1})
def solve_W(a, nu, T, data, K=48, nsteps=4000):
    ks = np.arange(-K, K+1)
    W = np.zeros(len(ks), complex); W[K + data] = 1.0   # data = y-frequency of the initial mode (0 or 1)
    def rhs(t, W):
        sh = np.zeros_like(W); sh[1:] += W[:-1]; sh[:-1] -= W[1:]   # What_{k-1} - What_{k+1}
        return -nu*(ks**2 + 1)*W - 0.5*a*np.exp(-nu*t)*sh
    dt = T/nsteps; t = 0.0
    for _ in range(nsteps):
        k1 = rhs(t, W); k2 = rhs(t+dt/2, W+dt/2*k1); k3 = rhs(t+dt/2, W+dt/2*k2); k4 = rhs(t+dt, W+dt*k3)
        W = W + dt/6*(k1 + 2*k2 + 2*k3 + k4); t += dt
    return ks, W

def EZ_reduced(a, c, d, nu, T, phis):
    ks, Wc = solve_W(a, nu, T, 0); _, Wd = solve_W(a, nu, T, 1)
    E = []; Z = []
    for phi in phis:
        W = c*Wc - d*np.exp(1j*phi)*Wd
        # torus averages: <w^2> = sum|W_k|^2 / 2 ; <(w_x)^2> same ; <(w_y)^2> = sum k^2 |W_k|^2 / 2
        u1sq = 0.5*(a*np.exp(-nu*T))**2
        E.append(0.5*(u1sq + 0.5*np.sum(np.abs(W)**2)))
        Z.append(0.5*(u1sq + 0.5*np.sum(np.abs(W)**2) + 0.5*np.sum(ks**2*np.abs(W)**2)))
    return np.array(E), np.array(Z)

def harmonics(vals):
    """Fourier coefficients in phi of a real sequence on a uniform phi grid."""
    c = np.fft.rfft(vals)/len(vals)
    return c   # c[0] = mean, c[m] = (A_m - i B_m)/2 for cos/sin coefficients

print("\nB. viscous reduction: harmonics in phi of E and Z")
M = 32; phis = np.arange(M)*2*np.pi/M
for (a, c, d, nu, T) in [(1, 1, 1, 0.1, 2.0), (1.3, -0.7, 0.9, 1/28, 4.0), (1, 1, 1, 0.0, 2.0)]:
    E, Z = EZ_reduced(a, c, d, nu, T, phis)
    hE, hZ = harmonics(E), harmonics(Z)
    print(f"   a={a} c={c} d={d} nu={nu} T={T}")
    print(f"     Z: A={hZ[0].real:.6f}  B(cos)={2*hZ[1].real:.6f}  sin coeff={-2*hZ[1].imag:.1e}  max|m>=2|={np.abs(hZ[2:]).max():.1e}")
    print(f"     E: A={hE[0].real:.6f}  B(cos)={2*hE[1].real:.6f}  sin coeff={-2*hE[1].imag:.1e}  max|m>=2|={np.abs(hE[2:]).max():.1e}")
    if nu == 0.0:
        print(f"     inviscid: formula A={(a*a+c*c+2*d*d)/4 + a*a*T*T*(c*c+d*d)/8:.6f} B={a*c*d*T/4:.6f}; "
              f"E formula={(a*a+c*c+d*d)/4:.6f}")

# ---------- C: full 3D pseudo-spectral Navier-Stokes ----------
def ns3d(u0_fn, nu, T, N=24, dt=0.005):
    k1 = np.fft.fftfreq(N, 1/N); kx, ky, kz = np.meshgrid(k1, k1, k1, indexing='ij')
    k2 = kx**2 + ky**2 + kz**2; k2n = np.where(k2 == 0, 1, k2)
    kmax = N//3; deal = (np.abs(kx) <= kmax) & (np.abs(ky) <= kmax) & (np.abs(kz) <= kmax)
    x = np.arange(N)*2*np.pi/N; X, Y, Zg = np.meshgrid(x, x, x, indexing='ij')
    u = np.array(u0_fn(X, Y, Zg)); uh = np.fft.fftn(u, axes=(1, 2, 3))*deal
    K = np.array([kx, ky, kz])
    def proj(fh):
        div = np.sum(K*fh, axis=0)
        return fh - K*(div/k2n)
    def nonlin(uh):
        ur = np.real(np.fft.ifftn(uh, axes=(1, 2, 3)))
        # omega x u form: N(u) = -P[(u.grad)u]; use rotational form -P[omega x u] (same after projection)
        oh = 1j*np.array([ky*uh[2]-kz*uh[1], kz*uh[0]-kx*uh[2], kx*uh[1]-ky*uh[0]])
        om = np.real(np.fft.ifftn(oh, axes=(1, 2, 3)))
        c = np.cross(om, ur, axis=0)
        return -proj(np.fft.fftn(c, axes=(1, 2, 3))*deal)
    n = int(round(T/dt)); E_ = np.exp(-nu*k2*dt); Eh = np.exp(-nu*k2*dt/2)
    for _ in range(n):   # Lawson RK4 (integrating factor)
        a1 = nonlin(uh); a2 = nonlin(Eh*(uh + dt/2*a1)); a3 = nonlin(Eh*uh + dt/2*a2)
        a4 = nonlin(E_*uh + dt*Eh*a3)
        uh = E_*uh + dt/6*(E_*a1 + 2*Eh*(a2 + a3) + a4)
    oh = 1j*np.array([ky*uh[2]-kz*uh[1], kz*uh[0]-kx*uh[2], kx*uh[1]-ky*uh[0]])
    E = 0.5*np.sum(np.abs(uh)**2)/N**6; Zv = 0.5*np.sum(np.abs(oh)**2)/N**6
    return E, Zv

print("\nC. full 3D Navier-Stokes (N=24, Lawson RK4) vs the reduction, a=c=d=1, nu=0.1, T=1")
a = c = d = 1.0; nu = 0.1; T = 1.0
phis_c = np.array([0.0, np.pi/3, np.pi/2, np.pi])
E_red, Z_red = EZ_reduced(a, c, d, nu, T, phis_c)
t0 = time.time()
for i, phi in enumerate(phis_c):
    E3, Z3 = ns3d(lambda X, Y, Zg: [a*np.sin(Y), 0*X, c*np.cos(X) - d*np.cos(X + Y + phi)], nu, T)
    print(f"   phi={phi:.4f}: E3D={E3:.10f} Ered={E_red[i]:.10f} dE={E3-E_red[i]:.1e} | "
          f"Z3D={Z3:.10f} Zred={Z_red[i]:.10f} dZ={Z3-Z_red[i]:.1e}")
print(f"   ({time.time()-t0:.1f}s)")
# fit A + B cos(phi) to the 3D values at 4 phases and report the residual
Zs = []
for phi in phis_c:
    pass
