# Synthetic waveforms and an incomplete conjecture

This directory preserves a motivation: investigate how geometry, surface tension
and distributed mechanics influence explicitly specified models. Its former
outline did **not** establish a conditional Navier–Stokes regularity theorem.
Clinical finite-time transitions are not thereby PDE singularities. No statement
about the current status of a general Navier–Stokes problem is needed here.

## Analytical sanity checks

Assume a smooth closed material domain Ω(t), a smooth incompressible velocity,
and outward normal n. Transport of volume and the divergence theorem give

    d|Ω|/dt = ∫∂Ω u·n dS = ∫Ω div u dx = 0.

For a sphere of positive radius, |Ω| = 4πr³/3, so 4πr²ṙ = 0 and ṙ = 0.
A proposed shrinking material sphere is therefore incompatible with these
assumptions. The radial field u = (ṙ/r)x has div u = 3ṙ/r, not zero when
shrinking. The alternative radial field proportional to x/|x|³ is singular
at the center and is not a smooth field on the filled ball. An open domain,
compressibility, or a multiphase interface would require a different model.

For an **unforced**, stationary sphere, use stress T = −pI + 2μD(u), outward
curvature κ = 2/r, exterior stress T_out = −p_ext I, and traction convention

    (T_in − T_out)n = −γκn.

Then u = 0 and spatially constant p = p_ext + 2γ/r satisfy the bulk equations,
incompressibility, the material kinematic condition and the traction jump for
every finite γ ≥ 0, r > 0. Constant pressure has zero spatial gradient. Thus
arbitrarily large γ/r or the defined scale ratio cannot force **every** solution
to blow up. This refutes a universal threshold-implies-blowup statement, not an
existential claim about some other initial data. These equilibria do not imply
stability or a continuation theorem for general moving interfaces.

For every fixed positive γ, 2γ/r diverges as r → 0+. Replacing γ by another
positive constant changes only the coefficient. Boundedness on a prescribed
vanishing-radius path requires γ(r) = O(r); alternatively constrain r away from
zero. Neither behavior follows from the demo or from a treatment label.

The claimed H¹ → L∞ inference in three dimensions was false. For nonzero
φ ∈ C_c∞ supported in a unit ball, choose x₀ inside the domain and
fε(x) = ε^(−1/2) φ((x−x₀)/ε), with support inside the domain. Change of variables
gives ||fε||₂ = ε||φ||₂, ||∇fε||₂ = ||∇φ||₂, and
||fε||∞ = ε^(−1/2)||φ||∞. H¹ remains bounded while the supremum diverges.
The H¹ → L⁶ embedding supplies no claimed L∞ bound. Independently, the outline
never controlled vortex stretching or the moving-boundary terms needed for its
Gronwall step. A continuation criterion must match its PDE, domain, boundary
conditions and solution class; these hypotheses were not supplied.

These are analytical arguments under explicit assumptions. Tests sample their
formulas to check code and signs; sampled floating-point agreement is not a
universal proof or a formal proof certificate.

## Synthetic diagnostics and units

The Python generator now solves the linear equation
R_mL dV/dt + V/C_b = P − PEEP separately on constant-pressure phases.
C_b = max(C₀(1 − decay·b), 0.05) mL/cmH2O is **prescribed**, and
R_mL = R × 10⁻³ converts R from cmH2O/(L/s). Tau is exactly R_mL C_b;
the previous 0.01 s floor is removed. Inspiration occupies 35% of a cycle.
Volume is continuous across pressure and compliance changes; the initial
volume is the periodic steady state for the first compliance. This is a
synthetic linear teaching model, not a Navier–Stokes or patient model.

The sampled cycle period is the nearest integer number of sampling intervals
(at least 20). Pressure and flow samples represent interval averages; volume
samples represent left edges. Flow is computed from exact endpoint volume
differences, avoiding the former independently reset pulses and misaligned
quadrature. Gaussian flow noise is integrated without detrending. The model
supplies known complete acquisition edges; CSV records default to unknown
edges and assume interval-average flow if volume must be integrated.

