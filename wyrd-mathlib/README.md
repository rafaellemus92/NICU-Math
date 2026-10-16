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

**Not formalised:** the enstrophy balance `dZ/dt = S − νD` and local existence of
smooth solutions (both standard; Mathlib has no Navier–Stokes theory). Turning
`no_closure` into a statement about solutions needs them. The uniform stretching
estimate that would make the Grönwall route prove regularity is the open problem
itself and is not claimed. Context: OpenAI's September 2026 manuscript claims
blow-up *with a smooth external force* (Clay's alternatives C/D); Clay's
11 September 2026 statement says the problem has "apparently been settled" and
that review is ongoing.

## Running it

```sh
cd experiments/wyrd-mathlib
lake exe cache get          # download Mathlib's prebuilt files (~3 min, ~7 GB)
lake build
lake env lean Audit.lean    # axioms used: no sorry, no native_decide
```

Skipping `cache get` means building Mathlib from source, which takes hours.
