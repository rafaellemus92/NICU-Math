# Endpoint sign of H_b(T) = Z(u_b(T)) − Z(U(T)) − b² e^{−2νT}/4: research folder

Branch `claude/endpoint-sign-research`, based on f4fe230. Commit cedb77c is on GitHub; the audit-repair
commit that adds this version of the README is local only. Nothing is merged. Author: Claude, session
"Inviscid run convergence past max|ω|", 19 October 2026. Fixed scope and target, unchanged throughout:
a = c = d = 1, ν = 1/28, φ = 37/100, T = 1/4, the sign of H_b(T) for every 0 < |b| ≤ 3/1000. No
trajectory was read, and no adjoint, q₂, DNS or validator run was made.

## Result

**Coefficient sign, certified conditionally:** J2 = Z2(T) − e^{−2νT}/4 lies in
[0.0082007206…, 0.0625641181…], so J2 > 0.

**Finite-b sign, certified conditionally on a strict smaller range only:** H_b(T) > 0 for every

    0 < |b| < 0.00261209,

the certified lower end of b* = (J2_lo / C_one,TR)^{1/2} = 0.0026120932319102… rounded down.
**|b| = 0.003, and every |b| with 0.00261209 ≤ |b| ≤ 0.003, remain unresolved.**

**Rule (D) fails.** This refers to the preregistered target comparison of PLAN.md, not to a defective
formula. The independent review found no defect in the inequalities of either stage. (D) asks whether
the certified bounds are sharp enough to decide the sign on the whole fixed range, and they are not:

    J2_lo  >  β² · C_one,TR,
    0.0082007206804663…  >  0.0108172578374079…      (not satisfied),

so the certified lower bound on H_b/b² at |b| = 0.003 is −0.0026165371569… and the sign there is
undetermined. This is a statement about these bounds; it is not evidence that H_b(T) is negative for
any b. C_one,TR ≤ 1201.9175374897… (λ = 10⁶, the best of the preregistered list) is the time-resolved
one-sided remainder constant, down from 6798.81 for the global one. (D) would hold with either
C_one,TR < 911.19… at the present J2 lower end, or a J2 lower end above 0.0108172578…, which with the
present remainder needs a bound |M| < 0.024523 in place of the current 0.027140.

All of this is conditional on the inherited assumptions listed below.

## Review status

- **First stage** (DERIVATION.md Sections 0–4, scripts/sign_enclosure.py): one independent AI review,
  no blocking or major issue; REVIEW.md §1.
- **Second stage** (PLAN.md sections A–F, scripts/tr_remainder.py): one independent AI review by the
  session "Navier Stokes-Speech", completed. It accepted the estimate conditionally on the inherited
  assumptions, found no defect in the inequalities, and requested four non-blocking repairs, applied
  in the audit-repair commit; REVIEW.md §2. Neither review is human refereeing or formal verification.

## Independently reproduced, checked by construction, and inherited

**Independently reproduced:**
- The first-stage enclosure: the first reviewer reran sign_enclosure.py with identical output and
  recomputed ‖V(T)‖, |M| and the lower end of J2 in plain mpf to about 45 digits.
- Every per-cell chain row: scripts/verify_percell.py recomputes the absorption chain recursion in
  mpmath, independently of the decimal implementation, and matches all 250 rows × 11 fields of
  results/chain_percell.json with maximal relative difference 2.7×10⁻³⁴ (results/percell_verification.json).
  The second reviewer also regenerated chain_percell.py byte for byte, reran it and matched every row.
- Formulas A–F: the second reviewer's own implementation, on the parent's decimal interval class,
  reproduced N_r, E_r, N̄ and C_one,TR at all five λ, D_w,TR(T), the lower end of J2, the decision and b*
  with directed rounding.
- The repaired scripts reproduce every numerical and decision field of the preserved outputs.

**Checked by construction, not reproduced:** the collapse check, which only confirms consistency with
the global constants and cannot detect a source-cell weight error; the synthetic and toy-equation
tests of scripts/test_tr.py.

**Inherited, not re-checked here:**
- the absorption certificate (validated enclosures, Lemma M, the closure, and its platform model:
  IEEE binary64 round-to-nearest, gradual underflow, no fused multiply-add);
- the parent note at cd9c9f0: C_A ≤ 4.06707921080, the analytic base-flow bounds, (I1)–(I6), the
  mean-zero Agmon inequality;
- the Route B dissipation estimate and the tightening's Lemmas A and B;
- the z2-endpoint enclosure: G ≤ 1.8534 and the interval for ½‖∇q₁(T)‖²;
- the source-only hull bounds;
- correct Python decimal and mpmath interval arithmetic.

## Lemma M, cell by cell

Lemma M (absorption-b003 NOTE §8.3) is phrased at T, but its argument applies to every cell. Each cell
update of the chain combines the previous cell's values and the validated inputs through sums,
products, exponentials and square roots of nonnegative quantities in which |b| and b² enter with
nonnegative coefficients and the previous values enter monotonically. By induction over the cells,
every per-cell row value computed at b = 0.003 is at least the same row value at any |b| ≤ 0.003, and
for each such b the row value bounds its quantity on [0, t_{j+1}], because the closure holds on all of
[0, T]. So every per-cell row used in sections A–F is valid uniformly for |b| ≤ 0.003, and A–F replace
|b| by β = 0.003 only where it appears with a nonnegative coefficient.

## Audit repairs applied

1. **Pins.** source-only-hull/results/full.json (SHA-256 0d2ab266…), which sets J2's lower end, is now
   pinned in both sign_enclosure.py and tr_remainder.py. sign_enclosure.py had no pins and now pins
   all six inputs it reads. tr_remainder.py also pins the per-cell file, the generated chain script,
   and requires the per-cell file to be the one whose 250 rows were verified.
