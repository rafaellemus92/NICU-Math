# Shared Air: what ChatGPT's "proof audit" got right, what it overstated, and what we changed

ChatGPT wrote a "Shared Air proof audit": a package of `README.txt`, `proof_notes.md` (proofs), a
standard-library Python checker `verify_shared_air.py` and its output `audit_results.json`. It is kept
as uploaded in [`../inputs/shared_air_proof_audit.zip`](../inputs/shared_air_proof_audit.zip).
It worked from the Markdown text of the model, [`../inputs/Shared_Air_Model_v1.md`](../inputs/Shared_Air_Model_v1.md).
The lines it cites (equations 196–205, limits 216–218 and 221) match v1. v2 keeps the same line
numbers but changes one of them: line 205, the locking condition, now says "to first order in weak
forcing" (section 10, edit 5). v2 also says it was revised after this audit, so the audited text is v1. By its own account
the live page did not load, so it never saw the simulator code.

The corrected page is [`../../web/public/shared-air/index.html`](../../web/public/shared-air/index.html),
live at https://nicu-math.vercel.app/shared-air. We built it from the original page, whose text is v1
(the removed lines in `results/corrections.diff` are v1's text). We did this independently of the v2
revision of the text (section 10).

We then checked it in three rounds:

1. Five independent verifiers (algebra, meaning, ablation, water/phase/statistics, literature) checked
   each claim against the page's own code. Three challengers then tried to refute the verifiers.
   Record: `results/verifier_findings.json`. Claim IDs below (C1, K7, M3, A2 …) point into that file.
   Its line numbers refer to the original page.
2. A 200-seed rerun settled the one real disagreement (section 4). Record: `results/adjudication/`.
3. We corrected the page, and two reviewers checked the corrections. Record: `results/review_findings.json`.

Numbers marked "(our rerun)" are printed by a script in `tools/`. The saved output is in `results/checks/`.
Section 11 lists the Lean proofs and the numerics elsewhere in this repository behind each claim.

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

Some graded claims are not in ChatGPT's package: the C6 phrase, the C7 headline wording and C13.
Others are there only in part. The package has C8's counterexample (`proof_notes.md` §3.2). It also
checks the identity behind C8's Δ at one point (gap 1/3, `verify_shared_air.py`), but it never writes
Δ or its conditions. C14's ratio is not written either, but it follows at once from the equilibrium
vᵢ* = W nᵢ/(n_E + Σnⱼ) in §3.1. Its "K sets only the time scale" clause is absent. The missing parts came
from ChatGPT's chat replies, which no verifier saw, so they were judged from a paraphrase (K1).

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
  moments differ (Z₂ = 0 vs 1). So synchrony alone does not say what happens next. Exact. Lean
  proves the same pair, repeated six times to make 24 cells, the model's pacemaker count
  (`same_synchrony_different_future_24`). One nuance: on the Ott–Antonsen manifold, where
  Z₂ = Z₁², Lean's Z₁′ = (K/2)(Z₁ − conj(Z₁) Z₂) (`Z1dot_eq`) becomes R′ = (K/2)R(1 − R²), which is
  3K/16 at R = 1/2. There R does fix its own future. So "R alone does not determine its future" is a
  statement about arbitrary phase configurations.
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
  as do the standard results behind its arguments (R5–R12, R15). ChatGPT also warned that a 2:1
  index built on the first circular moment can read 0 under perfect 2:1 locking (Lean:
  `two_to_one_moments`). That does not apply to the page: its index (`pliMax`) takes the best of
  the 1st, 2nd and 3rd harmonics.

## 3. What is overstated

**The spectral optimum is not Test 4's optimum (C7, M1).** ρ is a property of the linear model's
slowest mode. For g above about 0.1–0.2, that mode is mostly mom's own relaxation (K13). Its rate can
never beat hers: ρ(g) < 1/20 /s for every g > 0, at every delay (M5). At default steadiness, coupling
can raise ρ by at most 1.5× over no coupling (the actual best is 1.448×). Test 4's median gets 3.8×
faster: 39.25 s at K = 0 against 10.25 s at K = 1 (stored 200-run curve). So ρ cannot be what Test 4
measures. ChatGPT's package itself says so (`proof_notes.md`: ρ "is not the finite-threshold recovery
statistic used in Test 4"); the overstated headline is from its chat replies.

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
at τ = 0.02 and g = 1.73 at τ = 1.5 (our rerun). 2.98 is the edge of the swept range 0–3, so the
zero-delay optimum may lie higher. So the two disturbances favour very different gains.

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

- **The delay lifts the median.** Without delay the median falls to about 7.5–7.75 s from K = 2 with
  the cap on (6.75–7.25 s with it off) and stays there. With delay and no cap it still rises, from
  10.25 s at K = 1 to 48.5 s at K = 3.
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
  0.076. With cap = 1 no such state exists below g_c (our rerun).
- **Noise, not the heel stick, carries runs into the stuck state.** With all arousal noise off, the
  +1 heel stick never leaves the pair stuck for g = 0, 0.25, …, 3, at τ 0.02 or 1.5. At g = 3 the
  smallest infant kick that does is 1.33 (τ 0.02) or 1.41 (τ 1.5) over a long run, and 1.37 or 1.47
  within Test 4's window (our rerun, `kick_check.txt`). So the second state is there, and a large
  enough disturbance does flip the pair, but the heel stick alone is not large enough. Shared room
  noise lowers the threshold, so stuck runs already appear at K = 2 (review).
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

The v2 text's "removing it changes almost nothing" (section 10) is what that block shows. On the
page's 14 stored runs (seeds 5000+i) the K = 3 median is 140.25 s at both delays, with 11 of 14
(τ 0.02) and 10 of 14 (τ 1.5) never recovering (our rerun, `adjudicate_R14_seeds5000.txt`). Even
there the delay doubles the K = 2.5 median (9.75 against 20.875 s). On 200 fresh seeds the sentence
does not hold for the median.

The old page stored 14 runs per point. Those put the best setting on the default τ = 1.5 curve at
K = 2 and the K = 3 median at
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
and alarms raises it to 0.832 (review). The index (`pliMax`) is the best of the 1st, 2nd and 3rd
harmonics, so it checks only 1:1, 2:1 and 3:1, and the first-moment problem of section 2 does not
arise. A 3:2 rhythm shows up as 3:1, and 4:3 or 5:3 read near 0 (0.0005, 0.0011; review). Lean proves
the exact version for a perfect lock: a harmonic index counts bands, not ratios
(`three_two_looks_like_three_one`, `four_three_hidden`, `five_three_hidden` in Limits/Ratios.lean).

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
are unaffected. Real data would need a control adult matched to mom. This corrects the v2 text's
live-view note (v2 line 47), which calls the two adults matched in every condition.

**The same mother, awake against asleep, is not a matched control either.** With the same seeds, the
infant's and the other parent's series are identical in every condition (the alike world has g = 0),
so the table above also gives a within-mother comparison with no bond. Infant–mom synchrony is
higher with mom awake than asleep by +0.086 ± 0.013 (60 sessions, seeds 1000+i) and +0.096 ± 0.009
(100 sessions, seeds 20000+i), paired, mean ± SEM (our rerun, `within_mom_N60.txt`,
`within_mom_N100.txt`). That drop looks like a bond. Holding against not (skin-to-skin against the
bedside, mom awake) changes nothing in the alike world: every paired difference is exactly 0. So the
v2 text's "comparing the same mother across conditions (awake and asleep, holding and not) avoids
the problem" (v2 line 113) holds for holding and not, and fails for awake and asleep. The same caveat
applies to Lean's Limits/Mixture.lean, whose identification assumes the alike part is the same in
every condition: in the model that holds for responses of the infant alone, not for synchrony with
a mom who sleeps.

## 7. Corrections made to the page

The full diff, with the stored-results line left out, is `results/corrections.diff` (original page to
`web/public/shared-air/index.html`).

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
- **Literature wording.** Jaffe, Beebe and colleagues (2001): mid-range vocal-rhythm coordination at
  4 months predicted secure attachment at 12 months; higher coordination predicted disorganized or
  anxious-resistant attachment, and lower coordination avoidant attachment (as restated by the same
  authors, Beebe, Jaffe et al. 2010, PMC3763737). Van Leeuwen and colleagues (PNAS 2009, PMC2728950):
  six pregnant women breathing at paced rates; more epochs than surrogates at fast rates; "no
  evidence of a direct effect of maternal breathing movements on fetal heart rate". Their earlier,
  larger study found about as many epochs in surrogates (712 vs 741, BMC Physiol 2003), and a later
  one concludes the coupling is "present but generally weak" (PLoS ONE 2014). An earlier version of
  this correction removed "six" and the breathing-movements clause as unverified; both are in the
  PNAS text and were put back on 18 October (R14 note in `results/verifier_findings.json`).
- **Limits (18 October, after comparing with the v2 text).** The "truly fluid-coupled" bullet became
  "Life before birth": the fetus floats in amniotic fluid; in the placenta the two bloods are normally
  kept apart across a thin barrier, though a few fetal cells cross into the mother. A new bullet,
  "Ratios other than n:1", says what the locking index can and cannot see (section 5).
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
(no errors, no overflow; `render.txt`). The 18 October text edits (section 7, last three items)
changed no code; after them the same checks gave the same results.

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
- Literature: the "higher and lower coordination went with insecure attachment" reading now rests on
  the monograph authors' own restatement (Beebe, Jaffe et al. 2010), not only on a secondary source
  (K18). The 2001 monograph text itself was not seen.
- Whether any of this holds in real pairs is open. The model's parameters are illustrative, not fitted.

## 10. The v2 revision of the model text

[`../inputs/Shared_Air_Model_v2_revised.md`](../inputs/Shared_Air_Model_v2_revised.md) is the page
text revised on 16 October "after an independent audit by ChatGPT". Who revised it is not recorded.
It contains findings that need the simulator code, which ChatGPT did not see (the stuck state "above
about 2", "removing it changes almost nothing"), so whoever revised it ran the page. Our corrected
page was built from v1, independently of v2. v2 makes seven edits; line numbers are v2's.

| # | v2 edit | The corrected page | Verdict |
|---|---|---|---|
| 1 | Live note (47): the two adults "are matched in noise and exposure, so the difference isolates the bond" | Matched only while mom is awake and in the room | v2 is false in the live view with mom asleep or away (section 6) |
| 2 | Test 1 (113): the control adult must be matched to mom; "comparing the same mother across conditions (awake and asleep, holding and not) avoids the problem" | Asks for a matched control; makes no same-mother claim | Matching: agree. Same mother: holds for holding and not, fails for awake and asleep (section 6) |
| 3 | Test 2 (119): "with a matched control" | Test 2 caveat added | Agree |
| 4 | Test 4 (149): "the shape doesn't need the delay; removing it changes almost nothing", and the cap's second stable state above about 2 | Names both mechanisms: the delayed rebound and the cap | The second state is right (Lean Bistability.lean). "Changes almost nothing" holds on the page's 14 stored runs and for the never-recover tail, not for the median on 200 fresh seeds; the heel stick alone does not flip the pair (section 4) |
| 5 | Equations (205): 2:1 locking holds "to first order in weak forcing" | "to first order", plus the exact values | Agree (section 5) |
| 6 | Limits (222): "Life before birth. Even then maternal and fetal blood never mix …" | Same heading; the bloods are "normally kept apart", a few fetal cells cross, and the amniotic fluid is kept | "Never mix" is too strong; v2 also drops the amniotic fluid |
| 7 | Limits (223): "Ratios other than n:1. The locking index here detects 2:1 and 3:1" | Same heading; the index looks for 1:1, 2:1 and 3:1, a 3:2 rhythm reads as 3:1, and 4:3 or 5:3 read near 0 | v2 omits 1:1 and implies 3:2 goes unseen (section 5) |

The closing note (228) repeats edit 4 ("the inverted U in Test 4 turned out not to need the delay"),
which the 200-seed table does not support for the median. Two v1 passages that v2 keeps also differ
from the corrected page. "Fourteen runs per point" (143) describes the old page; the corrected page
stores 200. The Jaffe and Beebe sentence (149) names the mid-range and the high end but not the low
end, which the authors also report (section 7). v2's Van Leeuwen sentence (161, from v1) is right about the six mothers and the
breathing movements, and the corrected page now says both. v2 is kept as uploaded; these notes do
not change it.

## 11. Lean and numerics behind these claims

The Lean proofs are in [`../wyrd-mathlib/WyrdMathlib/`](../wyrd-mathlib/WyrdMathlib/) (Lean 4 with
Mathlib). The repository's Lean workflow builds them and fails on `sorry` or `native_decide`
(`../wyrd-mathlib/Audit.lean`). We did not rebuild them in this session. The results about the
model's dynamics are for the deterministic model at zero delay, except the delayed characteristic
function and the instability past g_c. Ratios, Direction and Mixture are exact statements about the
measures, not about the simulator. The Python cross-checks are in
[`../numerics/shared-air/`](../numerics/shared-air/) and
[`../numerics/shared-air-limits/`](../numerics/shared-air-limits/).

| Claim here | Lean | Numerics elsewhere |
|---|---|---|
| C1 linearization; delayed D(s, g, τ) | `SharedAir/Linearization.lean`: `hasFDerivAt_field`, `linField_eq_sysMatrix`; `SharedAir/Delay.lean`: `det_delayMatrix`, `Dd_eq_det`. Lean's field uses the displayed cap, without A⁺; at rest the two agree | `delay_crossing_xcheck.py` (state-space determinant = D(s)) |
| C2–C5 theorem, g*, its conditions | `SharedAir/Basic.lean`: `Hyp`, `complete_square`, `existsUnique_root_H`; `Dominant.lean`: `existsUnique_root_gt`, `re_le_of_root`; `Optimal.lean`: `optimal_coupling`; `Specific.lean`: `hyp_sharedAir`, `H_sharedAir`, `G_sharedAir`, `exists_optimum`, `optimum_bounds` (g* in (0.08035, 0.08036)) | `delay_argument_principle.py` (s*, g*) |
| g_c and C15 | `Optimal.lean`: `stable_iff`, `P_zero_pos_iff`, `P_gc`; `Specific.lean`: `gc_sharedAir`, `gc_bounds`, `stable_at_three` | `delay_crossing_xcheck.py` |
| C6, unstable past g_c at every delay | `Delay.lean`: `delay_unstable`; `Specific.lean`: `unstable_every_delay` | — |
| Section 4, delay thresholds (τ = 1.8356 at g = 3, 4.7613 at g = 1) and the τ = 3 Hopf | none | `delay_crossing_xcheck.py`, `delay_chebyshev_xcheck.py`, `delay_argument_principle.py`, `delay_newton_roots.py` |
| Section 3, M5 (ρ < 1/20 for g > 0) | at τ = 0 only: `Dominant.lean`: `P_neg_b` with `existsUnique_root_gt` (proved; not listed in Audit.lean) | — |
| Section 3, ρ is not Test 4's measure | `Optimal.lean` header; `Limits/Objective.lean`: `mom_untouched_iff`, `infant_best_moves_mom` | — |
| Section 4, the stuck state | `Limits/Bistability.lean`: `only_rest_upto_two`, `coarousal_exists_above_two`, `coarousal_stable_at_three`, `cubic_hurwitz`; with cap = 1: `no_coarousal_without_cap_general`, `only_rest_without_cap`. The page's A⁺ cap gives the same equilibria with Aₘ > 0, and one with Aₘ < 0 would be a no-cap equilibrium, which `no_coarousal_without_cap_general` excludes below g_c | `bistability_equilibria_sweep.py`, `bistability_proof_brackets.py`, `limits_checks.py` (g_sn 2.06888, state (1.91417, 2.79077), cap 0.07593) |
| C8 water | `SharedAir/WaterGradient.lean`: `aggregate_counterexample` (the 0 against 2/3 case) | — |
| C9, C14 water | `WaterGradient.lean`: `hasDerivAt_freeEnergy`, `dissipation_nonpos`, `dissipation_eq_zero_iff`, `equilibrium_eq`, `equilibrium_exists` | — |
| C10 phase moments | `SharedAir/PhaseMoments.lean`: `Z1dot_eq`, `same_synchrony_different_future_24`, `synchrony_rates` | — |
| C11 and section 5 | `SharedAir/Locking.lean`: `averaged_equilibrium_iff`, `averaged_stable_equilibrium_iff`, `two_to_one_moments`; `Limits/Ratios.lean`: `lockIndex_eq_one`, `lockIndex_eq_zero`, `three_two_looks_like_three_one`, `four_three_hidden`, `five_three_hidden`, `two_one_needs_second_harmonic`, `model_forcing_misses_n_m` | `limits_checks.py` (index tables) |
| C12 and section 6 | `SharedAir/Correlation.lean`: `corr_XM`, `corr_XO`, `contrast_pos_without_coupling`; `Limits/Direction.lean`: `room_leaks_when_unmatched`, `room_cancels_iff`; `Limits/Mixture.lean`: `additive_recover`, `additive_identified` (its constant alike part, see section 6) | — |

**No Lean counterpart.** These rest on the numerics and the node scripts here only:

- a₂ = 2e⁻² I₂(2) (Locking.lean says so in its header);
- the exact 2:1 locking thresholds of section 5 (`tools/lock_proto.js` is the reference);
- everything delayed beyond the characteristic function and the instability past g_c: the delay
  thresholds, the Hopf points, ρ < 1/20 at τ > 0, the rebound;
- everything noisy: the Test 4 table, the stuck-aroused counts, the room and same-mother tables;
- the size of the kick that flips the pair (Bistability.lean states it is not proved);
- the water identity Δ in general, its sign flip and the exponential bound of C9;
- C13, which is a literature check, not mathematics.
