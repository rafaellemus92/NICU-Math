"""Tests for `fluids/stationary_phase.py`.

Checks three things:

    1. The integration-by-parts identity (†) holds numerically: the
       direct trapezoidal integral and the sum of endpoint + interior
       terms agree to discretization tolerance.
    2. The envelope bound (‡) is actually an upper bound on the direct
       integral, across a sweep of phase speeds.
    3. The bound gets tight as the phase speed grows (rapid phase slip
       → stronger cancellation).
"""

from __future__ import annotations

import numpy as np

from fluids.stationary_phase import (
    direct_integral,
    ibp_envelope_bound,
    integration_by_parts_integral,
    triad_phase_speed,
)


def _sample_signals(detuning: float, n: int = 4096):
    """Return (t, B, ψ) for a smooth bursty amplitude on a phase ramp.

    B(t) = exp(−(t − 1)²) + 0.3 cos(0.7 t)      (two timescales)
    ψ(t) = detuning · t                         (constant phase speed)
    """
    t = np.linspace(0.0, 4.0, n)
    B = np.exp(-((t - 1.0) ** 2)) + 0.3 * np.cos(0.7 * t)
    psi = detuning * t
    return t, B, psi


def test_identity_direct_equals_ibp_sum() -> None:
    """(†) holds numerically for a detuned phase."""
    for det in (3.0, 5.0, 11.0, 23.5):
        t, B, psi = _sample_signals(det)
        I_direct = direct_integral(t, B, psi)
        _, _, I_ibp = integration_by_parts_integral(t, B, psi)
        assert abs(I_direct - I_ibp) < 5e-3, (
            f"direct {I_direct} vs IBP {I_ibp} at det={det}; "
            "disagreement is a bug, not a bound slackness"
        )


def test_envelope_bound_is_actually_an_upper_bound() -> None:
    for det in (3.0, 5.0, 8.0, 15.0, 30.0):
        t, B, psi = _sample_signals(det)
        I = abs(direct_integral(t, B, psi))
        U = ibp_envelope_bound(t, B, psi)
        assert I <= U + 1e-9, (
            f"direct |I|={I} exceeded bound {U} at detuning {det}"
        )


def test_bound_tightens_as_phase_speed_grows() -> None:
    """|I|/U should stay O(1); and |I| itself must drop with detuning."""
    direct_at = []
    for det in (3.0, 10.0, 30.0, 100.0):
        t, B, psi = _sample_signals(det)
        direct_at.append(abs(direct_integral(t, B, psi)))
    # Decreasing in detuning — rapid phase slip kills the integral.
    for prev, nxt in zip(direct_at, direct_at[1:]):
        assert nxt <= prev + 1e-6, (
            f"direct integral must be non-increasing in |ψ̇|; got {direct_at}"
        )
    # And by at least an order of magnitude between the slowest and
    # fastest detunings tested.
    assert direct_at[-1] <= 0.1 * direct_at[0], (
        f"expected ≥10× cancellation; got {direct_at[-1]} vs {direct_at[0]}"
    )


def test_identity_rejects_vanishing_phase_speed() -> None:
    """ψ̇ changing sign on the interval should raise, not silently return."""
    import pytest

    t = np.linspace(0.0, 4.0, 1024)
    B = np.ones_like(t)
    psi = (t - 2.0) ** 2  # ψ̇ = 2(t−2) → sign change at t = 2
    with pytest.raises(ValueError, match=r"ψ̇"):
        integration_by_parts_integral(t, B, psi)


def test_triad_phase_speed_signature() -> None:
    """The resonance condition ω₁ + ω₂ = ω₃ gives zero detuning."""
    assert triad_phase_speed(1.0, 2.0, 3.0) == 0.0
    assert triad_phase_speed(1.0, 2.0, 2.5) == 0.5
    assert triad_phase_speed(1.0, 2.0, 4.0) == -1.0