2. **Toy-equation tests**, scripts/test_tr.py, six tests, testing the same functions the calculation
   imports from scripts/tr_core.py:
   - On an exact piecewise-constant toy equation, the inclusive cell weight bounds the solution (exact/bound
     ≤ 0.885), and the weight that excludes the source cell is rejected.
   - In 4000 exact-rational trials the implemented summation by parts never fails. The broken forms fail:
     without the majorant 1541 times, without the end term 2393 times, with a shifted index 584 times, and
     with cell differencing of cumulative bounds 1541 times. The first and last are the same expression
     algebraically, so they are one broken form detected once, not two independent detections.
3. **All 250 per-cell rows verified,** as above.
4. **Wording:** Lemma M's per-cell coverage and the completed review status, as above.

## What was run

| run | wall time | outcome |
|---|---|---|
| sign_enclosure.py, first stage, to capture full output | 0.2 s | J2 > 0 |
| chain_percell.py, generated per-cell copy of absorb_chain.py | 0.8 s | per-cell rows |
| tr_remainder.py, first attempt | about 7 s | failed in a display helper; no result written |
| tr_remainder.py | 28.2 s | (D) not satisfied; results/tr_remainder.json |
| audit repairs: test_tr.py, first invocation | 0.1 s | import failure under -I; no test executed |
| audit repairs: verify_percell.py | 1.3 s | all 250 rows × 11 fields verified |
| audit repairs: sign_enclosure.py, pinned | 0.2 s | output identical to the preserved one |
| audit repairs: tr_remainder.py, pinned and refactored | 27.3 s | every numerical and decision field identical; output not kept, regenerated after the status-label fix below |
| audit repairs: test_tr.py | 0.6 s | 6 tests pass |
| audit repairs: tr_remainder.py, status label updated | 28.1 s | every numerical and decision field identical; results/tr_remainder.repaired.json |

Audit-repair numerical execution totalled about 58 s, under the five-minute cap. The repaired output's
plan hash differs from the preserved one only because a status line was appended to PLAN.md after the
run; the preregistered text is unchanged.

## Corrections to the earlier assessment

- **The 2335 cutoff is a heuristic comparison, not an exclusion certificate.** It was C < J2/β² with
  J2 ≈ 0.02101 taken from the uncertified N = 24 hierarchy in finite-time/results/measurements.json.
  It does not prove that a constant above 2335 rules out every J2 improvement; the true J2 is not
  certified to be near 0.021. The certified statement is weaker: every valid lower bound on J2 is at
  most its certified upper end 0.0625641181…, so only C_one > 0.0625641181…/β² ≈ 6951.57 would
  rigorously exclude resolving (D) by improving J2 alone.
- **The 3.6% figure is a heuristic comparison, not an exclusion certificate.** It compared the
  certified bound ‖V(T)‖ ≤ 0.014644 with the uncertified N = 24 value ‖∇V̄(T)‖ = 0.014139, which
  bounds ‖V(T)‖ only through Poincaré. It does not show that norm-only bounds on M are nearly
  exhausted: the true ‖V(T)‖ may be well below ‖∇V̄(T)‖, the N = 24 value has no error control, and
  the Cauchy–Schwarz step against ΔU(T) is not quantified.

## Failed attempts, preserved

- `attempts/sign_enclosure.attempt1.py`: aborted in a reporting line on `float()` of a non-point
  interval, after every enclosure had printed. Reconstructed after the fact; replaying the recorded
  patch reproduces the original scripts/sign_enclosure.py byte for byte, and the failing statement is
  on the line the traceback names (58). Output: `attempts/sign_enclosure.attempt1.output.txt`.
- `attempts/tr_remainder.attempt1.py`: aborted in the outward-display helper (mpmath's nstr formats an
  interval endpoint with brackets, so Decimal rejected it) after the synthetic checks, the per-cell
  chain check and the first λ had passed. No JSON was written. Fix: convert the point interval to mpf
  first. Output: `attempts/tr_remainder.attempt1.output.txt`.
- `attempts/test_tr.invocation1.output.txt`: `python3 -I -m unittest test_tr` could not import the
  module, because -I keeps the current directory off sys.path. No test executed. Fix: run the test file
  as a script, which adds its own folder.

## Files

- `DERIVATION.md`, `REVIEW.md`, `PLAN.md`, this README.
- `scripts/`: sign_enclosure.py; make_chain_percell.py and the generated chain_percell.py; tr_core.py
  (cell weights, majorant, summation by parts); tr_remainder.py; test_tr.py; verify_percell.py.
- `results/`: the preserved outputs (sign_enclosure.output.txt, chain_percell.json and its output,
  tr_remainder.json and its output), and the audit-repair outputs (percell_verification.json and its
  output, sign_enclosure.repaired.output.txt, tr_remainder.repaired.json and its output, test_tr.output.txt).
- `attempts/`: the three failed attempts with their verbatim output.
- `SHA256SUMS`.

Reproduce from `scripts/`, with `<FT>` the finite-time folder and fresh output paths:

    python3 -I test_tr.py -v
    python3 -I sign_enclosure.py <FT>
    python3 -I make_chain_percell.py && python3 -I chain_percell.py --json <new>/chain_percell.json
    python3 -I verify_percell.py <FT> <FT>/endpoint-sign/results/chain_percell.json <new>/percell_verification.json
    python3 -I tr_remainder.py <FT> <FT>/endpoint-sign/results/chain_percell.json <new>/tr_remainder.json

tr_remainder.py reads the verification record from results/percell_verification.json and accepts only
the pinned per-cell file.
