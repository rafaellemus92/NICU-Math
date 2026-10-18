"""Verify `stats.kuramoto` against the shared JSON vectors."""

from __future__ import annotations

import math

import numpy as np
import pytest

from stats.kuramoto import (
    kuramoto_from_onsets,
    live_frame,
    live_phase_from_onsets,
    order_parameter,
    order_parameter_series,
)

from .conftest import load_vector


KURAMOTO_CASES = load_vector("kuramoto")["cases"]
DEFAULT_TOL = load_vector("kuramoto")["tolerance"]


def _parse_phase(x) -> float:
    """Accept the string 'NaN' in the JSON vector."""
    if isinstance(x, str) and x.lower() == "nan":
        return math.nan
    return float(x)


@pytest.mark.parametrize("case", KURAMOTO_CASES, ids=lambda c: c["name"])
def test_order_parameter_matches_shared_vector(case: dict) -> None:
    phases = [_parse_phase(p) for p in case["input"]["phases"]]
    r, mp = order_parameter(phases)
    expected = case["expected"]
    assert abs(r - float(expected["r"])) < DEFAULT_TOL, (
        f"r mismatch: got {r}, expected {expected['r']}"
    )
    if expected["mean_phase_matters"]:
        assert abs(mp - float(expected["mean_phase"])) < DEFAULT_TOL, (
            f"mean_phase mismatch: got {mp}, expected {expected['mean_phase']}"
        )


# ─── Properties and the live/batch helpers ──────────────────────────────

def test_order_parameter_series_two_drifting_oscillators() -> None:
    n = 200
    p1 = np.mod(0.10 * np.arange(n), 2 * np.pi)
    p2 = np.mod(0.12 * np.arange(n), 2 * np.pi)
    frames = order_parameter_series([p1, p2], dt=0.01, t_start=0.0)
    assert len(frames) == n
    rs = np.array([f.r for f in frames])
    assert rs.max() > 0.95, "two detuned oscillators should transiently lock"
    assert rs.min() < 0.10, "two detuned oscillators should also antiphase"


def test_kuramoto_from_onsets_identical_trains_lock() -> None:
    onsets = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
    frames = kuramoto_from_onsets([onsets, onsets], t_max=4.0, dt=0.02,
                                  sigma=0.08)
    rs = np.array([f.r for f in frames[20:-20]])
    assert rs.mean() > 0.9


def test_kuramoto_from_onsets_antiphase_decouples() -> None:
    in_phase = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
    anti = in_phase + 0.25
    frames = kuramoto_from_onsets([in_phase, anti], t_max=4.0, dt=0.02,
                                  sigma=0.08)
    rs = np.array([f.r for f in frames[20:-20]])
    assert rs.mean() < 0.5


def test_live_phase_from_onsets_edge_cases() -> None:
    # Fewer than min_onsets in the window → NaN.
    assert math.isnan(live_phase_from_onsets(np.array([0.1]), now=5.0))
    # Onsets outside the window → NaN.
    assert math.isnan(live_phase_from_onsets(np.array([0.0, 0.1]), now=10.0))
    # Enough onsets inside → finite.
    onsets = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
    phase = live_phase_from_onsets(onsets, now=5.2)
    assert math.isfinite(phase)


def test_live_frame_r_is_one_when_phases_identical() -> None:
    f = live_frame(1.2, 1.2, t=5.0)
    assert abs(f.r - 1.0) < 1e-12
    assert f.t == 5.0


def test_order_parameter_series_length_mismatch_raises() -> None:
    with pytest.raises(ValueError, match="length mismatch"):
        order_parameter_series(
            [np.zeros(10, dtype=np.float64), np.zeros(9, dtype=np.float64)],
            dt=0.01,
        )
