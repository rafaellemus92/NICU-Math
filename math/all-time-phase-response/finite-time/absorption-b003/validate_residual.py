"""validate_residual.py -- rigorous a-posteriori enclosure of the residuals and norms of the
mathematical approximation (W_lin, q1^N) defined from the trajectory in trajectory/, independent of
how absorb_numerics.py produced that trajectory (no FFT, no solver internals; only the node values).

THE APPROXIMATION (exact definitions)
  nodes      t_j = j h, h = 1/50000, j = 0..12500 (exact rationals; T = 1/4; 50 fine cells per coarse cell)
  W_lin(t)   piecewise linear in t between the node vectors W_j in C^{43} (modes |n| <= 21) read from
             trajectory/W_nodes.npy; every stored double is taken as the exact dyadic rational it is
  Qtilde_j   := P Q_j, the exact Leray projection (mode-wise, on ktilde = (k_x, k_y, 1)) of the node
             arrays Q_j in C^{3 x 21 x 21} (|k_x|, |k_y| <= 10) read from trajectory/Q_nodes.npy;
             Qtilde_lin piecewise linear in t between them
  q1^N       := Re(e^{iz} Qtilde_lin(x, y, t)),   U_N := (a e^{-nu t} sin y, 0, Re(e^{ix} W_lin(y, t)))
  constants  a = c = d = 1, nu = 1/28, phi = 37/100 exactly; e^{-nu t_j}, cos phi, sin phi are enclosed
             in decimal interval arithmetic (../constants.py, Iv) and converted outward to double intervals
Solenoidality: div q1^N = 0 exactly because ktilde . Qtilde_k = 0 exactly for every mode (P is applied
inside the interval computation, so every norm below is a norm of the exactly solenoidal field);
div U_N = 0 for every W_lin.  Initial data: Q_0 is checked to be exactly (0, -i, 0) at k = 0 and zero
elsewhere, so Qtilde_0 equals the exact initial coefficient and e(0) = 0; W_0 is checked to be exactly
c at n = 0 and zero for n not in {0, 1}, and the representation error of W_1(0) = -d e^{i phi} is
enclosed and reported as epsW0 = ||W(., 0) - W_0||_{*,3}.

THE RESIDUALS (what is enclosed)
  r_W(t) := d/dt W_lin + nu (n^2 + 1) W_lin + (a e^{-nu t}/2) S W_lin,   (S X)_n = X_{n-1} - X_{n+1}
            [residual of W_lin in W_t = nu (W_yy - W) - i a e^{-nu t} sin(y) W, on |n| <= 22]
  r(t)   := d/dt Qtilde_lin + nu |ktilde|^2 Qtilde_lin
            + P[ a e^{-nu t} (sin y d_x Qtilde + (Qtilde_2 cos y, 0, 0)) + i w Qtilde + (0, 0, Qtilde_1 w_x + Qtilde_2 w_y) ]
            [residual of q1^N in L_{U_N} q1^N = 0, with w = Re(e^{ix} W_lin); modes |k_x| <= 11, |k_y| <= 31]
On the cell [t_j, t_j + h], tau = t - t_j:  e^{-nu t} = e^{-nu t_j} (1 - theta(tau)), 0 <= theta <= 1 - e^{-nu h} <= nu h,
and r = r_0 + tau r_1 + tau^2 r_2 - theta e^{-nu t_j} P T_sigma(Qtilde_lin), hence
  int_cell ||r|| <= h ||r_0|| + h^2/2 ||r_1|| + h^3/3 ||r_2|| + e^{-nu t_j} (nu h^2 / 2) max_nodes ||T_sigma(Qtilde)||
(||P f|| <= ||f||; a norm along the linear path is convex, so its cell maximum is at a node; int_0^h nu tau = nu h^2/2),
the same for ||grad r|| and for r_W in the (2+n^2)^3-weighted norm.  With dQ = Qtilde_{j+1} - Qtilde_j,
dW = W_{j+1} - W_j, D = dQ / h and T_w bilinear,
  r_0 = D + nu |ktilde|^2 Qtilde_j + P[ e_j T_sigma(Qtilde_j) + T_w(W_j, Qtilde_j) ]
  r_1 = nu |ktilde|^2 D + P[ e_j T_sigma(dQ)/h + ( T_w(W_{j+1}, Qtilde_{j+1}) - T_w(W_j, Qtilde_j) - T_w(dW, dQ) )/h ]
  r_2 = P T_w(dW, dQ) / h^2
(from T_w(W_j + dW, Qtilde_j + dQ) = T_w(W_j, Qtilde_j) + T_w(W_j, dQ) + T_w(dW, Qtilde_j) + T_w(dW, dQ)).
dQ is evaluated as P(Q_{j+1} - Q_j), the same exact object as P Q_{j+1} - P Q_j with a smaller enclosure.
Products with w are direct convolutions in k_y (Toeplitz sums over 21 terms) with the shift k_x -> k_x +- 1;
the y-derivative uses (n V) * X = k_y' (V * X) - V * (k_y X).

THE ARITHMETIC (rigorous)
Midpoint-radius interval arithmetic over IEEE 754 binary64 with round-to-nearest, vectorised in NumPy.
A complex interval is a disc {z : |z - (re + i im)| <= rad}.  Model: for doubles x, y and op in
{+, -, *, /}, |fl(x op y) - (x op y)| <= u |fl(x op y)| + eta with u = 2^-53 (half an ulp of the computed
result) and eta = 2^-1022 (covers the subnormal range under gradual underflow; the flush-to-zero and
denormals-are-zero modes are assumed off, which is NumPy's default); sqrt is correctly rounded;
abs and nextafter are exact; a NumPy sum of n doubles, in whatever order it is evaluated, satisfies
|fl(sum) - sum| <= gamma_{n-1} sum |x_i| + (n-1) eta with gamma_k = k u / (1 - k u) (Higham, Accuracy and
Stability of Numerical Algorithms, 2nd ed., Lemma 3.1 and section 4.2; valid for every summation order,
pairwise included).  Every radius is accumulated with nextafter(., +inf) after each operation, so each
computed radius is an upper bound of the exact radius formula.  Only elementwise ufuncs and np.sum are
used (no FMA, BLAS, FFT or matmul).  The scalar cell integrals and the coarse-cell aggregation are done
in the decimal interval class of ../constants.py; the written numbers are upper bounds rounded up.
Exact doubles: 1/h = 50000, 1/h^2 = 2.5e9, 1/2, the integer wavenumbers and |ktilde|^2; nu and h are
intervals.

Run from this folder:  python3 -B validate_residual.py [--cells N] [--out results/validated.json]
(about 11 minutes for all 12500 cells; NumPy only).
"""
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import importlib.util
import json
import platform
import time
from decimal import Decimal, Inexact, Rounded, localcontext, ROUND_CEILING
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('constants', HERE.parent / 'constants.py')
constants = importlib.util.module_from_spec(spec)
spec.loader.exec_module(constants)
Iv, TRAP = constants.Iv, constants.TRAP

