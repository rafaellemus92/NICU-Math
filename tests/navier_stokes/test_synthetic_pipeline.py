"""Synthetic count/timing regressions; these are not clinical validation."""
import numpy as np
import pytest

from navier_stokes.ventilator_ingest import generate_synthetic_waveform, segment_breaths


@pytest.mark.parametrize('noise', [0.0, 0.05])
def test_reported_50_breath_regression(noise):
    recording = generate_synthetic_waveform(n_breaths=50, compliance=1.0,
                                            noise_level=noise, seed=42)
    cycles = segment_breaths(recording)
    assert len(cycles) == 50
