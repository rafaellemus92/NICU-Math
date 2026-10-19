# Scoped certificate audit follow-up

Branch codex/endpoint-certificate-audit-repairs, exact base
3161f059c24878c9b5ea05e6cc081e72fb53bbc5. Attribution work at
4e86fa995243c3a428a253ee3333eb42251cd85f remains separate and unchanged.
No simulation or other research run.

1. Upstream provenance: time_refinement.final.json is hash-checked here but
   not parsed. It is nevertheless a mathematical/numerical dependency through
   the global D_r used by the upstream err_grad bound. The final postprocessor
   reads that bound from tr_remainder.repaired.json. The technical note's
   dependency table and current output labels now state this distinction.
   The historical PROVENANCE_ONLY identifier means no direct parsing here,
   not absence from the upstream arithmetic dependency chain.
2. Future outputs record the completed independent scalar reproduction at
   b03bfa45ae25d3543d7ecbd3a2361f990d01120f, with inherited certificates not
   revalidated. That audit covered the original algorithm, not these later
   implementation edits. All original outputs/status labels remain preserved.
3. Rate guard: mpmath1.3.0 compares [-1,1]<0 as None (undecidable), whereas
   [-2,-1]<0 is True. The former slipped past any(rate<0). Current code
   requires each lower endpoint>=0, and the duration's lower endpoint>0.
   An undecidable/false condition fails closed. Negative and straddling rates
   are rejected; zero, [0,1] and positive intervals are accepted. Zero growth
   is mathematically valid for inclusive source-cell weights and gives factor1.
   Fixed production rates remain positive, so no certificate result changes.

Eight focused tests pass, including explicit negative/straddling/zero/positive
interval cases and nonpositive/straddling durations. Fresh regression preserves
all old numerical and decision fields exactly; only status, input-role metadata,
source hash and timing change. Results are exclusive-create under
results/followup/. Combined timed tests/regression0.257927s with20s hard limits;
including the preliminary semantics probe, total execution is conservatively
under1s, below60s. No installed dependencies or old data changed.

Correction to a relayed report:377.312890 is the upper bound on C_new,
not beta² C_new. The latter is<=0.003395816008963. The endpoint lower margin
remains>=0.004804904671503 for H_b(T)/b², conditionally on inherited assumptions.

Bounded review: the existing certificate-note reviewer inspected this scoped
code/test/note diff, upstream err_grad formula and fresh logs read-only; no
blocking defect found. No independent execution, inherited-certificate review,
recursive reviewers or external contacts. Final handoff, this summary, manifest
and commit were not independently reviewed. Syntax and whitespace checks pass;
unrelated application/web/Lean tests were not run.
