# fluids/CLAIMS.md — the ledger

Every claim in `fluids/` lives in exactly one tier below. Nothing
merges without a tier assignment. See [`../RESEARCH.md`](../RESEARCH.md)
§3 for the tier definitions.

---

## Mathematical results

*(Statements with proof, assumptions, and boundary cases. Point to
the reference or the file carrying the proof.)*

- *(none yet; file them here with proof as new work lands)*

## Exact computations

*(Deterministic scripts whose output verifies the claim. Each entry:
one-line claim, script path, test path, commit SHA where it last
passed.)*

- **The φ-family of divergence-free periodic flows u^φ = (sin y,
  sin z, cos x − cos(x+y+φ)) is divergence-free, has φ-independent
  mean energy E, has zero total mean helicity H for every φ, and has
  mean vortex stretching S(φ) = ¼ cos φ.** Two members of the family
  (u^0 and u^π) therefore share identical Fourier magnitudes, energy,
  and total helicity but differ in current stretching by ½. The
  reduced state (E, H) does not determine even the sign of S. Script:
  [`exact/phi_family.py`](exact/phi_family.py). Test:
  [`tests/fluids/test_phi_family.py`](../tests/fluids/test_phi_family.py).
  Verified at machine precision on a 32³ spectral grid:
  `max |S − ¼ cos φ| ≈ 1.1 × 10⁻¹⁶`, `max |H| ≈ 1.4 × 10⁻¹⁶`,
  `max |E − E(0)| = 0`, `max |∇·u| = 0`.

- **Integration-by-parts cancellation for oscillatory contributions:**
  For a signal B(t) cos ψ(t) on an interval where ψ̇ stays bounded
  away from zero,
  `|∫ B cos ψ dt| ≤ (|B(a)|+|B(b)|)·sup|1/ψ̇| + ∫|d/dt(B/ψ̇)| dt`.
  Encoded as `fluids/stationary_phase.py`; verified numerically that
  the direct integral and the integration-by-parts expansion agree,
  that the envelope bound is actually an upper bound, and that rapid
  phase slip (large |ψ̇|) drives the integral toward zero at least
  linearly. Tests:
  [`tests/fluids/test_stationary_phase.py`](../tests/fluids/test_stationary_phase.py).
  The near-locking case (`ψ̇ → 0`) is where any proof targeting the
  full triad sum (★) has to do its work — the helper raises
  `ValueError` when ψ̇ changes sign so this isn't silently masked.

## Numerical evidence

*(Each entry: pre-registered hypothesis, path to plan.md, path to
results, preserved outcome regardless of sign.)*

- *(none yet; pre-register in `numerical/<slug>/plan.md` before running)*

## Proposed mechanisms

*(One paragraph each; name what would make it testable.)*

- **Phase organization among triadic interactions is the mechanism
  controlling accumulation of vortex stretching, not amplitudes
  alone.** Testable by (i) exact constructions showing that identical
  Fourier magnitudes can produce different Ṡ, and (ii) numerical
  studies measuring whether specific triad-phase features add
  predictive power over spectrum-and-current-stretching baselines on
  held-out flows.

- **Persistent favorable phase alignment among the small subset of
  helical triads carrying the energy flux (per Kang–Protas–Bustamante
  2021, [arXiv:2105.09425](https://arxiv.org/abs/2105.09425)) sustains
  stretching bursts; sufficiently rapid phase drift forces
  stationary-phase cancellation.** Testable by tracking amplitude-
  weighted triad phases during stretching bursts and quantifying
  persistence length. Mathematical route: a stationary-phase /
  integration-by-parts bound on ∫ B cos Ψ dt in intervals where Ψ̇
  stays bounded away from zero.

- **DNA ribbon topology (Călugăreanu–White–Fuller Lk = Tw + Wr) and
  Moffatt vortex-tube helicity share topological invariants, which
  suggests geometric diagnostics (writhe-like measures on vorticity
  tubes) worth tracking alongside algebraic ones.** Testable by
  constructing a tube-geometry diagnostic for simulated flows and
  checking whether it adds predictive value for stretching bursts
  beyond the helical-triad diagnostics.

## Contradicted / unresolved

*(Negative results preserved; superseded claims kept with their
superseding SHA. Never deleted.)*

- *(none yet)*

---

## Convention

When a claim moves tiers (e.g., a proposed mechanism becomes an exact
computation), **move the line, don't duplicate it.** Reference the PR
that moved it in the commit message.

When a claim is contradicted, move it to **Contradicted / unresolved**
with a one-line note on what showed it wrong, and link the superseding
work.
