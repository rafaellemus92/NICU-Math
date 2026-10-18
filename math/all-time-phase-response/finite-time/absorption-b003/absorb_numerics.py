"""absorb_numerics.py -- the numerical layer of NOTE.md (this folder): a computed approximation
q1^N of the linear coefficient q1 together with everything a posteriori validation needs, so that
the chain script (absorb_chain.py) can bound q1 - q1^N rigorously and then bound the nonlinear
remainder w = v - b q1.

What is computed (a = c = d = 1, nu = 1/28, phi = 0.37, T = 0.25; all torus-normalized norms):

  1. The base-flow amplitude W(y,t) of w = Re(e^{ix} W) on |n| <= KW Fourier modes, RK4 nodes on
     a uniform grid of step H. Between nodes W is the piecewise-LINEAR interpolant W_lin(t). For
     every cell the residual r_W := W_lin,t - [nu (W_lin,yy - W_lin) - i a e^{-nu t} sin(y) W_lin]
     is a polynomial of degree 1 in tau = t - t_j (the e^{-nu t} factor is frozen at t_j and its
     variation over the cell, |e^{-nu tau} - 1| <= nu H, is bounded separately), computed EXACTLY as
     a trigonometric polynomial (the product sin(y) W_lin reaches |n| = KW + 1 and is kept).
     Reported per cell: an upper bound of int_cell ||r_W||_{*,3} dt with ||X||_{*,m}^2 =
     sum_n (2+n^2)^m |X_n|^2 (the weight of PROOF.md's appendix).

  2. The k_z = 1 amplitude Q(x,y,t) of q1 = Re(e^{iz} Q) (q1 lives on k_z = +-1 exactly), on
     |k_x|, |k_y| <= KQ modes, RK4 nodes on the same grid; the Galerkin right-hand side is the
     exact projection P_K of the equation
         Q_t = nu (Delta_2 - 1) Q - P[ sigma Q_x + i w Q + (Q_2 sigma_y, 0, Q_1 w_x + Q_2 w_y) ],
     sigma = a e^{-nu t} sin y, w = Re(e^{ix} W_lin), P the Leray projector on the mode (k_x,k_y,1),
     with every product evaluated exactly on a padded NP x NP grid (no aliasing: KQ + KW + 1 < NP/2).
     Between nodes Q is the piecewise-linear interpolant Q_lin. For every cell the residual of
     q1^N := Re(e^{iz} Q_lin) in the FULL equation (Galerkin part AND tail, with the base flow
     U_N = (sigma, 0, Re(e^{ix} W_lin))) is a polynomial of degree 2 in tau plus the frozen-sigma
     correction; reported per cell: upper bounds of int_cell ||r|| dt and int_cell ||grad r|| dt.
     The difference U - U_N (the true base flow against the interpolated truncated one) is NOT in
     these residuals; the chain script adds it from the W error of item 1.

  3. Per cell, upper bounds (convex in tau on each cell, hence maxima of the two node values) of
     ||q1^N||, ||grad q1^N||, sup|q1^N| <= sum_k |Qhat_k|, sup|grad q1^N| <= sum_k |ktilde| |Qhat_k|,
     sup|grad^2 q1^N| <= sum_k |ktilde|^2 |Qhat_k|, with ktilde = (k_x, k_y, 1).

  Everything is aggregated over coarse cells of COARSE fine steps (sums of the integral bounds,
  maxima of the pointwise bounds) and written to results/numerics.json together with the
  parameters, the grid, the source hash and the inflation applied.

ROUNDING. The arithmetic is IEEE double. Every reported bound is multiplied by (1 + INFL) and
increased by ABS before it is written. The floating-point error of the operations behind each
O(1) number (FFTs of size NP = 64, sums of at most 3 NP^2 terms, products of two such fields) is
below 1e-13 relative, which INFL = 1e-10 covers by a factor above 10^3. The residual norms
(order 1e-5) arise by cancellation of O(1) terms, so their relative roundoff can itself be of
order 1e-10; for the integrated residuals (order 1e-8 per coarse cell) the margin is the absolute
term ABS = 1e-14 against an accumulated roundoff of order 1e-17 to 1e-18. This is a documented
safety margin, not a certified rounding bound; the chain script states it again.

Run from this folder:  python3 -B absorb_numerics.py   (about 2 minutes; NumPy only)
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import platform
import time
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------- parameters (fixed for this task)
A, C, D, NU, PHI, T = 1.0, 1.0, 1.0, 1.0 / 28.0, 0.37, 0.25
H = 2e-5                       # fine step (nodes); T/H must be an integer
NSTEP = int(round(T / H))
COARSE = 50                    # fine steps per coarse cell -> coarse width 1e-3
KQ, KW, NP = 10, 20, 64        # Q modes |k| <= KQ; W modes |n| <= KW; padded grid NP (KQ + KW + 1 = 31 < 32)
INFL, ABS = 1e-10, 1e-14
assert abs(NSTEP * H - T) < 1e-12 and NSTEP % COARSE == 0 and KQ + KW + 1 < NP // 2

HERE = Path(__file__).resolve().parent


def infl(x):
    return float(x) * (1.0 + INFL) + ABS


# ---------------------------------------------------------------- W: the base-flow amplitude
nW = np.arange(-(KW + 1), KW + 2)                 # extended index range for the exact product sin(y) W
inW = slice(1, 2 * KW + 2)                        # the KW modes inside the extended range
wgt3 = (2.0 + nW.astype(float) ** 2) ** 3         # weight (2+n^2)^3 on the extended range


def shiftdiff(X):
    """(S X)_n = X_{n-1} - X_{n+1} on the extended range; X is zero outside |n| <= KW."""
    S = np.zeros_like(X)
    S[1:] += X[:-1]
    S[:-1] -= X[1:]
    return S


def rhsW(t, W):
    """W_n' = -nu (n^2+1) W_n - (a e^{-nu t}/2) (W_{n-1} - W_{n+1}), truncated to |n| <= KW."""
    out = -NU * (nW ** 2 + 1) * W - (A * np.exp(-NU * t) / 2.0) * shiftdiff(W)
    out[0] = out[-1] = 0.0                        # Galerkin truncation
    return out