# ---------------------------------------------------------------- fixed parameters of the approximation
NSTEP, COARSE = 12500, 50
KQ, KW = 10, 20
NW = 2 * KW + 3                      # 43 stored W modes, n = -21..21
HINV = 50000.0                       # 1/h, exact double
HINV2 = 2.5e9                        # 1/h^2, exact double
U = 2.0 ** -53
ETA = 2.0 ** -1022
INF = np.inf


def up(x):
    return np.nextafter(x, INF)


def dn(x):
    return np.nextafter(x, -INF)


def gamma_factor(n):
    """(G, F) Python floats with G >= gamma_n = n u/(1 - n u) and F >= 1/(1 - gamma_n)."""
    nu_ = n * U                                   # exact
    G = float(up(nu_ / dn(1.0 - nu_)))
    F = float(up(1.0 / dn(1.0 - G)))
    return G, F


# ---------------------------------------------------------------- complex interval arrays (discs)
class CI:
    __slots__ = ('re', 'im', 'rad')

    def __init__(self, re, im, rad):
        self.re, self.im, self.rad = re, im, rad

    @property
    def shape(self):
        return self.re.shape

    def __getitem__(self, idx):
        return CI(self.re[idx], self.im[idx], self.rad[idx])


def exact(z):
    """Exact complex array (zero radius)."""
    z = np.asarray(z, dtype=complex)
    return CI(np.array(z.real, dtype=float), np.array(z.imag, dtype=float), np.zeros(z.shape))


def zeros(shape):
    return CI(np.zeros(shape), np.zeros(shape), np.zeros(shape))


def embed(a, shape, sl):
    """Place a into a zero array of the given shape at the slices sl."""
    out = zeros(shape)
    out.re[sl] = a.re
    out.im[sl] = a.im
    out.rad[sl] = a.rad
    return out


def rnd2(re, im):
    """Bound of the rounding error of forming re and im by one floating-point operation each."""
    return up(up(U * up(np.abs(re) + np.abs(im))) + 2 * ETA)


def mag1(a):
    return up(np.abs(a.re) + np.abs(a.im))         # >= |midpoint|


def cadd(a, b):
    re = a.re + b.re
    im = a.im + b.im
    return CI(re, im, up(up(a.rad + b.rad) + rnd2(re, im)))


def csub(a, b):
    re = a.re - b.re
    im = a.im - b.im
    return CI(re, im, up(up(a.rad + b.rad) + rnd2(re, im)))


