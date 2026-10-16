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

## Running it

```sh
cd experiments/wyrd-mathlib
lake exe cache get          # download Mathlib's prebuilt files (~3 min, ~7 GB)
lake build
lake env lean Audit.lean    # axioms used: no sorry, no native_decide
```

Skipping `cache get` means building Mathlib from source, which takes hours.
