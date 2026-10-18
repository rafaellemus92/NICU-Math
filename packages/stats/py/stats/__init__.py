"""`stats` — numpy implementation of the shared numeric helpers.

Twin of the TypeScript modules under `sgrounds/lib/piano/*.ts`. The
shared source of truth is `packages/stats/vectors/*.json`; both language
implementations must pass the same vectors to the same tolerance.
"""

from .fft import fft_in_place, ifft_in_place, next_pow2
from .hilbert import (
    analytic_signal,
    instantaneous_amplitude,
    instantaneous_phase,
    onset_density,
    unwrap_phase,
)
from .kuramoto import (
    kuramoto_from_onsets,
    live_frame,
    live_phase_from_onsets,
    order_parameter,
    order_parameter_series,
)

__all__ = [
    "fft_in_place",
    "ifft_in_place",
    "next_pow2",
    "analytic_signal",
    "instantaneous_amplitude",
    "instantaneous_phase",
    "onset_density",
    "unwrap_phase",
    "order_parameter",
    "order_parameter_series",
    "kuramoto_from_onsets",
    "live_frame",
    "live_phase_from_onsets",
]
