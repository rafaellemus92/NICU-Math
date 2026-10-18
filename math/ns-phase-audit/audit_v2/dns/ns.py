"""Independent pseudo-spectral Fourier-Galerkin solver for unforced 3D incompressible
Navier-Stokes on the 2pi-periodic cube. Written from scratch (numpy only).

  u_t + (u.grad)u = -grad p + nu Lap u,  div u = 0,  <u> = 0.

Rotational form: u_t = P[u x omega] - nu k^2 u  (P = Leray projector; the gradient
part grad(p + |u|^2/2) is removed by P).  Retained modes: cube max_i |k_i| <= K,
K = floor((N-1)/3), so the quadratic product evaluated on the N^3 grid is alias-free
on the retained modes (N > 3K).  Time stepping: classical RK4, fixed dt.

Normalisation: uh = rfftn(u)/N^3, so <|u|^2> = sum_k |uh_k|^2 over the full spectrum.
In the rfft half-spectrum, kz=0 (and kz=N/2) planes carry weight 1, others weight 2.
"""
import numpy as np

TWO_PI = 2.0 * np.pi


class Grid:
    def __init__(self, N, K=None):
        self.N = N
        self.K = (N - 1) // 3 if K is None else K
        k = np.fft.fftfreq(N, d=1.0 / N)            # integer wavenumbers, full axis
        kr = np.fft.rfftfreq(N, d=1.0 / N)          # half axis (last)
        self.kx = k[:, None, None]
        self.ky = k[None, :, None]
        self.kz = kr[None, None, :]
        shape = (N, N, N // 2 + 1)
        KX = np.broadcast_to(self.kx, shape)
        KY = np.broadcast_to(self.ky, shape)
        KZ = np.broadcast_to(self.kz, shape)
        self.kvec = np.stack([KX, KY, KZ]).astype(float)        # (3,N,N,N/2+1)
        self.k2 = (KX ** 2 + KY ** 2 + KZ ** 2).astype(float)
        K_ = self.K
        self.mask = ((np.abs(KX) <= K_) & (np.abs(KY) <= K_) & (np.abs(KZ) <= K_)).astype(float)
        self.mask[0, 0, 0] = 0.0                                    # mean zero
        w = np.full(N // 2 + 1, 2.0)
        w[0] = 1.0
        if N % 2 == 0:
            w[-1] = 1.0
        self.w = np.broadcast_to(w[None, None, :], shape)
        self.k2inv = np.where(self.k2 > 0, 1.0 / np.where(self.k2 > 0, self.k2, 1.0), 0.0)
        x = TWO_PI * np.arange(N) / N
        self.X = x[:, None, None]
        self.Y = x[None, :, None]
        self.Z = x[None, None, :]
        self.N3 = float(N) ** 3

    # transforms ---------------------------------------------------------
    def fwd(self, f):  # f: (..., N,N,N) real -> (..., N,N,N/2+1)
        return np.fft.rfftn(f, axes=(-3, -2, -1)) / self.N3

    def inv(self, fh):
        return np.fft.irfftn(fh * self.N3, s=(self.N, self.N, self.N), axes=(-3, -2, -1))

    # operators ----------------------------------------------------------
    def proj(self, fh):
        kd = (self.kvec * fh).sum(axis=0)
        return (fh - self.kvec * (kd * self.k2inv)) * self.mask

    def curl_h(self, uh):
        kx, ky, kz = self.kvec
        ux, uy, uz = uh
        return 1j * np.stack([ky * uz - kz * uy, kz * ux - kx * uz, kx * uy - ky * ux])

    def div_h(self, uh):
        return 1j * (self.kvec * uh).sum(axis=0)

    # diagnostics --------------------------------------------------------
    def inner(self, ah, bh):
        """<a.b> (normalised volume average) from half-spectra."""
        return float((self.w * (ah.conj() * bh).real).sum())

    def energy(self, uh):
        return 0.5 * self.inner(uh, uh)

    def enstrophy(self, uh):
        return 0.5 * float((self.w * self.k2 * (np.abs(uh) ** 2).sum(axis=0)).sum())

    def palin(self, uh):  # 1/2 <|grad omega|^2>
        return 0.5 * float((self.w * self.k2 ** 2 * (np.abs(uh) ** 2).sum(axis=0)).sum())


class NS:
    def __init__(self, N, nu=1.0 / 28.0, K=None):
        self.g = Grid(N, K)
        self.nu = nu
        self.visc = nu * self.g.k2

    def nonlin(self, uh):
        g = self.g
        u = g.inv(uh)
        w = g.inv(g.curl_h(uh))
        c = np.stack([u[1] * w[2] - u[2] * w[1],
                      u[2] * w[0] - u[0] * w[2],
                      u[0] * w[1] - u[1] * w[0]])
        return g.proj(g.fwd(c))

    def rhs(self, uh):
        return self.nonlin(uh) - self.visc * uh

    def step(self, uh, dt):
        k1 = self.rhs(uh)
        k2 = self.rhs(uh + 0.5 * dt * k1)
        k3 = self.rhs(uh + 0.5 * dt * k2)
        k4 = self.rhs(uh + dt * k3)
        return uh + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    def init_family(self, phi, a=1.0, b=1.0, c=1.0, d=1.0):
        g = self.g
        X, Y, Z = np.broadcast_arrays(g.X, g.Y, g.Z)
        u = np.stack([a * np.sin(Y), b * np.sin(Z), c * np.cos(X) - d * np.cos(X + Y + phi)])
        return g.proj(g.fwd(u))  # projection is identity here (div-free, retained)

    def run(self, uh, dt, nsteps, every=1, cb=None):
        """Advance nsteps; record (t, E, Z) every `every` steps (and at t=0)."""
        g = self.g
        ts, Es, Zs = [0.0], [g.energy(uh)], [g.enstrophy(uh)]
        for n in range(1, nsteps + 1):
            uh = self.step(uh, dt)
            if n % every == 0:
                ts.append(n * dt)
                Es.append(g.energy(uh))
                Zs.append(g.enstrophy(uh))
                if cb is not None:
                    cb(n, uh)
        return uh, np.array(ts), np.array(Es), np.array(Zs)


class NSTangent(NS):
    """Augmented system (u, v=du/dphi, w=d2u/dphi2):
       u_t = P[u x om(u)] - nu k^2 u
       v_t = P[u x om(v) + v x om(u)] - nu k^2 v
       w_t = P[u x om(w) + w x om(u) + 2 v x om(v)] - nu k^2 w
    RK4 on the augmented system gives the exact 1st/2nd phi-derivatives of the
    discrete RK4 map."""

    @staticmethod
    def cross(a, b):
        return np.stack([a[1] * b[2] - a[2] * b[1],
                         a[2] * b[0] - a[0] * b[2],
                         a[0] * b[1] - a[1] * b[0]])

    def rhs(self, Y):
        g = self.g
        uh, vh, wh = Y
        u, v, w = g.inv(uh), g.inv(vh), g.inv(wh)
        ou, ov, ow = g.inv(g.curl_h(uh)), g.inv(g.curl_h(vh)), g.inv(g.curl_h(wh))
        cr = self.cross
        nu_ = g.proj(g.fwd(cr(u, ou)))
        nv_ = g.proj(g.fwd(cr(u, ov) + cr(v, ou)))
        nw_ = g.proj(g.fwd(cr(u, ow) + cr(w, ou) + 2.0 * cr(v, ov)))
        return np.stack([nu_ - self.visc * uh, nv_ - self.visc * vh, nw_ - self.visc * wh])

    def init_aug(self, phi, d=1.0):
        g = self.g
        X, Y, Z = np.broadcast_arrays(g.X, g.Y, g.Z)
        uh = self.init_family(phi, d=d)
        zero = np.zeros_like(X)
        v = np.stack([zero, zero, d * np.sin(X + Y + phi)])     # d/dphi of u0
        w = np.stack([zero, zero, d * np.cos(X + Y + phi)])     # d2/dphi2 of u0
        return np.stack([uh, g.proj(g.fwd(v)), g.proj(g.fwd(w))])

    def zderivs(self, Y):
        g = self.g
        uh, vh, wh = Y
        Z = g.enstrophy(uh)
        wk = g.w * g.k2
        Z1 = float((wk * (uh.conj() * vh).real.sum(axis=0)).sum())
        Z2 = float((wk * ((np.abs(vh) ** 2).sum(axis=0) + (uh.conj() * wh).real.sum(axis=0))).sum())
        return Z, Z1, Z2
