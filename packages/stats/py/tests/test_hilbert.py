"""Verify `stats.hilbert` against the shared JSON vectors."""

from __future__ import annotations

import numpy as np
import pytest

from stats.hilbert import (
    analytic_signal,
    instantaneous_amplitude,
    instantaneous_phase,
    onset_density,
    unwrap_phase,
)

from .conftest import build_signal, load_vector


HILBERT_CASES = load_vector("hilbert")["cases"]
DEFAULT_TOL = load_vector("hilbert")["tolerance"]


def _closed_form_cosine(spec: dict) -> tuple[np.ndarray, np.ndarray]:
    """(cos, sin) at the grid points for a cosine spec."""
    n = int(spec["N"])
    k = int(spec["k"])
    A = float(spec.get("A", 1.0))
    idx = np.arange(n)
    arg = 2 * np.pi * k * idx / n
    return A * np.cos(arg), A * np.sin(arg)


def _run_analytic_signal(case: dict) -> None:
    sig = build_signal(case["input"])
    re, im = analytic_signal(sig)
    cos_expected, sin_expected = _closed_form_cosine(case["input"])
    trim = int(case["expected"].get("trim_edges", 0))
    tol = float(case["expected"].get("tolerance", DEFAULT_TOL))
    if trim > 0:
        re = re[trim:-trim]
        im = im[trim:-trim]
        cos_expected = cos_expected[trim:-trim]
        sin_expected = sin_expected[trim:-trim]
    assert np.max(np.abs(re - cos_expected)) < max(tol, 0.05), (
        f"real part mismatch (case {case['name']})"
    )
    assert np.max(np.abs(im - sin_expected)) < max(tol, 0.05), (
        f"imag part mismatch (case {case['name']})"
    )


def _run_instantaneous_amplitude(case: dict) -> None:
    sig = build_signal(case["input"])
    amp = instantaneous_amplitude(sig)
    trim = int(case["expected"].get("trim_edges", 0))
    core = amp[trim:len(amp) - trim] if trim > 0 else amp
    expected_mean = float(case["expected"]["amplitude_mean"])
    tol = float(case["expected"]["tolerance"])
    if core.size == 0:
        assert expected_mean == 0.0
        return
    assert abs(float(np.mean(core)) - expected_mean) < tol, (
        f"amplitude mean mismatch (case {case['name']})"
    )


def _run_unwrap_phase(case: dict) -> None:
    wrapped = np.array(case["input"]["wrapped_phase"], dtype=np.float64)
    expected = np.array(case["expected"]["unwrapped"], dtype=np.float64)
    tol = float(case["expected"]["tolerance"])
    assert np.max(np.abs(unwrap_phase(wrapped) - expected)) < tol


def _run_onset_density(case: dict) -> None:
    i = case["input"]
    density = onset_density(
        np.array(i["onsets"], dtype=np.float64),
        float(i["t_max"]),
        float(i["dt"]),
        float(i["sigma"]),
    )
    e = case["expected"]
    peak_idx = int(np.argmax(density))
    assert e["peak_index_min"] <= peak_idx <= e["peak_index_max"], (
        f"onset-density peak at idx {peak_idx}, expected in "
        f"[{e['peak_index_min']}, {e['peak_index_max']}]"
    )
    assert abs(float(np.mean(density))) < float(e["mean_abs_tol"])


RUNNERS = {
    "analytic_signal": _run_analytic_signal,
    "instantaneous_amplitude": _run_instantaneous_amplitude,
    "unwrap_phase": _run_unwrap_phase,
    "onset_density": _run_onset_density,
}


@pytest.mark.parametrize("case", HILBERT_CASES, ids=lambda c: c["name"])
def test_hilbert_matches_shared_vector(case: dict) -> None:
    fn = case["function"]
    runner = RUNNERS.get(fn)
    assert runner is not None, f"no test runner for hilbert function {fn!r}"
    runner(case)


# ─── A few free-form properties that complement the shared vectors ──────

def test_analytic_signal_envelope_of_pure_cosine_is_one() -> None:
    n = 256
    k = 5
    x = np.cos(2 * np.pi * k * np.arange(n) / n)
    amp = instantaneous_amplitude(x)
    core = amp[32:-32]
    assert abs(float(np.mean(core)) - 1.0) < 1e-2
    assert float(np.std(core)) < 1e-2


def test_instantaneous_phase_matches_closed_form_cosine() -> None:
    n = 256
    k = 4
    idx = np.arange(n)
    x = np.cos(2 * np.pi * k * idx / n)
    phase = instantaneous_phase(x)
    truth = 2 * np.pi * k * idx / n
    # Compare modulo 2π: both are wrapped to (−π, π], but at the branch cut
    # one may read +π while the other reads −π — same phase, different
    # representatives. `(diff + π) mod 2π − π` collapses that ambiguity.
    diff = np.mod(phase - truth + np.pi, 2 * np.pi) - np.pi
    core = slice(32, -32)
    assert np.max(np.abs(diff[core])) < 1e-2
