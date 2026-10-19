# Independent audit of `codex/mean-source-hull` at f4fe230: preserved scripts and outputs

**Status: review record only.** This folder adds no new claim, changes no certified output and
modifies no existing file. It preserves the independent checking scripts, their outputs and the
failed checker attempts from one audit, so the audit can be inspected and rerun after the session's
temporary files are gone. Audited commit: `f4fe230aa1f73988071f85086741f6e7db0fe9d4`
(implementation owner Codex). Auditor: Claude, session "Inviscid run convergence past max|ω|",
19 October 2026. Branch `claude/mean-source-hull-audit`, based directly on f4fe230.

## Verdict

Conditional acceptance; no defect found that changes any bound or decision. The defensible result:
for a = c = d = 1, ν = 1/28, φ = 37/100 and T = 1/4, and for every nonzero |b| ≤ 0.003, the
enstrophy difference Z(u_b(T)) − Z(U(T)) is positive and differs from its quadratic approximation
b²Z2(T) by at most 26.1%, because

    |R_Z(T; b)| ≤ b⁴ C_endpoint ≤ b² β² C_endpoint ≤ 0.26061 · b² · (lower bound of Z2(T)) ≤ 0.26061 · b² Z2(T).

It is conditional on the certificates and arithmetic assumptions listed below. It is an
endpoint-only statement. It does not establish that the interaction-generated contribution grows:
the certified interval for Z2(T) contains its initial value Z2(0) = 1/4, so even the sign of
Z2(T) − Z2(0) is undetermined, and the lower bound comes mostly from the q₁ energy, which already
starts at 1/4.

## What was reproduced and what was only inspected

Reproduced by execution, in a clean scratch checkout at f4fe230 with the existing verified arrays
(Python 3.13.16, NumPy 2.0.2, mpmath 1.3.0; the recorded runs used Python 3.12.14):

| check | outcome | record |
|---|---|---|
| 22 pinned input hashes; source hashes recorded in outputs; inherited absorption files unchanged since 419e6c3 | all match | transcripts/01, 07 |
| focused tests | 52 executions of 42 distinct tests, all pass | results/tests_*.log, transcripts/02 |
| `source_hull.py --mode full`, once, fresh output file | all 250 cell bounds and every derived bound identical to the recorded full.json | results/full.audit-claude.json, transcripts/03 |
| endpoint fractions, projecting each mode in exact rationals first | identical to endpoint.json; every projected coefficient exactly solenoidal | scripts/endpoint_exact.py, transcripts/04 |
| advective-form FFT oracle at 12 501 nodes and 12 500 fine-cell midpoints (non-rigorous) | no value above its hull bound; hull L_N 0.73% above a trapezoid estimate | scripts/source_oracle.py, transcripts/05 |
| full scalar chain in mpmath interval arithmetic from primitive inputs | agrees with every recorded upper endpoint to ≤ 2.2·10⁻³⁷ relative | scripts/scalar_chain.py, transcripts/06, 07 |
| lattice constants (non-rigorous) | Σ|k|⁻⁴ ≈ 16.532316 below the certified C_A² = 16.541133; A_λ ≈ 0.4414 below the bound 0.4745 | scripts/lattice_sanity.py, transcripts/08 |

The only differences between the fresh hull run and the recorded one are 251 timing fields, the
Python version and peak memory.

**Test count.** The earlier report said "52 tests". That is 52 executions of 42 distinct tests: the
source-only-hull suite already contains the 10 mean-q2-pilot kernel tests (7 hull + 10 kernel = 17),
and the separate mean-q2-pilot run executed those same 10 again. Distinct tests: 7 hull, 10 kernel,
9 endpoint, 8 tightening, 8 dissipation.

Inspected only, by reading: the retained-dissipation inequality (W) and (1); the generic linear
lemma (3); the full-remainder equation (4) and its five source bounds; the mean cancellation (6)–(7);
the three-term enstrophy identity (8); Lemma A with the cube subtraction (B) and (C)–(F); Lemma B,
(H) and (I); the endpoint derivation (1)–(5); the forcing discrepancy ΔF and the mean propagator.
Powers of b and ν were checked term by term. Zero spatial means hold for every field that needs
them: the data have zero mean and the flow conserves it; q₁, its approximation and the error live
on k_z = ±1; q₂, r, its z-mean and V have divergence-form forcing and zero data; W = w/b² for b ≠ 0.
The interval helpers of the inherited validator were reviewed in an earlier audit and only
exercised here.

## Inherited assumptions

1. IEEE binary64 round-to-nearest with gradual underflow, no FMA contraction or extended precision
   in NumPy's elementwise operations and np.sum, and a correct Python decimal module.
2. The absorption certificate at 419e6c3: its bounds ε₀, ε₁, δ, ε_W, S₁, N_w, K, and Lemma M making
   them uniform over |b| ≤ 0.003.
3. That certificate's closure through the enstrophy continuation criterion, giving smoothness on [0, T].
4. The parent note at cd9c9f0: the certified C_A, the analytic base-flow bounds behind M₁ and M₂,
   inequalities (I1)–(I6), and the mean-zero Agmon inequality.
