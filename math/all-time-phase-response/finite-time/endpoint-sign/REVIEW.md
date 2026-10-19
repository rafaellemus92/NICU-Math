# Independent review of the first stage (DERIVATION.md Sections 0–4, scripts/sign_enclosure.py)

One read-only reviewer (a single AI agent, no sub-agents, no network, no file writes), briefed with the
derivation, the script, its recorded output and the inherited inputs at f4fe230, and asked for
CONFIRMED / ISSUE / NOT CHECKED on seven items. It ran the script, whose output matched
results/sign_enclosure.output.txt exactly, and an independent plain-mpf recomputation at 50 digits
that reproduced ‖V(T)‖ ≤ 0.0146439795…, |M| ≤ 0.0271397025… and the lower end of J2,
0.0082007206804663…, to about 45 digits. This is AI review, not human refereeing or formal verification.

Outcome: no blocking or major issue; Sections 1–4 hold as stated, conditional on the inherited
certificates.

| item | outcome |
|---|---|
| 1. time-weighted propagator (1)–(2), per-cell m₁ endpoints, positivity of m₁ − ν | confirmed; m₁(t) ≥ γ = 2 > ν |
| 2. cell coverage and pairing of U_ℓ with its own factor | confirmed; minor: row order not asserted |
| 3. q₁ error forcing ΔF charged once at e^{τ₀}; no differencing of cumulative bounds | confirmed |
| 4. outward rounding | confirmed for every decision; minor: several displays rounded inward |
| 5. one-sided identity (5) and bound (6), uniformity in \|b\| | confirmed |
| 6. strict smaller-b conclusion, b* < β, nothing claimed for b* ≤ \|b\| ≤ β or at b = 0 | confirmed; minor: b* < β not asserted |
| 7. overstatement | minor: "certified"/"proved" labels in the printout lack "conditional"; 911.2 rounded in the wrong direction (911.19); hard-coded uncertified values not attributed to finite-time/results/measurements.json |

Display corrections recorded here, scripts/sign_enclosure.py and its output unchanged:

- J2 is certified in [0.0082007206…, 0.0625641181…]; rounded outward to six decimals it is
  [+0.008200, +0.062565], not the printed [+0.008201, +0.062564]. The sign is unaffected.
- The one-sided remainder at |b| = 0.003 is ≤ 0.0611893015, printed 0.061189; E − e^{−2νT}/4 has upper
  end 0.0354244…, printed 0.035424; the recorded |M| bound is 0.0418803…, printed 0.041880.
- The required constant for the fixed range with the current J2 lower end is C < 911.19, printed 911.2.
- b* = 1.09827100221×10⁻³ (certified lower end); the printed 1.098271×10⁻³ is below it.

The reviewer's recommendations (outward display, assertions on row order, G ≤ 1.8534 and b* < β,
"conditional" labels) were applied to the second-stage script tr_remainder.py before its first run.
The reviewer did not cover PLAN.md sections A–F or tr_remainder.py.
