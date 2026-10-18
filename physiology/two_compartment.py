"""Closed-form passive emptying of independent linear compartments.

For each compartment, R_i dV_i/dt + V_i/C_i = DeltaP(t). Initially
DeltaP = P_0 and V_i(0) = C_i P_0. Release to DeltaP = 0 at t = 0
then gives V_i(t) = C_i P_0 exp(-t / (R_i C_i)). V denotes excess
volume relative to the zero-driving-pressure equilibrium baseline,
not absolute resting end-expiratory volume or clinical residual volume.
No shared dynamic chest-wall coupling is assumed.

Equal total compliance and initial pressure imply equal initial total
excess volume, but do not determine the distribution of time constants
or the subsequent trajectory. See two_compartment.md for the derivation.
These are teaching instruments only, not validated for patient care or
prediction for any specific patient. Dependencies: numpy only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

__all__ = ["Compartment", "tau", "passive_retained_fraction",
           "passive_emptying_series"]


def _scalar(value: float, name: str, *, positive: bool = True) -> float:
    """Validate a finite real scalar in the requested physical domain."""
    raw = np.asarray(value)
    if raw.ndim != 0 or raw.dtype.kind not in "iuf":
        raise ValueError(f"{name} must be a finite real scalar")
    value = float(raw)
    if not np.isfinite(value) or value < 0 or (positive and value == 0):
        raise ValueError(f"{name} must be finite and {'positive' if positive else 'nonnegative'}")
    return value


@dataclass(frozen=True)
class Compartment:
    """Constant positive resistance R and compliance C in consistent units.

    R has pressure*time/volume units and C has volume/pressure units.
    Their product must remain finite and strictly positive in float64.
    This passive linear teaching model is not validated for patient care.
    """

    R: float
    C: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "R", _scalar(self.R, "R"))
        object.__setattr__(self, "C", _scalar(self.C, "C"))
        _scalar(self.R * self.C, "R*C")


def tau(compartment: Compartment) -> float:
    """Return the passive relaxation time R*C in the chosen time units."""
    return compartment.R * compartment.C


def _initial_state(compartments: Sequence[Compartment], P_0: float
                   ) -> tuple[np.ndarray, np.ndarray]:
    """Validate a nonempty collection and representable initial volumes."""
    compartments = tuple(compartments)
    if not compartments or any(not isinstance(c, Compartment) for c in compartments):
        raise ValueError("compartments must contain at least one Compartment")
    pressure = _scalar(P_0, "P_0", positive=False)
    compliance = np.array([c.C for c in compartments])
    with np.errstate(over="ignore", under="ignore"):
        initial = compliance * pressure
        total = initial.sum()
    if not np.isfinite(total) or (pressure > 0 and np.any(initial <= 0)):
        raise ValueError("initial volumes and their sum must be finite and representable")
    return initial, np.array([tau(c) for c in compartments])


def passive_emptying_series(compartments: Sequence[Compartment], P_0: float,
                            t_grid: np.ndarray) -> np.ndarray:
    """Return per-compartment excess volumes, shape (n_compartments, n_times).

    Entry [i, j] = C_i P_0 exp(-t_grid[j]/tau_i). Times must form a
    one-dimensional finite nonnegative array; empty, repeated, or unsorted
    times are allowed and retain their order. P_0 must be finite and
    nonnegative. At P_0 = 0 all volumes are zero. Positive initial volumes
    and their sum must be representable; late-time underflow to zero is
    allowed. No numerical ODE solver is used. Not validated for patient care.
    """
    initial, timescales = _initial_state(compartments, P_0)
    times = np.asarray(t_grid)
    if times.ndim != 1 or times.dtype.kind not in "iuf":
        raise ValueError("t_grid must be a one-dimensional real array")
    times = times.astype(float)
    if not np.all(np.isfinite(times)) or np.any(times < 0):
        raise ValueError("t_grid must be finite and nonnegative")
    with np.errstate(over="ignore", under="ignore"):
        return initial[:, None] * np.exp(-times[None, :] / timescales[:, None])


def passive_retained_fraction(compartments: Sequence[Compartment], P_0: float,
                              t: float) -> float:
    """Return sum(V_i(t))/sum(V_i(0)) at one finite nonnegative time.

    P_0 must be strictly positive: for zero pressure the fraction is 0/0
    and raises ValueError, even though the volume series is well defined.
    Positive initial volumes and their sum must be representable. The
    fraction is pressure-independent within this linear model's domain.
    This teaching instrument is not validated for patient care.
    """
    pressure = _scalar(P_0, "P_0")
    time = _scalar(t, "t", positive=False)
    compartments = tuple(compartments)
    initial, _ = _initial_state(compartments, pressure)
    volumes = passive_emptying_series(compartments, pressure, np.array([time]))
    return float(volumes[:, 0].sum() / initial.sum())


def main() -> None:
    """Print float64 approximations and same-formula consistency (R=C=P_0=1)."""
    for name, fractions in (("A", (0.5, 0.5)), ("B", (0.9, 0.1))):
        compartments = [Compartment(2.0, c) for c in fractions]
        expected = (np.exp(-1.0) if name == "A" else
                    0.9 * np.exp(-1.0 / 1.8) + 0.1 * np.exp(-5.0))
        retained = passive_retained_fraction(compartments, 1.0, 1.0)
        print(f"{name}: retained={retained:.17g}; formula-consistency discrepancy={abs(retained - expected):.3e}")


if __name__ == "__main__":
    main()
