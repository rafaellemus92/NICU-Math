# wyrd-mathlib: our proofs, connected to Mathlib

A sister project to [`../wyrd`](../wyrd). It depends on both
[Mathlib](https://github.com/leanprover-community/mathlib4) (`v4.35.0`, the
same Lean version as `wyrd`) and on `wyrd` itself. `wyrd` stays core-Lean
only, so it builds without the 7 GB Mathlib download.

## What's here

| Theorem | Statement |
|---|---|
| `isPrime_iff` | Our `IsPrime` is exactly Mathlib's `Nat.Prime` |
| `setOf_prime_infinite` | Mathlib's "the primes form an infinite set", proved by **our** Euclid |
| `solution_primes` | The ten pangram primes are `Nat.Prime` |
| `irrational_sqrt_two` | `Irrational (√2)` for the real number, derived from **our** core-Lean descent proof |
| `bertrand` | Bertrand's postulate (a prime between `n` and `2n`) for our `IsPrime`, from Mathlib's `Nat.bertrand` |

Once the bridge exists, anything Mathlib knows about primes applies to our
results, and the reverse.

## The rainbow (`WyrdMathlib/Rainbow/`)

Descartes' theory of the rainbow, proved. Sunlight enters a spherical drop at
angle `i`, bends by Snell's law (`sin i = n sin r`), reflects `k` times inside,
and leaves, turned by `D(i) = kπ + 2i − 2(k+1)r`. The light piles up where `D`
is stationary, and that bright fold is the bow.

| Theorem | Statement |
|---|---|
| `snell` | The refraction angle really satisfies Snell's law |
| `hasDerivAt_dev` | `D'(i) = 2 − 2(k+1) cos i / √(n² − sin² i)` |
| `deriv_dev_eq_zero_iff_eq` | For `1 < n < k+1`, the **only** stationary point on `[0, π/2]` is where `cos² i = (n² − 1)/(k(k+2))` (Newton and Halley's formula) |
| `dev_lt_of_ne`, `dev_isMinOn` | It is the **strict minimum** of the deviation |
| `water_primary`, `water_secondary` | Water (`n = 4/3`): `cos² i = 7/27` (primary) and `7/72` (secondary) |
| `primary_bow_water` | The primary bow is seen between **41° and 43°** from the antisolar point (true value 42.03°) |
| `secondary_bow_water` | The secondary bow between **50° and 52°** (true value 50.98°) |
| `alexander_dark_band` | **No light** with one or two internal reflections leaves between 43° and 50°, which is why the sky between the bows is darker |
| `colour_order` | **Colours**: a larger index (violet) gives a smaller primary bow and a larger secondary bow, so red is outside in the primary and inside in the secondary |
| `primary_red`, `primary_violet` | Real water: primary bow at 42–43° for red (`n = 1.331`) and 40–41° for violet (`n = 1.343`) |
| `secondary_red`, `secondary_violet` | Secondary bow at 50–51° (red) and 53–54° (violet) |
| `primary_spread`, `secondary_spread` | The colours spread over more than 1° (primary) and more than 2° (secondary) |
| `dark_band_of_red_le` | Red governs both edges of the dark band, so it holds for **every** colour from red (`n ≥ 1.331`) up |

The numeric bounds need sin and cos to about four decimal places, and Mathlib's
bounds stop at degree 3, so `TrigBounds.lean` proves Taylor bounds to degree 7
(each from the previous one, by a derivative argument). The colour theorems use
water's index for red (`1.331`, about 663–694 nm) and violet (`1.343`, about
402–410 nm). The ordering needs no calculus in `n`: a larger index bends every
ray more, so the minimum deviation (the bow) grows too.

The "dark" band is *darker*, not black: the theorems exclude refracted light
reflected once or twice, while external reflection, higher-order bows,
diffraction and the sun's disc still put some light there.

## Body water (`WyrdMathlib/BodyWater/`)

The physiology of total body water, as theorems about simple models. These are
**for understanding, not dosing**; every file says what its model leaves out.
Newborn figures come from *Body Composition in the Fetus and Newborn: Effects of
Intrauterine Growth Aberration* (abdominalkey.com).

| Theorem | Statement |
|---|---|
| `dilution_recovers`, `dilution_overestimate` | Indicator dilution `V = I / C` works, and tracer lost before sampling always makes the volume look bigger, by `1/(1 − e)` (e.g. D₂O overstates TBW by about 4%) |
| `water_load_split`, `adult_water_load`, `newborn_water_load` | Free water spreads in proportion to effective osmoles: 2/3 into the cells for an adult, only 34/78 ≈ 43.6% for a term newborn |
| `isotonic_stays_extracellular` | Isotonic fluid whose solute stays out (0.9% saline) leaves cell water unchanged (iso-osmolar dextrose does not) |
| `solute_load_shrinks_cells` | Extra effective solute outside the cells shrinks them |
| `adrogue_madias` | From Edelman's relation: `v` litres at concentration `c` change sodium by `v(c − Na)/(W + v)` |
| `per_litre_scaling_underestimates` | Scaling the per-litre form `(c − Na)/(TBW + 1)` down to a small volume **underestimates** the model change; about 42% for 10 mL in a 3 kg newborn |
| `smaller_body_bigger_change_abs` | The same fluid moves sodium further, in either direction, in a smaller body |
| `free_water_deficit` | `W(Na/140 − 1)` litres of free water bring model sodium to 140 (a total, never a rate) |
| `water_fraction_falls` | Losing extracellular water after birth lowers the body's water fraction |
| `more_water_less_fat` | At equal fat-free-mass hydration, more water means less fat, consistent with term SGA (more water) and LGA (more fat) infants |

