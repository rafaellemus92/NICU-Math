# numerics: independent numerical cross-checks

Small scripts that recompute, in floating point or exact rational arithmetic,
numbers that appear in the Lean theorems ([`../wyrd-mathlib`](../wyrd-mathlib),
[`../wyrd`](../wyrd)) and in the audits. They are evidence, not proofs: a Lean
theorem is checked by the kernel, a script here only shows that an independent
computation gives the same number.

They were written during the work and curated here. Each script starts with a
comment that says what it checks and what it was called before.

## Running

Run each script from its own folder:

```sh
cd shared-air
python3 -I delay_crossing_xcheck.py > delay_crossing_xcheck.out.txt
```

Requirements: Python 3 and numpy. The pangram, rainbow and `*_modes.py` scripts
use only the standard library. Nothing reads the network or the uploaded
packages in [`../inputs`](../inputs). The saved `<script>.out.txt` files were
produced with Python 3.13.16 and numpy 2.5.3. Every script finishes in under a
minute; the slowest is `shared-air/delay_newton_roots.py` (about 45 s). The run
time printed by `pangram/smallest_sum_search_cost.py` varies between runs.

Notation in the tables: "Lean" names are theorems in
`../wyrd-mathlib/WyrdMathlib/<Topic>/*.lean` unless another path is given.

## Shared Air ([`shared-air/`](shared-air))

