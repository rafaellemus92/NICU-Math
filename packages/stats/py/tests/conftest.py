"""Pytest collection root for the stats package. No fixtures here beyond
the one path helper every test module reuses."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest


VECTORS_DIR = Path(__file__).resolve().parents[2] / "vectors"


@pytest.fixture(scope="session")
def vectors_dir() -> Path:
    assert VECTORS_DIR.is_dir(), f"shared vectors dir missing: {VECTORS_DIR}"
    return VECTORS_DIR


def load_vector(name: str) -> dict:
    """Load one shared JSON vector by filename stem (e.g. 'kuramoto')."""
    path = VECTORS_DIR / f"{name}.json"
    with path.open() as f:
        return json.load(f)


def build_signal(spec: dict) -> np.ndarray:
    """Build an input signal from a formula spec in a hilbert vector case.

    The vector file describes signals by formula (not by listing N floats
    each) so the TS twin can construct the identical input. Supported
    formulas: 'cosine', 'zeros'.
    """
    formula = spec["signal_formula"]
    n = int(spec["N"])
    if formula == "cosine":
        k = int(spec["k"])
        A = float(spec.get("A", 1.0))
        idx = np.arange(n)
        return A * np.cos(2 * np.pi * k * idx / n)
    if formula == "zeros":
        return np.zeros(n, dtype=np.float64)
    raise ValueError(f"unknown signal_formula: {formula!r}")
