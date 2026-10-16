import Mathlib.Analysis.SpecialFunctions.Trigonometric.Inverse
import Mathlib.Analysis.SpecialFunctions.Sqrt

/-!
# The rainbow: definitions

Descartes (1637): sunlight enters a spherical raindrop at incidence angle `i`,
bends to angle `r` (Snell's law, `sin i = n · sin r`, `n` = refractive index),
reflects `k` times inside the drop, and leaves. Each event turns the ray:

* entering and leaving: `i - r` each;
* each internal reflection: `π - 2r`.

So the total deviation is `D(i) = 2(i - r) + k(π - 2r) = kπ + 2i - 2(k+1)r`.

Rays pile up where `D` is stationary. That bright fold (a *caustic*) is the
rainbow. `k = 1` is the primary bow, `k = 2` the secondary.
-/

namespace Wyrd.Rainbow

open Real

/-- Refraction angle inside the drop, from Snell's law `sin i = n · sin r`. -/
noncomputable def refr (n i : ℝ) : ℝ := arcsin (sin i / n)

/-- Total deviation of a ray entering at incidence `i` and reflecting `k` times inside. -/
noncomputable def dev (k : ℕ) (n i : ℝ) : ℝ := k * π + 2 * i - 2 * (k + 1) * refr n i

/-- The incidence angle of the `k`-th bow: where `cos² i = (n² - 1) / (k(k+2))`. -/
noncomputable def bowIncidence (k : ℕ) (n : ℝ) : ℝ := arccos (√((n ^ 2 - 1) / (k * (k + 2))))

/-- `refr` really satisfies Snell's law (for `n ≥ 1`, so `sin i / n` is a valid sine). -/
theorem snell {n : ℝ} (hn : 1 ≤ n) (i : ℝ) : n * sin (refr n i) = sin i := by
  have hn0 : 0 < n := by linarith
  have h1 : -1 ≤ sin i / n := by
    rw [le_div_iff₀ hn0]; nlinarith [neg_one_le_sin i, sin_le_one i]
  have h2 : sin i / n ≤ 1 := by
    rw [div_le_iff₀ hn0]; nlinarith [neg_one_le_sin i, sin_le_one i]
  rw [refr, sin_arcsin h1 h2]
  field_simp

end Wyrd.Rainbow
