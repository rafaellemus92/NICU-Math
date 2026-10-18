# physiology/CLAIMS.md — the ledger

Every claim in `physiology/` lives in exactly one tier below. See
[`../RESEARCH.md`](../RESEARCH.md) §3 for the tier definitions.

---

## Mathematical results

*(Statements with proof, assumptions, and boundary cases.)*

- *(none yet)*

## Exact computations

*(Deterministic scripts whose output verifies the claim.)*

- **A two-compartment linear respiratory model with aggregate
  compliance C = C₁ + C₂ and matched branch resistances yields
  different retained excess-volume fractions depending on how C is
  distributed.** With R₁ = R₂ = 2R, compare A: (C/2, C/2) and
  B: (0.9C, 0.1C). Both equilibrate at the same initial driving
  pressure P₀ > 0, hence both start with total excess volume CP₀.
  After release to zero driving pressure, at t = RC:
  A = exp(−1) = **0.36787944117144233**;
  B = 0.9 exp(−1/1.8) + 0.1 exp(−5) = **0.51705187336359804**.
  **Verified at machine precision** (formerly pending PR #7):
  analytically derived closed forms, floating evaluation discrepancy
  0.000e+00 in both unit-scale cases; not a formal proof certificate.
  See [physiology/two_compartment.py](two_compartment.py) and
  [derivation and limits](two_compartment.md). Tests:
  [`tests/physiology/test_two_compartment.py`](../tests/physiology/test_two_compartment.py),
  **41 passed**; headline errors < 1e−10 and at float64 roundoff scale;
  independent solve_ivp maximum absolute volume errors **7.981e−11**
  (symmetric) and **2.604e−11** (heterogeneous), both < 1e−6.
  Verified implementation commit: `aa73b1350b14f18608a1a1564906cd3fc7fa2645`.
  This is a summary-statistic obstruction for independent passive linear
  compartments, with no shared dynamic chest-wall coupling. Volumes are
  relative to the zero-driving-pressure equilibrium baseline, not resting
  end-expiratory absolute volume or clinical residual volume. Teaching
  instrument only: no specific-patient inference, nonlinear compliance,
  recruitment, or validated predictive clinical tool is claimed.

## Numerical evidence

*(Pre-registered hypothesis, path to plan.md, held-out outcome.)*

- *(none yet)*

## Clinical evidence

*(Primary source with DOI/PMID, n, population, limits of
generalization. Per-paper note in `references/`.)*

- **Periodic breathing is detectable from standard NICU chest-
  impedance monitoring in 32-week preterm infants, peaking around days
  7–14 at approximately 6.5% of monitored time** (Mohr et al. 2015,
  n = 70; chest-impedance method does not establish individual
  physiological loop gain). PMID: 25954054.
- **Sleep is associated with coupled neural, hemodynamic, and CSF
  oscillations in human adults** (Fultz et al. 2019). Does not
  establish the same mechanism in preterm infants.
- **Transmural pressure, lung-volume-dependent pulmonary vascular
  resistance, and respiratory-pressure effects on ventricular loading
  cannot all be adequately represented by a single aggregate
  resistance** (Bronicki & Baden, "Cardiopulmonary Interactions",
  2016, review).

## Proposed mechanisms

*(One paragraph each; name what would make each testable.)*

- **A sleep-state-dependent delayed-feedback respiratory model may
  predict onset and duration of periodic breathing better than a
  history-only baseline.** Testable with the PhysioNet PICS dataset
  ([picsdb/1.0.0](https://physionet.org/content/picsdb/1.0.0/)) for
  initial feasibility (ECG + impedance, no sleep-stage labels), then a
  dataset with sleep-stage labels for the state-dependence hypothesis.

- **Skin-to-skin contact lowers periodic-breathing burden; the effect
  may be mediated by changes in sleep-state organization rather than
  independently.** Testable by within-infant matched-period comparison,
  controlling for motion artifacts and the reason skin-to-skin was
  initiated.

- **Patterned breathing coupling** (slow phrase-level envelope of a
  chant or similar practice entraining respiration) **may change the
  probability of sleep-onset transitions, independent of the acoustic
  pitch.** Not applicable to the neonatal context without separate
  consideration. Testable in adults by a within-subject comparison of
  (quiet rest / paced breathing / neutral humming at matched breathing
  / meaningful chant at matched breathing) with respiration, ECG, and
  EEG-defined sleep-onset measurements. The spiritual significance of
  the practice is a separate question from the physiological
  mechanism.

## Contradicted / unresolved

*(Preserved as negative results; never deleted.)*

- *(none yet)*
