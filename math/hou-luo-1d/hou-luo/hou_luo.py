#!/usr/bin/env python3
"""
hou_luo.py -- the 1D Hou-Luo model, with a viscosity knob.

WHAT THIS IS
The Hou-Luo model (Luo & Hou, PNAS 2014) is a one-line caricature of what
happens on the WALL of a swirling flow inside a pipe. That pipe setup is where
finite-time blowup of the 3D Euler equations (no viscosity) was later proven
rigorously, with computer assistance, by Chen & Hou.

    omega_t + u * omega_x = theta_x + nu    * omega_xx
    theta_t + u * theta_x =           kappa * theta_xx
    u_x = H(omega)                     (H = Hilbert transform)

on the periodic interval x in [-1/2, 1/2).

    omega : vorticity-like quantity (how hard the fluid is spinning)
    theta : swirl-like quantity (in the 3D picture, the swirl squared)
    u     : velocity along the wall; u(0) = 0 is a stagnation point
    nu    : viscosity, the knob (nu = 0 is the inviscid model)

The engine: a gradient in theta spins up omega, omega induces a flow u that
squeezes toward x = 0, the squeeze steepens theta, and the loop feeds itself.
With nu = kappa = 0 this blows up in finite time for suitable smooth data
(Choi, Hou, Kiselev, Luo, Sverak & Yao, CPAM 2017).

THE QUESTION THE KNOB ASKS
Viscosity spreads things out (diffusion); the loop above concentrates them.
Which one wins, and how does the answer depend on nu? That is the Millennium
problem's question in miniature -- but only in miniature: this is a 1D toy,
and nothing it does settles the 3D Navier-Stokes equations.

HOW TO READ THE OUTPUT
If max|omega| grows like 1/(T - t), then 1/max|omega| falls on a straight line
that hits zero at the blowup time T. Exponential growth never hits zero.
That "reciprocal plot" is the cleanest visual test for finite-time blowup.

NUMERICS
Pseudo-spectral in x (FFT), Lawson integrating-factor RK4 in time (viscosity
handled exactly), adaptive time step, Hou-Li high-order Fourier filter.
A uniform grid cannot follow a true singularity forever: each run stops when
the solution is no longer resolved (energy piles up at the smallest scales).
Pushing past that needs an adaptive mesh -- see CLAUDE.md for next steps.

USAGE
    python hou_luo.py                      # inviscid + viscosity sweep + figure
    python hou_luo.py --N 32768            # finer grid
    python hou_luo.py --nus 1e-3 3e-4 1e-4 # choose your own viscosities
    python hou_luo.py --check              # grid-convergence check (N vs 2N)
"""

import argparse
import json
import time

import numpy as np