def wnorm3(X):
    return float(np.sqrt(np.sum(wgt3 * np.abs(X) ** 2)))


W = np.zeros(2 * KW + 3, complex)
W[KW + 1] = C                                     # n = 0
W[KW + 2] = -D * np.exp(1j * PHI)                 # n = 1
Wnodes = np.empty((NSTEP + 1, 2 * KW + 3), complex)
Wnodes[0] = W
for j in range(NSTEP):
    t = j * H
    k1 = rhsW(t, W); k2 = rhsW(t + H / 2, W + H / 2 * k1); k3 = rhsW(t + H / 2, W + H / 2 * k2); k4 = rhsW(t + H, W + H * k3)
    W = W + H / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    Wnodes[j + 1] = W
assert np.isfinite(Wnodes).all()

# residual of the piecewise-linear interpolant, per fine cell, in the weighted norm
int_rW = np.empty(NSTEP)
for j in range(NSTEP):
    Wj, Wn = Wnodes[j], Wnodes[j + 1]
    Dw = (Wn - Wj) / H
    e_j = np.exp(-NU * j * H)
    SWj, SDw = shiftdiff(Wj), shiftdiff(Dw)
    r0 = Dw + NU * (nW ** 2 + 1) * Wj + (A * e_j / 2.0) * SWj
    r1 = NU * (nW ** 2 + 1) * Dw + (A * e_j / 2.0) * SDw
    # frozen-sigma correction: |e^{-nu tau} - 1| <= nu H on the cell, applied to (a e_j / 2) S W_lin
    corr = (A * e_j / 2.0) * NU * H * (wnorm3(SWj) + H * wnorm3(SDw))
    int_rW[j] = H * wnorm3(r0) + H * H / 2 * wnorm3(r1) + H * corr

