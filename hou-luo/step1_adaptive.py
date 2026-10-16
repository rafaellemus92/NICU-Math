#!/usr/bin/env python3
"""
step1_adaptive.py -- Step 1 of CLAUDE.md: follow the inviscid 1D Hou-Luo
singularity far past the point where a uniform grid gives up.

    omega_t + u omega_x = theta_x,   theta_t + u theta_x = 0,   u_x = H(omega)

on the periodic interval x in [-1/2, 1/2), nu = 0 only. Initial data
omega0 = 0, theta0 = 1 - cos(2 pi x); the singularity forms at x = 0.
omega is odd and theta is even in x for all time; the code uses that symmetry.

METHOD (see step1_plan.md)
* Uniform computational grid alpha in [-1/2, 1/2); physical x = x(alpha) with
  x' = rho(alpha), an analytic periodic sinh-type density
      rho ~ z / (1 + z),   z = r cosh(L sin(pi alpha) / pi),
  tiny near alpha = 0 (cell size ~ r/N), growing geometrically with N/L points
  per e-fold of |x|, saturating at ~1/N in the far field.
* The Hilbert transform on the stretched grid is split into the FFT Hilbert
  transform in alpha plus a dense correction with a *smooth* kernel
      K(a, b) = rho(b) cot(pi (x(a) - x(b))) - cot(pi (a - b)),
  which the trapezoid rule integrates with spectral accuracy. K depends only
  on the mesh, so it is built once per mesh. Odd symmetry halves its size.
* RK4 in time (Lawson = RK4 at nu = 0), Hou-Li filter in alpha, adaptive dt.
* The mesh is static between remesh events. When the |omega| peak gets within
  `remesh_cells` cells of x = 0, a new mesh with a smaller r is built and the
  solution is moved over by evaluating its trigonometric interpolant.

This is a toy model. Nothing here is evidence about 3D Navier-Stokes.

USAGE
    python step1_adaptive.py --N 8192 --L 128 --wmax-target 1e4
    python step1_adaptive.py --N 16384 --L 128 --wmax-target 1e4   # 2N check
    python step1_adaptive.py --N 8192 --uniform --t-end 0.74         # = hou_luo.py
"""

import argparse
import json
import time

import numpy as np

rfft, irfft = np.fft.rfft, np.fft.irfft

# 12-point Gauss-Legendre on [0, 1]: exact to round-off for the cell integrals
# below, because rho varies by at most a factor exp(L/N) across one cell.
_GLX, _GLW = np.polynomial.legendre.leggauss(12)
_GLX, _GLW = 0.5 * (_GLX + 1.0), 0.5 * _GLW


def mirror(f):
    """f(-alpha) on the grid alpha_j = (j - N/2)/N  (index 0 is its own mirror)."""
    return np.roll(f[::-1], 1)


def odd_part(f):
    return 0.5 * (f - mirror(f))


def even_part(f):
    return 0.5 * (f + mirror(f))


