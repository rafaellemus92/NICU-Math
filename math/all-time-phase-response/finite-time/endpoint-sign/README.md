# Endpoint sign of H_b(T) = Z(u_b(T)) − Z(U(T)) − b² e^{−2νT}/4: local research folder

Local research only: branch `claude/endpoint-sign-research` based on f4fe230, not pushed, not merged.
Author: Claude, session "Inviscid run convergence past max|ω|", 19 October 2026. Fixed scope and
target, unchanged throughout: a = c = d = 1, ν = 1/28, φ = 37/100, T = 1/4, the sign of H_b(T) for
every 0 < |b| ≤ 3/1000. No trajectory was read, and no adjoint, q₂, DNS or validator run was made.

## Result

**Coefficient sign, certified conditionally (first stage, independently reviewed):**
J2 = Z2(T) − e^{−2νT}/4 lies in [0.0082007206…, 0.0625641181…], so J2 > 0. Conditional on the
inherited certificates listed in DERIVATION.md; reviewed in REVIEW.md.

**Finite-b sign over the fixed range: not certified.** The exact unresolved inequality is the
preregistered rule (D) of PLAN.md,

    J2_lo  >  β² · C_one,TR,
    0.0082007206804663…  >  0.0108172578374079…      (fails),

so the certified lower bound on H_b/b² at |b| = 0.003 is −0.0026165371569… and the sign there is
undetermined. C_one,TR ≤ 1201.9175374897… (λ = 10⁶, the best of the preregistered list) is the
time-resolved one-sided remainder constant, down from 6798.81 for the global constant. (D) would hold
with either C_one,TR < 911.19… at the present J2 lower end, or a J2 lower end above 0.0108172578…,
which with the present remainder needs a bound |M| < 0.024523 instead of the current 0.027140.

Information only, not the target and resting on the unreviewed second stage: with C_one,TR the positive
sign holds for 0 < |b| < 2.612093×10⁻³ (first stage alone: 1.098271×10⁻³).

## What was run

| stage | wall time | outcome |
|---|---|---|
| sign_enclosure.py (recorded first stage, rerun once to capture full output) | 0.2 s | J2 > 0 |
| chain_percell.py (generated copy of absorb_chain.py, per-cell log) | 0.8 s | rows at every 50th cell and final values identical to the committed chain.json |
| tr_remainder.py, first attempt | about 7 s | failed in a display helper after the checks passed; no result written |
| tr_remainder.py | 28.2 s | collapse checks, synthetic checks, monotonicity checks passed; (D) not certified |

Total numerical execution of the second stage was about 36 s, under the five-minute cap.

The collapse check runs the same code with global inputs and weights and reproduces
route-b-tightening's N_r, E_r and N̄ for all five λ to better than 10⁻²⁵ relative. Every
time-resolved quantity is below its global counterpart. The largest remaining term is the mean
self-interaction of w, 603.16 of N̄ ≤ 615.50 at λ = 10⁶; the time-resolved retained dissipation is
D_w ≤ 26061.11 against the global 50101.78.

## Status of each step

- DERIVATION.md Sections 0–4 and sign_enclosure.py: new, reviewed once, no blocking or major issue.
- PLAN.md sections A–F and tr_remainder.py: new derivation and code, **not independently reviewed**.
  They were preregistered in PLAN.md before any run. Anything that rests on them, including
  C_one,TR and the 2.612×10⁻³ range, is conditional and pending its own review. The negative
  decision concerns this bound only; it is not evidence that H_b(T) is negative at any b.

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
  patch reproduces scripts/sign_enclosure.py byte for byte, and the failing statement is on the
  line the traceback names (58). Output: `attempts/sign_enclosure.attempt1.output.txt`.
- `attempts/tr_remainder.attempt1.py`: aborted in the new outward-display helper (mpmath's nstr formats
  an interval endpoint with brackets, so Decimal rejected it) after the synthetic checks, the per-cell
  chain verification and the first λ had passed. No JSON was written. Fix: convert the point interval
  to mpf first. Output: `attempts/tr_remainder.attempt1.output.txt`.

## Files

- `DERIVATION.md`, `REVIEW.md`, `PLAN.md`, this README.
- `scripts/`: sign_enclosure.py (reviewed), make_chain_percell.py and the generated chain_percell.py,
  tr_remainder.py.
- `results/`: sign_enclosure.output.txt, chain_percell.json and its output, tr_remainder.json and its output.
- `attempts/`: the two failed attempts with their verbatim output.
- `SHA256SUMS`.

Reproduce from `scripts/` with `<FT>` the finite-time folder:

    python3 -I sign_enclosure.py <FT>
    python3 -I make_chain_percell.py && python3 -I chain_percell.py --json <new path>/chain_percell.json
    python3 -I tr_remainder.py <FT> <new path>/chain_percell.json <new path>/tr_remainder.json
