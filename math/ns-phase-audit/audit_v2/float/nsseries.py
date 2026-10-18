"""
Floating-point Taylor-series engine for unforced incompressible Navier-Stokes
on the 2pi-periodic cube (written from scratch, numpy only).

    u_t + (u.grad)u = -grad p + nu Lap u,   div u = 0,   <u> = 0.

Write u(x,t) = sum_n U_n(x) t^n.  In rotational form
    u_t = P(u x omega) + nu Lap u,          omega = curl u,
so that
    (n+1) U_{n+1} = nu Lap U_n + P sum_{j=0}^{n} U_j x curl U_{n-j}.          (R)
(advective variant: replace the sum by -P sum_j (U_j.grad) U_{n-j}; the two
sums differ by a gradient, killed by P -- see docstring of `series`).

Pseudo-spectral evaluation: U_n stored as unnormalised numpy FFT coefficients on
an N^3 grid; derivatives, Leray projector P and Laplacian are diagonal in k;
products are formed pointwise on the grid.  Support bound: U_n has
max_i |k_i| <= n+1 (U_0 does; the product in step n has support <= n+2;
diagonal operators do not enlarge it).  The product in step n is alias-free on
an N-grid iff the 2(n+2)+1 integers -(n+2)..(n+2) are distinct mod N, i.e.
N >= 2(n+2)+1.  The last step needed for Z up to order nmax is n = nmax-1, so
N >= 2*nmax + 3 suffices (N=24 for nmax<=10, N=28 for nmax<=12, N=32 for
nmax<=14).  The order-nmax enstrophy <omega_j . omega_{nmax-j}> only needs the
k=0 mode of a product of support <= nmax+2 < N: exact.

All parameters may be COMPLEX: every operation is polynomial (bilinear
products, linear operators, bilinear -- not Hermitian -- averages), so a run
with complex alpha, beta, gamma, p, q, nu returns the analytic continuation of
the Taylor coefficients, which is what is needed to separate polynomial
degrees by discrete Fourier analysis on circles.

Initial condition:
    u1 = alpha sin y
    u2 = beta  sin z
    u3 = gamma cos x - (p e^{i(x+y)} + q e^{-i(x+y)})/2
With p = delta e^{i phi}, q = delta e^{-i phi} this is
    u3 = gamma cos x - delta cos(x+y+phi).
"""
import numpy as np

FFT = np.fft.fftn
IFFT = np.fft.ifftn
AX = (1, 2, 3)


class Grid:
    def __init__(self, N, dtype=np.complex128):
        self.N = N
        self.dtype = dtype
        rdt = np.float64 if dtype == np.complex128 else np.longdouble
        self.rdt = rdt
        k1 = np.round(np.fft.fftfreq(N, 1.0 / N)).astype(int)
        KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij")
        self.Kint = np.array([KX, KY, KZ])
        self.K = self.Kint.astype(rdt)
        self.K2 = (self.K ** 2).sum(0)
        self.K2inv = np.where(self.K2 > 0, 1.0 / np.where(self.K2 > 0, self.K2, 1), 0).astype(rdt)
        self.Kinf = np.abs(self.Kint).max(0)
        pi = np.pi if rdt == np.float64 else np.arccos(np.longdouble(-1))
        x = (2 * pi * np.arange(N, dtype=rdt)) / N
        self.X = np.meshgrid(x, x, x, indexing="ij")
        self.pi = pi


def cross(a, b):
    return np.array([a[1] * b[2] - a[2] * b[1],
                     a[2] * b[0] - a[0] * b[2],
                     a[0] * b[1] - a[1] * b[0]])


def curl_hat(K, Uh):
    return 1j * cross(K, Uh)


def project(K, K2inv, Vh):
    kd = (K * Vh).sum(0) * K2inv
    out = Vh - K * kd
    out[:, 0, 0, 0] = 0
    return out


def initial_field(g, alpha, beta, gamma, p, q):
    X, Y, Zc = g.X
    dt = g.dtype
    one_j = np.array(1j, dtype=dt)
    u = np.zeros((3,) + X.shape, dtype=dt)
    u[0] = alpha * np.sin(Y)
    u[1] = beta * np.sin(Zc)
    u[2] = gamma * np.cos(X) - (p * np.exp(one_j * (X + Y)) + q * np.exp(-one_j * (X + Y))) / 2
    return u


