> Historical PR15 record from a9aaf1f, referring to source 77916bb.
> Dates, passes, pending-review language and paths below describe that session.
> Use [README.md](README.md) for current scratch-only commands and
> [the correction review](../../../docs/reconciliation/CORRECTIONS.md) for fresh checks.

> Historical PR15 import record, retained with commands relocated to the canonical
> `math/ns-phase-audit/enstrophy-jet/` folder. Source map paths refer to that
> original import, not the combined tree. Fresh validation is in
> `docs/reconciliation/REVIEW.md`; these historical passes are not new runs.

# Selective research import record

Owner: Codex. Branch: `codex/import-flow-research`.
Base and draft-PR target: `codex/integrate-research-workspace`, fixed commit
`ab448aaa429bf3bc3c4c5bc2a41b5be6778e1f28`.
Source: `rafaellemus92/NICU-Math`, branch `claude/breath-rhythm-ns-jet`,
`77916bb51ea88ea6e1b2cddd2cd6e9309993383f` (remote tips verified).
No whole-branch merge. The source authors/AI credits remain in RESULTS.md.

## Selection and adaptations

`navier-stokes-jet/` is relocated under `math/`, excluding its dependency
manifest and duplicative earlier-run archive. The complete coefficient table is
kept for self-contained reproduction, including the intentional 0–12 overlap.
Shared Air audit/tools/results are selectively relocated to `math/shared-air/`;
HTML, manifest, app-writing regeneration tool, machine-specific browser tool/log
and HTML corrections diff are not copied. Speech motivations link the pinned
`letters/words.md`; the broader essay/correspondence is not copied.

`exact_single_nu.py` now fails on mismatches/missing requested orders.
`float_check.py` now enforces a documented 1e-10 per-order relative tolerance,
finite values, requested-order coverage and phase resolution. New tests include
CLI negative controls, the numerical tolerance boundary, and exact stored
E/Z overlap. Shared Air's loader points to the existing integrated HTML.
Imported prose distinguishes historical evidence from fresh runs, removes
unverified announcement claims, and corrects stale pending-publication wording.
No publication status outside this repository was verified.

Every source-derived file is mapped to its full source Git blob in
[SOURCE_FILES.json](SOURCE_FILES.json). Imported historical outputs remain
historical; the file map makes any local adaptations inspectable against source.

## Historical PR15 validation (2026-10-18)

Environment: Python 3.12.14, numpy 2.5.4, python-flint 0.9.0, pytest 9.1.1;
Node v24.19.0. Temporary venv `/tmp/flow-venv`; no dependency manifest changes.
Commands below are from repository root (Python means that venv's interpreter).

- `python -m pytest -q math/ns-phase-audit/enstrophy-jet/tests`: **18 passed, 5.15 s**.
  Source tests regenerate symbolic E/Z through 8; independent exact rotational
  jet through 6 at ν=1/28 and −2/3; float through 8 at ν=1/28 and 1/3,
  φ=0, 0.971, 2.16. Stored parity/degree checks reach 10, stored energy identity
  reaches E order 14 (Z order 13). These are not order-14 regeneration.
  Added tests compare stored E/Z coefficients through 12 with
  `ns-phase-audit/audit_v2/exact/z12_unit.json` using exact rationals and
  trailing-zero normalization; all match. Negative controls fail as expected.
- `python math/ns-phase-audit/enstrophy-jet/taylor_exact.py 10 --out /tmp/flow-series-n10.json`:
  **26.7 s**, then exact dict comparison of both E/Z with `results/series.json`
  for every order 0–10: **all match**. This extends fresh symbolic coverage to 10.
- `python math/ns-phase-audit/enstrophy-jet/exact_single_nu.py 1/28 8 --series math/ns-phase-audit/enstrophy-jet/results/series.json`:
  **zero mismatches, 5.8 s**; divergence, reality, support and mean-force diagnostics clean.
- `python math/ns-phase-audit/enstrophy-jet/float_check.py --nmax 8 --grid 20 --phases 24`:
  ν=0, 1/28, 1/3; **worst scaled error 2.8e-14 < 1e-10**, 1.3 s.
- `node math/shared-air/tools/quick_check.js`: **all 16 DEF.pulse fields match**.
- `node math/shared-air/tools/lock_proto.js`: onset **4.00023** at n/G
  128/32, 256/64 and 512/128; numerical agreement, not an exact proof.
- `node math/shared-air/tools/theory_check.js`: completed; deterministic
  τ=1.5 coarse-band alarm timings 16.90, 15.70, 16.92, 18.78, 32.54 s
  agree with the source audit. Other printed theory diagnostics are not a
  fresh certification of every historical claim.

## Deferred work and runtime estimate

No full symbolic order-14 regeneration or float order-40 sweep was run.
Historical order-14 symbolic run: 624.2 s, versus 15.6 s through 10.
Current order-10 benchmark: 26.7 s (some contention from concurrent focused
checks). Simple scaling predicts 624.2 × 26.7 / 15.6 ≈ **1,068 s (18 min)**.
Budget **15–30 min** for order 14; this is an extrapolation, not a measured bound.
Historical order-40 sweep: about **2.5 min and 2 GB RAM**. Applying the same
hardware factor gives about **4.3 min**, but exact/FFT costs differ; provision
**4–10 min and at least 2 GB free RAM**, then remeasure before a full run.
No coefficient-growth asymptotic or divergence theorem follows from finite jets.

Full order-14 FFT comparison, standalone full leaf/decomposition runs,
200-seed Shared Air adjudication, stored sweep regeneration, browser, app,
Lean and unrelated research suites were not run. The source test's small
leaf-target calculation did run. No rigorous Taylor remainder, finite-time
optimum, Navier–Stokes regularity result, speech solver or clinical validation
is claimed. Automatic build checks are infrastructure checks, not math proof.

## Data and scope review

Selected files were reviewed for secret-like patterns, machine-specific paths,
patient records and licensed full texts. None were found in the retained
artifacts; synthetic model outputs and bibliographic references are retained.
Actual machine-specific browser setup was excluded; redacted scratchpad labels
in historical records remain provenance, not runnable paths. No credentials,
patient data or paid APIs were used. Root README, app/web, navier_stokes,
dependency manifests, patient schema and global guidance are untouched.
Independent exact-diff review and final SHA/PR/check status are in the PR handoff.
