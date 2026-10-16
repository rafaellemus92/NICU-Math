#!/usr/bin/env python3
"""Step 1 figure: the reciprocal plot for the inviscid 1D Hou-Luo model on the
adaptive mesh, with its supporting panels. Tall stacked panels, large text.

    python step1_plot.py step1_N4096 step1_N8192 step1_N16384

Also writes step1_results.json (the numbers behind the figure).
"""
import json
import os
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from plot_results import SURFACE, INK, INK2, MUTED, GRID, AXIS, ORANGE, _style, _orange_ramp

# ordinal ramp for the three resolutions (light -> dark = coarse -> fine);
# validated with the dataviz palette checker (light surface, ordinal mode)
BLUES3 = ["#74adec", "#2f76cf", "#17498c"]


def load(prefix):
    d = np.load(prefix + ".npz")
    with open(prefix + ".json") as fh:
        summ = json.load(fh)
    hist = {k[5:]: d[k] for k in d.files if k.startswith("hist_")}
    snaps = [{k: d[f"snap{i}_{k}"] for k in ("t", "wmax", "x", "omega", "theta")}
             for i in range(int(d["n_snaps"]))]
    return hist, snaps, summ


def baseline_uniform(N=8192, cache="baseline_uniform_N%d.npz"):
    """max|omega|(t) of hou_luo.py's uniform-grid inviscid run (cached)."""
    path = cache % N
    if not os.path.exists(path):
        import hou_luo as hl
        r = hl.run(N=N, nu=0.0, verbose=False)
        np.savez(path, t=r["t"], wmax=r["wmax"])
    d = np.load(path)
    return d["t"], d["wmax"]


def sliding_T(hist, window=61):
    """Local blowup-time estimate: the t-intercept of a straight line fitted to
    1/max|omega| over a sliding window. Constant if max|omega| ~ 1/(T - t)."""
    ok = hist["wmax"] > 0
    t, w = hist["t"][ok], hist["wmax"][ok]
    y = 1.0 / w
    out_t, out_T, out_w = [], [], []
    h = window // 2
    for i in range(h, t.size - h):
        sl = slice(i - h, i + h + 1)
        a, b = np.polyfit(t[sl], y[sl], 1)
        if a < 0:
            out_t.append(t[i]); out_T.append(-b / a); out_w.append(w[i])
    return np.array(out_t), np.array(out_T), np.array(out_w)