def initial_hat(g, alpha, beta, gamma, p, q):
    """U_0 written exactly in (unnormalised numpy) Fourier space: a field
    sum_k F_k e^{ik.x} has fftn coefficients N^3 F_k.  Building U_0 this way
    avoids roundoff garbage outside its support |k_i|<=1 (which the factor
    nu|k|^2 in (R) would otherwise amplify like (nu N^2)^n/n!)."""
    N = g.N
    N3 = np.array(N ** 3, dtype=g.rdt)
    Uh = np.zeros((3, N, N, N), dtype=g.dtype)
    I = np.array(1j, dtype=g.dtype)
    m1 = N - 1  # index of wavenumber -1
    # u1 = alpha sin y = alpha (e^{iy} - e^{-iy})/(2i)
    Uh[0, 0, 1, 0] = alpha * N3 / (2 * I)
    Uh[0, 0, m1, 0] = -alpha * N3 / (2 * I)
    # u2 = beta sin z
    Uh[1, 0, 0, 1] = beta * N3 / (2 * I)
    Uh[1, 0, 0, m1] = -beta * N3 / (2 * I)
    # u3 = gamma cos x - (p e^{i(x+y)} + q e^{-i(x+y)})/2
    Uh[2, 1, 0, 0] = gamma * N3 / 2
    Uh[2, m1, 0, 0] = gamma * N3 / 2
    Uh[2, 1, 1, 0] = -p * N3 / 2
    Uh[2, m1, m1, 0] = -q * N3 / 2
    return Uh


def series(alpha, beta, gamma, p, q, nu, nmax, g, form="rot", mask=True,
           want_E=True, diag=False):
    """Return dict with Taylor coefficients Z[n], E[n] (n=0..nmax) of
    Z = 1/2 <|curl u|^2>, E = 1/2 <|u|^2>  (bilinear averages, no conjugation).

    form='rot' : N_n = P sum_j U_j x curl U_{n-j}
    form='adv' : N_n = -P sum_j (U_j . grad) U_{n-j}
    Equivalence: for div-free a,b
        (a.grad)b + (b.grad)a = grad(a.b) - a x curl b - b x curl a,
    and the j-sum runs over both (j, n-j) and (n-j, j), so
        sum_j (U_j.grad)U_{n-j} = grad(1/2 sum_j U_j.U_{n-j}) - sum_j U_j x curl U_{n-j};
    P kills the gradient, hence both forms give the same U_{n+1}.
    mask=True zeroes modes outside the proven support max|k_i| <= n+2 of the
    step-n product (they are exactly zero mathematically; only roundoff lives there).
    """
    N = g.N
    if N < 2 * nmax + 3 and nmax > 0:
        raise ValueError("grid too small for alias-free products: need N >= 2*nmax+3")
    Uh = [initial_hat(g, alpha, beta, gamma, p, q)]
    Up, Wp, Gp = [], [], []
    Z = np.zeros(nmax + 1, dtype=g.dtype)
    E = np.zeros(nmax + 1, dtype=g.dtype)
    outside = []
    nuc = np.array(nu, dtype=g.dtype)
    for n in range(nmax + 1):
        Uhn = Uh[n]
        Up.append(IFFT(Uhn, axes=AX))
        Wp.append(IFFT(curl_hat(g.K, Uhn), axes=AX))
        if form == "adv":
            # gradient tensor G[l][i] = d_l U_i
            Gp.append(np.array([IFFT(1j * g.K[l][None] * Uhn, axes=AX) for l in range(3)]))
        # Taylor coefficients of Z and E at order n
        s = 0
        for j in range(n + 1):
            s = s + (Wp[j] * Wp[n - j]).sum(0).mean()
        Z[n] = s / 2
        if want_E:
            s = 0
            for j in range(n + 1):
                s = s + (Up[j] * Up[n - j]).sum(0).mean()
            E[n] = s / 2
        if n == nmax:
            break
        if form == "rot":
            S = cross(Up[0], Wp[n])
            for j in range(1, n + 1):
                S = S + cross(Up[j], Wp[n - j])
        elif form == "adv":
            S = 0
            for j in range(n + 1):
                a = Up[j]
                G = Gp[n - j]
                S = S - np.array([a[0] * G[0][i] + a[1] * G[1][i] + a[2] * G[2][i] for i in range(3)])
        else:
            raise ValueError(form)
        Sh = FFT(S, axes=AX)
        if diag:
            sc = np.abs(Sh).max()
            outside.append(float(np.abs(Sh[:, g.Kinf > n + 2]).max() / sc) if sc > 0 and (g.Kinf > n + 2).any() else 0.0)
        if mask:
            Sh[:, g.Kinf > n + 2] = 0
        PSh = project(g.K, g.K2inv, Sh)
        Uh.append((nuc * (-g.K2) * Uhn + PSh) / (n + 1))
    out = {"Z": Z, "E": E}
    if diag:
        out["outside"] = outside
        out["Uh"] = Uh
    return out


