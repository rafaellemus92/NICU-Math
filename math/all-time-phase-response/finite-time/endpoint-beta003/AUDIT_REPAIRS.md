# Audit reproduction and bounded repairs

Base: 0f258a1add2b9e339d6c28f3599c43c4ad8241c3. Independent audit inspected
read-only at b03bfa45ae25d3543d7ecbd3a2361f990d01120f, folder
`finite-time/independent-checks/endpoint-beta003-0f258a1/`.

The independent implementation used the parent's 40-digit directed Decimal
interval arithmetic instead of mpmath. It recomputed J2, cumulative dissipation
and sup-norm integrals, full-r bounds, nonself components, both old self bounds,
new divergence bound and final comparison from primitive hash-checked inputs,
without reading the parent's totals as arithmetic inputs. Its recorded margin
is at least 0.004804904671503767. The reviewer reported approximately six seconds
for the overall bounded audit; the published scalar component log records 1.4s.
Original mpmath check.py/test_check.py were inspected, not run. Inherited
certificates were not revalidated. Separate resolved Fourier-field binary64
checks are empirical algebra checks, not rigorous PDE enclosures.

Repairs preserve INPUTS.json and all original plans, results and SHA256SUMS:
- The time_refinement.final.json pin remains explicitly provenance-only. Its
  bytes are hash-checked, but its JSON is not parsed or consumed numerically.
  New outputs label every input's role. Historical input hashes stay unchanged.
- Production propagation weights now call inclusive_tail_weights. The toy test
  exercises that actual helper for x'=log(2)(x+1), x(0)=0 on two unit cells;
  x(2)=3 exactly. Growth is represented in units of log(2), so all weights are
  exact rational powers of 2. Cell source mass log(2) lies strictly between 2/3
  and 3/4 by midpoint/trapezoid integration of 1/t on [1,2]. Inclusive weights 4,2
  give a majorant at least 4; excluded weights 2,1 give at most 9/4<3.
  Thus omission of the source cell is detected against an exact solution,
  not merely against another manually written exponential expression.

Focused acceptance plan, recorded before fresh tests: rerun the postprocessor
and compare all previous numerical/decision fields; source hashes, timing and
new role labels may differ. Run focused tests. In a temporary copy mutate the
production helper to exclude source-cell growth and require the toy test to
fail. Keep fresh logs and outputs, including expected mutation failures. At
most 300 seconds aggregate numerical execution; hard timeout 60s per invocation.
No numerical evolution, validator, LFS, parameter sweep or external action.
A single bounded review of changed code and technical note will be recorded
below. Historical SHA256SUMS describes the original commit, not repaired code;
REPAIR_SHA256SUMS will identify this stage's files.

## Completed checks and review

`results/repair/regression.json` matches every prior numerical and decision
field exactly. Input-role metadata is new; source hashes and timing differ.
Seven focused tests pass. The temporary production-helper mutation fails the
exact toy test at its coverage assertion, as intended; its failure log is
preserved. Aggregate numerical process time 0.538384s, including mutation.
Syntax compilation and git diff whitespace checks pass. Unrelated web,
application and Lean suites were not rerun for these scoped changes.

One authorized bounded AI reviewer (`/root/certificate_note_review`) inspected
the changed code, exact toy and actual mutation evidence, standalone note,
repair record, stored results and published audit README. No blocking defects
were found. Its only editorial finding was missing spaces in this repair
record, corrected without changing code or numerical outputs. It confirmed
the fixed conditional statement, absorption/cumulative-weight arguments,
provenance-only role and accurate independent-audit limitations.

This reviewer ran no numerical checks, revalidated no inherited certificate,
externally verified no literature, and contacted no additional reviewer.
The primary-literature context and references were supplied by the parent's
separate bounded primary-source check. Subsequent editorial corrections,
this review summary, manifests, handoff/index and eventual commit were not
independently reviewed. No formal verification or human peer review is claimed.