def cmul_i(a):
    return CI(-a.im, a.re, a.rad)                 # exact


def cneg(a):
    return CI(-a.re, -a.im, a.rad)                # exact


def cconj(a):
    return CI(a.re, -a.im, a.rad)                 # exact


def cmul(a, b):
    """Product of two complex interval arrays (broadcasting)."""
    p1 = a.re * b.re
    p2 = a.im * b.im
    p3 = a.re * b.im
    p4 = a.im * b.re
    re = p1 - p2
    im = p3 + p4
    s = up(up(up(np.abs(p1) + np.abs(p2)) + up(np.abs(p3) + np.abs(p4))) + up(np.abs(re) + np.abs(im)))
    rerr = up(up(U * s) + 6 * ETA)                # six roundings: four products, one subtraction, one addition
    ma, mb = mag1(a), mag1(b)
    rad = up(up(up(up(ma * b.rad) + up(mb * a.rad)) + up(a.rad * b.rad)) + rerr)
    return CI(re, im, rad)


def cscale(a, k):
    """Multiply by an exactly representable real array or scalar k."""
    re = a.re * k
    im = a.im * k
    return CI(re, im, up(up(np.abs(k) * a.rad) + rnd2(re, im)))


def cmul_rs(a, m, r):
    """Multiply by the real scalar interval [m - r, m + r] (Python floats, r >= 0)."""
    re = a.re * m
    im = a.im * m
    rad = up(up(up(mag1(a) * r) + up(abs(m) * a.rad)) + up(r * a.rad))
    return CI(re, im, up(rad + rnd2(re, im)))


def cdiv_pos(a, k):
    """Divide by an exactly representable positive real array k."""
    re = a.re / k
    im = a.im / k
    return CI(re, im, up(up(a.rad / k) + rnd2(re, im)))


def csum(a, axis):
    """Sum along an axis with the order-independent summation error bound.
    tot_abs: the computed S = fl(sum fl(|re_i| + |im_i|)) satisfies S >= (1 - u)(1 - gamma_{n-1}) sum(|re_i| + |im_i|)
    and (1 - u)(1 - gamma_{n-1}) >= 1 - gamma_n because gamma_n - gamma_{n-1} >= u, so sum(|re_i| + |im_i|) <= S F
    with F >= 1/(1 - gamma_n); likewise sum rad_i <= fl(sum rad_i) F. The midpoint error is <= gamma_{n-1} sum |x_i|
    per component, i.e. <= G tot_abs in total, plus (n-1) eta per component."""
    n = a.re.shape[axis]
    G, F = gamma_factor(n)
    re = np.sum(a.re, axis=axis)
    im = np.sum(a.im, axis=axis)
    tot_abs = up(np.sum(np.abs(a.re) + np.abs(a.im), axis=axis) * F)      # >= sum (|re_i| + |im_i|)
    radsum = up(np.sum(a.rad, axis=axis) * F)                             # >= sum rad_i
    err = up(up(G * tot_abs) + 2 * n * ETA)
    return CI(re, im, up(radsum + err))


def abs_hi(a):
    """Upper bound of |z| over the disc."""
    m = up(np.sqrt(up(up(a.re * a.re) + up(a.im * a.im))))
    return up(m + a.rad)


def sum_hi(x):
    """Upper bound of the exact sum of the (upper-bound) entries of x."""
    n = x.size
    G, F = gamma_factor(n)
    return float(up(up(np.sum(x) * F) + n * ETA))


def wnorm_hi(a, w, half):
    """Upper bound of sqrt(c sum_k w_k |a_k|^2), c = 1/2 if half else 1; w exact nonnegative."""
    ab = abs_hi(a)
    sq = up(up(ab * ab) * w)
    s = sum_hi(sq)
    if half:
        s = 0.5 * s
    return float(up(np.sqrt(s)))


def l1sums_hi(a, KT_hi, KT2):
    """Upper bounds of sum_k |a_k|, sum_k |ktilde| |a_k|, sum_k |ktilde|^2 |a_k| for a of shape (3, ...)."""
    ab = abs_hi(a)
    sq = up(ab * ab)
    mk = up(np.sqrt(up(up(sq[0] + sq[1]) + sq[2])))
    return sum_hi(mk), sum_hi(up(mk * KT_hi)), sum_hi(up(mk * KT2))


# ---------------------------------------------------------------- decimal enclosures -> double intervals
def iv_to_mr(iv):
    """Iv [lo, hi] -> (m, r) doubles with [m - r, m + r] containing [lo, hi]."""
    m = float(iv.lo)
    with localcontext() as ctx:
        ctx.prec = 120
        ctx.rounding = ROUND_CEILING
        dm = Decimal(m)
        r = max(iv.hi - dm, dm - iv.lo, Decimal(0))
    return m, float(up(up(float(r))))