# ---------------------------------------------------------------- Q: the k_z = 1 amplitude of q1
kk = np.fft.fftfreq(NP, 1.0 / NP).astype(float)          # integer wavenumbers -32..31
KX, KY = np.meshgrid(kk, kk, indexing='ij')             # arrays indexed [x-mode, y-mode]
KT2 = KX ** 2 + KY ** 2 + 1.0                           # |ktilde|^2
KT = np.sqrt(KT2)
MASK = (np.abs(KX) <= KQ) & (np.abs(KY) <= KQ)          # Galerkin set
xg = 2 * np.pi * np.arange(NP) / NP
XG, YG = np.meshgrid(xg, xg, indexing='ij')
EIX = np.exp(1j * XG)
SINY, COSY = np.sin(YG), np.cos(YG)

f2 = lambda f: np.fft.fft2(f, axes=(-2, -1), norm='forward')     # Fourier coefficients
if2 = lambda f: np.fft.ifft2(f, axes=(-2, -1), norm='forward')   # values on the grid


def proj(Fh):
    """Leray projector on the modes ktilde = (k_x, k_y, 1)."""
    dot = KX * Fh[0] + KY * Fh[1] + Fh[2]
    return Fh - np.stack([KX, KY, np.ones_like(KX)]) * (dot / KT2)


def wfields(Wv):
    """Grid values of w = Re(e^{ix} W(y)), w_x, w_y from the W coefficients on the extended range."""
    cw = np.zeros(NP, complex); cwy = np.zeros(NP, complex)
    idx = nW % NP
    cw[idx] = Wv
    cwy[idx] = 1j * nW * Wv
    Wy_ = np.fft.ifft(cw, norm='forward')          # W(y_m)
    Wyy_ = np.fft.ifft(cwy, norm='forward')        # W_y(y_m)
    Wg, Wyg = Wy_[None, :], Wyy_[None, :]          # broadcast over x
    w = np.real(EIX * Wg) + 0.0 * XG
    wx = np.real(1j * EIX * Wg) + 0.0 * XG
    wy = np.real(EIX * Wyg) + 0.0 * XG
    return w, wx, wy


def transport_w(Qh, wf):
    """P[ i w Q + (0, 0, Q_1 w_x + Q_2 w_y) ] (exact on the padded grid), bilinear in (Q, W)."""
    w, wx, wy = wf
    Q = if2(Qh)
    Tp = np.empty_like(Q)
    Tp[0] = 1j * w * Q[0]
    Tp[1] = 1j * w * Q[1]
    Tp[2] = 1j * w * Q[2] + Q[0] * wx + Q[1] * wy
    return proj(f2(Tp))


def transport_sigma(Qh, e_t):
    """P[ sigma Q_x + (Q_2 sigma_y, 0, 0) ] with sigma = a e_t sin y, sigma_y = a e_t cos y; linear in Q."""
    Q = if2(Qh)
    Qx = if2(1j * KX * Qh)
    Tp = A * e_t * SINY * Qx
    Tp[0] = Tp[0] + A * e_t * COSY * Q[1]
    return proj(f2(Tp))


def rhsQ(t, Qh, Wv):
    e_t = np.exp(-NU * t)
    Th = transport_sigma(Qh, e_t) + transport_w(Qh, wfields(Wv))
    return (-NU * KT2 * Qh - Th) * MASK


def l2(Fh):
    return float(np.sqrt(0.5 * np.sum(np.abs(Fh) ** 2)))


def h1(Fh):
    return float(np.sqrt(0.5 * np.sum(KT2 * np.abs(Fh) ** 2)))


def l1sums(Qh):
    m = np.sqrt(np.sum(np.abs(Qh) ** 2, axis=0))     # |Qhat_k| in C^3
    return float(m.sum()), float((KT * m).sum()), float((KT2 * m).sum())


