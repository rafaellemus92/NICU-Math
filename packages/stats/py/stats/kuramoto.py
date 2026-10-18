"""Kuramoto order parameter and live-phasor helpers.

Twin of `sgrounds/lib/piano/kuramoto.ts`. For N oscillators with
instantaneous phases θⱼ:

    z(t) = (1/N) · Σⱼ exp(i θⱼ(t))
    r(t) = |z(t)|          ∈ [0, 1]      (phase-locking strength)
    ψ(t) = arg(z(t))                      (mean phase)

Non-finite phases are treated as "oscillator has no data yet" and
skipped, so `order_parameter` on a short window with one or more hands
silent still returns a sensible number for the hands that are active.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .hilbert import instantaneous_phase, onset_density

__all__ = [
    "KuramotoFrame",
    "order_parameter",
    "order_parameter_series",
    "kuramoto_from_onsets",
    "live_frame",
    "live_phase_from_onsets",
]


@dataclass
class KuramotoFrame:
    t: float
    r: float
    mean_phase: float
    phase_lh: float
    phase_rh: float


def order_parameter(phases) -> tuple[float, float]:
    """Single-frame (r, mean_phase). Non-finite entries are skipped."""
    arr = np.asarray(phases, dtype=np.float64).ravel()
    mask = np.isfinite(arr)
    n = int(mask.sum())
    if n == 0:
        return 0.0, 0.0
    good = arr[mask]
    c_mean = float(np.mean(np.cos(good)))
    s_mean = float(np.mean(np.sin(good)))
    r = float(np.hypot(c_mean, s_mean))
    mean_phase = float(np.arctan2(s_mean, c_mean))
    return r, mean_phase


def order_parameter_series(
    phases: list[np.ndarray],
    dt: float,
    t_start: float = 0.0,
) -> list[KuramotoFrame]:
    """Frame-by-frame r(t) from N parallel phase time series.

    All input series must share length. Returns `len` frames.
    """
    if not phases:
        return []
    n = phases[0].size
    for p in phases:
        if p.size != n:
            raise ValueError("order_parameter_series: length mismatch")
    phases = [np.asarray(p, dtype=np.float64) for p in phases]
    frames: list[KuramotoFrame] = []
    for i in range(n):
        snapshot = np.array([p[i] for p in phases], dtype=np.float64)
        r, mp = order_parameter(snapshot)
        frames.append(KuramotoFrame(
            t=t_start + i * dt,
            r=r,
            mean_phase=mp,
            phase_lh=phases[0][i] if len(phases) > 0 else 0.0,
            phase_rh=phases[1][i] if len(phases) > 1 else 0.0,
        ))
    return frames


def kuramoto_from_onsets(
    onsets_by_hand: list[np.ndarray],
    t_max: float,
    dt: float,
    sigma: float,
) -> list[KuramotoFrame]:
    """Build r(t) end-to-end: onset density → Hilbert phase → order parameter."""
    if t_max <= 0:
        return []
    phases = [instantaneous_phase(onset_density(o, t_max, dt, sigma))
              for o in onsets_by_hand]
    return order_parameter_series(phases, dt, 0.0)


def live_frame(phase_lh: float, phase_rh: float, t: float) -> KuramotoFrame:
    """Instantaneous frame from two live phases."""
    r, mp = order_parameter([phase_lh, phase_rh])
    return KuramotoFrame(t=t, r=r, mean_phase=mp,
                         phase_lh=phase_lh, phase_rh=phase_rh)


def live_phase_from_onsets(
    onsets: np.ndarray,
    now: float,
    window_sec: float = 4.0,
    dt: float = 0.025,
    sigma: float = 0.1,
    margin_sec: float = 0.5,
    min_onsets: int = 2,
) -> float:
    """Phase of a sliding Hilbert window.

    See the TS twin for rationale; reports phase at `window_sec − margin_sec`
    into the window so endpoint Hilbert artifacts don't dominate. Returns
    NaN when fewer than `min_onsets` onsets fall in the window.
    """
    window_start = now - window_sec
    onsets = np.asarray(onsets, dtype=np.float64).ravel()
    inside = onsets[(onsets >= window_start) & (onsets <= now)] - window_start
    if inside.size < min_onsets:
        return float("nan")
    density = onset_density(inside, window_sec, dt, sigma)
    phases = instantaneous_phase(density)
    idx = max(0, min(phases.size - 1,
                     int(round((window_sec - margin_sec) / dt))))
    return float(phases[idx])