Segmentation uses pressure hysteresis: thresholds at 30% and 70% of the
10th-to-90th percentile pressure span, each confirmed for 40 ms; onsets must
be at least 300 ms apart. The detected onset is the first sample of a
confirmed high run. No interior ground-truth boundaries are used. Unknown
initial high phases and trailing cycles are discarded; explicitly known
complete synthetic edges are retained. Cropped records must clear the edge
flags. Cycle timestamps now retain the recording origin. The old `flow_threshold`
argument is removed; `min_phase_seconds` and `min_cycle_seconds` are keyword-only
to prevent old positional flow thresholds from silently changing units. Flat pressure gives
no cycles; nonfinite/misaligned waveforms are rejected. This detector assumes
distinct pressure phases and is not validated for spontaneous breathing,
variable baselines, high-frequency ventilation, or clinical recordings.

The volume-range/pressure-range descriptor is **not prescribed C**. Even
without noise, finite inspiration and expiration limit the volume excursion.
For constant C in periodic steady state its continuous-time value is
C(1−A)(1−B)/(1−AB), with A=exp(−T_in/τ), B=exp(−T_out/τ).
Sampling can miss the peak, and extrema are biased by noise. No clinical
calibration or unbiased parameter recovery is asserted. The CLI reports the
prescribed schedule separately and now exercises default noise again.

The separate web demo remains a prescribed, floored RC-shaped illustration
with an arbitrary recovery ramp. It is unchanged by this Python pipeline
repair and is not a coupled RC ODE solver. Neither demo models treatment.

- `classify_compliance` / `classifyCompliance`: descriptive synthetic bins;
  low below 0.3, intermediate below 1.0, higher from 1.0 mL/cmH2O. Within the
  intermediate bin a slope below −0.1 mL/cmH2O per breath is called declining.
  Invalid inputs and empty summaries yield `insufficient_data`.
- `squared_flow_time_derivative`: (dQ/dt)², units mL²/s⁴ when Q is mL/s.
  No spatial curl, vorticity or enstrophy can be recovered from this alone.
- `flow_derivative_evolution`: per-cycle means and peaks of that quantity.
- `kinetic_energy_per_length`: ρQ_SI²/(2A), J/m for a uniform plug-flow
  cross-section assumption, not total NS energy.
- `scaled_flow_derivative_index`: retained historical scaling ν mean((dQ_SI/dt)²)/A,
  units m⁶/s⁵; not dissipation or a validated physiological diagnostic.
- `capillary_pressure_ratio`: (γ/r)/(ρν²/L²), using half the spherical pressure
  jump by convention; no regularity threshold is inferred.
- `loop_metric_distance`: reference-scaled descriptor distance, not an attractor
  reconstruction. PCA loop geometry depends on axis units. Power-law fitting
  and its extrapolated zero crossing do not predict clinical events.
  `estimate_decay_exponent` now returns `DecayFit(status, exponent, horizon, reason)`.
  Invalid/nondeclining fits or crossings within the observed window have no
  exponent/horizon. A resolved horizon is relative to the selected window,
  conditional on the chosen fit form; it is not an event prediction.

Misleading former API names have been replaced, and in-repository callers updated.
`estimate_critical_constant` now raises `NotImplementedError` because the assumed
compliance-to-PDE mapping is absent. `surface_tension_response` is an illustrative
saturating function using its supplied γ₀, not a dosing tool. P–V flow integration
uses mL/s × s = mL; the previous web code applied an erroneous additional 10⁻³.

Run `python -m pytest -q tests/navier_stokes` and `python -m navier_stokes.demo`.
Web math checks: `node --experimental-strip-types --test web/tests/ns.test.mjs`
(Node 24 used). See [claim ledger](CLAIMS.md) for preserved retired statements.

Synthetic teaching use only; not validated for patient care. No patient data are
used. The retained legacy metadata/CSV parser is not a de-identification guarantee
or approval to process clinical data. The existing database schema requires a
separate privacy/data-model review; this correction does not enable, migrate,
access or remove it. Shared Air coupling multipliers remain placeholders; no
speech model is introduced. Periodic-flow and Lean work are unchanged and not
rerun. The two-compartment model is unchanged; its focused suite is rerun to
record numerical verification versions alongside the precision-label correction.