def float_up(d):
    """Smallest double >= the Decimal d (d finite)."""
    f = float(d)
    if Decimal(f) < d:
        f = float(up(f))
    assert Decimal(f) >= d
    return f


def fmt_up(d, digits=4):
    """Decimal d printed with `digits` significant digits, rounded towards +infinity."""
    with localcontext() as ctx:
        ctx.prec = digits
        ctx.rounding = ROUND_CEILING
        ctx.traps[Inexact] = ctx.traps[Rounded] = False       # printing only; the rounding here is deliberate
        return format(+Decimal(d), 'E')


def cos_sin_iv(x, terms=30):
    """Enclosures of cos x, sin x for an Iv x with |x| <= 1 (alternating Taylor series, remainder <= first omitted term)."""
    x2 = x.sq()
    c, s = Iv.of(1), x
    tc, ts = Iv.of(1), x
    for k in range(1, terms):
        tc = tc * x2 / ((2 * k - 1) * (2 * k))
        ts = ts * x2 / ((2 * k) * (2 * k + 1))
        c = c + (tc if k % 2 == 0 else -tc)
        s = s + (ts if k % 2 == 0 else -ts)
    tc = tc * x2 / ((2 * terms - 1) * (2 * terms))
    ts = ts * x2 / ((2 * terms) * (2 * terms + 1))
    return c + Iv(tc.hi.copy_negate(), tc.hi), s + Iv(ts.hi.copy_negate(), ts.hi)


# ---------------------------------------------------------------- grids
# small grid: k_x, k_y = -KQ..KQ (21 x 21); big grid: k_x = -(KQ+1)..KQ+1 (23), k_y = -(KQ+KW+1)..KQ+KW+1 (63)
ks = np.arange(-KQ, KQ + 1).astype(float)
NBX, NBY = 2 * KQ + 3, 2 * (KQ + KW + 1) + 1
kbx = np.arange(-(KQ + 1), KQ + 2).astype(float)
kby = np.arange(-(KQ + KW + 1), KQ + KW + 2).astype(float)
KXb, KYb = np.meshgrid(kbx, kby, indexing='ij')
KT2b = KXb ** 2 + KYb ** 2 + 1.0                 # exact integers
KTb_hi = up(np.sqrt(KT2b))                       # >= |ktilde|
SL_SMALL = (slice(None), slice(1, 1 + 2 * KQ + 1), slice(KW + 1, KW + 1 + 2 * KQ + 1))   # small grid inside the big one
# Toeplitz index: M[ky', ky] = Vpad[ky' - ky + 2 KW + 2], Vpad has V_m at m + 2 KW + 2 for |m| <= KW + 1 and zeros elsewhere
TIDX = (kby[:, None] - ks[None, :] + (2 * KW + 2)).astype(int)
NPAD = 4 * KW + 5
# W residual on the extended range n = -(KW+2)..KW+2 (45 modes)
nWx = np.arange(-(KW + 2), KW + 3).astype(float)
WGT3x = (2.0 + nWx ** 2) ** 3                    # exact integers (< 2^53)
NUn2x = nWx ** 2 + 1.0


def project(a):
    """Leray projection on the big grid: v - ktilde (ktilde . v)/|ktilde|^2."""
    dot = cadd(cadd(cscale(a[0], KXb), cscale(a[1], KYb)), a[2])
    q = cdiv_pos(dot, KT2b)
    out = zeros(a.shape)
    for comp, k in ((0, KXb), (1, KYb), (2, None)):
        r = csub(a[comp], cscale(q, k) if k is not None else q)
        out.re[comp], out.im[comp], out.rad[comp] = r.re, r.im, r.rad
    return out


def project_small(a):
    """Exact-arithmetic-defined Leray projection of a node array on the small grid (interval evaluation)."""
    KX, KY = np.meshgrid(ks, ks, indexing='ij')
    KT2 = KX ** 2 + KY ** 2 + 1.0
    dot = cadd(cadd(cscale(a[0], KX), cscale(a[1], KY)), a[2])
    q = cdiv_pos(dot, KT2)
    out = zeros(a.shape)
    for comp, k in ((0, KX), (1, KY), (2, None)):
        r = csub(a[comp], cscale(q, k) if k is not None else q)
        out.re[comp], out.im[comp], out.rad[comp] = r.re, r.im, r.rad
    return out