def make_figure(prefixes, path="step1_reciprocal.png"):
    runs = [load(p) for p in prefixes]
    runs.sort(key=lambda r: r[2]["N"])
    colors = BLUES3[-len(runs):] if len(runs) <= 3 else \
        [matplotlib.colormaps["Blues"](v) for v in np.linspace(0.45, 0.95, len(runs))]
    hist_f, snaps_f, summ_f = runs[-1]                      # finest run
    fit = summ_f["fits"]["last_1_decades"]
    T = fit["T"]
    tb, wb = baseline_uniform(8192)

    fig, axes = plt.subplots(4, 1, figsize=(6.4, 17.6), facecolor=SURFACE,
                             gridspec_kw={"hspace": 0.62})

    # --- A: the reciprocal plot, whole run --------------------------------
    ax = axes[0]
    ax.plot(tb, 1.0 / wb, color=ORANGE, lw=3.2, label="uniform grid, N = 8192 (hou_luo.py)",
            zorder=2)
    for (hist, _, summ), c in zip(runs, colors):
        ax.plot(hist["t"], 1.0 / hist["wmax"], color=c, lw=2.0, zorder=3,
                label=f"adaptive mesh, N = {summ['N']}")
    ax.plot(tb[-1], 1.0 / wb[-1], "o", color=ORANGE, ms=8, mec=SURFACE, mew=1.5, zorder=5)
    ax.annotate("uniform grid gives up here\n(max |ω| = 9.4)", (tb[-1], 1.0 / wb[-1]),
                xytext=(-178, 8), textcoords="offset points", fontsize=8.5, color=INK2,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    tt = np.array([0.74, T])
    a_fit = 1.0 / (fit["omega_range"][0]) / (T - fit["fit_window_t"][0])
    ax.plot(tt, a_fit * (T - tt), color=MUTED, lw=1.2, ls="--", zorder=1,
            label="straight line through max|ω| = 10³ … 10⁴")
    ax.plot(T, 0, "o", color=INK, ms=7, mec=SURFACE, mew=1.5, zorder=6)
    ax.annotate(f"T = {T:.5f}", (T, 0), xytext=(-62, 14), textcoords="offset points",
                fontsize=9.5, color=INK, fontweight="bold")
    ax.set_xlim(0.30, 0.86)
    ax.set_ylim(0, 0.52)
    ax.set_xlabel("time", fontsize=9.5, color=INK2)
    ax.set_ylabel("1 / max |ω|", fontsize=9.5, color=INK2)
    _style(ax, "A · The reciprocal plot",
           "1/max|ω| runs straight into zero: max|ω| ≈ 1/(T − t). All curves coincide where\n"
           "the uniform grid is still resolved; the adaptive mesh carries on to max|ω| = 10⁴")
    ax.set_title("A · The reciprocal plot", loc="left", fontsize=11.5, color=INK, pad=36,
                 fontweight="bold")
    ax.legend(fontsize=8, frameon=False, loc="upper right", labelcolor=INK2, handlelength=1.6)

    # --- B: zoom on the last two decades ---------------------------------
    ax = axes[1]
    for (hist, _, summ), c in zip(runs, colors):
        ax.plot(hist["t"], 1.0 / hist["wmax"], color=c, lw=2.0, label=f"N = {summ['N']}")
    tt = np.array([T - 0.012, T])
    ax.plot(tt, a_fit * (T - tt), color=MUTED, lw=1.2, ls="--", zorder=1,
            label="straight-line fit, max|ω| from 10³ to 10⁴")
    ax.plot(T, 0, "o", color=INK, ms=7, mec=SURFACE, mew=1.5, zorder=6)
    for wv, lab, off, ha, va in ((100, "max |ω| = 100", (-8, -4), "right", "top"),
                                 (1000, "1 000", (-8, -5), "right", "top"),
                                 (10000, "10 000", (9, 3), "left", "bottom")):
        okf = hist_f["wmax"] > 0
        tv = np.interp(1.0 / wv, (1.0 / hist_f["wmax"][okf])[::-1], hist_f["t"][okf][::-1])
        ax.plot(tv, 1.0 / wv, "o", color=colors[-1], ms=8, mec=SURFACE, mew=1.5, zorder=5)
        ax.annotate(lab, (tv, 1.0 / wv), xytext=off, textcoords="offset points",
                    fontsize=8.5, color=INK2, ha=ha, va=va)
    ax.set_xlim(T - 0.0115, T + 0.0014)
    ax.set_ylim(0, 0.0112)
    ax.ticklabel_format(axis="x", useOffset=False)
    ax.set_xlabel("time", fontsize=9.5, color=INK2)
    ax.set_ylabel("1 / max |ω|", fontsize=9.5, color=INK2)
    nres = {1: "One resolution lies", 2: "Both resolutions lie", 3: "All three resolutions lie"}
    _style(ax, "B · The last two decades, zoomed",
           f"{nres.get(len(runs), 'All resolutions lie')} on one line; growth exponent "
           f"p = {fit['p']:.4f}")
    ax.legend(fontsize=8, frameon=False, loc="lower left", labelcolor=INK2, handlelength=1.6)

    # --- C: where the local fit puts T, as the run proceeds ---------------
    ax = axes[2]
    for (hist, _, summ), c in zip(runs, colors):
        tl, Tl, wl = sliding_T(hist)
        m = wl > 4
        ax.plot(wl[m], Tl[m], color=c, lw=2.0, label=f"N = {summ['N']}")
    ax.axhline(T, color=MUTED, lw=1.0, ls="--", zorder=0)
    ax.text(4.3, T + 0.0025, f"T = {T:.5f}", fontsize=9, color=INK2)
    # the uniform-grid estimates from the baseline check, for contrast
    for Nb, Tb, wend in ((4096, 0.92572, 7.86), (8192, 0.90395, 9.43), (16384, 0.88120, 11.45)):
        ax.plot(wend, Tb, "o", color=ORANGE, ms=8, mec=SURFACE, mew=1.5, zorder=5)
    ax.annotate("uniform-grid fits\n(N = 4096, 8192, 16384)", (9.43, 0.90395), xytext=(30, 10),
                textcoords="offset points", fontsize=8.5, color=INK2,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax.set_xscale("log")
    ax.set_xlim(4, 1.3e4)
    ax.set_ylim(0.835, 0.935)
    ax.set_xlabel("max |ω| reached so far  (log scale)", fontsize=9.5, color=INK2)
    ax.set_ylabel("blowup time from a local fit", fontsize=9.5, color=INK2)
    _style(ax, "C · The estimate of T settles down",
           "Local straight-line fits to 1/max|ω| converge once max|ω| ≳ 100 (curves coincide)")
    ax.legend(fontsize=8, frameon=False, loc="upper right", labelcolor=INK2, handlelength=1.6)

    # --- D: self-similar collapse of the spike -----------------------------
    ax = axes[3]
    want = [16, 128, 1024, 8192]
    chosen = []
    for wv in want:
        i = int(np.argmin([abs(np.log(s["wmax"] / wv)) for s in snaps_f]))
        if not chosen or chosen[-1] is not snaps_f[i]:
            chosen.append(snaps_f[i])
    ramp = _orange_ramp(len(chosen))
    for s, c in zip(chosen, ramp):
        j = int(np.argmax(np.abs(s["omega"])))
        xs = abs(s["x"][j])
        m = np.abs(s["x"]) < 12 * xs
        ax.plot(s["x"][m] / xs, s["omega"][m] / s["wmax"], color=c, lw=1.8,
                label=f"max|ω| = {s['wmax']:.3g},  x* = {xs:.1e}")
    ax.set_xlim(-8, 8)
    ax.set_ylim(-1.15, 1.15)
    ax.axvline(0, color=AXIS, lw=0.8, zorder=0)
    ax.set_xlabel("x / x*(t)   (x* = position of the |ω| peak)", fontsize=9.5, color=INK2)
    ax.set_ylabel("ω / max |ω|", fontsize=9.5, color=INK2)
    _style(ax, "D · One shape at every scale",
           f"Rescaled profiles collapse while x* shrinks by 10⁹;  width ∝ (T − t)^{fit['c0']:.3f}")
    ax.legend(fontsize=8, frameon=False, loc="lower right", labelcolor=INK2, handlelength=1.6)

    fig.text(0.015, 0.004,
             "1D Hou–Luo model, ν = 0 · adaptive mesh (N = %s) · a toy, not the 3D equations"
             % " / ".join(str(r[2]["N"]) for r in runs), fontsize=7.5, color=MUTED)
    fig.savefig(path, dpi=200, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)
    return runs


def write_summary(runs, extra_prefixes=(), path="step1_results.json"):
    rows = []
    for pfx in list(extra_prefixes):
        pass
    for hist, snaps, summ in runs:
        f1 = summ["fits"].get("last_1_decades", {})
        f2 = summ["fits"].get("last_2_decades", {})
        rows.append({"N": summ["N"], "L": summ["L"], "cfl": summ["cfl"], "dt_scale": summ["dt_scale"],
                     "remesh_cells": summ["remesh_cells"], "remesh_target": summ["remesh_target"],
                     "status": summ["status"], "t_final": summ["t_final"],
                     "wmax_final": summ["wmax_final"], "xstar_final": summ["xstar_final"],
                     "hmin_final": summ["hmin_final"], "tail_max": summ["tail_max"],
                     "n_remesh": summ["n_remesh"], "steps": summ["steps"], "seconds": summ["seconds"],
                     "T_last_decade": f1.get("T"), "p_last_decade": f1.get("p"),
                     "c_last_decade": f1.get("c0"), "T_last_2_decades": f2.get("T"),
                     "p_last_2_decades": f2.get("p"), "c_last_2_decades": f2.get("c0")})
    out = {"model": "1D Hou-Luo, nu = 0, omega0 = 0, theta0 = 1 - cos(2 pi x)",
           "caveat": "A 1D toy model. Nothing here is evidence about 3D Navier-Stokes.",
           "runs": rows}
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)
    return out


if __name__ == "__main__":
    prefixes = sys.argv[1:] or ["step1_N4096", "step1_N8192", "step1_N16384"]
    prefixes = [p for p in prefixes if os.path.exists(p + ".json")]
    runs = make_figure(prefixes)
    write_summary(runs)
    print("Wrote step1_reciprocal.png and step1_results.json for", prefixes)
