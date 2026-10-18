# Fluid/respiratory claim correction ledger

Scope: corrections to `navier_stokes/` and the corresponding web presentation,
not a reassessment of unrelated research. Original source is preserved at commit
`ab448aaa429bf3bc3c4c5bc2a41b5be6778e1f28`. Superseding implementation commit:
`745e846634033478beadda96da27951660d93678` (with a subsequent input-handling
review fix on this branch). See [derivations and assumptions](README.md).

## Motivation and incomplete conjecture

Respiratory mechanics motivates questions about geometry, surface tension and
distributed dynamics. A model-specific continuation theorem would require a
specified PDE and solution class, boundary/initial compatibility, controlled
geometry, and actual vortex-stretching estimates. Those gaps remain. No claimed
clinical-to-PDE equivalence or conditional regularity result is established here.

## Analytical identities / teaching results

- A smooth incompressible closed material domain conserves volume; a material
  sphere with positive radius cannot shrink under those assumptions.
- With stated outward-normal traction convention, u=0 and p=p_ext+2γ/r form
  stationary unforced spherical equilibria for every finite γ≥0 and r>0.
- Lowering positive constant γ does not eliminate the 2γ/r divergence as r→0+.
- The compact-support scaling example in README disproves the asserted H¹→L∞
  estimate in three dimensions.

These have elementary analytical derivations, not formal proof artifacts.
Numerical samples are implementation checks only. The separate two-compartment
closed-form result and periodic-flow/Lean work are neither changed nor reverified.

## Synthetic numerical demonstrations

The RC-shaped waveform generator, prescribed recovery and descriptive thresholds
are synthetic teaching choices. They provide no numerical evidence for PDE
regularity or clinical efficacy. Temporal-flow derivatives have units mL²/s⁴,
not spatial enstrophy units. There is no patient-specific validation.

## Retired / contradicted or unresolved

| Before at ab448aa | Corrected disposition |
| --- | --- |
| H¹→L⁶ implies ||ω||∞ ≤ C||ω||H¹ in 3D | False; compactly supported rescaling counterexample. |
| Energy bounds control vortex stretching, hence a linear Gronwall enstrophy estimate | Unproved; the required coefficient and boundary control were assumed. |
| A shrinking closed material sphere constructs incompressible blowup | Incompatible with volume conservation for a smooth filled domain. |
| Above a γ/curvature threshold the solution must blow up | Universal version contradicted by static spheres; existential version not settled by this counterexample. |
| Lower positive γ removes the 1/r singularity and restores smoothness | False radius-limit deduction; no smoothing theorem established. |
| Neonatal respiratory failure and recovery demonstrate PDE blowup and regularization | Unsupported equivalence; observations are motivation only. |
| Synthetic labels smooth/approaching/critical/singular imply treatment need | Replaced by descriptive compliance/data-quality labels with unvalidated thresholds. |
| Scalar (dQ/dt)² is an enstrophy proxy and its scaled value is dissipation | Renamed temporal-flow diagnostics with explicit units; no spatial inference. |
| Compliance observations identify a PDE critical constant | Retired estimator raises NotImplementedError. |

No claim is made here about the current status of any general Navier–Stokes
problem. No patient database work, new speech model, or recalibration of Shared
Air placeholders is part of this correction.

## Synthetic pipeline repair plan (before implementation)

Base: `14fe98a43ca49784540de8fcb03a9f931754975e`. Software consistency work,
not a new research theorem. First reproduce 50 prescribed breaths yielding
48 clean segments or 468 default-noise segments (seed 42).

Acceptance checks: recover prescribed counts and onsets within one sampling
interval on synthetic pressure cycles at noise fractions 0, 0.01, 0.05; seeds
7, 42, 2026; sample rates 100, 200, 1000 Hz. Confirm separate held-out seeds
and rates without tuning to them. Explicitly discard unverified partial edge
cycles; known synthetic complete edges may be declared as such. Do not use
interior ground-truth boundaries as detector input.

For a constant-parameter periodic RC fixture, check noiseless per-cycle net
volume change near floating roundoff, retain the stated RC time constant
without an undocumented floor, and check sampling convergence of the volume
excursion/pressure-range descriptor against its finite-cycle analytical value.
Target absolute descriptor error <= 0.015 at 100 Hz and decreasing errors with
refinement, not exact recovery of prescribed compliance at arbitrary rates.
Report noisy descriptor bias instead of tuning it away. The pressure/flow
noise remains synthetic measurement noise, not a physiologically calibrated model.

Replace fabricated decay horizons with explicit fit statuses; no clinical
forecast or PDE interpretation. Preserve failed checks and explain any necessary
change to this plan. Precision/runtime documentation corrections add no theorem.