def shift_ky(a, s):
    """(shift_ky a)[.., ky'] = a[.., ky' - s] on the big grid (zero fill)."""
    out = zeros(a.shape)
    if s > 0:
        out.re[..., s:], out.im[..., s:], out.rad[..., s:] = a.re[..., :-s], a.im[..., :-s], a.rad[..., :-s]
    else:
        out.re[..., :s], out.im[..., :s], out.rad[..., :s] = a.re[..., -s:], a.im[..., -s:], a.rad[..., -s:]
    return out


def T_sigma(ab):
    """a [ sin y d_x Q + (Q_2 cos y, 0, 0) ] for Q on the big grid (a = 1):
    (sin y Q_x)[ky'] = (k_x/2) (Q[ky'-1] - Q[ky'+1]),  (cos y Q_2)[ky'] = (Q_2[ky'-1] + Q_2[ky'+1]) / 2."""
    qm, qp = shift_ky(ab, 1), shift_ky(ab, -1)
    out = cscale(csub(qm, qp), 0.5 * KXb)
    extra = cscale(cadd(qm[1], qp[1]), 0.5)
    first = cadd(out[0], extra)
    out.re[0], out.im[0], out.rad[0] = first.re, first.im, first.rad
    return out


def toeplitz(V, X4):
    """Y[ch, kx, ky'] = sum_ky V[ky' - ky] X4[ch, kx, ky]; V on m = -(KW+1)..KW+1 (43), X4 on the small grid."""
    pad = zeros((NPAD,))
    pad.re[KW + 1:KW + 1 + NW], pad.im[KW + 1:KW + 1 + NW], pad.rad[KW + 1:KW + 1 + NW] = V.re, V.im, V.rad
    M = pad[TIDX]                                                     # (63, 21)
    prod = cmul(CI(M.re[None, None], M.im[None, None], M.rad[None, None]),
                CI(X4.re[:, :, None, :], X4.im[:, :, None, :], X4.rad[:, :, None, :]))   # (4, 21, 63, 21)
    return csum(prod, -1)                                             # (4, 21, 63)


def T_w(W, Q):
    """P-free transport by w = Re(e^{ix} W): i w Q + (0, 0, Q_1 w_x + Q_2 w_y), on the big grid.
    W: CI (43,) exact or interval; Q: CI (3, 21, 21) on the small grid."""
    X4 = zeros((4, 2 * KQ + 1, 2 * KQ + 1))
    for c in range(3):
        X4.re[c], X4.im[c], X4.rad[c] = Q.re[c], Q.im[c], Q.rad[c]
    kyQ2 = cscale(Q[1], ks[None, :])
    X4.re[3], X4.im[3], X4.rad[3] = kyQ2.re, kyQ2.im, kyQ2.rad
    out = zeros((3, NBX, NBY))
    Vplus = cscale(W, 0.5)                                            # e^{ix}: W_m / 2, shift k_x -> k_x + 1
    Vminus = cscale(cconj(CI(W.re[::-1], W.im[::-1], W.rad[::-1])), 0.5)   # e^{-ix}: conj(W_{-m}) / 2, k_x -> k_x - 1
    for V, sx, iota in ((Vplus, 2, +1), (Vminus, 0, -1)):
        Y = toeplitz(V, X4)                                           # (4, 21, 63): k_x = -KQ..KQ -> big index kx + sx
        sl = (slice(sx, sx + 2 * KQ + 1), slice(None))
        iY = cmul_i(Y)
        for c in range(3):
            cur = out[c][sl]
            new = cadd(cur, iY[c])
            out.re[c][sl], out.im[c][sl], out.rad[c][sl] = new.re, new.im, new.rad
        # third component extra: iota * i * Y[Q1]  +  i (ky' Y[Q2] - Y[ky Q2])
        dx = iY[0] if iota > 0 else cneg(iY[0])
        dy = cmul_i(csub(cscale(Y[1], kby[None, :]), Y[3]))
        cur = out[2][sl]
        new = cadd(cur, cadd(dx, dy))
        out.re[2][sl], out.im[2][sl], out.rad[2][sl] = new.re, new.im, new.rad
    return out