## Periodic Navier–Stokes (`WyrdMathlib/PeriodicNS/`)

An explicit periodic field showing that **magnitude-only descriptions lose the
information that decides vortex stretching**. Take
`v = (sin y, sin z, cos x − cos(x + y))` on the `2π`-periodic cube, with every
derivative computed by Lean's `deriv` and every average a genuine integral over
`[0, 2π]³`.

| Theorem | Statement |
|---|---|
| `div_v`, `curl_v`, `grad_v` | `v` is divergence-free, with vorticity `(sin(x+y) − cos z, sin x − sin(x+y), −cos y)` |
| `quantities_v` | `E = 1`, `Z = 5/4`, `D = ⟨\|∇ω\|²⟩ = 7/2`, stretching `S = 1/4`, `⟨\|∇v\|²⟩ = 5/2` |
| `quantities_smul`, `same_spectrum` | `±A v` share `E`, `Z`, `D` and every Fourier magnitude, but `S = ±A³/4` |
| `opposite_signs`, `rates` | So `S − νD` has opposite signs once `A > 14ν` (`1/8` and `−3/8` at `A = 1`, `ν = 1/28`) |
| `no_closure`, `no_spectral_closure` | `S − νD` is not a function of `(E, Z, D, ν)`, nor of all Fourier magnitudes plus `ν` |
| `galerkin_enstrophy_bound` | A fixed Fourier cutoff gives `Z_K ≤ K² E_K(0)`: bounded, but worse as `K → ∞` |
| `gronwall_variable` | `Z' ≤ a Z ⇒ Z(t) ≤ Z(0) exp ∫₀ᵗ a`: the step a regularity proof would use |
| `energy_vanishes_speed_blows` | A shrinking core can carry vanishing energy while its speed blows up |
| `not_B_implies_D`, `D_and_B_consistent` | Clay (B) failing gives (D); (D) with forcing does not refute (B) |

**The phase family** `u_φ = (sin y, sin z, cos x − cos(x + y + φ))` (from the lab
packages; audit in [`../ns-phase-audit`](../ns-phase-audit)):

| Theorem | Statement |
|---|---|
| `quantities_vphi`, `growth_iff` | `E = 1`, `Z = 5/4`, `D = 7/2` for every `φ`, but `S = cos φ / 4`. So `S − νD > 0` exactly when `cos φ > 14ν/A` |
| `zero_growth_at_pi_div_three`, `neg_v_translate` | `φ = π/3` has zero initial growth at `ν = 1/28`, and `−v` is `u_π` shifted by `(π, π, π)` |
| `rotShift_vphi`, `mirror_fixes_vphi`, `quantities_even` | A rotation by `π` about `z` plus a shift maps `u_φ` to `u_{−φ}`, and a mirror fixes `u_φ` |
| `not_before`, `at_first_order`, `order_seven_m_two` | The counting core of the harmonic selection rules: given the 2D-3C fact, a `cos mφ` term (`\|m\| ≥ 2`) in the enstrophy Taylor series cannot appear before `t^{3\|m\|}`. There it is `ν`-free; at `t⁷` the `cos 2φ` term is `∝ ν` |