The delayed linearisation of the perceived world has characteristic function
`D(s) = (s+a)(s+b)(s+d) + h g (s+b) e^{-sτ} - c g² (s+d) e^{-2sτ}` with the
model's `a = 1/30`, `b = 1/20`, `d = 1/4`, `c = r q = 1/250` (`r = 1/25`,
`q = 1/10`), `h = 3/40`. The Lean results are about zero delay; these scripts
supply the numerical "delay caveat" in the
[wyrd-mathlib README](../wyrd-mathlib/README.md#shared-air-wyrdmathlibsharedair)
with three independent methods plus a root count.

| Script | What it checks | Key result (from the `.out.txt`) | Cross-checks |
|---|---|---|---|
| `delay_crossing_xcheck.py` | `det(sI − A0 − A1 e^{-sτ}) = D(s)` at sample points; the zero-delay threshold `g_c`; for `g = 1, 3`, every root `s = iω` of `D` and the delays at which it occurs, with crossing direction | "state-space det == D(s): OK"; `τ = 0` threshold `g_c = 3.8580006723817983` (the script prints it as `g*`); `g = 1`: `ω = 0.223749`, smallest crossing `τ = 4.761271577453111`; `g = 3`: `ω = 0.428787`, `τ = 1.8355853001211138`; both crossings move rightwards (sign `+1`), residual `\|D\| < 1e-16` | `det_delayMatrix`, `Dd_eq_det` (Delay.lean); `stable_iff` (Optimal.lean); `gc_bounds` (Specific.lean); the delay caveat (`τ ≈ 1.8356` at `g = 3`, `τ ≈ 4.7613` at `g = 1`) |
| `delay_chebyshev_xcheck.py` | Chebyshev collocation of the delay generator: convergence in `N`, residual `\|D(λ)\|`, critical `τ` by bisection | at `g = 3, τ = 2` the rightmost eigenvalues are `0.01191945 ± 0.42186598i` and `−0.01182892` for every `N` in 10…60, residual `≤ 7.8e-15`; critical `τ = 1.835585` (`g = 3`) and `4.761272` (`g = 1`), the same at `N = 20, 40, 60`, with eigenvalues `±0.428787i` and `±0.223749i` there | same as above |
| `delay_newton_roots.py` | Newton iteration from a 41 × 61 grid of starting points; rightmost roots and the delay where stability is lost | `g = 3, τ = 2`: `+0.0119 ± 0.4219i`; `g = 1, τ = 5`: `+0.0035 ± 0.2197i`; stability lost at `τ ≈ 1.8356` (`g = 3`) and `τ ≈ 4.7613` (`g = 1`) | same as above |
| `delay_argument_principle.py` | number of roots in the right half-plane (argument principle), `g_c` from its closed form, and the optimal coupling `g*` | `g = 3`: 0 roots at `τ = 0, 1.0, 1.83`, 2 at `τ = 1.84, 2.0, 5.0`; `g = 1`: 0 at `τ ≤ 4.76`, 2 at `τ = 4.765, 6.0`; `g_c = 3.858000672381799`; `g = 3.85`: 0 roots at `τ = 0`, 2 at `τ = 3`; `g = 3.87`: 1 at `τ = 0`, 3 at `τ = 3`; `s* = −0.04827092064398199`, `g* = 0.08035588629272802` | `gc_bounds` (`3.858 < g_c < 3.8581`), `stable_iff`, `unstable_every_delay` (above `g_c` a positive real root for every delay), `optimum_bounds` (`s* ∈ (−0.048271, −0.04827)`, `g* ∈ (0.08035, 0.08036)`) |

## Shared Air limits ([`shared-air-limits/`](shared-air-limits))

The "Test 4" bistability results in `Limits/Bistability.lean` and the other
limit theorems. `f(y, g)` is the first component of the field on the curve
where the other two vanish (`bistF` in Lean); `y` is the mother's arousal `A_m`.

| Script | What it checks | Key result | Cross-checks |
|---|---|---|---|
| `bistability_equilibria_sweep.py` | all equilibria for `g ∈ {0.5, 1, 1.5, 1.8, 1.9, 2.0, 2.1, 2.2, 2.5, 3.0}`, with and without the capacity limit, and the largest real part of the Jacobian eigenvalues at each | without the cap: no equilibrium other than rest at any `g` of the sweep. With the cap: none up to `g = 2.0`; at `g = 2.1`, `(A_i, A_m) = (0.5398, 1.32875)` with max Re `+0.01271` and `(0.90095, 1.72627)` with max Re `−0.01669`; at `g = 3`, `(0.10395, 0.55524)` with `+0.02335` and `(1.91417, 2.79077)` with `−0.14952`. Rest is stable throughout (max Re `−0.04416` at `g = 0.5` to `−0.01286` at `g = 3`) | `only_rest_without_cap`, `only_rest_upto_two`, `coarousal_exists_above_two`, `coarousal_stable_at_three` |
| `bistability_proof_brackets.py` | the numbers the Lean proofs use: the intermediate-value brackets, the `g = 3` equilibrium and its Routh–Hurwitz quantity, the minimum of `f2(u)` and of the `g ≤ 2` bound `Φ(g, u)` | `f(1.3, 2.1) = −0.000654 < 0 < f(1.4, 2.1) = 0.001353`; `f(2.79, 3) = 0.000267 > 0 > f(2.792, 3) = −0.000429`; equilibrium `y = 2.79077`, `x = 1.91417`, `cap = 0.07593` (Lean uses `x ∈ [1.91, 1.92]`, `cap ≤ 0.08`); eigenvalues `−0.5587, −0.1495, −0.3122`; characteristic polynomial `[1, 1.02048, 0.30467, 0.02608]`, `c2 c1 − c0 = 0.28483`; `min f2 = 0.0021303` at `u = 2.1155`; `min Φ = 0.000754` on `(0, 2] × [0, 20]` | `coarousal_exists_above_two` (IVT on `[1.3, 1.4]`), `coarousal_stable_at_three` (IVT on `[2.79, 2.792]`, private `bist_coeffs`, `cubic_hurwitz`), private `bist_f2_pos`, `only_rest_upto_two` |
| `limits_checks.py` | (1) harmonic lock index of a perfect `n:m` lock, `k = 1…5`; (2) first-order resonant average of `sin(lθ) P(ψ)` along `n:m` orbits, for the model's pulse `P(ψ) = e^{2(cos ψ − 1)} − 0.30851657`; (3) the coupling `g_sn` where co-arousal equilibria first appear, Routh–Hurwitz at `g = 3`; (4) clinical values; (5) margin of the "rest only" bound | (1) 2:1 → `[0, 1, 0, 1, 0]`; 3:1 and 3:2 → `[0, 0, 1, 0, 0]`; 5:3 → `[0, 0, 0, 0, 1]`; 4:3 → `[0, 0, 0, 1, 0]`. (2) nonzero only when `m ∣ l·n`: `(l,n,m) = (1,2,1)`: `−0.5705`, `(1,3,1)`: `−0.0433`, `(2,3,2)`: `−0.1083`, `(3,5,3)`: `0.00765`; `0` to 10 decimals for `(1,3,2), (1,5,3), (1,4,3), (2,5,3)`. (3) `g_sn ≈ 2.06888499`; at `g = 3`, `c2 = 1.02048`, `c1 = 0.30467`, `c0 = 0.02608`, `c2 c1 − c0 = 0.28483`. (4) `2.2^{1/10} = 1.0820374`, `2.2^{0.035} = 1.0279803`, `140 (2.2^{0.035} − 1) = 3.9172` bpm, `1 − e^{−1.8} = 0.8347011`. (5) `min F = 0.000754` over `g ∈ (0, 2]`, attained at `g = 2` | `lockIndex_eq_one`, `lockIndex_eq_zero`, `three_two_looks_like_three_one`, `five_three_hidden`, `four_three_hidden`; `resonant_average_vanishes`, `model_forcing_misses_n_m`; `only_rest_upto_two` and `coarousal_exists_above_two` (`2 < g_sn < 2.1`); `coarousal_stable_at_three`; `q10_per_degree` (`1.082 < · < 1.0821`), `chest_warmth_bpm` (`3.9 < · < 3.94`), `warming_after_twelve_minutes` (`0.8346 < · < 0.8348`) |

## Periodic Navier–Stokes ([`navier-stokes/`](navier-stokes))

Fields on the `2π`-periodic cube: `u_φ = (sin y, sin z, cos x − cos(x+y+φ))`,
`v = u_0`, and the rescaled `v_k`. Normalised averages; `E = ½⟨|u|²⟩`,
`Z = ½⟨|ω|²⟩`, `D = ⟨|∇ω|²⟩`, `S = ⟨ω·(∇u)ω⟩`. Lean names are in
`WyrdMathlib/PeriodicNS/`. The lab audit itself is in
[`../ns-phase-audit`](../ns-phase-audit).

| Script | What it checks | Key result | Cross-checks |
|---|---|---|---|
| `nslab_v1_exact_identities.py` | FFT re-derivation (16³) of the exact `t = 0` identities claimed by `periodic_ns_lab_v1`: `S = cos φ/4`, `Z'(0) = cos φ/4 − 7ν/2`, `Z''(0) = 5/4 − (5/2)ν cos φ + 11ν²`, high-shell energy `7/48` and enstrophy `9/16`, all-new-mode coefficients `11/24` and `19/16` | max abs error `6.66e-16` over `φ ∈ {0, 0.7, π/3, 2, π}`, `ν ∈ {1/28, 0.1, 0}`; new-mode coefficients `0.45833333333333337` (`11/24`) and `1.1875000000000002` (`19/16`) | `quantities_vphi` (`S = cos φ/4`, `D = 7/2`). `Z'(0) = S − νD` is the enstrophy balance, which is **not** formalised; this checks it numerically for `u_φ`. The other identities are lab claims (`periodic_ns_lab_v1/results/exact_dynamics.json`, `exact_phase_family.json`, `proof_notes.md` in `../inputs/periodic_ns_lab_v1.zip`), not Lean theorems. Identical to `../ns-phase-audit/checks_v1/nslab_check.py` |
| `phase_family_quantities.py` | `E, Z, D, S` of `u_φ` on a 24³ grid with hand-written derivatives (no FFT), `φ ∈ {0, 0.7, π/3, 2}` | `E = 1.0`, `Z = 1.25`, `D = 3.5` for every `φ`; `S = 0.25, 0.19121054682112218, 0.12500000000000003, −0.10403670913678553` against `cos φ/4 = 0.25, 0.19121054682112212, 0.12500000000000003, −0.1040367091367856` | `quantities_vphi`; `zero_growth_at_pi_div_three` (`S = 1/8 = D/28` at `φ = π/3`) |
| `phase_family_modes.py` | exact Fourier expansion in `(x, y, z, φ)` of `\|u_φ\|²`, `\|ω\|²`, `\|∇ω\|²`, `ω·(∇u)ω`; prints the mode lists | constant terms `2`, `5/2`, `7/2` and `cos φ/4` (printed as `1/8 * cos φ + 1/8 * cos φ`); the lists are the ones in the proof of `quantities_vphi`, where the constant stretching mode is written `1/4 * cos φ` | `quantities_vphi` (PhaseFamily.lean) |
| `phase_family_modes_check.py` | evaluates each list from `phase_family_modes.py` at 5 random `(x, y, z, φ)` against the closed-form integrand | 20 of 20 comparisons `True` (agreement to `1e-12`) | the mode lists used for `quantities_vphi` |
| `quantities_v_modes.py` | the same expansion at `φ = 0` for `v`, plus `\|∇v\|²` | constant terms `2`, `5/2`, `7/2`, `1/4`, `5/2` with 7, 9, 7, 15, 7 modes; the lists are the ones in the proof of `quantities_v` | `quantities_v` (Averages.lean: `E = 1`, `Z = 5/4`, `D = 7/2`, `S = 1/4`, `⟨\|∇v\|²⟩ = 5/2`) |
| `scaling_counterexample.py` | `E, Z, D, S` of `v_k` for `k = 1…4`, spectral (`N = 48`) and 4th-order finite differences (`N = 64, 128`); the ratio `S / (Z^0.75 D^0.2)` | spectral: `E = 1`, `Z = 1.25, 5, 11.25, 20`, `D = 3.5, 56, 283.5, 896`, `S = 0.25, 2, 6.75, 16`, abs errors `≤ 1.4e-12`, `max \|div\| = 0`; FD4 at `N = 128` within relative `2.0e-4`; ratio `0.164605328589, 0.267402145199, 0.355163860817, 0.434396066457` equal to the predicted `0.1646… · k^0.7` | `quantities_vScaled` (`Z = 5k²/4`, `D = 7k⁴/2`, `S = k³/4`), `ratio_vScaled`, `no_power_law_bound`, `fitted_law_fails` (Scaling.lean) |

## Rainbow ([`rainbow/`](rainbow))

Descartes' bow: `D(i) = kπ + 2i − 2(k+1) r` with `sin i = n sin r`; the bow is
at `cos² i = (n² − 1)/(k(k+2))`. Red is `n = 1.331`, violet `n = 1.343`. Lean
names are in `WyrdMathlib/Rainbow/`.

| Script | What it checks | Key result | Cross-checks |
|---|---|---|---|
| `bow_angles_vs_index.py` | bow angles as a function of `n`, colour widths, slopes, and the index at which each bow crosses a whole degree | `n = 4/3`: primary `42.0297°`, secondary `50.9781°`; `n = 1.331`: `42.3698°`, `50.3651°`; `n = 1.343`: `40.6459°`, `53.4778°`; widths for `1.331 → 1.343`: `1.7240°` and `3.1126°`; primary `= 43°` at `n = 1.32672`, secondary `= 50°` at `n = 1.32962`. Its IAPWS table and wavelength lines use the index relative to vacuum and are superseded by the next script | `primary_bow_water` (`41°–43°`, true `42.03°`), `secondary_bow_water` (`50°–52°`, true `50.98°`), `primary_red`, `primary_violet`, `secondary_red`, `secondary_violet`, `colour_order`, `primary_spread` (`> 1°`), `secondary_spread` (`> 2°`), `dark_band_of_red_le` (every `n ≥ 1.331` is past both thresholds) |
| `water_index_air_relative.py` | index of water relative to air (IAPWS R9-97 over an Edlén-type air index) against the Quan & Fry (1995) fit at 20 °C and 10 °C; which wavelengths `n = 1.331` and `n = 1.343` correspond to; 400–700 nm widths | IAPWS check value `1.3344` (0 °C, 1000 kg/m³, 589 nm); IAPWS/air and Quan–Fry differ by at most `5e-5` from 400 to 750 nm; `n = 1.331` ↔ `663 nm` (20 °C), `694 nm` (10 °C); `n = 1.343` ↔ `402 nm`, `410 nm`; widths 400–700 nm: primary `1.874°` / `1.876°`, secondary `3.382°` / `3.387°` | the wavelengths quoted for red (`663–694 nm`) and violet (`402–410 nm`) in the [wyrd-mathlib README](../wyrd-mathlib/README.md#the-rainbow-wyrdmathlibrainbow); not a Lean theorem (Lean takes `n` as given) |
| `bow_lemma_intervals.py` | the exact rationals in the Lean statements; the bow-angle intervals implied by the four-decimal arcsin brackets proved in Lean; which other light paths reach 43°–50° | `k = 1`: `cos² i = 257187/1000000` (red), `267883/1000000` (violet), `sin² r = 742813/1771561`, `732117/1803649`; `k = 2`: `771561/8000000`, `803649/8000000`, `7228439/14172488`, `7196351/14429192`. Implied intervals: primary red `[42.353°, 42.388°]`, violet `[40.635°, 40.669°]`, secondary red `[50.121°, 50.626°]`, violet `[53.238°, 53.743°]`, all inside the stated whole-degree ranges (`conservative-ok=True`); widths `[1.684°, 1.753°]` and `[2.613°, 3.621°]`. At `n = 1.331`, paths with 0, 1 or 2 internal reflections stay out of 43°–50° (1 reaches up to `42.37°`, 2 starts at `50.37°`); 3 to 7 internal reflections enter it | `primary_red`, `primary_violet`, `secondary_red`, `secondary_violet`, `primary_spread`, `secondary_spread`; `alexander_dark_band` and its caveat that the band is darker, not black |
| `primary_spectrum_brackets.py` | finds, in exact rationals, the four-decimal brackets for `a = arcsin √(sin² r)`, `b = arcsin √(cos² i)` certified by the Taylor bounds `T5` (below) and `T7` (above), and the margins of `(180 + lo)π/180 < 4a + 2b < (180 + hi)π/180` | red: `a ∈ [0.7043, 0.7044]` (true `0.704342`), `b ∈ [0.5318, 0.5319]` (true `0.531859`), margins `0.00617` and `0.01068` rad; violet: `a ∈ [0.6907, 0.6908]`, `b ∈ [0.5440, 0.5441]`, margins `0.01108` and `0.00578` rad | `primary_red`, `primary_violet` (SpectrumPrimary.lean uses exactly these endpoints) |
| `secondary_spectrum_brackets.py` | checks, in exact rationals, the brackets used for `k = 2` and the margins of `d1 π/180 < 6a + 2b < d2 π/180` (secondary bow `= 360° − (6a + 2b)`) | all eight bracket conditions `True`: red `0.7949 < 0.795432 < 0.7959`, `0.3151 < 0.315778 < 0.3165`; violet `0.7836 < 0.784134 < 0.7846`, `0.3218 < 0.322510 < 0.3232`; margins red `0.00653` and `0.00212` rad, violet `0.00449` and `0.00416` rad | `secondary_red`, `secondary_violet` (lemmas `spectrumSecondary_{red,violet}_{a,b}_{lo,hi}` in SpectrumSecondary.lean) |

## Pangram ([`pangram/`](pangram))

| Script | What it checks | Key result | Cross-checks |
|---|---|---|---|
| `smallest_sum_search_cost.py` | a Python replica of the kernel search in `../wyrd/Wyrd/Minimal.lean` (`cands`, `ec`) over every even `N` from 1352 to 4294, with the same candidate primes, pair filter and letter rule; reads `../coupled_prime26_pangram.py` (or a path given as the first argument) | `\|V\| = 525` candidate primes; no "found at" line, so no pangram below 4296; 47625 candidate pairs and 40288 search nodes in total, at most 360 nodes for one sum (`N = 4080`); about 0.6 s | `smallest_pangram_sum`, `no_smaller_pangram` (`../wyrd/Wyrd/Smallest.lean`); `lower_bound` gives the start 1352. The complete enumeration of all solutions is in [`../checks`](../checks) |

## Body water

There is no numerical script for body water. The scratch folder `_raw/tbw/`
held only web pages fetched as sources for `../wyrd-mathlib/WyrdMathlib/BodyWater/`. The one
that the Lean files cite is *Body Composition in the Fetus and Newborn: Effects
of Intrauterine Growth Aberration*,
<https://abdominalkey.com/body-composition-in-the-fetus-and-newborn-effects-of-intrauterine-growth-aberration/>.
The figures taken from it, and where they are used:

| Statement in the source | Lean |
|---|---|
| "At term, the TBW is down to 78% of body weight, with 44% being in the ECW compartment, 34% in the ICW compartment, and the rest (22%) being solid body mass. At 1 year of age the TBW is approximately 70% of body weight; most of it is in the ICW (42%)" | `term_and_one_year_add_up` (Newborn.lean), `newborn_water_load` (`34/78` of a water load enters the cells, Osmotic.lean) |
| "During the first week of life, all newborn infants experience a reduction of extracellular body fluid with a maximum of 10% to 15%" | `water_fraction_falls`, `term_newborn_ten_percent_loss` (Newborn.lean) |
| Indicator dilution `V = I ÷ Pl_I` | `dilution_recovers` (Compartments.lean) |
| LGA infants have more fat and less total body water than AGA infants, SGA infants more water and less fat (term SGA versus AGA: 790 ± 13 versus 688 ± 16 mL/kg, Cassady and Milstead 1971) | `more_water_less_fat` (Newborn.lean) |

A second source, StatPearls *Physiology, Water Balance* (PMID 31082103, NCBI
Bookshelf NBK541059), could not be fetched: the Bookshelf returned a reCAPTCHA
page and the Europe PMC full-text request a 404, so only its metadata was
retrieved. The page copies themselves are not kept.

## What was not kept, and why

| Former file in `_raw/` | Reason |
|---|---|
| `build.py` | Not a numerical check: it spliced proofs into a `sorry` copy of `Limits/Bistability.lean` read from an absolute path. Its result is the finished `../wyrd-mathlib/WyrdMathlib/Limits/Bistability.lean`, which contains no `sorry`. |
| `f2.py` | One-off expansion of the polynomial `f2(u)` into exact coefficients while writing `bist_f2_pos`. Positivity is proved in Lean, and the minimum (`0.0021303` at `u = 2.1155`) is printed by `shared-air-limits/bistability_proof_brackets.py`. |
| `measure2.py` | Debugging variant of `measure.py` without the repeat-free-pair filter. It reports a spurious hit at `N = 1590` (`MP+MAP, LT+RBL, CIH+IEX, QJ+DWV, UZ+OSF`: 26 letters but only 22 distinct), which is why Lean's `cands` requires `nodupB`. |
| `limits/check2.py` | Subset of `num.py` (now `bistability_proof_brackets.py`): the same `f(y, g)` values at the brackets and the same `f2` minimum (`0.00213032` at `u ≈ 2.1155`, searched on `[0, 50]` instead of `[0, 10]`). |
| `limits/scaling_check.py` | Subset of `scalreview-num/check.py` (now `navier-stokes/scaling_counterexample.py`): same normalised `E, Z, D, S` and `ratio/k^0.7 = 0.164605328589`, without the finite-difference check. It also covered `k = 5`. |
| `limreview-num/check.py` | Needs scipy, which is not installed; otherwise identical to `limreview-num/check2.py`. |
| `limreview-num/check2.py` | Every number it prints is printed by a kept script: `g_sn = 2.0688849947` and the clinical values by `limits_checks.py`, both `g = 3` equilibria by `bistability_equilibria_sweep.py`, and `s*`, `g*`, `g_c` by `delay_argument_principle.py`. |
| `tbw/` (`ak.html`, `ak.txt`, `ncbi.html`, `ncbi.txt`, `ft.xml`, `probe.out`) | Not scripts: saved web pages (one third-party copy of a book chapter, a reCAPTCHA page, a 404 response, and Europe PMC metadata). Summarised under "Body water" above. |

No script needed a `misc/` folder.
