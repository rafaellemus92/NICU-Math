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
