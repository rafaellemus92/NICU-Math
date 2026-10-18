"""Phone-friendly figure for hou_luo.py: three stacked panels."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
ORANGE = "#eb6834"                       # the inviscid run (nu = 0)
BLUES = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281",
         "#0d366b"]                     # viscosity sweep, more viscous = lighter


def _orange_ramp(n):
    """One-hue ordinal ramp: orange mixed toward the surface, light -> full."""
    o = np.array(matplotlib.colors.to_rgb(ORANGE))
    s = np.array(matplotlib.colors.to_rgb(SURFACE))
    fracs = np.linspace(0.38, 1.0, n)
    return [tuple(s + f * (o - s)) for f in fracs]


def _style(ax, title, subtitle=None):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
    ax.tick_params(which="both", colors=MUTED, labelsize=9, length=3)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.set_title(title, loc="left", fontsize=11.5, color=INK, pad=22,
                 fontweight="bold")
    if subtitle:
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=9,
                color=INK2, va="bottom")


def _nu_label(nu):
    m, e = f"{nu:.0e}".split("e")
    return f"$\\nu$ = {m}×10$^{{{int(e)}}}$"


def peak_scaling(visc):
    nus = np.array([r["nu"] for r in visc])
    peaks = np.array([r["wmax"].max() for r in visc])
    slope, icpt = np.polyfit(np.log(nus), np.log(peaks), 1)
    return nus, peaks, slope, icpt


def make_figure(inv, fit, visc, path):
    visc = sorted(visc, key=lambda r: -r["nu"])          # most viscous first
    colors = BLUES[: len(visc)] if len(visc) <= len(BLUES) else \
        [matplotlib.colormaps["Blues"](v) for v in np.linspace(0.35, 0.95, len(visc))]

    fig, axes = plt.subplots(3, 1, figsize=(6.4, 12.6), facecolor=SURFACE,
                             gridspec_kw={"hspace": 0.62})

    # --- A: growth over time ------------------------------------------------
    ax = axes[0]
    for r, c in zip(visc, colors):
        ax.plot(r["t"], r["wmax"], color=c, lw=1.8, label=_nu_label(r["nu"]))
    ax.plot(inv["t"], inv["wmax"], color=ORANGE, lw=2.2, label="$\\nu$ = 0 (no viscosity)")
    ax.plot(inv["t"][-1], inv["wmax"][-1], "o", color=ORANGE, ms=7,
            mec=SURFACE, mew=1.5, zorder=5)
    ax.annotate("grid can't follow it\npast this point",
                (inv["t"][-1], inv["wmax"][-1]), xytext=(-118, 4),
                textcoords="offset points", fontsize=8.5, color=INK2,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax.set_yscale("log")
    ax.set_ylim(0.3, None)
    ax.set_xlim(0, max(r["t"][-1] for r in visc))
    ax.set_xlabel("time", fontsize=9.5, color=INK2)
    ax.set_ylabel("max |ω|  (log scale)", fontsize=9.5, color=INK2)
    _style(ax, "A · Viscosity catches the squeeze",
           "Every viscous run peaks and decays; less viscosity, later and higher peak")
    leg = ax.legend(fontsize=8, frameon=False, loc="lower right", ncol=2,
                    labelcolor=INK2, handlelength=1.6, columnspacing=1.0)

    # --- B: peak height vs viscosity ---------------------------------------
    ax = axes[1]
    nus, peaks, slope, icpt = peak_scaling(visc)
    xx = np.logspace(np.log10(nus.min()) - 0.3, np.log10(nus.max()) + 0.15, 50)
    ax.plot(xx, np.exp(icpt) * xx ** slope, color=MUTED, lw=1.2, ls="--",
            zorder=1)
    for n, p, c in zip(nus, peaks, colors):
        ax.plot(n, p, "o", color=c, ms=9, mec=SURFACE, mew=1.5, zorder=3)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.invert_xaxis()
    ax.set_xlabel("viscosity $\\nu$  (log scale, decreasing →)", fontsize=9.5, color=INK2)
    ax.set_ylabel("peak max |ω|", fontsize=9.5, color=INK2)
    ax.text(0.04, 0.88, f"peak $\\propto$ $\\nu^{{{slope:.2f}}}$", transform=ax.transAxes,
            fontsize=10.5, color=INK)
    ax.yaxis.set_minor_formatter(matplotlib.ticker.FormatStrFormatter("%g"))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%g"))
    _style(ax, "B · Smaller viscosity, higher peak",
           "Straight line on log–log: the peak keeps rising as $\\nu$ → 0, slowly")

    # --- C: the squeeze, inviscid profiles ----------------------------------
    ax = axes[2]
    snaps = inv["snaps"][-5:]
    ramp = _orange_ramp(len(snaps))
    x = inv["x"]
    for s, c in zip(snaps, ramp):
        ax.plot(x, s["omega"], color=c, lw=1.8, label=f"t = {s['t']:.3f}")
    half = 0.06
    ax.set_xlim(-half, half)
    ax.axvline(0, color=AXIS, lw=0.8, zorder=0)
    ax.set_xlabel("position x  (wall of the pipe; x = 0 is the stagnation point)",
                  fontsize=9.5, color=INK2)
    ax.set_ylabel("ω(x)", fontsize=9.5, color=INK2)
    _style(ax, "C · The squeeze, with no viscosity",
           "ω piles into an ever-narrower spike at x = 0")
    ax.legend(fontsize=8, frameon=False, loc="lower left", labelcolor=INK2,
              handlelength=1.6)

    fig.text(0.015, 0.006,
             "1D Hou–Luo model · pseudo-spectral, N = %d · a toy, not the 3D equations"
             % inv["N"], fontsize=7.5, color=MUTED)
    fig.savefig(path, dpi=200, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)
