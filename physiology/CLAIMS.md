# physiology/CLAIMS.md — the ledger

Every claim in `physiology/` lives in exactly one tier below. See
[`../RESEARCH.md`](../RESEARCH.md) §3 for the tier definitions.

---

## Mathematical results

*(Statements with proof, assumptions, and boundary cases.)*

- *(none yet)*

## Proposed model calculation (unimplemented and unvalidated)

*(Deterministic scripts whose output verifies the claim.)*

- **A two-compartment linear respiratory model with aggregate
  compliance C = C₁ + C₂ and matched branch resistances yields
  different passive-emptying residuals depending on how C is
  distributed.** Specifically, with R₁ = R₂ = 2R and C_total = C,
  comparing (C₁, C₂) = (C/2, C/2) vs (0.9C, 0.1C) over passive
  emptying for time RC gives distinct retained-volume fractions.
  Script: `two_compartment.py` *(not implemented here; PR #7 is the startup reconciliation)*.

## Numerical evidence

*(Pre-registered hypothesis, path to plan.md, held-out outcome.)*

- *(none yet)*

## Candidate clinical references (imported from PR #5; not verified here)

The following are source branch notes, not validated clinical conclusions.
Verify citations, measurements and applicability before promoting them to clinical
evidence; no patient dataset or experiment is authorized by this scaffold.

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

## Proposed mechanisms (future questions; synthetic-only current scope)

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
