"""Integration-by-parts cancellation for oscillatory contributions.

The question `fluids/CLAIMS.md` surfaces is: can a sum like

                      N
    S(t)  =  Σ   B_τ(t) · cos Ψ_τ(t)                                 (★)
                 τ=1

be bounded in time **by its phase organization alone**, independently
of how large the individual amplitudes |B_τ| grow? For a single term
with non-vanishing phase speed, the answer is yes, and the identity
that makes it work is standard integration by parts:

    ∫_a^b B cos Ψ dt
       = [ B sin Ψ / Ψ̇ ]_a^b
         − ∫_a^b  (d/dt (B / Ψ̇))  ·  sin Ψ  dt .                     (†)

When Ψ̇ never vanishes on [a, b], (†) gives

    | ∫_a^b B cos Ψ dt |
       ≤ (|B(a)| + |B(b)|) · sup |1/Ψ̇|
         + ∫_a^b | d/dt (B / Ψ̇) | dt .                                (‡)

Reading (‡): a bursty amplitude B can be large on intervals where Ψ
rotates fast enough that B/Ψ̇ varies slowly — the right side stays
controlled. The hard cases, as `fluids/CLAIMS.md` notes, are the
*near-locking* intervals where Ψ̇ approaches zero; those are where any
proof targeting (★) has to do its work. This module encodes (†) and
(‡) as directly runnable numerics so claims about the right-hand side
can be verified against the left-hand side on example signals.

Dependencies: numpy only.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "direct_integral",
    "integration_by_parts_integral",
    "ibp_envelope_bound",
    "triad_phase_speed",
]


# ─── Direct and IBP evaluations ─────────────────────────────────────────

def direct_integral(t: np.ndarray, B: np.ndarray, psi: np.ndarray) -> float:
    """Compute  ∫ B(t) · cos ψ(t) dt  on [t[0], t[-1]] by trapezoid.

    Reference evaluation; this is the left-hand side of (†).
    """
    return float(np.trapezoid(B * np.cos(psi), t))


def integration_by_parts_integral(
    t: np.ndarray, B: np.ndarray, psi: np.ndarray,
) -> tuple[float, float, float]:
    """Compute the right-hand side of identity (†) term-by-term.

    Returns (endpoint_term, interior_term, total)
    where
        endpoint_term = [B sin ψ / ψ̇]_a^b
        interior_term = − ∫ (d/dt (B / ψ̇)) · sin ψ dt
        total         = endpoint_term + interior_term

    `total` must equal `direct_integral(t, B, psi)` up to the
    discretization error of the finite-difference derivatives and the
    trapezoid rule. Any disagreement reveals a bug.

    Raises `ValueError` if ψ̇ changes sign on the interval; the
    identity is only usable where ψ̇ stays away from zero.
    """
    psi_dot = np.gradient(psi, t)
    if np.any(psi_dot == 0) or (np.min(psi_dot) * np.max(psi_dot) < 0):
        raise ValueError(
            "ψ̇ changes sign (or vanishes) on the interval; the "
            "stationary-phase identity requires ψ̇ bounded away from zero. "
            "Split the interval at the stationary points first."
        )

    # Endpoint term [B sin ψ / ψ̇]_a^b.
    endpoint = (B[-1] * np.sin(psi[-1]) / psi_dot[-1]
                - B[0] * np.sin(psi[0]) / psi_dot[0])

    # Interior term: − ∫ d/dt(B/ψ̇) · sin ψ dt.
    quotient = B / psi_dot
    dquotient = np.gradient(quotient, t)
    interior = -float(np.trapezoid(dquotient * np.sin(psi), t))

    return float(endpoint), interior, float(endpoint) + interior


# ─── Envelope bound (‡) ─────────────────────────────────────────────────

def ibp_envelope_bound(
    t: np.ndarray, B: np.ndarray, psi: np.ndarray,
) -> float:
    """Upper bound  |∫ B cos ψ dt|  via (‡).

    Returns the right-hand side of

        | ∫ B cos ψ dt | ≤ (|B(a)| + |B(b)|) · sup |1/ψ̇|
                             + ∫ | d/dt (B/ψ̇) | dt .

    When ψ̇ varies little, this bound is tight; when ψ̇ nearly
    stationaries, the bound inflates. Both regimes are visible if
    the caller sweeps a parameter that detunes the phase speed.
    """
    psi_dot = np.gradient(psi, t)
    if np.min(np.abs(psi_dot)) <= 0:
        return float("inf")
    inv_psi_dot = 1.0 / psi_dot
    endpoint = (abs(B[0]) + abs(B[-1])) * float(np.max(np.abs(inv_psi_dot)))
    dquotient = np.gradient(B * inv_psi_dot, t)
    interior = float(np.trapezoid(np.abs(dquotient), t))
    return endpoint + interior


# ─── Convenience: triad phase speed ─────────────────────────────────────

def triad_phase_speed(
    omega_1: float, omega_2: float, omega_3: float,
) -> float:
    """Phase speed of a triadic combination  ψ(t) = (ω_1 + ω_2 − ω_3) t.

    For a resonant triad with wavenumbers k_1 + k_2 + k_3 = 0 and
    characteristic frequencies ω_j, this is the natural detuning that
    enters (★). A small detuning is a locking candidate; large detuning
    is where (‡) earns its keep.

    Returned as a plain float; the caller usually builds `psi` as
    `(w1 + w2 - w3) * t + phi_offset`.
    """
    return float(omega_1 + omega_2 - omega_3)