Qh = np.zeros((3, NP, NP), complex)
Qh[1, 0, 0] = -1j                                   # q1(0) = sin z e_y = Re(-i e^{iz}) e_y
assert abs(h1(Qh) - 2 ** -0.5) < 1e-15 and abs(l2(Qh) - 2 ** -0.5) < 1e-15

ncoarse = NSTEP // COARSE
agg = {k: np.zeros(ncoarse) for k in ['int_r', 'int_gradr', 'int_rW', 'sup_q', 'sup_gradq', 'sup_absq', 'sup_absgradq', 'sup_abshessq',
                                      'tail_at_nodes', 'frozen_sigma_part']}
node_gradq = np.empty(NSTEP + 1)
node_gradq[0] = h1(Qh)
tic = time.time()
for j in range(NSTEP):
    t = j * H
    Wj, Wn = Wnodes[j], Wnodes[j + 1]
    Wm = 0.5 * (Wj + Wn)                                      # W_lin at the midpoint
    k1 = rhsQ(t, Qh, Wj); k2 = rhsQ(t + H / 2, Qh + H / 2 * k1, Wm)
    k3 = rhsQ(t + H / 2, Qh + H / 2 * k2, Wm); k4 = rhsQ(t + H, Qh + H * k3, Wn)
    Qn = Qh + H / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    # --- residual of the piecewise-linear interpolant on this cell, full equation (Galerkin part + tail)
    Dq = (Qn - Qh) / H
    Dw = (Wn - Wj) / H
    e_j = np.exp(-NU * t)
    wfj, wfd = wfields(Wj), wfields(Dw)
    Ts_Q, Ts_D = transport_sigma(Qh, e_j), transport_sigma(Dq, e_j)
    r0 = Dq + NU * KT2 * Qh + Ts_Q + transport_w(Qh, wfj)
    r1 = NU * KT2 * Dq + Ts_D + transport_w(Dq, wfj) + transport_w(Qh, wfd)
    r2 = transport_w(Dq, wfd)
    corr_l2 = NU * H * (l2(Ts_Q) + H * l2(Ts_D))          # |e^{-nu tau} - 1| <= nu H on the cell
    corr_h1 = NU * H * (h1(Ts_Q) + H * h1(Ts_D))
    cell_r = H * l2(r0) + H * H / 2 * l2(r1) + H ** 3 / 3 * l2(r2) + H * corr_l2
    cell_gr = H * h1(r0) + H * H / 2 * h1(r1) + H ** 3 / 3 * h1(r2) + H * corr_h1
    c = j // COARSE
    agg['int_r'][c] += cell_r
    agg['int_gradr'][c] += cell_gr
    agg['int_rW'][c] += int_rW[j]
    agg['frozen_sigma_part'][c] += H * corr_h1
    # pointwise bounds, convex in tau: maxima of the node values
    s0a, s1a, s2a = l1sums(Qh); s0b, s1b, s2b = l1sums(Qn)
    agg['sup_q'][c] = max(agg['sup_q'][c], l2(Qh), l2(Qn))
    agg['sup_gradq'][c] = max(agg['sup_gradq'][c], h1(Qh), h1(Qn))
    agg['sup_absq'][c] = max(agg['sup_absq'][c], s0a, s0b)
    agg['sup_absgradq'][c] = max(agg['sup_absgradq'][c], s1a, s1b)
    agg['sup_abshessq'][c] = max(agg['sup_abshessq'][c], s2a, s2b)
    agg['tail_at_nodes'][c] = max(agg['tail_at_nodes'][c], l2((Ts_Q + transport_w(Qh, wfj)) * (~MASK)))
    Qh = Qn
    node_gradq[j + 1] = h1(Qh)
    if (j + 1) % 2500 == 0:
        print(f'  step {j + 1}/{NSTEP}  t={t + H:.3f}  |grad q1^N|={node_gradq[j + 1]:.6f}  cell int|r|={cell_r:.2e}  int|grad r|={cell_gr:.2e}', flush=True)
