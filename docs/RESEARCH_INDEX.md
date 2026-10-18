# Research index

This is a map of existing material and open questions, not a literature review or
an endorsement of clinical validity. No patient data or licensed full texts belong here.

| Area | Evidence category | Location and status |
| --- | --- | --- |
| Seeded logistic scenarios | Unvalidated physiological models; numerical output | `bayes.py`: illustrative coefficients/noise for acidosis, NEC and extubation. Several UI inputs do not enter the equations. No calibration, clinical validation or causal interpretation. |
| Scenario smoke checks | Numerical evidence / software verification | `tests/test_smoke.py`: deterministic seeds, bounded summaries, histogram conservation, request limits. These establish software behavior only. |
| Prime pangram definitions and packing arguments | Mathematical proof claims, subject to independent review | `pangram/README.md`, `pangram/structure.py`, `pangram/congruences.py`. Inspect definitions and assumptions before citing; not re-proved in this startup task. |
| Prime pangram counts and witnesses | Reported exact calculations | `pangram/engine.py`, `pangram/core.py`, `pangram/results/`. Exactness depends on arithmetic bounds, enumeration completeness and verification. Full rerun not performed in this task. |
| Order/base scans and weighted sums | Numerical/computational evidence | `pangram/orders.py`, `pangram/run_order_scan.py`, `pangram/results/`. Physically motivated letter orders are motivations, not established physiological links. |
| Respiratory mechanics and neonatal hemodynamics | Future synthetic research scope / hypotheses | No validated mechanistic model or new proof supplied by this repair. Specify equations, units, boundary/initial conditions and falsifiable predictions before experiments. |
| Phase-sensitive dynamics | Hypotheses only | Clinical observations may motivate questions; a clinical finite-time transition is not a PDE singularity. No established bridge to pangram calculations and no claim to solve Navier–Stokes regularity. |
| Legacy evidence retrieval | Unvalidated application pipeline | `search.py`, `answer.py`, `ingest*.py`, `schema.sql`. Disabled in default startup. Retrieval, citations, ingestion variants and DB schema compatibility require separate integration review. |

For each new item record: claim ID and category; precise statement; assumptions and
units; source citation or code/commit; reproducible command and seed; result;
limitations; independent reviewer and status. Keep hypotheses separate from proven
results, exact arithmetic separate from floating-point evidence, and mathematical
validity separate from physiological validity. Record inspirations as motivations.