def shift_w(X):
    """(S X)_n = X_{n-1} - X_{n+1} on the extended range (45) from X on 43 modes."""
    Xe = embed(X, (len(nWx),), slice(1, 1 + NW))
    out = zeros(Xe.shape)
    out.re[1:], out.im[1:], out.rad[1:] = Xe.re[:-1], Xe.im[:-1], Xe.rad[:-1]
    b = zeros(Xe.shape)
    b.re[:-1], b.im[:-1], b.rad[:-1] = Xe.re[1:], Xe.im[1:], Xe.rad[1:]
    return csub(out, b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cells', type=int, default=NSTEP)
    ap.add_argument('--out', type=Path, default=HERE / 'results' / 'validated.json')
    ap.add_argument('--trajectory', type=Path, default=HERE / 'trajectory')
    args = ap.parse_args()
    with localcontext(TRAP):
        run(args)


def run(args):
    tic = time.time()
    Wn = np.load(args.trajectory / 'W_nodes.npy')
    Qn = np.load(args.trajectory / 'Q_nodes.npy', mmap_mode='r')
    assert Wn.shape == (NSTEP + 1, NW) and Qn.shape == (NSTEP + 1, 3, 2 * KQ + 1, 2 * KQ + 1)
    assert Wn.dtype == np.complex128 and Qn.dtype == np.complex128
    traj_sha = {'W_nodes.npy': hashlib.sha256(Wn.tobytes()).hexdigest(),
                'Q_nodes.npy': hashlib.sha256(np.ascontiguousarray(Qn).tobytes()).hexdigest()}
    numerics = json.loads((HERE / 'results' / 'numerics.json').read_text())
    assert numerics['trajectory']['sha256_of_array_bytes'] == traj_sha, 'trajectory does not match results/numerics.json'
    assert np.isfinite(Wn).all() and np.isfinite(Qn).all()

    nu = Iv.of('1/28')
    h = Iv.of('1/50000')
    half_h2_nu = nu * h.sq() / 2                       # int_0^h nu tau dtau
    a_half = Iv.of('1/2')                               # a/2 with a = 1
    nu_m, nu_r = iv_to_mr(nu)

    # --- initial data checks (exact comparisons of the stored doubles)
    Q0 = Qn[0]
    assert Q0[1, KQ, KQ] == -1j and np.count_nonzero(Q0) == 1, 'Q_0 is not exactly the initial coefficient (0, -i, 0)'
    W0 = Wn[0]
    assert W0[KW + 1] == 1.0 and np.count_nonzero(np.delete(W0, [KW + 1, KW + 2])) == 0, 'W_0 is not exactly the initial data outside n = 1'
    cphi, sphi = cos_sin_iv(Iv.of('0.37'))
    dre = -cphi - Iv.of(Decimal(float(W0[KW + 2].real)))          # exact decimal of the stored double
    dim = -sphi - Iv.of(Decimal(float(W0[KW + 2].imag)))
    epsW0 = (Iv.of(27) * (dre.sq() + dim.sq())).sqrt()           # weight (2 + 1^2)^3 = 27 at n = 1
    epsW0_f = float_up(epsW0.hi)

    # --- e^{-nu t_j} enclosures at all nodes
    e_mr = [iv_to_mr((-nu * Iv.of(j) / 50000).exp()) for j in range(NSTEP + 1)]

    ncells = args.cells
    ncoarse = (ncells + COARSE - 1) // COARSE
    keys = ['int_r', 'int_gradr', 'int_rW', 'sup_q', 'sup_gradq', 'sup_absq', 'sup_absgradq', 'sup_abshessq', 'frozen_sigma_part']
    agg = {k: [Iv.of(0) for _ in range(ncoarse)] for k in keys}
    diag = {'max_rel_rad_r0': 0.0, 'max_rel_rad_norm_q': 0.0, 'sum_int_r': Iv.of(0), 'sum_int_gradr': Iv.of(0), 'sum_int_rW': Iv.of(0)}

    def node_data(j):
        Qt = project_small(exact(Qn[j]))                               # exactly solenoidal approximation node
        Qb = embed(Qt, (3, NBX, NBY), SL_SMALL)
        W = exact(Wn[j])
        Ts = T_sigma(Qb)
        Tw = T_w(W, Qt)
        SW = shift_w(W)
        d = dict(Qt=Qt, Qb=Qb, W=W, Ts=Ts, Tw=Tw,
                 nq=wnorm_hi(Qb, 1.0, True), ngq=wnorm_hi(Qb, KT2b, True),
                 nTs=wnorm_hi(Ts, 1.0, True), ngTs=wnorm_hi(Ts, KT2b, True),
                 nSW=wnorm_hi(SW, WGT3x, False), l1=l1sums_hi(Qb, KTb_hi, KT2b))
        return d

    prev = node_data(0)
    last_print = time.time()
    for j in range(ncells):
        cur = node_data(j + 1)
        c = j // COARSE
        e_m, e_r = e_mr[j]
        # ---------------- q1^N residual on the cell
        dQ = project_small(csub(exact(Qn[j + 1]), exact(Qn[j])))     # = Qtilde_{j+1} - Qtilde_j (P linear), tighter enclosure
        dQb = embed(dQ, (3, NBX, NBY), SL_SMALL)
        dW = csub(cur['W'], prev['W'])
        Tdiff = T_w(dW, dQ)
        Dq = cscale(dQb, HINV)
        tr0 = cadd(cmul_rs(prev['Ts'], e_m, e_r), prev['Tw'])
        r0 = cadd(cadd(Dq, cmul_rs(cscale(prev['Qb'], KT2b), nu_m, nu_r)), project(tr0))
        cross = cscale(csub(csub(cur['Tw'], prev['Tw']), Tdiff), HINV)
        tr1 = cadd(cmul_rs(cscale(T_sigma(dQb), HINV), e_m, e_r), cross)
        r1 = cadd(cmul_rs(cscale(Dq, KT2b), nu_m, nu_r), project(tr1))
        r2 = project(cscale(Tdiff, HINV2))
        n0, n1, n2 = wnorm_hi(r0, 1.0, True), wnorm_hi(r1, 1.0, True), wnorm_hi(r2, 1.0, True)
        g0, g1, g2 = wnorm_hi(r0, KT2b, True), wnorm_hi(r1, KT2b, True), wnorm_hi(r2, KT2b, True)
        e_hi = Iv.of(Decimal(e_m)) + Iv.of(Decimal(e_r))
        corr_l2 = e_hi * half_h2_nu * max(prev['nTs'], cur['nTs'])
        corr_h1 = e_hi * half_h2_nu * max(prev['ngTs'], cur['ngTs'])
        cell_r = h * n0 + h.sq() / 2 * n1 + h.sq() * h / 3 * n2 + corr_l2
        cell_gr = h * g0 + h.sq() / 2 * g1 + h.sq() * h / 3 * g2 + corr_h1
        # ---------------- W residual on the cell (weighted norm)
        E = cscale(dW, HINV)
        Wx, Ex = embed(prev['W'], (len(nWx),), slice(1, 1 + NW)), embed(E, (len(nWx),), slice(1, 1 + NW))
        rW0 = cadd(cadd(Ex, cmul_rs(cscale(Wx, NUn2x), nu_m, nu_r)), cmul_rs(cscale(shift_w(prev['W']), 0.5), e_m, e_r))
        rW1 = cadd(cmul_rs(cscale(Ex, NUn2x), nu_m, nu_r), cmul_rs(cscale(shift_w(E), 0.5), e_m, e_r))
        w0, w1 = wnorm_hi(rW0, WGT3x, False), wnorm_hi(rW1, WGT3x, False)
        cell_rW = h * w0 + h.sq() / 2 * w1 + e_hi * half_h2_nu * a_half * max(prev['nSW'], cur['nSW'])
        # ---------------- aggregation (upper bounds; sup quantities convex along the linear path -> node maxima)
        agg['int_r'][c] = agg['int_r'][c] + cell_r
        agg['int_gradr'][c] = agg['int_gradr'][c] + cell_gr
        agg['int_rW'][c] = agg['int_rW'][c] + cell_rW
        agg['frozen_sigma_part'][c] = agg['frozen_sigma_part'][c] + corr_h1
        for key, idx in (('sup_q', 'nq'), ('sup_gradq', 'ngq')):
            v = max(prev[idx], cur[idx])
            agg[key][c] = Iv.of(max(agg[key][c].hi, Decimal(v)))
        for key, i in (('sup_absq', 0), ('sup_absgradq', 1), ('sup_abshessq', 2)):
            v = max(prev['l1'][i], cur['l1'][i])
            agg[key][c] = Iv.of(max(agg[key][c].hi, Decimal(v)))
        # ---------------- diagnostics of the enclosure quality
        rel = float(np.max(r0.rad) / max(float(np.max(np.abs(r0.re) + np.abs(r0.im))), 1e-300))
        diag['max_rel_rad_r0'] = max(diag['max_rel_rad_r0'], rel)
        relq = float(np.max(prev['Qt'].rad) / float(np.max(np.abs(prev['Qt'].re) + np.abs(prev['Qt'].im))))
        diag['max_rel_rad_norm_q'] = max(diag['max_rel_rad_norm_q'], relq)
        prev = cur
        if time.time() - last_print > 30 or j + 1 == ncells:
            print(f'  cell {j + 1}/{ncells}  t={(j + 1) / HINV:.4f}  cell int||r||<={float_up(cell_r.hi):.3e}  int||grad r||<={float_up(cell_gr.hi):.3e}  '
                  f'int||r_W||<={float_up(cell_rW.hi):.3e}  ||grad q1^N||<={cur["ngq"]:.6f}  max rel radius r0 {rel:.1e}  ({time.time() - tic:.0f} s)', flush=True)
            last_print = time.time()
    for k in ('int_r', 'int_gradr', 'int_rW'):
        diag['sum_' + k] = sum((agg[k][c] for c in range(ncoarse)), Iv.of(0))
    wall = time.time() - tic

    P0 = numerics['parameters']
    out = {
        'parameters': {k: P0[k] for k in ('a', 'c', 'd', 'nu', 'phi', 'T', 'H', 'NSTEP', 'COARSE', 'KQ', 'KW', 'NP')},
        'approximation': {
            'definition': 'W_lin: piecewise linear in t between the stored node doubles W_j (exact dyadic rationals), nodes t_j = j/50000; '
                          'Qtilde_j := P Q_j (exact Leray projection of the stored node doubles on ktilde = (k_x, k_y, 1)); '
                          'q1^N := Re(e^{iz} Qtilde_lin); U_N := (a e^{-nu t} sin y, 0, Re(e^{ix} W_lin)); a = c = d = 1, nu = 1/28, phi = 37/100 exactly',
            'solenoidal': 'div q1^N = 0 exactly (P applied inside the interval computation); div U_N = 0',
            'initial_data': 'Q_0 equals the exact initial coefficient (checked bitwise); W_0 exact except the n = 1 mode, whose representation error is epsW0',
            'residual_equations': 'see the module docstring of validate_residual.py',
        },
        'arithmetic': {
            'summary': 'validated midpoint-radius interval arithmetic in IEEE binary64 (u = 2^-53, eta = 2^-1022, order-independent summation bound), '
                       'decimal interval arithmetic for e^{-nu t_j}, cos phi, sin phi and the scalar cell integrals; every written number is an upper bound rounded up',
            'u': U, 'eta': ETA,
            'summation_bound': 'gamma_{n-1} sum|x_i| + (n-1) eta, gamma_k = k u/(1 - k u), any evaluation order (Higham 2002, Lemma 3.1, section 4.2)',
            'numpy': np.__version__, 'python': platform.python_version(), 'machine': platform.machine(),
        },
        'provenance': {
            'validator_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'numerics_source_sha256': P0['source_sha256'],
            'trajectory_sha256_of_array_bytes': traj_sha,
            'cells_validated': ncells, 'complete': ncells == NSTEP, 'wall_seconds': wall,
        },
        'initial': {'epsW0': epsW0_f, 'epsW0_interval': [str(epsW0.lo), str(epsW0.hi)], 'eps0_0': 0.0,
                    'cos_phi': [str(cphi.lo), str(cphi.hi)], 'sin_phi': [str(sphi.lo), str(sphi.hi)]},
        'conventions': numerics['conventions'] | {'inflation': 'none: every value below is a rigorous upper bound (see arithmetic)'},
        'coarse_t_right': [str(Iv.of(c + 1) / 1000) for c in range(ncoarse)],
        'cells': {k: [float_up(v.hi) for v in vals] for k, vals in agg.items()},
        'diagnostics': {
            'sum_int_r': float_up(diag['sum_int_r'].hi), 'sum_int_gradr': float_up(diag['sum_int_gradr'].hi), 'sum_int_rW': float_up(diag['sum_int_rW'].hi),
            'max_relative_radius_r0': diag['max_rel_rad_r0'], 'max_relative_radius_Qtilde': diag['max_rel_rad_norm_q'],
            'sum_int_r_inflated_numerics': numerics['diagnostics']['sum_int_r'], 'sum_int_gradr_inflated_numerics': numerics['diagnostics']['sum_int_gradr'],
            'sum_int_rW_inflated_numerics': numerics['diagnostics']['sum_int_rW'],
        },
    }
    # the chain reads parameters['ncoarse'], ['coarse_width'], ['INFL'], ['ABS'], ['source_sha256']; provide them explicitly
    out['parameters'].update(ncoarse=ncoarse, coarse_width=P0['coarse_width'], INFL=0.0, ABS=0.0,
                             source_sha256=out['provenance']['validator_sha256'], nu_exact='1/28', phi_exact='37/100', h_exact='1/50000')
    args.out.parent.mkdir(exist_ok=True)
    args.out.write_text(json.dumps(out, indent=1) + '\n')
    print(f'wrote {args.out.relative_to(HERE) if args.out.is_relative_to(HERE) else args.out}  (wall {wall:.0f} s; cells {ncells}/{NSTEP})')
    print(f"epsW0 <= {fmt_up(epsW0.hi)}   sum int||r|| <= {out['diagnostics']['sum_int_r']:.4e} (inflated numerics: {numerics['diagnostics']['sum_int_r']:.4e})   "
          f"sum int||grad r|| <= {out['diagnostics']['sum_int_gradr']:.4e} ({numerics['diagnostics']['sum_int_gradr']:.4e})   "
          f"sum int||r_W|| <= {out['diagnostics']['sum_int_rW']:.4e} ({numerics['diagnostics']['sum_int_rW']:.4e})")
    print(f"max relative radius of r0 {diag['max_rel_rad_r0']:.1e}, of Qtilde {diag['max_rel_rad_norm_q']:.1e}")


if __name__ == '__main__':
    main()
