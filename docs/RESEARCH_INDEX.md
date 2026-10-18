# Research index

This is a map of existing material and open questions, not a literature review or
an endorsement of clinical validity. No patient data or licensed full texts belong here.

| Area | Evidence category | Location and status |
| --- | --- | --- |
| Seeded logistic scenarios | Unvalidated physiological models; numerical output | `api/app/bayes.py`: illustrative coefficients/noise for acidosis, NEC and extubation. Several UI inputs do not enter the equations. No calibration, clinical validation or causal interpretation. |
| Scenario smoke checks | Numerical evidence / software verification | `tests/test_smoke.py`: deterministic seeds, bounded summaries, histogram conservation, request limits. These establish software behavior only. |
| Prime pangram definitions and packing arguments | Mathematical proof claims, subject to independent review | `math/pangram-prime-words/README.md`, `math/pangram-prime-words/structure.py`, `math/pangram-prime-words/congruences.py`. Inspect definitions and assumptions before citing; not re-proved in this startup task. |
| Prime pangram counts and witnesses | Reported exact calculations | `math/pangram-prime-words/engine.py`, `math/pangram-prime-words/core.py`, `math/pangram-prime-words/results/`. Exactness depends on arithmetic bounds, enumeration completeness and verification. Full rerun not performed in this task. |
| Order/base scans and weighted sums | Numerical/computational evidence | `math/pangram-prime-words/orders.py`, `math/pangram-prime-words/run_order_scan.py`, `math/pangram-prime-words/results/`. Physically motivated letter orders are motivations, not established physiological links. |
| Respiratory mechanics and neonatal hemodynamics | Future synthetic research scope / hypotheses | No validated mechanistic model or new proof supplied by this repair. Specify equations, units, boundary/initial conditions and falsifiable predictions before experiments. |
| Two-compartment passive emptying | Analytically derived closed form; floating evaluation verified at machine precision; unvalidated teaching model | `physiology/two_compartment.py`, `physiology/two_compartment.md`, `tests/physiology/test_two_compartment.py`; source PR #13 at `49c5f82889b0535ab7272aaaafa03842cbda574e`. Equal total compliance and initial excess volume do not determine the trajectory. No patient-specific inference. |
| Phase-sensitive dynamics | Hypotheses only | Clinical observations may motivate questions; a clinical finite-time transition is not a PDE singularity. No established bridge to pangram calculations and no claim to solve Navier–Stokes regularity. |
| Phase-family checks | Numerical evidence / AI audit | `math/phase-family-checks/`: distinct preserved scripts/logs, with corrected radius caveats. |
| Phase-family perturbation | Finite-grid numerical evidence | `math/phase-family-perturbation/`: observed finite-b behavior; sampled smallness constants are uncertified. |
| Oscillation | Standard identities / numerical checks | `math/oscillation/`: lock maps and triad coherence; no established clinical/PDE equivalence. |
| Respiratory claim audit and site | Standard / refuted / open / synthetic, per claim | `navier_stokes/`, `web/`: counterexamples remain refutations; `/outline`, `/proof` redirect. |
| Speech motivations | Analogy / proposed research | `math/speech-motivations/`: no speech model implemented. |
| Canonical all-time response | Unrefereed paper argument / finite-grid checks | `math/all-time-phase-response/`: application of known stability, not proven novelty or a certified numerical radius. |
| Finite-time enstrophy error bound | Paper proof with evaluated constants (not formalized); numerical consistency checks | `math/all-time-phase-response/finite-time/`: certified finite-time radius β₁(T) and \|Z(u_b) − Z(U) − b²Z2\| ≤ C_Z(T) b⁴ for \|b\| < β₁(T); C_Z far above the measured remainder, obstruction documented. Not about b = 1 or general regularity. |
| Legacy evidence retrieval | Unvalidated application pipeline | `api/app/search.py`, `api/app/answer.py`, `api/app/ingest*.py`, `api/app/schema.sql`. Disabled in default startup. Retrieval, citations, ingestion variants and DB schema compatibility require separate integration review. |

For each new item record: claim ID and category; precise statement; assumptions and
units; source citation or code/commit; reproducible command and seed; result;
limitations; independent reviewer and status. Keep hypotheses separate from proven
results, exact arithmetic separate from floating-point evidence, and mathematical
validity separate from physiological validity. Record inspirations as motivations.

The preserved `math/` tree also contains Lean proofs, audits and numerical
experiments catalogued in `math/README.md`; this reconciliation does not re-prove
or certify those claims. `RESEARCH.md` and the `fluids/`, `physiology/` and
`packages/stats/` scaffolds reconcile PR #5: planned artifacts and unverified
reference notes are explicitly labeled. See their ledgers before citing a claim.

## Fluid/respiratory claim correction

See [navier_stokes/CLAIMS.md](../navier_stokes/CLAIMS.md) and its analytical
derivations. This separates respiratory motivation, an incomplete conjecture,
analytical sanity checks and synthetic numerical demonstrations. No changes to
periodic-flow/Lean artifacts or the two-compartment result; no clinical validation.

Synthetic-pipeline follow-up: pressure-phase segmentation and consistent
piecewise RC sampling replace the former noisy crossing detector. See the
pre-recorded acceptance checks and measured limitations in
[navier_stokes/CLAIMS.md](../navier_stokes/CLAIMS.md). This is software/model
consistency, not clinical validation or a new fluid-dynamics theorem.

## Reconciled research

See [the canonical math map](../math/README.md#reconciled-evidence-and-status)
and [reconciliation review](reconciliation/REVIEW.md) for pinned sources,
source preservation, claim decisions and fresh tests.