def phi_scan(M, nmax, g, alpha=1.0, beta=1.0, gamma=1.0, delta=1.0, nu=0.0,
             form="rot", mask=True, phi0=0.0):
    """Run the recurrence at M equispaced phases phi_k = phi0 + 2pi k/M and
    return (Zphi[M, nmax+1], c[nmax+1, M]) where c[n, m mod M] are the Laurent
    coefficients:  Z_n(phi) = sum_m c[n,m] e^{i m phi}.
    delta may be complex (then p = delta e^{i phi}, q = delta e^{-i phi} is the
    analytic continuation)."""
    Zphi = np.zeros((M, nmax + 1), dtype=g.dtype)
    Ephi = np.zeros((M, nmax + 1), dtype=g.dtype)
    phis = []
    for k in range(M):
        phi = phi0 + 2 * g.pi * k / M
        phis.append(phi)
        e = np.exp(np.array(1j, dtype=g.dtype) * phi)
        r = series(alpha, beta, gamma, delta * e, delta / e if delta != 0 else 0 * e, nu,
                   nmax, g, form=form, mask=mask)
        Zphi[k] = r["Z"]
        Ephi[k] = r["E"]
    # c_m = (1/M) sum_k Z(phi_k) e^{-i m phi_k}
    kk = np.arange(M)
    mm = np.arange(M)
    mm = np.where(mm > M // 2, mm - M, mm)
    phis = np.array(phis, dtype=g.rdt)
    ph = np.exp(np.array(-1j, dtype=g.dtype) * np.outer(mm.astype(g.rdt), phis))  # [m, k]
    c = (ph @ Zphi) / M  # [m, n]
    return Zphi, c.T, mm, Ephi


def laurent(c, mm, n, m):
    """pick coefficient c_{n,m} from the [n, idx] array using the m-labels mm."""
    idx = int(np.where(mm == m)[0][0])
    return c[n, idx]


def param_scan(name, L, r, M, nmax, g, base=None, phi0=0.0):
    """Polynomial-degree decomposition in ONE parameter by sampling it on the
    complex circle  name = r e^{2 pi i l / L}, l=0..L-1 (other parameters from
    `base`), combined with the M-point phase DFT.  Returns
        a[n, k, idx_m]  = coefficient of name^k e^{i m phi} in [t^n]Z,
    for k = 0..L-1 (exact, no aliasing, as long as L > max degree, which is
    <= n+2 for amplitudes and <= n for nu), and the m labels.
    name in {'alpha','beta','gamma','delta','nu'}."""
    b = dict(alpha=1.0, beta=1.0, gamma=1.0, delta=1.0, nu=0.0)
    if base:
        b.update(base)
    cs = []
    for l in range(L):
        w = g.rdt(r) * np.exp(np.array(2j, dtype=g.dtype) * g.pi * l / L)
        bb = dict(b)
        bb[name] = w
        _, c, mm, _ = phi_scan(M, nmax, g, phi0=phi0, **bb)
        cs.append(c)
    cs = np.array(cs)  # [l, n, idx_m]
    ks = np.arange(L)
    F = np.exp(np.array(-2j, dtype=g.dtype) * g.pi * np.outer(ks, np.arange(L)).astype(g.rdt) / L) / L  # [k, l]
    a = np.einsum("kl,lnm->nkm", F, cs)
    a = a / (g.rdt(r) ** ks)[None, :, None]
    return a, mm