def fourier_eval(f, a, chunk=512):
    """Evaluate the trigonometric interpolant of the periodic samples f at the
    arbitrary points a (period 1, grid alpha_j = (j - N/2)/N)."""
    N = f.size
    c = rfft(f) / N                       # c_k, k = 0..N/2
    k = np.arange(N // 2 + 1)
    # samples live at alpha_j = (j - N/2)/N, so shift the phase accordingly
    phase0 = np.exp(2j * np.pi * k * 0.5)  # e^{2 pi i k (1/2)} = (-1)^k
    c = c * phase0
    c[1:-1] *= 2.0                        # real signal: pair k with -k
    out = np.empty_like(a, dtype=float)
    for s in range(0, a.size, chunk):
        aa = a[s:s + chunk]
        E = np.exp(2j * np.pi * np.outer(aa, k[:-1]))
        val = (E * c[:-1]).sum(axis=1).real
        # Nyquist term: c_{N/2} cos(pi N a), c_{N/2} is real for real f
        val += (c[-1] * np.cos(np.pi * N * aa)).real
        out[s:s + chunk] = val
    return out


def fourier_point(f_hat, a, deriv=0):
    """Value (deriv=0) or alpha-derivative (deriv=1,2) of the trigonometric
    interpolant with rfft coefficients f_hat (samples at alpha_j=(j-N/2)/N) at
    one point a. The Nyquist mode is dropped from derivatives."""
    N = 2 * (f_hat.size - 1)
    k = np.arange(1, N // 2)
    ph = np.exp(2j * np.pi * k * (a + 0.5))
    val = 2.0 * np.sum((f_hat[1:-1] * (2j * np.pi * k) ** deriv) * ph).real
    if deriv == 0:
        val += f_hat[0].real + (f_hat[-1] * np.exp(1j * np.pi * N * (a + 0.5))).real
    return val / N


def refine_peak(g, w_hat, j, iters=5):
    """Spectrally accurate |w| maximum near grid index j: Newton on w_alpha = 0.
    Returns (|w| at the peak, alpha of the peak)."""
    a = float(g.alpha[j])
    for _ in range(iters):
        d1 = fourier_point(w_hat, a, 1)
        d2 = fourier_point(w_hat, a, 2)
        if d2 == 0.0:
            break
        step = -d1 / d2
        step = max(-1.0 / g.N, min(1.0 / g.N, step))
        a += step
        if abs(step) < 1e-15:
            break
    return abs(fourier_point(w_hat, a, 0)), a


# ----------------------------------------------------------------------------
# The stretched mesh and everything that depends on it
# ----------------------------------------------------------------------------
class MeshMap:
    def __init__(self, N, L=128.0, r=1.0, uniform=False, build_kernel=True):
        self.N, self.L, self.r, self.uniform = N, float(L), float(r), uniform
        self.alpha = (np.arange(N) - N // 2) / N          # alpha[N//2] = 0
        k = np.arange(N // 2 + 1)
        self.k = k
        self.ddx = 1j * 2.0 * np.pi * k
        self.ddx[-1] = 0.0                                  # drop Nyquist derivative
        self.hilb = -1j * np.sign(k).astype(complex)        # H e^{ikx} = -i sgn(k) e^{ikx}
        self.hilb[-1] = 0.0
        self.integ = np.zeros(N // 2 + 1, dtype=complex)
        self.integ[1:-1] = 1.0 / (2j * np.pi * k[1:-1])     # antiderivative, zero mean
        self.filt = np.exp(-36.0 * (k / (N // 2)) ** 36)    # Hou-Li filter
        self.tail = k > N // 4

        # -- density rho(alpha) = x'(alpha) and x(alpha) ---------------------
        if uniform:
            self.C = 1.0
            self.rho = np.ones(N)
            self.drho = np.zeros(N)
            self.x = self.alpha.copy()
        else:
            # cell integrals of the unnormalised density on alpha >= 0
            a0 = self.alpha[N // 2:]                                     # 0 .. 1/2 - 1/N
            nodes = a0[:, None] + _GLX[None, :] / N
            cell = (self._rhot(nodes)[0] * _GLW[None, :]).sum(axis=1) / N
            self.C = 0.5 / cell.sum()                                    # so that x(1/2) = 1/2
            xpos = np.concatenate(([0.0], np.cumsum(cell)[:-1])) * self.C  # x(alpha >= 0)
            x = np.empty(N)
            x[N // 2:] = xpos
            x[1:N // 2] = -xpos[:0:-1]                                   # odd mirror
            x[0] = -0.5
            self.x = x
            rt, drt = self._rhot(self.alpha)
            self.rho, self.drho = self.C * rt, self.C * drt
        self.h = self.rho / N                 # local cell size in x
        self.hmin = float(self.h[N // 2])
        self.hmax = float(self.h.max())

        # -- dense correction kernel for odd input, even output ---------------
        self.M = None
        if build_kernel and not uniform:
            self._build_kernel()

    # analytic density (unnormalised) and its alpha-derivative
    def _rhot(self, a):
        s = np.sin(np.pi * a) / np.pi
        z = self.r * np.cosh(self.L * s)
        rho = z / (1.0 + z)
        dz = self.r * self.L * np.sinh(self.L * s) * np.cos(np.pi * a)
        return rho, dz / (1.0 + z) ** 2

    def rho_at(self, a):
        if self.uniform:
            return np.ones_like(a)
        return self.C * self._rhot(a)[0]

    def x_at(self, a):
        """x(alpha) at arbitrary alpha in [-1/2, 1/2], accurate relative to |x|."""
        a = np.asarray(a, dtype=float)
        if self.uniform:
            return a.copy()
        sgn = np.sign(a)
        aa = np.abs(a)
        N = self.N
        j = np.minimum((aa * N).astype(int), N // 2 - 1)        # cell index on alpha >= 0
        aj = j / N
        xj = self.x[N // 2 + j]
        # integral of rho from aj to aa by Gauss-Legendre on the partial cell
        nodes = aj[:, None] + (aa - aj)[:, None] * _GLX[None, :]
        inc = (self._rhot(nodes)[0] * _GLW[None, :]).sum(axis=1) * (aa - aj) * self.C
        return sgn * (xj + inc)

    def alpha_of(self, xt, iters=6):
        """Inverse map: alpha with x(alpha) = xt, for xt in [-1/2, 1/2]."""
        xt = np.asarray(xt, dtype=float)
        if self.uniform:
            return xt.copy()
        sgn = np.sign(xt)
        xa = np.abs(xt)
        N = self.N
        xpos = self.x[N // 2:]
        j = np.clip(np.searchsorted(xpos, xa, side="right") - 1, 0, N // 2 - 1)
        a = j / N + (xa - xpos[j]) / self.rho[N // 2 + j]       # linear guess
        for _ in range(iters):
            a = np.clip(a, 0.0, 0.5)
            a = a - (self.x_at(a) - xa) / self.rho_at(a)
        a = np.clip(a, 0.0, 0.5)
        return sgn * a

    def _build_kernel(self, chunk=1024):
        """M[i, j] = (K(a_i, a_j) - K(a_i, -a_j)) / N for rows a_i >= 0 (plus the
        point alpha = 1/2) and columns 0 < a_j < 1/2. Acting on w restricted to
        the columns it gives the dense part of H(omega) for odd omega."""
        N = self.N
        self.rows = np.concatenate(([0], np.arange(N // 2, N)))      # alpha = 1/2, 0, ..., 1/2 - 1/N
        self.cols = np.arange(N // 2 + 1, N)                          # 0 < alpha < 1/2
        ar = self.alpha[self.rows].copy()
        ar[0] = 0.5
        xr = self.x[self.rows].copy()
        xr[0] = 0.5
        ac, xc, rc = self.alpha[self.cols], self.x[self.cols], self.rho[self.cols]
        diag = -self.drho / (2.0 * np.pi * self.rho)                  # K(a, a)
        M = np.empty((self.rows.size, self.cols.size))
        for s in range(0, self.rows.size, chunk):
            e = min(s + chunk, self.rows.size)
            A, X = ar[s:e, None], xr[s:e, None]
            with np.errstate(divide="ignore", invalid="ignore"):
                Kp = rc * (1.0 / np.tan(np.pi * (X - xc))) - 1.0 / np.tan(np.pi * (A - ac))
            Km = rc * (1.0 / np.tan(np.pi * (X + xc))) - 1.0 / np.tan(np.pi * (A + ac))
            same = (A == ac)                                          # diagonal pairs
            if same.any():
                ii, jj = np.nonzero(same)
                Kp[ii, jj] = diag[self.rows[s:e][ii]]
            M[s:e] = (Kp - Km) / N
        self.M = M

    # -- spectral helpers ---------------------------------------------------
    def deriv_alpha(self, f_hat):
        return irfft(self.ddx * f_hat, n=self.N)

    def hilbert_u(self, w):
        """For odd omega samples w: returns u_x = H(omega) (even) and u (odd)."""
        N = self.N
        w_hat = rfft(w)
        ux = irfft(self.hilb * w_hat, n=N)
        if not self.uniform:
            corr = self.M @ w[self.cols]
            ux[0] += corr[0]
            ux[N // 2:] += corr[1:]
            ux[1:N // 2] = ux[N - 1:N // 2:-1]                          # even mirror
        u = irfft(self.integ * rfft(ux * self.rho), n=N)                # u_alpha = u_x rho, mean 0
        return ux, u

    def tail_fraction(self, f_hat):
        e = np.abs(f_hat) ** 2
        tot = e.sum()
        return float(np.sqrt(e[self.tail].sum() / tot)) if tot > 0 else 0.0


# ----------------------------------------------------------------------------
# Dynamics
# ----------------------------------------------------------------------------
def rhs(g, w, th):
    w_hat, th_hat = rfft(w), rfft(th)
    w_a, th_a = g.deriv_alpha(w_hat), g.deriv_alpha(th_hat)
    _, u = g.hilbert_u(w)
    v = u / g.rho                                   # advection speed in alpha
    return -v * w_a + th_a / g.rho, -v * th_a


def rk4_step(g, w, th, dt):
    k1w, k1t = rhs(g, w, th)
    k2w, k2t = rhs(g, w + 0.5 * dt * k1w, th + 0.5 * dt * k1t)
    k3w, k3t = rhs(g, w + 0.5 * dt * k2w, th + 0.5 * dt * k2t)
    k4w, k4t = rhs(g, w + dt * k3w, th + dt * k3t)
    w = w + dt / 6.0 * (k1w + 2 * (k2w + k3w) + k4w)
    th = th + dt / 6.0 * (k1t + 2 * (k2t + k3t) + k4t)
    w = irfft(g.filt * rfft(w), n=g.N)
    th = irfft(g.filt * rfft(th), n=g.N)
    return odd_part(w), even_part(th)


def initial_data(g):
    w0 = np.zeros(g.N)
    th0 = 1.0 - np.cos(2.0 * np.pi * g.x)
    return w0, th0


def remesh(g_old, w, th, r_new):
    g_new = MeshMap(g_old.N, g_old.L, r_new)
    N = g_new.N
    # only alpha >= 0 (plus alpha = -1/2) is needed; mirror the rest
    idx = np.concatenate(([0], np.arange(N // 2, N)))
    a_old = g_old.alpha_of(g_new.x[idx])
    a_old[0] = -0.5
    w_new, th_new = np.empty(N), np.empty(N)
    w_new[idx] = fourier_eval(w, a_old)
    th_new[idx] = fourier_eval(th, a_old)
    w_new[1:N // 2] = -w_new[N - 1:N // 2:-1]
    th_new[1:N // 2] = th_new[N - 1:N // 2:-1]
    return g_new, odd_part(w_new), even_part(th_new)


def run(N=8192, L=128.0, r0=0.05, uniform=False, t_end=2.0, wmax_target=1e4,
        cfl=0.5, dt_scale=1.0, tail_tol=1e-6, remesh_cells=48, remesh_target=192,
        snap_factor=2.0, max_seconds=None, verbose=True, log_every=200):
    """Integrate the inviscid model until max|omega| >= wmax_target, t >= t_end,
    loss of resolution, or the wall-clock budget. Returns a dict of time series,
    snapshots of omega(x), the remesh log and the stop reason."""
    g = MeshMap(N, L, r0, uniform=uniform)
    w, th = initial_data(g)
    keys = ("t", "wmax", "xstar", "txmax", "umax", "uxmin", "width", "tail",
            "tail_th", "hmin", "dt", "wmax_grid", "width0", "l2w", "l2t")
    hist = {k: [] for k in keys}
    snaps, remeshes = [], []
    next_snap = 1.0
    t, steps, status = 0.0, 0, "reached t_end"
    clock = time.time()
    tail_max = 0.0

    while True:
        w_hat, th_hat = rfft(w), rfft(th)
        wx = g.deriv_alpha(w_hat) / g.rho
        tx = g.deriv_alpha(th_hat) / g.rho
        ux, u = g.hilbert_u(w)
        j = int(np.argmax(np.abs(w)))
        wmax_grid = float(abs(w[j]))
        if wmax_grid > 0:
            wmax, a_peak = refine_peak(g, w_hat, j)
            xstar = float(abs(g.x_at(np.array([a_peak]))[0]))
        else:
            wmax, xstar = 0.0, 0.0
        txmax, umax = float(np.max(np.abs(tx))), float(np.max(np.abs(u)))
        wxmax = float(np.max(np.abs(wx)))
        wx0 = float(abs(wx[N // 2]))                          # omega_x at x = 0, exact
        l2w = float(np.sqrt(np.sum(w * w * g.rho) / N))       # ||omega||_2, exact quadrature
        l2t = float(np.sqrt(np.sum(th * th * g.rho) / N))
        tail, tail_th = g.tail_fraction(w_hat), g.tail_fraction(th_hat)
        tail_max = max(tail_max, tail)

        dt = min(cfl / (N * max(float(np.max(np.abs(u / g.rho))), 1e-300)),
                 0.05 / max(wmax, 1e-12),
                 0.05 / np.sqrt(max(txmax, 1e-12)),
                 1e-2) * dt_scale
        dt = min(dt, t_end - t) if t_end - t > 0 else dt

        for k_, v_ in zip(keys, (t, wmax, xstar, txmax, umax, float(np.min(ux)),
                                 wmax / wxmax if wxmax > 0 else np.nan, tail,
                                 tail_th, g.hmin, dt, wmax_grid,
                                 wmax / wx0 if wx0 > 0 else np.nan, l2w, l2t)):
            hist[k_].append(v_)

        if wmax >= next_snap:
            snaps.append({"t": t, "wmax": wmax, "x": g.x.copy(), "omega": w.copy(),
                          "theta": th.copy()})
            next_snap = wmax * snap_factor

        if verbose and steps % log_every == 0:
            print(f"    t={t:.6f} max|w|={wmax:10.4g} x*={xstar:9.3e} hmin={g.hmin:8.2e}"
                  f" x*/hmin={xstar / g.hmin:6.1f} tail={tail:8.1e} dt={dt:8.1e}"
                  f" ({time.time() - clock:6.1f}s)", flush=True)

        if not np.isfinite(wmax):
            status = "stopped: non-finite values"
            break
        if tail > tail_tol:
            status = "stopped: grid can no longer resolve the solution"
            break
        if wmax >= wmax_target:
            status = f"reached max|omega| target {wmax_target:g}"
            break
        if t >= t_end - 1e-14:
            break
        if max_seconds is not None and time.time() - clock > max_seconds:
            status = "stopped: wall-clock budget"
            break
        if dt < 1e-13 * max(t, 1e-3):
            status = "stopped: time step underflow"
            break

        # remesh when the peak approaches the plateau edge
        if not uniform and xstar < remesh_cells * g.hmin and wmax > 1.0:
            r_new = g.r * xstar / (remesh_target * g.hmin)
            g, w, th = remesh(g, w, th, r_new)
            remeshes.append({"t": t, "wmax": wmax, "r": g.r, "hmin": g.hmin,
                             "xstar_cells": xstar / g.hmin})
            if verbose:
                print(f"    remesh #{len(remeshes)} at t={t:.6f}: r={g.r:.3e} "
                      f"hmin={g.hmin:.2e} x*/hmin={xstar / g.hmin:.0f}", flush=True)
            continue                                   # recompute diagnostics on the new mesh

        w, th = rk4_step(g, w, th, dt)
        t += dt
        steps += 1

    if not snaps or snaps[-1]["t"] != t:
        snaps.append({"t": t, "wmax": wmax, "x": g.x.copy(), "omega": w.copy(),
                      "theta": th.copy()})
    out = {k: np.array(v) for k, v in hist.items()}
    out.update(N=N, L=L, r0=r0, uniform=uniform, cfl=cfl, dt_scale=dt_scale,
               remesh_cells=remesh_cells, remesh_target=remesh_target,
               status=status, steps=steps, snaps=snaps, remeshes=remeshes,
               tail_max=tail_max, seconds=time.time() - clock,
               x=g.x.copy(), omega=w.copy(), theta=th.copy(), hmin_final=g.hmin)
    if verbose:
        print(f"  N={N:<6d} L={L:g} t={t:.8f}  max|omega|={wmax:10.6g}  steps={steps}"
              f"  remeshes={len(remeshes)}  tail_max={tail_max:.1e}"
              f"  ({out['seconds']:.1f}s)  {status}")
    return out


# ----------------------------------------------------------------------------
# Blowup diagnostics
# ----------------------------------------------------------------------------
def blowup_fit(res, wlo, whi=None):
    """Fit 1/max|omega| = a (T - t) on the window wlo <= max|omega| <= whi.
    Returns T, the growth exponent p (max|omega| ~ (T-t)^-p) and the width
    exponent c (width ~ (T-t)^c) measured with the fitted T."""
    t, w, width = res["t"], res["wmax"], res["width"]
    whi = w[-1] if whi is None else whi
    m = (w >= wlo) & (w <= whi)
    if m.sum() < 10:
        return None
    a, b = np.polyfit(t[m], 1.0 / w[m], 1)
    T = -b / a
    resid = 1.0 / w[m] - (a * t[m] + b)
    tau = T - t[m]
    ok = tau > 0
    p = -np.polyfit(np.log(tau[ok]), np.log(w[m][ok]), 1)[0]
    c = np.polyfit(np.log(tau[ok]), np.log(width[m][ok]), 1)[0]
    c0 = np.polyfit(np.log(tau[ok]), np.log(res["width0"][m][ok]), 1)[0]
    return {"T": float(T), "p": float(p), "c": float(c), "c0": float(c0),
            "fit_window_t": [float(t[m][0]), float(t[m][-1])],
            "omega_range": [float(w[m][0]), float(w[m][-1])],
            "max_rel_resid": float(np.max(np.abs(resid) * w[m]))}


def local_T(res, every=1):
    """T_loc(t) = t + max|omega| / (d max|omega| / dt): the blowup time a pure
    1/(T - t) law would predict from the local slope. Constant if p = 1."""
    t, w = res["t"][::every], res["wmax"][::every]
    dw = np.gradient(w, t)
    good = dw > 0
    return t[good], (t + w / np.where(good, dw, np.nan))[good]


def thin(a, n=2000):
    a = np.asarray(a)
    if a.size <= n:
        return a
    idx = np.unique(np.linspace(0, a.size - 1, n).astype(int))
    return a[idx]


def summarize(res, decades=(1.0, 2.0)):
    wend = float(res["wmax"][-1])
    fits = {}
    for d in decades:
        f = blowup_fit(res, wend / 10 ** d)
        if f:
            fits[f"last_{d:g}_decades"] = f
    return {
        "N": res["N"], "L": res["L"], "r0": res["r0"], "uniform": res["uniform"],
        "cfl": res["cfl"], "dt_scale": res["dt_scale"],
        "remesh_cells": res["remesh_cells"], "remesh_target": res["remesh_target"],
        "status": res["status"], "steps": int(res["steps"]), "seconds": res["seconds"],
        "t_final": float(res["t"][-1]), "wmax_final": wend,
        "xstar_final": float(res["xstar"][-1]), "width_final": float(res["width"][-1]),
        "hmin_final": res["hmin_final"], "tail_max": res["tail_max"],
        "n_remesh": len(res["remeshes"]), "remeshes": res["remeshes"],
        "r_final": res["remeshes"][-1]["r"] if res["remeshes"] else res["r0"],
        "fits": fits,
    }


def save(res, prefix):
    summ = summarize(res)
    with open(prefix + ".json", "w") as fh:
        json.dump(summ, fh, indent=2)
    series = {k: thin(res[k]) for k in ("t", "wmax", "xstar", "txmax", "umax",
                                        "uxmin", "width", "tail", "tail_th",
                                        "hmin", "dt", "wmax_grid", "width0",
                                        "l2w", "l2t")}
    np.savez_compressed(prefix + ".npz",
                        **{f"hist_{k}": v for k, v in series.items()},
                        **{f"snap{i}_{k}": s[k] for i, s in enumerate(res["snaps"])
                           for k in ("t", "wmax", "x", "omega", "theta")},
                        n_snaps=len(res["snaps"]), x=res["x"], omega=res["omega"],
                        theta=res["theta"])
    return summ


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--N", type=int, default=8192)
    ap.add_argument("--L", type=float, default=128.0,
                    help="ramp steepness; N/L = cells per e-fold of |x|. Keep fixed across N.")
    ap.add_argument("--r0", type=float, default=0.05, help="initial mesh ratio hmin/hmax")
    ap.add_argument("--uniform", action="store_true", help="rho = 1: reproduces hou_luo.py")
    ap.add_argument("--t-end", type=float, default=2.0)
    ap.add_argument("--wmax-target", type=float, default=1e4)
    ap.add_argument("--cfl", type=float, default=0.5)
    ap.add_argument("--dt-scale", type=float, default=1.0)
    ap.add_argument("--tail-tol", type=float, default=1e-6)
    ap.add_argument("--remesh-cells", type=float, default=48)
    ap.add_argument("--remesh-target", type=float, default=192)
    ap.add_argument("--max-seconds", type=float, default=None)
    ap.add_argument("--out", default=None, help="output prefix (default step1_N<N>)")
    ap.add_argument("--log-every", type=int, default=200)
    args = ap.parse_args()

    print(f"Inviscid 1D Hou-Luo model on an adaptive mesh: N={args.N} L={args.L:g}")
    res = run(N=args.N, L=args.L, r0=args.r0, uniform=args.uniform, t_end=args.t_end,
              wmax_target=args.wmax_target, cfl=args.cfl, dt_scale=args.dt_scale,
              tail_tol=args.tail_tol, remesh_cells=args.remesh_cells,
              remesh_target=args.remesh_target, max_seconds=args.max_seconds,
              log_every=args.log_every)
    prefix = args.out or f"step1_N{args.N}" + ("_uniform" if args.uniform else "")
    summ = save(res, prefix)
    for name, f in summ["fits"].items():
        print(f"  {name}: T = {f['T']:.7f}  p = {f['p']:.4f}  c = {f['c']:.3f} c0 = {f['c0']:.3f}"
              f"  (max|omega| {f['omega_range'][0]:.3g} .. {f['omega_range'][1]:.3g},"
              f" max rel resid {f['max_rel_resid']:.1e})")
    print(f"Wrote {prefix}.json and {prefix}.npz")


if __name__ == "__main__":
    main()