5. The interval helpers of the validator.
6. The identity of the stored arrays, fixed by their hashes.
7. The convention that q₂ is the b² coefficient.

## Minor findings, none affecting a bound

- The coverage test in source-only-hull checks range arithmetic, not the code path. Coverage is
  enforced by the per-cell 51-node check and the final row assertion, and the oracle here confirmed
  it. Repair: exercise the per-cell function on a synthetic node array.
- C_endpoint uses the rounded G = 1.8534 while |M| uses the exact upper bound 1.853301043406. Both are
  valid; using the exact value in C_endpoint would give β²C_endpoint ≤ 0.0622918.
- The full run took 52 s here against 36.6 s recorded, inside its 180 s watchdog.

## Failed checker attempts and their corrections

Neither failure involved the audited code, and no reported number comes from a failed attempt.

**scripts/scalar_chain.py went through three versions.** The first two are preserved in attempts/
with their verbatim terminal output.

1. `attempts/scalar_chain.attempt1.py` aborted at line 80 with `ValueError`: `float()` was applied to
   a non-point interval, the lower Z2 endpoint formed by subtracting two point intervals. Fix:
   extract endpoints with `.a` and `.b` before converting.
2. `attempts/scalar_chain.attempt2.py` aborted at line 34 with "can only create mpf from zero-width
   interval". This exposed a real rigor defect present in the first version: the I_y accumulator
   started as a plain `mpf(0)`, and adding point intervals to it silently produced plain mpf values
   with round-to-nearest, so the first version's I_y and everything downstream were not outward
   rounded. Fix: start the accumulator as `iv.mpf(0)`. While fixing it, a second rigor defect was
   found by inspection: the validated cell maxima were read through their shortest round-trip
   decimal strings, whose enclosure need not contain the exact binary value. Fix: convert the float
   exactly with `iv.mpf(float(...))`.
3. The final version ran cleanly. Its printed values agree with the non-rigorous first version to
   all displayed digits; only the final run is reported.

The two earlier files were reconstructed after the fact, because the script had been patched in
place. attempt1 was rewritten from its original text, attempt2 was produced by replaying the first
patch exactly as it was applied, and replaying the second patch on attempt2 reproduces
scripts/scalar_chain.py byte for byte. The failing statements sit on exactly the lines the original
tracebacks name (80 and 34).

**The first lattice sanity estimate was wrong.** `attempts/lattice_sanity.attempt1.py` truncated on
the cube [−200, 200]³ but added the tail 4π/(R + ½) that belongs to the region outside a ball. The
region outside the cube is strictly smaller, so the tail was overcounted by roughly 0.02, giving a
spurious Σ|k|⁻⁴ ≈ 16.5429, above C_A². Its output is the last block of transcripts/07. Fix,
scripts/lattice_sanity.py: truncate on the ball |k| ≤ R with the matching tail, giving 16.532316
at R = 150 and R = 300. The "literature value" string printed by that script is a value recalled by
the auditor and hard-coded; the computation is what confirms it. Both lattice checks are
non-rigorous sanity checks; the rigorous C_A is inherited.

## Files

- `scripts/`: the final independent checkers, as run. compare_hull_output.py, pins_check.py and
  compare_and_provenance.py were run inline during the audit and are preserved verbatim.
- `attempts/`: the failed versions and their verbatim output.
- `results/`: machine outputs of the audit runs, unchanged: the fresh hull output and log, the test
  logs, the exact endpoint fractions and the scalar-chain output.
- `transcripts/`: terminal output of the final runs, copied verbatim. Nothing was rerun to produce
  this folder.
- `SHA256SUMS`: hashes of every file above.

The trajectory arrays are not duplicated here; they are in Git LFS on `claude/absorption-b003-T025`,
with raw-array SHA-256 529b1e4c… (Q) and 825078dc… (W).

## Rerunning

From `finite-time/`, with the arrays at `<traj>` and a fresh output path `<out>`:

    python3 -I source-only-hull-audit/scripts/pins_check.py
    (cd source-only-hull && python3 -B source_hull.py --trajectory <traj> --mode full --output <out>/hull.json)
    python3 -I source-only-hull-audit/scripts/compare_hull_output.py source-only-hull/results/full.json <out>/hull.json
    python3 -I source-only-hull-audit/scripts/endpoint_exact.py <traj> z2-endpoint/results/endpoint.json <out>/endpoint_fracs.json
    python3 -I source-only-hull-audit/scripts/source_oracle.py <traj> <out>/hull.json
    python3 -I source-only-hull-audit/scripts/scalar_chain.py . <out>/hull.json <out>/endpoint_fracs.json <out>/scalar_out.json
    python3 -I source-only-hull-audit/scripts/compare_and_provenance.py <out>/scalar_out.json <out>/hull.json
    python3 -I source-only-hull-audit/scripts/lattice_sanity.py

Measured audit wall times: tests 2.5 s, hull run 52.4 s, oracle 77.0 s, exact endpoint and scalar
checks about 2 s, plus two short lattice checks that were not timed.