**Not formalised:** the enstrophy balance `dZ/dt = S − νD` and local existence of
smooth solutions (both standard; Mathlib has no Navier–Stokes theory). Turning
`no_closure` into a statement about solutions needs them. The uniform stretching
estimate that would make the Grönwall route prove regularity is the open problem
itself and is not claimed. Context: OpenAI's September 2026 manuscript claims
blow-up *with a smooth external force* (Clay's alternatives C/D); Clay's
11 September 2026 statement says the problem has "apparently been settled" and
that review is ongoing.

## Shared Air (`WyrdMathlib/SharedAir/`)

An audit of the *Shared Air* mother–infant model's equations, not of its
biology. The perceived world, linearised at zero input and zero noise, is
`x' = −a x − z + r g y`, `y' = −b y + q g x`, `z' = −d z + h g x` with the
model's coefficients `a = 1/30`, `b = 1/20`, `d = 1/4`, `r q = 1/250`, `h = 3/40`.

| Theorem | Statement |
|---|---|
| `hasFDerivAt_field`, `linField_eq_sysMatrix` | That linear system really is the Fréchet derivative of the model's nonlinear field (cap and cubic terms included) at rest |
| `optimal_coupling`, `optimum_bounds` | At zero delay there is exactly one best coupling `g* ∈ (0.08035, 0.08036)`, with decay rate `−s*`, `s* ∈ (−0.048271, −0.048270)` |
| `stable_iff`, `gc_bounds` | At zero delay the rest state is stable exactly when `g < g_c = 15/8 + √2265/24 ≈ 3.858` |
| `delay_unstable`, `unstable_every_delay` | Above `g_c` it is unstable for **every** delay |
| `same_synchrony_different_future_24`, `synchrony_rates` | Two 24-cell populations with the same synchrony `‖Z₁‖ = 1/2` whose synchrony changes at different rates (`K/4` and `0`): one number cannot predict its own future |
| `hasDerivAt_freeEnergy`, `equilibrium_eq`, `equilibrium_exists` | Osmotic water flow is a gradient flow: free energy never increases, and equilibrium means equal osmolality everywhere |
| `aggregate_counterexample` | Equal total cell volume can carry different net water flux |
| `contrast_pos_without_coupling` | A noisier control adult makes `corr(infant, mom) − corr(infant, control)` positive with **no** bond at all |
| `averaged_stable_equilibrium_iff`, `two_to_one_moments` | First-order averaged 2:1 locking holds iff `\|Δ\| < k`. A perfect 2:1 lock has first moment 0 and second moment 1 |

**Delay caveat (numerical, not Lean):** below `g_c` delay can still destabilise.
Two independent methods (imaginary-axis crossing, Chebyshev collocation)
give `τ ≈ 1.8356 s` at `g = 3` and `τ ≈ 4.7613 s` at `g = 1`. The zero-delay results
must not be read as statements about the delayed model.

## What the Shared Air model can't tell you (`WyrdMathlib/Limits/`)

The model's own list of limits, turned into theorems where mathematics has
something exact to say.

| Limit | Theorems | What is proved |
|---|---|---|
| Ratios other than n:1 | `lockIndex_eq_one`, `lockIndex_eq_zero`, `three_two_looks_like_three_one`, `five_three_hidden`, `resonant_average_vanishes`, `model_forcing_misses_n_m` | Under a perfect `n:m` lock the `k`-th harmonic index is 1 if `n ∣ k`, else 0. It counts bands, not ratios: 3:2 reads exactly like 3:1, and 5:3 and 4:3 are invisible to the 2nd and 3rd harmonics. For every periodic pulse shape, forcing through `sin θ` has zero first-order average along any `n:m` orbit with `m > 1` |
| Direction of influence | `calming_reverses_lag`, `mirroring_keeps_lag`, `room_leaks_when_unmatched`, `room_cancels_iff` | Same leader, opposite assumed sign of response: the correlation peak moves from "mom first" to "infant first". A control whose exposure is timed differently produces a lag signal with no bond |
| Which world is real | `alike_explains_any_one_condition`, `two_conditions_never_enough`, `additive_identified`, `three_conditions_miss_interaction`, `four_conditions_identify_interaction` | One or two bedside conditions never identify the mixture. Bedside-awake, skin-awake and skin-asleep do (the sleeping mother separates the paths). With interaction, the full 2 × 2 design is needed |
| How many sessions | `sessions_chebyshev`, `sessions_enough` | A distribution-free Chebyshev bound: error `≤ δ` once `n ≥ 4σ²/(δΔ²)` |
| Arousal is one number | `no_coactivation`, `vagal_determined_by_symp` | Sympathetic drive above rest forces vagal tone below rest; co-activation is unrepresentable |
| Clinical values | `q10_per_degree`, `chest_warmth_bpm`, `warming_after_twelve_minutes`, `resting_rate_not_identifiable` | The stated numbers agree: 8.2% per °C, about 3.9 bpm at 140 bpm, 83.5% warmed after 12 min. Resting rate cannot separate the cells' own rate from vagal tone |
| Whose good | `mom_untouched_iff`, `infant_best_moves_mom` | Mom stays at rest exactly when `g = 0`, while the system's best recovery needs `g* > 0`. No coupling serves both; the objective is a choice |
| Test 4's second state | `only_rest_without_cap`, `only_rest_upto_two`, `coarousal_exists_above_two`, `coarousal_stable_at_three`, `cubic_hurwitz` | Without the capacity limit, rest is the only equilibrium on the whole sweep `0 ≤ g ≤ 3`. With it, rest is still the only one up to `g = 2`; a co-arousal equilibrium appears by `g = 2.1`, and at `g = 3` it is linearly stable, so the pair is bistable |

Not mathematics, and not claimed: which world is real (only recordings decide),
life before birth and the placenta, and any number as a clinical value.

## Running it

```sh
cd experiments/wyrd-mathlib
lake exe cache get          # download Mathlib's prebuilt files (~3 min, ~7 GB)
lake build
lake env lean Audit.lean    # axioms used: no sorry, no native_decide
```

Skipping `cache get` means building Mathlib from source, which takes hours.
