# Shared Air: what ChatGPT's "proof audit" got right, what it overstated, and what we changed

ChatGPT wrote a "Shared Air proof audit": a package of `proof_notes.md` (proofs), a
standard-library Python checker, its output (`audit_results.json`) and a README. It is not copied here.
It worked from a Markdown description of the model. By its own account the live page did not load,
so it never saw the simulator code.

We then checked it in three rounds:

1. Five independent verifiers (algebra, meaning, ablation, water/phase/statistics, literature) checked
   each claim against the page's own code. Three challengers then tried to refute the verifiers.
   Record: `results/verifier_findings.json`. Claim IDs below (C1, K7, M3, A2 …) point into that file.
   Its line numbers refer to the original page.
2. A 200-seed rerun settled the one real disagreement (section 4). Record: `results/adjudication/`.
3. We corrected the page, and two reviewers checked the corrections. Record: `results/review_findings.json`.

Numbers marked "(our rerun)" are printed by a script in `tools/`. The saved output is in `results/checks/`.

**Terms.** *g* (the page's "responsiveness" K) is how strongly mom is moved by the infant and acts on
it. *τ* is mom's response delay. *Aᵢ* and *Aₘ* are the infant's and mom's arousal (0 at rest).
*Steadiness* is the page's slider for how fast mom settles on her own (default 1).
*ρ(g)* is the slowest decay rate of the simplified linear model (noise off, near rest). Its inverse
is the longest time constant. *g\** is the gain where ρ is largest. *g_c* is the gain past which the
rest state is unstable at every delay. *Test 4* gives the infant a heel stick at 80 s, then times how long the
infant's heart rate takes to get back within 10 bpm of baseline and stay there 15 s. A run that does
not manage this within the 140-s window is counted as *never recovering*. *cap* is mom's capacity to
soothe, which halves when her arousal reaches 0.8. *DEF* is the block of stored results inside the
page (DEF.sweep for Test 4, DEF.pulse for Test 5b, DEF.room for Test 1).

Two terms from dynamics. A *saddle-node* is the point where a new pair of steady states appears, one
stable and one not. A *Hopf* point is where a steady state starts to oscillate on its own.

## 1. What ChatGPT claimed

| ID | Claim | Verdict |
|---|---|---|
| C1 | Linearization near rest, and the delayed characteristic function D(s,g,τ) | holds |
| C2–C5 | Completing-the-square theorem: ρ(g) has exactly one maximum, at g* ≈ 0.0804; rest is stable for g < g_c ≈ 3.858 (τ = 0) | holds, under its stated conditions |
| C6 | For g > g_c the rest state is unstable at every delay; "delay is not required" for the effect | first half holds; second half partly |
| C7 | Headline: a finite coupling maximizes recovery speed; more coupling slows recovery and destabilizes | overstated |
| C8–C9, C14 | Water-compartment results: aggregation identity, free-energy decay, equilibrium ratio | hold |
| C10 | Two cell groups with the same average synchrony can change at different rates | holds |
| C11 | 2:1 locking threshold: a₂ = 0.1865; the formula is first-order only | holds; error measured at +21% |
| C12 | Subtracting correlations can create a "bond" from unequal noise alone | holds; bites in the model only off-protocol |
| C13 | A textbook chapter swaps the Hartnoll (2000) AGA/SGA row | holds |
| C15 | The Test 4 sweep stops at g = 3 < g_c, so the theorem does not validate that plot | holds; the gap is wider than stated |

Several graded claims (the C6 phrase, the C7 headline, C8, C13, C14) are not in ChatGPT's package. They came
from its chat replies, which no verifier saw, so they were judged from a paraphrase (K1).

## 2. What holds

- **Linearization (C1).** This is the model simplified to small disturbances near rest. It matches
  the code exactly: the Jacobian residual is 0. The code differs from the page's displayed equations
  in small ways that do not touch the linearization. The cap uses max(Aₘ, 0), there are voice terms,
  and the shortest delay is one 0.02-s step. The page now shows the first two; the one-step minimum
  delay is still not shown.
- **The theorem (C2–C5).** Every step checks out symbolically. On 2,500 random parameter sets that meet
  its conditions it passes every check (627 of them needed 40-digit arithmetic). For the page's
  constants it gives:
  g* = 0.0803558863, ρ(g*) = 0.0482709206 /s (time constant 20.7 s),
  g_c = 15/8 + √2265/24 = 3.8580006724.
  ρ at g = 0, 1, 3, 4 is 0.033333, 0.038554, 0.012859, −0.002250 (our rerun, `theory_check.txt`).
  The conditions matter. At steadiness ≤ 2/3, which the slider allows, the best gain is g = 0. In the
  slider's range the conditions hold only for steadiness in (2/3, 19/9] (C5).
- **Unstable past g_c at every delay (C6, first half).** D(0, g, τ) does not depend on τ, so a root
  crossing at s = 0 crosses for every delay.
- **Water aggregation identity (C8).** Lumping cells with different water-to-solute ratios rᵢ into one
  compartment misstates the water flux. When permeability is proportional to solute, the error is
  Δ = K_tot Σ wᵢ (rᵢ − r̄)² / (rᵢ r̄²) ≥ 0. It is zero only when all ratios are equal.
  The identity passed 1,000 of 1,000 exact random checks. Without the proportionality the sign can
  flip (example: Δ = −7/30). The free energy is a strict Lyapunov function, and the stated
  exponential bound holds, though it is loose (true decay is a median 112× faster) (C9). The
  two-compartment equilibrium is V_I/V_E = n_I/n_E (C14).
- **Phase-moment counterexample (C10).** Z₁ is the average of the cells' phases as points on a
  circle; its length R is the synchrony index (1 = all in step, 0 = spread out). Two four-cell
  configurations both have Z₁ = 1/2. One has R′ = K/4 and the other R′ = 0, because their second
  moments differ (Z₂ = 0 vs 1). So synchrony alone does not say what happens next. Exact.
- **Correlation counterexample (C12).** Take a shared input U and independent unit noises:
  X = U + e₁, M = U + e₂, O = U + 3e₃. Then Corr(X,M) − Corr(X,O) = 1/2 − 1/√20 = 0.276, with no
  direct link from X to M. The covariance contrast is 0. Inside the model this does not bite under the
  test protocol, because the other parent is built and treated exactly like mom. The stored
  alike-world bond is −0.022 ± 0.055 (DEF.room). It does bite off-protocol (section 6).
- **Hartnoll row (C13).** The primary abstract reads: SGA 906 (833–954) vs AGA 844 (637–958) mL/kg,
  median (range), p = 0.019, N = 42 (Hartnoll, Bétrémieux, Modi, *Arch Dis Child Fetal Neonatal Ed*
  2000;83:F56–F59). The chapter's table prints the groups the other way round. Its own text says SGA
  was 62 mL/kg higher. Also confirmed: ECW is 60/86 = 0.698 of TBW at 24 weeks and 44/78 = 0.564 at
  term. StatPearls' 2/3 and 1/3 are fractions of TBW. The chapter's 35 AGA / 7 SGA split is
  unverified (only the chapter gives it).
- **The 2:1 harmonic (C11).** a₂ is the strength of the part of mom's pulse that repeats twice per
  beat, the part that can pull the infant toward 2:1. a₂ = 2e⁻² I₂(2) = 0.18647806660946678, found
  three ways, including the page's own code. ChatGPT's two references check out (Mori 2012, *J Math Biol*; Nakao 2016, *Contemp Phys*),
  as do the standard results behind its arguments (R5–R12, R15).

## 3. What is overstated

**The spectral optimum is not Test 4's optimum (C7, M1).** ρ is a property of the linear model's
slowest mode. For g above about 0.1–0.2, that mode is mostly mom's own relaxation (K13). Its rate can
never beat hers: ρ(g) < 1/20 /s for every g > 0, at every delay (M5). At default steadiness, coupling
can raise ρ by at most 1.5× over no coupling (the actual best is 1.448×). Test 4's median gets 3.8×
faster: 39.25 s at K = 0 against 10.25 s at K = 1 (stored 200-run curve). So ρ cannot be what Test 4
measures.

Why: a heel stick hits only the infant. It puts only 3–5% of its push into the slow mode, the
pattern that decays at rate ρ (infant-arousal amplitude 0.033–0.049 for g between 0.2 and 3.8).
That is already well inside the 10-bpm band, whose edge is at arousal 0.2232 (meaning verifier; M6). Getting back within 10 bpm is decided by
the fast infant-and-soothing pair, which decays at 0.14–0.17 /s. More coupling swings that pair back
faster. So Test 4 keeps improving far past g* = 0.08. Tightening the band does not rescue g*: the
best gain approaches g* only logarithmically. It gets within 50% of g* only for a band of about
10⁻²³ arousal units (M2).

**Where ρ does apply (M3, M4).** It applies to disturbances that reach mom. One example is the page's
alarm, which kicks the infant by +0.30 and mom by +0.35. There, recovery of the pair as a whole
tracks 1/ρ: rank correlation +0.94 to +0.99, with the best gain at 0.11–0.15. Over the worst case
across arousal kicks, the best gain is 0.07–0.10. These optima move with g* when steadiness
changes, which shows that ρ, not coincidence, sets them.

Our rerun is simpler: deterministic, a kick from rest, the last exit from the band. For the alarm, the
pair's arousal norm is fastest at g = 0.18, 0.14 and 0.11 for bands of 0.2232, 0.1 and 0.03. At
τ = 1.5 and the coarse band, the times at g = 0, 0.08, 0.5, 1, 2 are 16.90, 15.70, 16.92, 18.78 and
32.54 s. For the heel stick, with the infant's 10-bpm band as a proxy, the fastest gain is g = 2.98
at τ = 0.02 and g = 1.73 at τ = 1.5 (our rerun). So the two disturbances favour very different gains.

The pair-level optimum is flat. In noisy runs it shows up only when the same random noise is replayed
with and without the alarm, or in large ensembles.
A single run scored by the page's rule puts it at 0.35–0.75 (M4).

**"Delay is not required" (C6, second half).** ChatGPT's argument, the zero-delay optimum of ρ, does
not bear on Test 4. The verifiers also disagreed about the conclusion itself. The 200-seed rerun
below settles it: the delay is required for the rise in the median, but not for the runs that never
recover.

**C11** was graded "partly" by its verifier. The critic argued for "confirmed", since ChatGPT itself
called the formula first-order (K11). Either way, the size of the error matters, and section 5 gives it.

## 4. What actually makes Test 4's U-shape

Test 4 protocol, 200 fresh seeds (300000+i) per point. "Cap off" sets mom's soothing capacity to stay
at 1. τ = 0.02 s is the shortest delay the code allows (one step). Each cell gives the median
recovery in seconds, with the share of runs that never recover in brackets.

| K | τ 0.02, cap on | τ 0.02, cap off | **τ 1.5, cap on (default)** | τ 1.5, cap off |
|---|---|---|---|---|
| 0 | 38.875 (4.5%) | 38.875 (4.5%) | 38.875 (4.5%) | 38.875 (4.5%) |
| 0.5 | 12.25 | 11.75 | 12.875 | 12.5 |
| 1 | 9.5 | 9.125 | 10.5 | 10.25 |
| 1.5 | 8.375 | 8 | 11.25 | 18.875 |
| 2 | 7.75 (4%) | 7.25 | 22.625 (3.5%) | 23.75 |
| 2.5 | 7.5 (28%) | 7 | 25.25 (25.5%) | 36 |
| 3 | 7.75 (39.5%) | 6.75 | 49.75 (38.5%) | 48.5 (2%) |

Source: `results/adjudication/*.json`. Our standalone runner on the corrected page reproduces the
earlier run on the original page in every shared field (the stuck-aroused counts are new).

- **The delay lifts the median.** Without delay the median falls to about 7–7.5 s by K = 2 and
  stays there. With delay and no cap it still rises, from 10.25 s at K = 1 to 48.5 s at K = 3.
  Delayed soothing overshoots, and the rebound carries heart rate back out of the band. At τ = 1.5
  the noise-free rebound crosses +10 bpm near g = 2 (+9.8 bpm at 1.9, +10.3 at 2.0), and recovery
  jumps from 8.5 to 23 s (C15, meaning verifier).
- **The cap makes the never-recover tail.** With the cap on, 39.5% (τ 0.02) and 38.5% (τ 1.5) of runs
  never recover at K = 3. With the cap off, 0% and 2% do. Nearly every never-recovering run with the
  cap on ends with mom stuck aroused: 79 of 79 and 76 of 77 at K = 3. With the cap off, none of the
  4 never-recovering runs at τ = 1.5 is stuck aroused. Here "stuck aroused" means mom's mean arousal
  over the last 80 s is above 1.
  The cause is a saddle-node. With noise off, a second stable state, with both partners aroused,
  appears at g = 2.0689. Where the steady states sit does not depend on the delay; their stability
  was checked without delay. At g = 3 the stuck state has Aᵢ = 1.914 and Aₘ = 2.791, where cap is
  0.076. With cap = 1 no such state exists below g_c (our rerun). Noise pushes runs into it. Shared
  room noise lowers the threshold, so stuck runs already appear at K = 2 (review).
- **At τ = 3 (Test 4's second curve) the delay does more.** The rest state itself starts to oscillate
  at g = 1.6117 (period 20.7 s), inside the sweep (our rerun). Most never-recovering runs at K = 1.75–2.5
  oscillate; stuck-aroused runs take over from K = 3 (A13). The page's Euler step gives 1.5995, which
  converges to 1.6117 as the step shrinks (K10). At τ = 1.5 no oscillation starts below g_c. A Hopf
  crossing below g_c needs τ > 1.574 s (C6).

**How the disagreement arose.** The ablation verifier concluded that delay was not needed. It used
seeds 5000+i, the same block as the page's stored curve. A challenger found that block to be an
outlier: at τ = 0.02 and K = 3, 25/40 runs never recovered, against 11/40 on seeds 6000+i (Fisher
p = 0.003) and 161/400 on a large pool (A2). The 200-seed table shows both were partly right: the
cap explains the tail, and the delay explains the median.

The old page stored 14 runs per point. Those put the best setting at K = 2 and the K = 3 median at
140.25 s, the value scored for a run that never recovers. With 200 runs, the best setting is K = 1
(10.25 s), and K = 3 has a median of 50.125 s, with 82 of 200 runs never recovering. The corrected page at R = 14
reproduces the old curve exactly (`regen_def_R14.txt`). So the change comes from the number of runs,
not from a change to the model.

## 5. Exact 2:1 locking numbers (Test 5)

The model reduces the infant's pacemaker to one phase pushed by mom's heartbeat, with noise off, at
the stored rates: infant 149.59 bpm, mom 76.27 bpm, so the infant sits 2.95 bpm below twice mom's
rate (our rerun, `lock_proto.txt`, `quick_check.txt`).

| | first-order formula | exact |
|---|---|---|
| locking starts at pulse strength | 3.31 | **4.00** (same at three resolutions) |
| locking range closes again at | never | **19.7** |
| detuning reversed (+0.309 rad/s) | 3.31 | 2.95 |
| infant 10 bpm above 2:1 | 11.2 | **8.4** (closes at 33.7) |
| infant 10 bpm below 2:1 | 11.2 | **never** (up to 40) |

Second-order averaging, the next step of the same approximation, explains the gap. The pulse also slows the cell slightly on average, by
0.00396 ε² rad/s. That works against the pull toward 2:1 when the infant is below the ratio, and
helps it when the infant is above (C11, K7). A noise-free 16-cell population locks at about 4.10
(median of 12 draws; C11).

In the full noisy model nothing locks fully. The page's locking index runs from 0 (no fixed beat
timing) to 1 (perfect lock). At pulse strength 16 it is only 0.426 (other parent 0.075). Removing breathing swings raises it to 0.576. Removing breathing swings, noise
and alarms raises it to 0.832 (review). The index checks only 1:1, 2:1 and 3:1. So a 3:2 rhythm shows
up as 3:1, and 4:3 or 5:3 read near 0 (0.0005, 0.0011; review).

## 6. The room-subtraction caveat

Tests 1, 2 and 3 subtract the infant–other-parent correlation from the infant–mom correlation. In the
alike world there is no bond, so the difference should average zero. It does only when the two
adults are treated alike. Here are 300-s sessions, alike world, as mean ± SEM (our rerun,
`room_check_N60.txt`, `room_check_N100.txt`):

| mom | 60 sessions (seeds 1000+i) | 100 sessions (seeds 20000+i) |
|---|---|---|
| awake, skin-to-skin (test protocol) | −0.037 ± 0.034 | −0.020 ± 0.021 |
| asleep | −0.123 ± 0.037 | −0.116 ± 0.024 |
| out of the room | −0.206 ± 0.042 | −0.225 ± 0.031 |

The cause is the alarms. Asleep, mom gets half the alarm kick; out of the room, she misses it. With
the lower asleep set point removed the effect stays (−0.108), and with the full kick restored it
mostly goes (−0.048) (review). In the live view's single 90-s window the sign is unreliable: the
difference reads below zero in 59–66% of windows with mom asleep or away, against 46–50% with her
awake (review). The tests themselves keep both adults awake and present, so their stored results
are unaffected. Real data would need a control adult matched to mom.

## 7. Corrections made to the page

The full diff, with the stored-results line left out, is `results/corrections.diff`.

- **Locking (Test 5).** New `locked21`/`lockRange21` in the model: the exact 2:1 range for one forced
  phase, found from the RK4 period map. `expPulse` now stores the exact onset, the closing strength and
  the ±10 bpm onsets. The finding text and chart now give first-order and exact values side by side.
  The 10-bpm case is split into above and below. The push percentage uses the hypothetical infant's
  own rate (34%). The equations block calls the formula "to first order".
- **Test 4 mechanism.** "The response overshoots" became two named mechanisms: the delayed rebound,
  and the capacity to soothe giving out. The stuck state "from a responsiveness of about 2" and the
  oscillation above about 1.6 at a 3-s delay are stated only for default settings. "Those are the
  runs that never settle" appears only when some runs never settle. Ties are shown (0.5–0.75). The
  bedside text now says the pair-level rate is best below 0.1 and explains why that is a different
  measure.
- **Test 4 data.** The stored curves use 200 runs per point (was 14). A run with your settings uses
  30. The description says a later relapse doesn't count.
- **Room subtraction.** Caveats were added to the live note, to Test 1's bedside box and to Test 2.
- **Literature wording.** Jaffe, Beebe and colleagues: mid-range coordination at 4 months was optimal
  for attachment at 12 months. Van Leeuwen: paced breathing, more epochs than surrogates at fast
  rates, an earlier larger study with about as many epochs in surrogates. "The authors conclude the
  coupling is present but weak." The unverified "six mothers" and "no direct path through breathing
  movements" were removed.
- **Display matches code.** The page now shows: 16/8 cells in the batch tests (24/12 live); the V
  clamp; A⁺ in cap; the voice terms; and that the synchrogram index covers only 1:1, 2:1 and 3:1.
- **One code fix.** Voice now raises the infant's vagal tone only when mom is present, as the voice
  arousal terms already required.

## 8. Independent review of the corrections

Two reviewers checked an intermediate version (`results/review_findings.json`). They found **no
blockers**. Every number the edits rely on reproduced. That includes the stored data from a fresh
run, the saddle-node at 2.069, the Hopf at 1.61, the onset of 4.0002 at every resolution, the range
closing at 19.71, +10 bpm from 8.376 and −10 bpm never. The page loaded without errors at 1100 px
and 390 px, in light and dark, with no horizontal scroll. There was no NaN in any text for any
slider setting or injected edge case.

They raised 11 should-fix items and 10 nits, a few found by both reviewers. Examples: the 3:2
sentence was wrong; "drags the cells slower" misdescribed the net effect; the push percentage used
the wrong rate; two finding sentences vanished on a default rerun; chart labels overlapped at phone
width. **All were applied.** One
change followed: the default user-run count dropped from 40 to 30 runs, to cut the wait (the
reviewer timed 40-run reruns at 41–44 s in headless Chromium).

The final page has not had a second full review. On it we reran: the DEF.pulse comparison, the full
200-run DEF.sweep regeneration (identical, 2 min 18 s), the locking checks and the Chromium check
(no errors, no overflow; `render.txt`).

## 9. Still open, or deliberately unchanged

- Test 4 scores the *first* 15-s hold in band, so later relapses are missed. The page now says so;
  the rule is unchanged (A14, K15).
- Without any heel stick, some high-K runs still score as "never recovering": at K = 3, τ = 1.5,
  10 of 40 on seeds 5000+i (the outlier block of section 4) and 6 of 40 on seeds 6000+i (A9). So the test partly measures
  getting stuck, whether or not there was a stick.
- The equations block does not say that the code's delay is at least one 0.02-s step. So the
  zero-delay theorem describes a setting the code cannot run (the slider also starts at 0.5 s).
- Cell phase noise is not scaled with the time step (a hidden calibration constant; no test changes
  dt). The recorded infant heart rate reads high under strong pulse forcing: 150.48 against 143.84 bpm
  by beat count at strength 16, and about 0.9 bpm at the default 6 (water/phase/statistics verifier).
- The "room is subtracted" wording in Test 2's bedside box and finding, and in Test 3, is kept. It is
  valid under the test protocol, where the two adults are matched.
- Literature: the "tighter coordination went with less secure attachment" reading rests partly on
  a mid-range optimum stated in the abstract and partly on a secondary source (K18). Not settled.
- Whether any of this holds in real pairs is open. The model's parameters are illustrative, not fitted.