# ----------------------------------------------------------------------------
# Spectral setup
# ----------------------------------------------------------------------------
class Grid:
    def __init__(self, N):
        self.N = N
        self.dx = 1.0 / N
        self.x = np.arange(N) / N - 0.5
        k = np.arange(N // 2 + 1)                       # rfft wavenumbers
        self.k = k
        self.kap = 2.0 * np.pi * k                      # length-1 domain
        self.ddx = 1j * self.kap
        self.ddx[-1] = 0.0                              # drop Nyquist derivative
        # u_x = H(omega) with H(e^{ikx}) = -i sgn(k) e^{ikx}
        #   =>  u_hat = -omega_hat / (2 pi |k|)    (mean of u set to zero)
        self.u_mult = np.zeros_like(self.kap)
        self.u_mult[1:] = -1.0 / self.kap[1:]
        # Hou-Li filter: kills the top few percent of modes, keeps the rest
        self.filt = np.exp(-36.0 * (k / (N // 2)) ** 36)
        self.tail = k > N // 4                          # for resolution check

    def fields(self, w_hat, t_hat):
        N = self.N
        w = np.fft.irfft(w_hat, n=N)
        u = np.fft.irfft(self.u_mult * w_hat, n=N)
        wx = np.fft.irfft(self.ddx * w_hat, n=N)
        tx = np.fft.irfft(self.ddx * t_hat, n=N)
        return w, u, wx, tx

    def nonlinear(self, w_hat, t_hat):
        _, u, wx, tx = self.fields(w_hat, t_hat)
        return np.fft.rfft(-u * wx + tx), np.fft.rfft(-u * tx)

    def tail_fraction(self, w_hat):
        e = np.abs(w_hat) ** 2
        tot = e.sum()
        return float(np.sqrt(e[self.tail].sum() / tot)) if tot > 0 else 0.0


def initial_data(g):
    """omega0 = 0, theta0 = 1 - cos(2 pi x): smooth, even, rising on [0, 1/2].
    The squeeze forms at the stagnation point x = 0."""
    w0 = np.zeros(g.N)
    th0 = 1.0 - np.cos(2.0 * np.pi * g.x)
    return np.fft.rfft(w0), np.fft.rfft(th0)


# ----------------------------------------------------------------------------
# Time stepping
# ----------------------------------------------------------------------------
def lawson_rk4(g, w_hat, t_hat, dt, Lw, Lt):
    """One step of v_t = L v + N(v), L diagonal (diffusion), integrated exactly."""
    Ew, Ew2 = np.exp(Lw * dt), np.exp(Lw * dt / 2)
    Et, Et2 = np.exp(Lt * dt), np.exp(Lt * dt / 2)

    k1w, k1t = g.nonlinear(w_hat, t_hat)
    k2w, k2t = g.nonlinear(Ew2 * (w_hat + 0.5 * dt * k1w),
                           Et2 * (t_hat + 0.5 * dt * k1t))
    k3w, k3t = g.nonlinear(Ew2 * w_hat + 0.5 * dt * k2w,
                           Et2 * t_hat + 0.5 * dt * k2t)
    k4w, k4t = g.nonlinear(Ew * w_hat + dt * Ew2 * k3w,
                           Et * t_hat + dt * Et2 * k3t)

    w_new = Ew * w_hat + dt / 6 * (Ew * k1w + 2 * Ew2 * (k2w + k3w) + k4w)
    t_new = Et * t_hat + dt / 6 * (Et * k1t + 2 * Et2 * (k2t + k3t) + k4t)
    return w_new * g.filt, t_new * g.filt


def run(N=8192, nu=0.0, kappa=None, t_end=1.3, cfl=0.5, tail_tol=1e-6,
        snap_factor=1.5, verbose=True):
    """Integrate until t_end or until the grid can no longer resolve the solution.

    Returns a dict of time series plus omega(x) snapshots taken each time
    max|omega| grows by `snap_factor`.
    """
    kappa = nu if kappa is None else kappa
    g = Grid(N)
    w_hat, t_hat = initial_data(g)
    Lw = -nu * g.kap ** 2
    Lt = -kappa * g.kap ** 2

    hist = {k: [] for k in ("t", "wmax", "txmax", "umax", "uxmin", "width",
                            "tail")}
    snaps = []
    next_snap = 1.0
    t, steps, status = 0.0, 0, "reached t_end"
    clock = time.time()

    while True:
        w, u, wx, tx = g.fields(w_hat, t_hat)
        ux = np.fft.irfft(g.ddx * g.u_mult * w_hat, n=N)
        wmax = float(np.max(np.abs(w)))
        txmax = float(np.max(np.abs(tx)))
        umax = float(np.max(np.abs(u)))
        wxmax = float(np.max(np.abs(wx)))
        tail = g.tail_fraction(w_hat)

        hist["t"].append(t)
        hist["wmax"].append(wmax)
        hist["txmax"].append(txmax)
        hist["umax"].append(umax)
        hist["uxmin"].append(float(np.min(ux)))
        hist["width"].append(wmax / wxmax if wxmax > 0 else np.nan)
        hist["tail"].append(tail)

        if wmax >= next_snap:
            snaps.append({"t": t, "wmax": wmax, "omega": w.copy()})
            next_snap = wmax * snap_factor

        if tail > tail_tol:
            status = "stopped: grid can no longer resolve the solution"
            break
        if t >= t_end - 1e-14:
            break
        if not np.isfinite(wmax):
            status = "stopped: non-finite values"
            break

        dt = min(cfl * g.dx / max(umax, 1e-12),
                 0.05 / max(wmax, 1e-12),
                 0.05 / np.sqrt(max(txmax, 1e-12)),
                 1e-2,
                 t_end - t)
        w_hat, t_hat = lawson_rk4(g, w_hat, t_hat, dt, Lw, Lt)
        t += dt
        steps += 1

    if not snaps or snaps[-1]["t"] != t:
        snaps.append({"t": t, "wmax": wmax, "omega": w.copy()})
    out = {k: np.array(v) for k, v in hist.items()}
    out.update(N=N, nu=nu, kappa=kappa, status=status, steps=steps,
               x=g.x, snaps=snaps, seconds=time.time() - clock)
    if verbose:
        print(f"  N={N:<6d} nu={nu:<8.1e} t={t:.6f}  max|omega|={wmax:10.4g}"
              f"  steps={steps:<6d} ({out['seconds']:.1f}s)  {status}")
    return out


# ----------------------------------------------------------------------------
# Blowup diagnostics
# ----------------------------------------------------------------------------
def blowup_fit(res, frac=0.5):
    """Fit 1/max|omega| = a (T - t) on the late part of an inviscid run.

    Uses points where max|omega| is at least `frac` of its final value. On a
    uniform grid that window is short, so treat T as a rough estimate. Returns T, the fitted
    growth exponent (omega ~ (T-t)^-p, expect p ~ 1), and the length-scale
    exponent c (width ~ (T-t)^c).
    """
    t, w, width = res["t"], res["wmax"], res["width"]
    m = w >= frac * w[-1]
    if m.sum() < 10:
        return None
    a, b = np.polyfit(t[m], 1.0 / w[m], 1)
    T = -b / a
    tau = T - t[m]
    ok = tau > 0
    p = -np.polyfit(np.log(tau[ok]), np.log(w[m][ok]), 1)[0]
    c = np.polyfit(np.log(tau[ok]), np.log(width[m][ok]), 1)[0]
    return {"T": float(T), "p": float(p), "c": float(c),
            "fit_window": [float(t[m][0]), float(t[m][-1])],
            "omega_range": [float(w[m][0]), float(w[m][-1])]}


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--N", type=int, default=8192, help="grid points")
    ap.add_argument("--nus", type=float, nargs="*",
                    default=[3e-3, 1e-3, 3e-4, 1e-4, 3e-5],
                    help="viscosities for the sweep")
    ap.add_argument("--t-end", type=float, default=1.3,
                    help="end time for the viscous runs")
    ap.add_argument("--check", action="store_true",
                    help="grid-convergence check: inviscid run at N/2, N, 2N")
    ap.add_argument("--out", default="hou_luo_results", help="output prefix")
    ap.add_argument("--no-plot", action="store_true")
    args = ap.parse_args()

    print("Inviscid run (nu = 0):")
    inv = run(N=args.N, nu=0.0)
    fit = blowup_fit(inv)
    if fit:
        print(f"  reciprocal-plot blowup time T ~ {fit['T']:.5f}")
        print(f"  growth exponent p ~ {fit['p']:.3f}  (max|omega| ~ (T-t)^-p; scaling predicts 1)")
        print(f"  width exponent  c ~ {fit['c']:.3f}  (width ~ (T-t)^c)")

    print(f"\nViscous sweep (run to t = {args.t_end}):")
    visc = [run(N=args.N, nu=nu, t_end=args.t_end) for nu in args.nus]
    for r in visc:
        i = int(np.argmax(r["wmax"]))
        print(f"  nu={r['nu']:.1e}: peak max|omega| = {r['wmax'][i]:.4g} at t = {r['t'][i]:.4f}")
    scaling = None
    if len(visc) >= 2:
        nus = np.array([r["nu"] for r in visc])
        peaks = np.array([r["wmax"].max() for r in visc])
        a = float(np.polyfit(np.log(nus), np.log(peaks), 1)[0])
        scaling = {"peak_vs_nu_exponent": a}
        print(f"  peak max|omega| ~ nu^{a:.3f}")

    checks = []
    if args.check:
        print("\nGrid-convergence check (inviscid):")
        for N in (args.N // 2, args.N * 2):
            r = run(N=N, nu=0.0)
            f = blowup_fit(r)
            checks.append({"N": N, "T": f["T"] if f else None,
                           "wmax_final": float(r["wmax"][-1])})
            if f:
                print(f"  N={N}: T ~ {f['T']:.5f}, p ~ {f['p']:.3f}, c ~ {f['c']:.3f}")

    summary = {
        "inviscid": {"N": inv["N"], "status": inv["status"],
                     "t_final": float(inv["t"][-1]),
                     "wmax_final": float(inv["wmax"][-1]), "fit": fit},
        "viscous": [{"nu": r["nu"], "status": r["status"],
                     "peak_wmax": float(r["wmax"].max()),
                     "t_peak": float(r["t"][int(np.argmax(r["wmax"]))])}
                    for r in visc],
        "peak_scaling": scaling,
        "grid_check": checks,
    }
    with open(args.out + ".json", "w") as fh:
        json.dump(summary, fh, indent=2)
    print(f"\nWrote {args.out}.json")

    if not args.no_plot:
        from plot_results import make_figure
        make_figure(inv, fit, visc, args.out + ".png")
        print(f"Wrote {args.out}.png")


if __name__ == "__main__":
    main()
