"""Verify the φ-family claim from `fluids/exact/phi_family.py`.

Four separate assertions, each tracking a distinct part of the claim:

    1. ∇·u = 0 identically  (within spectral precision)
    2. E = E(φ)             is φ-independent
    3. H ≡ 0                for every φ
    4. S(φ) = ¼ cos φ       for every φ

Together they establish the ledger entry: two members of the family
can share E and H yet differ in current stretching S, so the reduced
state (E, H) does not determine the dynamics even in sign.
"""

from __future__ import annotations

import numpy as np
import pytest

from fluids.exact.phi_family import (
    mean_abs_divergence,
    mean_energy,
    mean_helicity,
    mean_stretching,
    sweep_phi,
    velocity,
    velocity_gradient,
    vorticity,
)

PHIS = np.linspace(0.0, 2 * np.pi, 13)
# Spectral differentiation of trig polynomials on a 2π grid is exact
# modulo floating-point roundoff. Allow a very tight tolerance.
TOL = 1e-12


# ─── 1. divergence-free ─────────────────────────────────────────────────

@pytest.mark.parametrize("phi", PHIS)
def test_divergence_free(phi: float) -> None:
    u = velocity(phi, n=32)
    residual = mean_abs_divergence(u)
    assert residual < TOL, f"∇·u ≠ 0 at φ={phi:.3f}: residual={residual}"


# ─── 2. energy is phi-independent ───────────────────────────────────────

def test_energy_is_phi_independent() -> None:
    data = sweep_phi(PHIS, n=32)
    E = data["E"]
    assert np.max(np.abs(E - E[0])) < TOL, f"E varies with φ: {E}"


# ─── 3. total helicity is zero for every phi ────────────────────────────

@pytest.mark.parametrize("phi", PHIS)
def test_helicity_zero(phi: float) -> None:
    u = velocity(phi, n=32)
    G = velocity_gradient(u)
    w = vorticity(u, G=G)
    H = mean_helicity(u, w)
    assert abs(H) < TOL, f"⟨u·ω⟩ ≠ 0 at φ={phi:.3f}: H={H}"


# ─── 4. stretching matches ¼ cos φ ──────────────────────────────────────

@pytest.mark.parametrize("phi", PHIS)
def test_stretching_matches_quarter_cos(phi: float) -> None:
    u = velocity(phi, n=32)
    G = velocity_gradient(u)
    w = vorticity(u, G=G)
    S = mean_stretching(w, G)
    expected = 0.25 * np.cos(phi)
    assert abs(S - expected) < TOL, (
        f"S(φ={phi:.3f}) = {S}, expected {expected} (|Δ| = {abs(S-expected)})"
    )


# ─── 5. the convergence-thesis consequence ──────────────────────────────

def test_phi_zero_and_phi_pi_share_E_and_H_but_differ_in_S() -> None:
    """The headline claim written out as a single assertion."""
    u0 = velocity(0.0, n=32)
    up = velocity(np.pi, n=32)
    G0 = velocity_gradient(u0)
    Gp = velocity_gradient(up)
    w0 = vorticity(u0, G=G0)
    wp = vorticity(up, G=Gp)

    E0, Ep = mean_energy(u0), mean_energy(up)
    H0, Hp = mean_helicity(u0, w0), mean_helicity(up, wp)
    S0, Sp = mean_stretching(w0, G0), mean_stretching(wp, Gp)

    assert abs(E0 - Ep) < TOL,  f"E differs: {E0} vs {Ep}"
    assert abs(H0) < TOL and abs(Hp) < TOL,  f"H nonzero: {H0}, {Hp}"
    assert abs(S0 - 0.25) < TOL,   f"S(0) should be +¼: got {S0}"
    assert abs(Sp - (-0.25)) < TOL, f"S(π) should be −¼: got {Sp}"
    # And therefore:
    assert abs(S0 - Sp) > 0.49, (
        f"S differs between φ=0 and φ=π by {abs(S0 - Sp):.3f}; "
        "if this ever fails, the central claim is wrong."
    )
