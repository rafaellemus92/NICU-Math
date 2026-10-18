"""Analytic signal, instantaneous phase/amplitude, phase unwrapping,
and Gaussian-smoothed onset density.

Twin of `sgrounds/lib/piano/hilbert.ts`. The analytic signal of a real
input x is  x + i·H{x}  where H is the Hilbert transform; the standard
FFT-based construction:

    1. X[k] = FFT(x)
    2. Multiply by  h = [1, 2, 2, ..., 2, 1, 0, 0, ..., 0]
       (h[0] = 1, h[N/2] = 1 for even N, h[1..N/2-1] = 2)
    3. z = IFFT(h · X)

See `packages/stats/vectors/hilbert.json` for the shared test cases.
"""

from __future__ import annotations

import numpy as np

from .fft import fft_in_place, ifft_in_place, next_pow2

__all__ = [
    "analytic_signal",
    "instantaneous_phase",
    "instantaneous_amplitude",
    "onset_density",
    "unwrap_phase",
]


def analytic_signal(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return (real, imag) parts of the analytic signal, length len(x)."""
    x = np.asarray(x, dtype=np.float64).ravel()
    n_orig = x.size
    if n_orig == 0:
        return np.zeros(0), np.zeros(0)
    n = next_pow2(n_orig)
    re = np.zeros(n, dtype=np.float64)
    im = np.zeros(n, dtype=np.float64)
    re[:n_orig] = x

    fft_in_place(re, im)

    # Apply Hilbert multiplier.
    half = n >> 1
    # k = 0: leave as-is.
    re[1:half] *= 2.0
    im[1:half] *= 2.0
    # k = n/2 (Nyquist): leave as-is for even n.
    re[half + 1:] = 0.0
    im[half + 1:] = 0.0

    ifft_in_place(re, im)
    return re[:n_orig].copy(), im[:n_orig].copy()


def instantaneous_phase(x: np.ndarray) -> np.ndarray:
    """Per-sample phase in radians, wrapped to (−π, π]."""
    re, im = analytic_signal(x)
    return np.arctan2(im, re)


def instantaneous_amplitude(x: np.ndarray) -> np.ndarray:
    """Per-sample envelope magnitude."""
    re, im = analytic_signal(x)
    return np.hypot(re, im)


def unwrap_phase(phase: np.ndarray) -> np.ndarray:
    """Remove 2π discontinuities, for plotting (not for the order parameter)."""
    phase = np.asarray(phase, dtype=np.float64).ravel()
    if phase.size == 0:
        return phase.copy()
    out = np.empty_like(phase)
    out[0] = phase[0]
    offset = 0.0
    for i in range(1, phase.size):
        diff = phase[i] - phase[i - 1]
        if diff > np.pi:
            offset -= 2 * np.pi
        elif diff < -np.pi:
            offset += 2 * np.pi
        out[i] = phase[i] + offset
    return out


def onset_density(
    onsets: np.ndarray,
    t_max: float,
    dt: float,
    sigma: float,
) -> np.ndarray:
    """Smoothed spike train on a uniform time grid.

        density(t) = Σᵢ (1 / (σ√(2π))) · exp(−(t − tᵢ)² / (2σ²))

    Mean-subtracted before return so the Hilbert transform gets a
    zero-mean input (DC otherwise swamps the phase estimate).

    `sigma` is in the same time units as the onsets (seconds, usually).
    Kernel truncated at 4σ for speed.
    """
    if t_max <= 0 or dt <= 0:
        return np.zeros(0, dtype=np.float64)
    n_samples = max(2, int(np.ceil(t_max / dt)))
    out = np.zeros(n_samples, dtype=np.float64)
    onsets = np.asarray(onsets, dtype=np.float64).ravel()
    if onsets.size == 0:
        return out

    norm = 1.0 / (sigma * np.sqrt(2 * np.pi))
    two_sig2 = 2 * sigma * sigma
    half_width = int(np.ceil(4 * sigma / dt))

    for tk in onsets:
        center = int(round(tk / dt))
        lo = max(0, center - half_width)
        hi = min(n_samples - 1, center + half_width)
        if lo > hi:
            continue
        idx = np.arange(lo, hi + 1)
        dts = idx * dt - tk
        out[lo:hi + 1] += norm * np.exp(-(dts * dts) / two_sig2)

    out -= out.mean()
    return out
