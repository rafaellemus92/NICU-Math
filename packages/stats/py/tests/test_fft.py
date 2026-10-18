"""Verify `stats.fft` against the shared JSON vectors.

The TS twin in sgrounds/lib/piano must pass the same cases to the
same tolerance; a disagreement is a bug (or a change that needs
mirroring to the other language).
"""

from __future__ import annotations

import numpy as np
import pytest

from stats.fft import fft_in_place, ifft_in_place, next_pow2

from .conftest import load_vector


@pytest.mark.parametrize("case", load_vector("fft")["cases"],
                         ids=lambda c: c["name"])
def test_fft_matches_shared_vector(case: dict) -> None:
    tol = load_vector("fft")["tolerance"]
    re = np.array(case["input"]["re"], dtype=np.float64)
    im = np.array(case["input"]["im"], dtype=np.float64)
    fft_in_place(re, im)
    exp_re = np.array(case["expected"]["re"], dtype=np.float64)
    exp_im = np.array(case["expected"]["im"], dtype=np.float64)
    assert np.max(np.abs(re - exp_re)) < tol, f"re mismatch: {re} vs {exp_re}"
    assert np.max(np.abs(im - exp_im)) < tol, f"im mismatch: {im} vs {exp_im}"


def test_round_trip_restores_signal() -> None:
    rng = np.random.default_rng(7)
    for n in (4, 8, 16, 64, 256):
        re = rng.standard_normal(n).astype(np.float64)
        orig = re.copy()
        im = np.zeros(n, dtype=np.float64)
        fft_in_place(re, im)
        ifft_in_place(re, im)
        assert np.max(np.abs(re - orig)) < 1e-10
        assert np.max(np.abs(im)) < 1e-10


def test_non_power_of_two_raises() -> None:
    re = np.zeros(5)
    im = np.zeros(5)
    with pytest.raises(ValueError, match=r"power of 2"):
        fft_in_place(re, im)


def test_next_pow2() -> None:
    assert next_pow2(1) == 1
    assert next_pow2(2) == 2
    assert next_pow2(3) == 4
    assert next_pow2(5) == 8
    assert next_pow2(0) == 1
    assert next_pow2(-7) == 1
    assert next_pow2(1024) == 1024
    assert next_pow2(1025) == 2048