wall = time.time() - tic
assert np.isfinite(Qh).all()

# Galerkin truncation sanity: energy in the outermost retained shell of Q and W at T
shell = MASK & ((np.abs(KX) == KQ) | (np.abs(KY) == KQ))
shell_frac = float(np.sqrt(np.sum(np.abs(Qh[:, shell]) ** 2) / np.sum(np.abs(Qh) ** 2)))
w_shell = float(np.max(np.abs(Wnodes[-1][[1, -2]])) / np.max(np.abs(Wnodes[-1])))

out = {
    'parameters': dict(a=A, c=C, d=D, nu=NU, phi=PHI, T=T, H=H, NSTEP=NSTEP, COARSE=COARSE, ncoarse=ncoarse,
                       coarse_width=H * COARSE, KQ=KQ, KW=KW, NP=NP, INFL=INFL, ABS=ABS,
                       numpy=np.__version__, python=platform.python_version(), wall_seconds=wall,
                       source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),
    'conventions': {
        'norms': 'torus-normalized L2; ||q||^2 = (1/2) sum_k |Qhat_k|^2 for q = Re(e^{iz} Q); ||X||_{*,3}^2 = sum_n (2+n^2)^3 |X_n|^2',
        'int_r': 'upper bound of int_cell ||r|| dt, r = residual of q1^N = Re(e^{iz} Q_lin) in the full equation with base flow U_N; Galerkin part and tail',
        'int_gradr': 'same for ||grad r||',
        'int_rW': 'upper bound of int_cell ||r_W||_{*,3} dt, r_W = residual of W_lin (Galerkin part and the |n| = KW+1 tail)',
        'sup_q, sup_gradq': 'maxima over the coarse cell of ||q1^N||, ||grad q1^N|| (convex in tau on each fine cell)',
        'sup_absq, sup_absgradq, sup_abshessq': 'maxima over the coarse cell of sum_k |Qhat_k|, sum_k |ktilde||Qhat_k|, sum_k |ktilde|^2 |Qhat_k| (bounds of sup|q1^N|, sup|grad q1^N|, sup|grad^2 q1^N|)',
        'inflation': 'every value below is x(1+INFL)+ABS of the computed double-precision number',
    },
    'coarse_t_right': [(c + 1) * COARSE * H for c in range(ncoarse)],
    'cells': {k: [infl(v) for v in vals] for k, vals in agg.items()},
    'diagnostics': {
        'node_gradq1_every_coarse': [float(node_gradq[c * COARSE]) for c in range(ncoarse + 1)],
        'gradq1_at_T_uninflated': float(node_gradq[-1]),
        'sum_int_r': float(agg['int_r'].sum()), 'sum_int_gradr': float(agg['int_gradr'].sum()), 'sum_int_rW': float(agg['int_rW'].sum()),
        'max_tail_at_nodes': float(agg['tail_at_nodes'].max()),
        'Q_outer_shell_fraction_at_T': shell_frac, 'W_outer_mode_fraction_at_T': w_shell,
        'W_nodes_at_T_abs': [float(abs(x)) for x in Wnodes[-1][inW]],
    },
}
(HERE / 'results').mkdir(exist_ok=True)
(HERE / 'results' / 'numerics.json').write_text(json.dumps(out, indent=1) + '\n')
print(f'wrote results/numerics.json  (wall {wall:.0f} s)')
print(f"|grad q1^N|(T) = {node_gradq[-1]:.6f}   sum int|r| = {agg['int_r'].sum():.3e}   sum int|grad r| = {agg['int_gradr'].sum():.3e}   "
      f"sum int|r_W|_*3 = {agg['int_rW'].sum():.3e}   max tail at nodes = {agg['tail_at_nodes'].max():.2e}   outer-shell fraction Q = {shell_frac:.1e}, W = {w_shell:.1e}")
