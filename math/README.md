# math: proofs, audits and numerical checks

This folder holds the mathematics done with Claude between 16 and 18 October
2026. It is separate from the NICU evidence-search app at the root of this
repository: the app does not use anything here, and nothing here is clinical
advice.

The guide lists the work in roughly the order it was done. Each entry says what
it is, how certain it is, and where to find it.

**Status labels**

| Label | Meaning |
|---|---|
| **Proved in Lean** | A Lean 4 proof that the Lean kernel has checked. The audit files confirm it uses no `sorry` (an unfinished proof) and no `native_decide` (trusting compiled code instead of the kernel). |
| **Checked numerically** | A script recomputes the result. This is evidence, not proof. |
| **Audit** | A review of claims made elsewhere (ChatGPT's packages, the Shared Air model, the user's own ideas), with a verdict for each claim. |
| **Open** | Not proved and not claimed. |

## Map

| Path | What it holds | Status |
|---|---|---|
| [`coupled_prime26_pangram.py`](coupled_prime26_pangram.py), [`checks/`](checks/), [`prime-pangram/`](prime-pangram/) | The prime pangram and related searches | Checked numerically |
| [`wyrd/`](wyrd/) | Core Lean proofs: the pangram, Euclid, √2 | Proved in Lean |
| [`wyrd-mathlib/`](wyrd-mathlib/) | Lean + Mathlib: the bridge to Mathlib, √2, the rainbow, body water, Shared Air, its limits, periodic Navier–Stokes | Proved in Lean |
| [`ns-phase-audit/`](ns-phase-audit/) | Independent audit of ChatGPT's periodic Navier–Stokes lab v2 | Audit |
| [`all-time-phase-response/`](all-time-phase-response/) | All-time small-b proof with symbolic constants; direct second variations and bounded refinement pilot | Analytic argument; numerical evidence (separated) |
| [`numerics/`](numerics/) | 19 scripts that recompute numbers used in the theorems and audits | Checked numerically |
| [`reports/`](reports/) | Physics and biology fact-check | Audit |
| [`pangram-prime-words/`](pangram-prime-words/) | Perfect pangrams of pronounceable prime words, from a separate session (PR #2) | Checked numerically |
| [`hou-luo-1d/`](hou-luo-1d/) | A 1D blowup lab from a separate session (PR #1) | Checked numerically (1D toy model) |
| [`inputs/`](inputs/) | The user's uploaded source materials | Source material |
| [`phase-family-checks/`](phase-family-checks/) | Checks of the β = 0 reduction, the b² phase response, Codex's second-order response, and the PR #17 compliance table | Checked numerically |
| [`../navier_stokes/`](../navier_stokes/), [`../web/`](../web/) | The surfactant conjecture and the site (PRs #8, #16, #17): respiratory motivation, an incomplete conjecture with its gaps, synthetic demos | Open: a conjecture, not checked |

---

## 1. The coupled prime-26 pangram (16 October)

### The finder: [`coupled_prime26_pangram.py`](coupled_prime26_pangram.py)

Finds five pairs of primes that share one sum (Goldbach pairs), where the ten
primes' base-26 names together use every letter A–Z exactly once.

Plain base-26 names have no solution up to N = 18,250. With *coupled* digits
(each letter = its digit + the digit to its right, mod 26 — still reversible),
the smallest solution is N = 4296:

```
UKR + TEP  = 4296    (1187 + 3109)
 DB + NMF  = 4296    (53 + 4243)
 YL + AQV  = 4296    (349 + 3947)
 SH + CWZ  = 4296    (293 + 4003)
 IJ + OGX  = 4296    (659 + 3637)
```

Run from this folder (standard library only):

```
python3 coupled_prime26_pangram.py          # coupled, ~0.2s
python3 coupled_prime26_pangram.py --plain  # plain, no solution (about 4 s)
```

Formal proofs of these facts (in Lean 4) live in [`wyrd/`](wyrd/).

[`checks/`](checks/) is a computer search, not a Lean proof, that enumerates
*every* solution instead of stopping at the first: exactly 12 five-pair pangrams
exist under the coupled naming (all with N ≤ 15990), and none at all under plain
naming, for every even N up to the 457000 cutoff beyond which the names are too
long to fit the alphabet.

Caveat: the coupling rule was chosen after the plain search failed, so the
result shows that *a* simple reversible naming yields a pangram, not that
primes "want" to spell the alphabet.

[`prime-pangram/`](prime-pangram/) preserves the Prime-26 search programs and
raw results (`search/`) and a copy of the NICU-Module pronounceable-prime
pangram project with its onset/coda lists and dictionaries (`nicu-pangram/`),
with a README giving definitions, reproduction commands, runtimes and what is
still unfinished.

### The Lean proofs: [`wyrd/`](wyrd/)

**Proved in Lean**, in core Lean 4 without Mathlib. Read
[`wyrd/README.md`](wyrd/README.md) for how the proofs work and
[`wyrd/ROADMAP.md`](wyrd/ROADMAP.md) for what comes next.

| Result | Theorem | File |
|---|---|---|
| **Encoding.** Decoding a name gives back the number, so different numbers get different names. | `decode_encode`, `encode_injective` | [`Wyrd/Encoding.lean`](wyrd/Wyrd/Encoding.lean) |
| **The solution.** The five pairs have the names above; the ten numbers are prime, each pair sums to 4296, and every letter appears exactly once. | `solution_names`, `solution_isPangram` | [`Wyrd/Pangram.lean`](wyrd/Wyrd/Pangram.lean) |
| **Lower bound.** Any five-pair prime pangram has sum at least 1352. | `lower_bound` | [`Wyrd/Pangram.lean`](wyrd/Wyrd/Pangram.lean) |
| **Distinct primes.** In any pangram, the ten primes are all different. | `primes_nodup` | [`Wyrd/Distinct.lean`](wyrd/Wyrd/Distinct.lean) |
| **Parity.** Any pangram has an even sum and never uses the prime 2. | `sum_even`, `two_not_mem` | [`Wyrd/Parity.lean`](wyrd/Wyrd/Parity.lean) |
| **Minimality: N = 4296 is the smallest sum.** The kernel runs a search over the 1,472 even sums from 1352 to 4294 and finds nothing; `ec_complete` proves the search would have found any pangram that existed. | `smallest_pangram_sum` | [`Wyrd/Smallest.lean`](wyrd/Wyrd/Smallest.lean), [`Wyrd/Minimal.lean`](wyrd/Wyrd/Minimal.lean) |
| **Euclid.** There are infinitely many primes. | `primes_infinite` | [`Wyrd/Euclid.lean`](wyrd/Wyrd/Euclid.lean) |
| **√2.** No fraction squares to 2 (infinite descent, whole-number form). | `no_fraction_squares_to_two` | [`Wyrd/Sqrt2.lean`](wyrd/Wyrd/Sqrt2.lean) |

### Searches that support it

- [`checks/`](checks/): **checked numerically.** Two independent enumerators
  (Python and C) list every solution, as described above. The 457000 cutoff is
  argued on paper in [`checks/README.md`](checks/README.md), not in Lean.
- [`prime-pangram/`](prime-pangram/): **checked numerically.** Every number in
  its README is marked *reproduced* (re-run on 16 October) or *archived*
  (copied from earlier logs). One count is **open**: the K = 6 exact count did
  not finish.
- [`numerics/pangram/smallest_sum_search_cost.py`](numerics/pangram/smallest_sum_search_cost.py):
  **checked numerically.** A Python copy of the Lean kernel search. It finds no
  pangram below 4296.

### A related search: prime-word perfect pangrams ([`pangram-prime-words/`](pangram-prime-words/))

From a separate session (merged as PR #2, moved here from the repository root).
A different question: can the 26 letters be split into pronounceable words that
are each prime under bijective base 26 (A = 1 … Z = 26)? **Checked
numerically**, with every number printed by a named script:

- Under English onset and coda lists there are 16,243 prime words and **no**
  perfect pangram. The reason is structural: a word's value is congruent to its
  last letter mod 26, so every coda must end in a letter coprime to 26, and the
  odd codas can hold at most 17 of the 20 consonants (`structure.py`).
- Under a free consonant–vowel–consonant rule there are exactly 11,261,264,735,669
  perfect pangrams, confirmed by two independent counters.
- The alphabetical digit assignment is what blocks the English case: it puts all
  six vowels on odd digits. 125 of 200 random assignments admit solutions.

Read [`pangram-prime-words/README.md`](pangram-prime-words/README.md) for the
definitions, the scripts and the full tables.

---

## 2. wyrd-mathlib: the proofs connected to Mathlib (16–17 October)

**Proved in Lean**, for every theorem named in this section. The project
depends on Mathlib `v4.35.0` and on [`wyrd/`](wyrd/). Full theorem tables:
[`wyrd-mathlib/README.md`](wyrd-mathlib/README.md). All paths below are inside
[`wyrd-mathlib/WyrdMathlib/`](wyrd-mathlib/WyrdMathlib/).

### 2.1 The bridge and √2 (`Bridge.lean`, `Sqrt2.lean`)

Connects the core project to Mathlib, so that Mathlib's results about primes
apply to ours, and the reverse.

- `isPrime_iff`: our `IsPrime` is exactly Mathlib's `Nat.Prime`.
- `setOf_prime_infinite`: Mathlib's "the primes form an infinite set", proved
  with our Euclid. `solution_primes`: the ten pangram primes are `Nat.Prime`.
- `bertrand`: Bertrand's postulate (a prime between n and 2n) for our
  `IsPrime`. This one borrows Mathlib's proof; our own proof is **open**.
- `irrational_sqrt_two`: √2 is irrational as a real number, derived from the
  core descent proof.

### 2.2 The rainbow (`Rainbow/`)

Descartes' theory. Sunlight enters a spherical drop, bends by Snell's law,
reflects k times inside and leaves. Light piles up where the total turning
angle is stationary, and that bright fold is the bow.

- `deriv_dev_eq_zero_iff_eq`, `dev_isMinOn`: for 1 < n < k+1 the only
  stationary point is at cos² i = (n² − 1)/(k(k+2)), and it is the strict
  minimum of the deviation.
- `primary_bow_water`, `secondary_bow_water`: for water (n = 4/3) the primary
  bow is between 41° and 43° and the secondary between 50° and 52°.
- `alexander_dark_band`: no light reflected once or twice inside the drop
  leaves between 43° and 50°, which is why the sky between the bows is darker
  (darker, not black).
- `colour_order`, `primary_red`, `primary_violet`, `secondary_red`,
  `secondary_violet`, `primary_spread`, `secondary_spread`,
  `dark_band_of_red_le`: red is outside in the primary bow and inside in the
  secondary, with real-water angles for red and violet.

### 2.3 Body water (`BodyWater/`)

Total body water as theorems about simple models. For understanding, not for
dosing; each file says what its model leaves out.

- `dilution_recovers`, `dilution_overestimate`: indicator dilution V = I/C
  works, and tracer lost before sampling makes the volume look bigger (D₂O
  overstates total body water by about 4%).
- `newborn_water_load`: free water spreads by effective osmoles: 2/3 enters the
  cells in an adult, only 34/78 ≈ 43.6% in a term newborn.
- `adrogue_madias`, `per_litre_scaling_underestimates`: the Adrogué–Madias
  formula from Edelman's relation; scaling its per-litre form down to 10 mL in
  a 3 kg newborn gives a figure about 30% too small: the model change is more than
  1.42 times the per-litre estimate.
- `free_water_deficit`, `water_fraction_falls`, `more_water_less_fat`.

### 2.4 Shared Air (`SharedAir/`)

An audit of the *equations* of the Shared Air mother–infant model (see
[`inputs/`](inputs/)), not of its biology. Mostly about its linearisation at
rest with zero delay.

- `hasFDerivAt_field`: that linear system really is the derivative of the
  model's nonlinear field at rest.
- `optimal_coupling`, `optimum_bounds`: at zero delay there is exactly one best
  coupling, g* ∈ (0.08035, 0.08036).
- `stable_iff`, `gc_bounds`: at zero delay, rest is stable exactly when
  g < g_c = 15/8 + √2265/24 ≈ 3.858. `unstable_every_delay`: above g_c it is
  unstable for every delay.
- `same_synchrony_different_future_24`: two populations with the same
  synchrony number can change at different rates, so one number cannot predict
  its own future.
- `hasDerivAt_freeEnergy`, `equilibrium_eq`: osmotic water flow between cells
  never increases free energy, and its equilibrium is equal osmolality.
- `contrast_pos_without_coupling`: a noisier control adult produces a positive
  "bond" contrast with no bond at all.
- `averaged_stable_equilibrium_iff`, `two_to_one_moments`: first-order 2:1
  locking.

The delayed model (τ > 0) is only **checked numerically**: stability is lost
at τ ≈ 1.8356 s for g = 3 and τ ≈ 4.7613 s for g = 1
([`numerics/shared-air/`](numerics/shared-air/)).

### 2.5 The Shared Air limits (`Limits/`)

The model's own list of what it cannot tell you, turned into theorems.

- **Ratios** (`Ratios.lean`): the harmonic lock index counts bands, not ratios.
  A 3:2 lock reads exactly like 3:1, and 5:3 and 4:3 are invisible to the 2nd
  and 3rd harmonics (`three_two_looks_like_three_one`, `five_three_hidden`,
  `model_forcing_misses_n_m`).
- **Direction** (`Direction.lean`): flipping the assumed sign of the response
  moves the correlation peak from "mom first" to "infant first"
  (`calming_reverses_lag`); an unmatched control produces a lag signal with no
  bond (`room_leaks_when_unmatched`).
- **Which world is real** (`Mixture.lean`): one or two bedside conditions never
  identify the mixture (`two_conditions_never_enough`). Bedside-awake,
  skin-awake and skin-asleep do when the effects add (`additive_identified`);
  with an interaction, the full 2 × 2 design is needed
  (`three_conditions_miss_interaction`, `four_conditions_identify_interaction`).
- **Sessions** (`Sessions.lean`): a distribution-free bound on how many
  sessions are enough (`sessions_chebyshev`, `sessions_enough`).
- **Arousal is one number** (`Arousal.lean`): co-activation of sympathetic and
  vagal drive cannot be represented (`no_coactivation`).
- **Clinical values** (`Values.lean`): the stated numbers agree with each other
  (`q10_per_degree`, `chest_warmth_bpm`, `warming_after_twelve_minutes`), and
  the resting rate cannot separate the cells' own rate from vagal tone
  (`resting_rate_not_identifiable`).
- **Whose good** (`Objective.lean`): no coupling leaves mom at rest and also
  gives the best recovery (`mom_untouched_iff`, `infant_best_moves_mom`).
- **Test 4's second state** (`Bistability.lean`): without the capacity limit,
  rest is the only equilibrium for 0 ≤ g ≤ 3. With it, rest is still the only
  one up to g = 2, a co-arousal equilibrium exists at g = 2.1, and at g = 3 it
  is linearly stable, so the pair is bistable (`only_rest_without_cap`,
  `only_rest_upto_two`, `coarousal_exists_above_two`,
  `coarousal_stable_at_three`).

### 2.6 Periodic Navier–Stokes (`PeriodicNS/`)

Theorems about given velocity fields on the 2π-periodic cube **at one
instant**. The Navier–Stokes evolution itself is not formalised. Notation:
E = energy, Z = enstrophy, D = ⟨|∇ω|²⟩, S = vortex stretching, all as volume
averages.

| Topic | What is proved | File |
|---|---|---|
| **Example field** | v = (sin y, sin z, cos x − cos(x + y)) is divergence-free, with E = 1, Z = 5/4, D = 7/2, S = 1/4 (`div_v`, `curl_v`, `quantities_v`) | `Example.lean`, `Averages.lean` |
| **Sign flip** | ±A v share E, Z, D and every Fourier magnitude, but S = ±A³/4. So S − νD is not a function of those numbers (`no_closure`, `no_spectral_closure`, `opposite_signs`) | `SignFlip.lean` |
| **Galerkin** | A fixed Fourier cutoff K gives Z_K ≤ K² E_K(0): bounded, but worse as K → ∞ (`galerkin_enstrophy_bound`) | `Galerkin.lean` |
| **Grönwall** | Z′ ≤ a Z implies Z(t) ≤ Z(0) exp ∫ a, the step a regularity proof would use (`gronwall_variable`) | `Gronwall.lean` |
| **Blowup scalings** | Arithmetic about assumed blowup exponents: the swirl Reynolds number blows up, vorticity ~ 1/(t_b − t) is not integrable (the Beale–Kato–Majda divergence), and a shrinking core can have vanishing energy while its speed blows up (`swirl_reynolds_blowup`, `vorticity_not_integrable`, `energy_vanishes_speed_blows`). No solution with these scalings is constructed. | `Blowup.lean`, `CoreScaling.lean` |
| **Clay statements** | The quantifier logic of Clay's alternatives B and D (`not_B_implies_D`, `D_and_B_consistent`) | `Quantifiers.lean` |
| **Phase family** | u_φ = (sin y, sin z, cos x − cos(x + y + φ)) has the same E, Z, D for every φ but S = cos φ/4. So S − νD, the initial enstrophy growth rate in the standard balance, is zero at φ = π/3 when ν = 1/28; and −v is a shifted copy of u_π (`quantities_vphi`, `growth_iff`, `zero_growth_at_pi_div_three`, `neg_v_translate`) | `PhaseFamily.lean` |
| **Selection rules** | The counting core of the audit's argument (section 3): a cos mφ term with \|m\| ≥ 2 cannot appear in Z before t^(3\|m\|), is ν-free there, and at t⁷ the cos 2φ term is proportional to ν (`not_before`, `at_first_order`, `order_seven_m_two`). Two inputs are proved on paper only, in [AUDIT.md §4.2](ns-phase-audit/audit_v2/AUDIT.md#42-structural-explanation) | `SelectionRules.lean` |
| **Phase symmetry** | A rotation by π plus a shift maps u_φ to u_−φ, and a mirror fixes u_φ (`rotShift_vphi`, `mirror_fixes_vphi`, `quantities_even`) | `PhaseSymmetry.lean` |
| **Scaling counterexample** | Rescaling by an integer k keeps E = 1 but gives Z = 5k²/4, D = 7k⁴/2, S = k³/4. So no bound S ≤ C Z^a D^b with 2a + 4b < 3 holds for all fields, and the fitted Z^0.75 D^0.2 law fails like k^0.7 (`quantities_vScaled`, `no_power_law_bound`, `fitted_law_fails`) | `Scaling.lean` |

### 2.7 How the proofs are checked: Audit.lean and CI

- [`wyrd-mathlib/Audit.lean`](wyrd-mathlib/Audit.lean) prints the axioms of
  every listed theorem (136 of them), and
  [`wyrd/Audit.lean`](wyrd/Audit.lean) does the same for the 14 core theorems.
  Only Lean's standard axioms `propext`, `Classical.choice` and `Quot.sound`
  may appear (some theorems use fewer). `sorryAx` would mean an unfinished
  proof; `Lean.ofReduceBool` would mean `native_decide`.
- On 18 October 2026 the axioms of all 136 + 14 theorems were printed from an
  existing local build of the identical source (sgrounds commit `e29a9fe`, see
  [Provenance](#provenance)). Every one uses only those three axioms.
- CI ([`../.github/workflows/lean.yml`](../.github/workflows/lean.yml)) builds
  both Lean projects and runs both audits, and fails if `sorryAx` or
  `ofReduceBool` appears. It runs on every push or pull request that changes
  `math/wyrd/`, `math/wyrd-mathlib/` or the workflow file, and can be started
  by hand from the Actions tab. Its result for this repository is shown there.
- [`ns-phase-audit/README.md`](ns-phase-audit/README.md) gives the count as
  130; it was written before the six theorems of `Scaling.lean` were added.

---

## 3. Audit of ChatGPT's periodic Navier–Stokes lab v2 (16 October)

**Audit**, with exact computations. Start with
[`ns-phase-audit/audit_v2/AUDIT.md`](ns-phase-audit/audit_v2/AUDIT.md); the
folder guide is [`ns-phase-audit/README.md`](ns-phase-audit/README.md).

- **What was audited.** ChatGPT's `periodic_ns_lab_v2` package (now kept in
  [`inputs/periodic_ns_lab_v2_audit.zip`](inputs/periodic_ns_lab_v2_audit.zip)),
  which studies the phase family u_φ under the unforced 3D Navier–Stokes
  equations with ν = 1/28. Four independent lines checked it: an exact
  rational Taylor series with symbolic ν, a floating-point series, a DNS solver
  written from scratch, and a reading of the package code. A cross-check
  compared all four with each other and with the package outputs.
- **Headline.** No mathematical error and no false numerical claim. The
  package's central identity is confirmed exactly with ν kept symbolic: the
  cos 2φ coefficient of the order-6 term of Z is **−6487/1555200 for every ν**.
- **Why it appears at order 6, and why it is ν-free.** Without the `sin z`
  mode the flow stays independent of z (all three velocity components kept,
  "2D-3C"), and then Z has only `1` and `cos φ` terms at every order (P1).
  Counting wave vectors along each axis, with the grading "amplitude degree +
  power of ν = n + 2", then shows that a cos mφ term with |m| ≥ 2 cannot appear
  before order 3|m|, and has no ν there (P2).
- **Predictions from that argument, all confirmed exactly.** At order 7 the
  cos 2φ coefficient is (207269/7257600) ν, so zero for Euler; cos 3φ first
  appears at order 9, ν-free (`z_{9,3} = −21381938959/211843247616000`); cos 4φ
  first appears at order 12.
- **Smaller findings.** The numbers reproduce to about 8 decimals; some printed
  9th decimals depend on the integrator. Reproducibility bugs: bare
  `pytest -q` fails to collect, `--dt` is ignored in `optimize`, and some counts
  are hard-coded.
- **Lean side.** The phase family, its symmetry and the counting part of P2
  are proved (section 2.6). P1 and the time evolution are not in Lean.
- **Running it.** Python 3 + numpy (sympy for one script). Scripts that read
  the package expect it unzipped next to `audit_v2/`:
  `cd ns-phase-audit && unzip ../inputs/periodic_ns_lab_v2_audit.zip`
  (creates `periodic_ns_lab_v2/`). Full commands: AUDIT.md §8.
- [`ns-phase-audit/checks_v1/nslab_check.py`](ns-phase-audit/checks_v1/nslab_check.py):
  the earlier FFT re-derivation of the v1 lab's exact identities.

---

## 4. Numerical cross-checks and the physics–biology fact-check (curated 18 October)

### [`numerics/`](numerics/)

**Checked numerically.** 19 small scripts in five topic folders. Each recomputes
numbers that appear in the Lean theorems or the audits, has its output saved
next to it (`*.out.txt`), and is mapped in [`numerics/README.md`](numerics/README.md)
to the theorems it supports. Each runs from its own folder with `python3 -I` in
under a minute.

- [`shared-air/`](numerics/shared-air/): four methods for the delayed model.
  Critical delay τ ≈ 1.8356 at g = 3 and 4.7613 at g = 1;
  g_c = 3.858000672381799 and g* = 0.08035588629272802.
- [`shared-air-limits/`](numerics/shared-air-limits/): the brackets and
  margins used in `Bistability.lean`, the coupling g_sn ≈ 2.06888499 where
  co-arousal equilibria first appear, and the clinical values.
- [`navier-stokes/`](numerics/navier-stokes/): E, Z, D, S for the phase family
  and the rescaled fields; the Fourier mode lists used in the Lean proofs; the
  v1 lab's exact identities to 6.66e-16.
  `nslab_v1_exact_identities.py` is a copy of `ns-phase-audit/checks_v1/nslab_check.py`.
- [`rainbow/`](numerics/rainbow/): bow angles 42.0297° and 50.9781° at
  n = 4/3; red n = 1.331 corresponds to 663–694 nm and violet n = 1.343 to
  402–410 nm; the Taylor brackets used in the Lean proofs.
- [`pangram/`](numerics/pangram/): the Python copy of the minimality search.
- Body water has no script; `numerics/README.md` lists the source figures and
  the Lean theorems that use them.

### [`reports/physics-biology-factcheck.md`](reports/physics-biology-factcheck.md)

**Audit.** The user's ideas linking particle physics, gravity and cosmology to
physiology and medicine, checked against primary sources, as the user asked
for pushback rather than validation. Every derived number is computed by a
script, and an adversarial verifier rechecked them. Each of the 21 ideas gets a
verdict: true, partly true, a metaphor that maps onto real structure, false as
stated, unsupported, or outside physics. Scripts, outputs and data are in
[`reports/physics-biology/`](reports/physics-biology/) and re-run offline.

---

## 5. The 1D Hou–Luo blowup lab (separate session, 16 October)

**Checked numerically, in a one-dimensional toy model. It is not 3D
Navier–Stokes, and nothing in it is evidence about the 3D equations.** Read
[`hou-luo-1d/NOTE_FOR_CHATGPT.md`](hou-luo-1d/NOTE_FOR_CHATGPT.md) first, then
the lab brief [`hou-luo-1d/hou-luo/CLAUDE.md`](hou-luo-1d/hou-luo/CLAUDE.md).

- **The model.** A 1D caricature of swirling flow along the wall of a pipe, the
  setting of Chen and Hou's 3D Euler blowup result, with a viscosity knob, for
  watching concentration fight diffusion.
- **Uniform grid (baseline).** Without viscosity, max|ω| reaches about 9.4 at
  t ≈ 0.761 before the grid loses resolution; this is loss of resolution, not
  a singularity. With viscosity ν = 3e-3 to 3e-5, every run peaks and decays.
- **Adaptive mesh (Step 1).** The inviscid run is followed to max|ω| = 10⁴.
  1/max|ω| extrapolates linearly to zero at T ≈ 0.844513 (the run itself was
  followed to max|ω| = 10⁴ at t = 0.844444), and the peak's distance from
  x = 0 shrinks like (T − t)^c with c = 3.000 ± 0.003. This agrees with the
  published value 2.99870 ± 6e-5 for this 1D model (Chen, Hou and Huang, 2022),
  as quoted by a citation-checking agent.
- **What it is not.** The note records that no 3D strip-fitting code, 3D
  spectra or fitted law S ≤ C Z^0.75 D^0.2 was found in any session; that law
  is examined in `Scaling.lean` (section 2.6).
- **Open.** Steps 2–4 of the lab: dynamic rescaling, whether viscosity always
  wins in the toy, and reading the formal statements.
- **Provenance.** Copied unchanged from `rafaellemus92/NICU-Module`, branch
  `claude/peaceful-wozniak-oaprql`, folder `hou-luo/`, commit `8cb11e6`. The
  solver needs numpy; the plots need matplotlib.

---

## 6. Source materials: [`inputs/`](inputs/)

The files the user uploaded during the work: two versions of the Shared Air
model, ChatGPT's two audit ZIPs, ChatGPT's Navier–Stokes lab packages v1 and
v2, and the original pangram script.
[`inputs/README.md`](inputs/README.md) describes each file in one line. Four
screenshots from the conversation are not included.

---

## How to build and check

### Lean

Both projects pin Lean 4.35.0 (`lean-toolchain`); install it with elan.

From the repository root:

```sh
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh

cd math/wyrd                 # core project: builds without Mathlib
lake build                   # took 17 min in the logged run, mostly the minimality search
lake env lean Audit.lean     # prints the axioms of each theorem

cd ../wyrd-mathlib           # needs ../wyrd next to it
lake exe cache get           # prebuilt Mathlib files (about 7 GB)
lake build
lake env lean Audit.lean
```

Skipping `lake exe cache get` means building Mathlib from source, which takes
hours. The log of a core build is in
[`prime-pangram/logs/lean-build-2026-10-16.log`](prime-pangram/logs/lean-build-2026-10-16.log).
The READMEs inside `wyrd/` and `wyrd-mathlib/` still say `cd experiments/...`;
in this repository the folder is `math/`.

### Python

Python 3 and numpy are enough for every script, with these exceptions:

- `ns-phase-audit/audit_v2/code_audit/symmetry_sympy.py` needs sympy;
- the Hou–Luo plots need matplotlib;
- the C programs in `checks/` and `prime-pangram/` need a C compiler such as gcc;
- `reports/physics-biology/tools/epmc*.py` need network access (they are not
  needed to reproduce any number).

The saved outputs in `numerics/` were produced with Python 3.13.16 and numpy
2.5.3. Run any script that reads an uploaded package with `python3 -I`.

---

## Provenance

- `coupled_prime26_pangram.py`, `checks/`, `prime-pangram/`, `wyrd/`,
  `wyrd-mathlib/`, `ns-phase-audit/` and the pangram text of this README were
  imported with their full history (git subtree) from
  `rafaellemus92/sgrounds`, branch `claude/new-session-sbrl43`, folder
  `experiments/`, at source commit
  `e29a9fe90b660aa11bb0b4ae114d65297448bf10`. In this repository's history the
  matching subtree commit is `f1752bf`.
- `hou-luo-1d/hou-luo/` is the branch `claude/peaceful-wozniak-oaprql` (PR #1),
  merged with its history and moved here; `NOTE_FOR_CHATGPT.md` was added.
- `pangram-prime-words/` is the former root `pangram/` folder (PR #2), moved
  here with `git mv` so its history follows it.
- This repository was previously named `NICU-Module`.
- `inputs/` holds the user's uploads.
- `numerics/` and `reports/` were curated on 18 October from scratch files of
  the same work. Their READMEs list what was kept, what was dropped and why.

---

## 7. The phase family: β = 0 reduction, all-time small-b response, checks (18 October)

Two folders from the same day, by different owners.

[`all-time-phase-response/`](all-time-phase-response/) (owner: Codex; patch of local commit
`ddbca048`, imported from the user's upload) proves, with symbolic constants, that for
fixed ν > 0 one sufficiently small b works for all time: the perturbed flows are global and
smooth, the second-order coefficients E₂, Z₂, S₂ solve explicit linear equations, and the
observable remainders after subtracting them are O(b⁴) with exponential decay. **Analytic
argument with symbolic constants, plus numerical evidence, kept separate.** No numerical
radius is certified: the sufficient condition has the form |b| ≤ ν e^{−A}/(2KF); with the
note's own explicit constants it admits no b above 10^(−10⁷⁰) at ν = 1/28, and with the exact
base-flow integral in place of the note's majorant no b above 10^(−160) (review in
[`phase-family-checks/`](phase-family-checks/)). The order b⁴ is testable; the certified radius
is not, and the numerical evidence stops at T = 0.5. Its §1 writes out the
β = 0 reduction that [`ns-phase-audit/`](ns-phase-audit/) §7.5 had left as "not written out".

[`phase-family-checks/`](phase-family-checks/) (owner: Claude) checks the β = 0 reduction three
ways, measures the b² scaling of the phase harmonics at T = 1 and its loss by T = 8, reproduces
Codex's second-order response at T = 0.5 with an independent solver to six figures, and
reproduces the PR #17 compliance table from the repository's generator, identifying the
resistance bias as regression dilution. **Checked numerically.**

---

## What remains open

**Navier–Stokes.** The Millennium problem is untouched. Everything in
`PeriodicNS/` is about given fields at one instant, or arithmetic about
assumed blowup exponents; the evolution, local existence and the enstrophy
balance dZ/dt = S − νD are not formalised. Specifically missing
([AUDIT.md §7](ns-phase-audit/audit_v2/AUDIT.md#7-what-remains-unproven)):

1. **A cutoff-uniform estimate.** No bound uniform in the Fourier cutoff
   connects the finite-cutoff simulations to the actual PDE, so the numerical
   rankings are not theorems.
2. **A remainder bound for the Taylor jets.** The order 6, 7, 9 and 12 results
   are exact statements about derivatives at t = 0. Nothing bounds the error of
   the series at t = 2 or t = 4.
3. **Global optimality in φ.** The optimiser certifies only a local maximum
   (φ* ≈ 0.970364 at T = 2).
4. **Nonvanishing of the leading |m| ≥ 5 coefficient.** The first cos mφ
   coefficient is computed to be nonzero only for |m| = 2, 3, 4.

P1 at the solution level is now written out in
[`all-time-phase-response/PROOF.md`](all-time-phase-response/PROOF.md) §1 and checked in
[`phase-family-checks/`](phase-family-checks/); it is not in Lean.

**The all-time small-b result** (section 7) is a qualitative theorem: there is a
b₀ > 0 below which the restored-mode flows are global and smooth with O(b²)
response and O(b⁴) remainder, uniformly in time. What is open: any useful value of
b₀ (the proved sufficient condition is astronomically small), control at b = 1, a
remainder bound with evaluated constants, and the inviscid b ≠ 0 problem, where
nothing of the argument survives. The computed flows at b ≤ 1 are smooth to the
times computed; that is numerical evidence, not a certificate (§7.1).

**The surfactant conjecture** ([`../navier_stokes/`](../navier_stokes/) and
[`../web/`](../web/)) is **Open: a conjecture, not checked**. PR #16 replaced its
seven-step outline by three standard identities, three named gaps and one refuted
deduction; the gaps are the threshold mechanism, control of vortex stretching, and
a regularity criterion in the free-boundary setting, two of which are the
obstructions of the general problem.

**Smaller open items.**

- Pangram: the plain-naming non-existence, the list of 12 coupled solutions and
  the 457000 cutoff are computer searches, not Lean proofs; our own proof of
  Bertrand's postulate; a faster minimality check ([`wyrd/ROADMAP.md`](wyrd/ROADMAP.md)).
  The K = 6 count in `prime-pangram/` did not finish.
- Shared Air: results for the delayed model (τ > 0) are numerical only, and the
  zero-delay theorems must not be read as statements about the delayed, noisy
  or nonlinear model. Which of the model's three worlds is real is not a
  mathematical question; only recordings can decide.
- Rainbow band widths to 0.1°, and body water over time (postnatal diuresis):
  [`wyrd/ROADMAP.md`](wyrd/ROADMAP.md).
- Hou–Luo: Steps 2–4 (section 5).
