import Mathlib

/-!
# Clinical values: what can be checked, and what cannot be supplied

The source: "Every parameter was chosen to give realistic resting heart and
breathing rates, not fitted to patients." Mathematics cannot turn a chosen
parameter into a clinical value. It can check that the stated numbers agree with
each other, and show why resting rates cannot pin the parameters down.

* `q10_per_degree`: `Q10 = 2.2` means a factor `2.2^(1/10) ∈ (1.0820, 1.0821)`
  per degree. That matches the source's "about 8% faster per degree".
* `chest_warmth_rate`, `chest_warmth_bpm`: the default chest warmth `0.35 °C`
  gives a factor `2.2^0.035 ∈ (1.0279, 1.0281)`. At 140 bpm that is between 3.9
  and 3.94 bpm, the source's "a few beats per minute" that "will hide in noise".
* `warming_solution`, `warming_after_twelve_minutes`: with the 400 s time
  constant, the infant's temperature after the 12 minutes of skin-to-skin in
  Test 6 has covered `1 − e^(−1.8) ∈ (0.8346, 0.8348)` of the way.
* `resting_rate_not_identifiable`: the resting rate
  `ω (1 + 0.25 · 0.1)(1 − 0.4 V₀)` (expiration, `A = 0`, `T = 0`) is the same for
  a one-parameter family of `(ω, V₀)`. A resting heart rate cannot recover
  intrinsic rate and vagal tone separately.
-/

namespace Wyrd.Limits

theorem q10_per_degree :
    1.082 < (2.2 : ℝ) ^ (1 / 10 : ℝ) ∧ (2.2 : ℝ) ^ (1 / 10 : ℝ) < 1.0821 := by
  sorry

theorem chest_warmth_rate :
    1.0279 < (2.2 : ℝ) ^ (0.035 : ℝ) ∧ (2.2 : ℝ) ^ (0.035 : ℝ) < 1.0281 := by
  sorry

theorem chest_warmth_bpm :
    3.9 < 140 * ((2.2 : ℝ) ^ (0.035 : ℝ) - 1) ∧ 140 * ((2.2 : ℝ) ^ (0.035 : ℝ) - 1) < 3.94 := by
  sorry

/-- `T(t) = T_c (1 − e^(−t/400))` solves `T' = (T_c − T)/400` with `T(0) = 0`. -/
theorem warming_solution (Tc t : ℝ) :
    HasDerivAt (fun s => Tc * (1 - Real.exp (-s / 400)))
      ((Tc - Tc * (1 - Real.exp (-t / 400))) / 400) t ∧
    Tc * (1 - Real.exp (-0 / 400)) = 0 := by
  sorry

theorem warming_after_twelve_minutes :
    0.8346 < 1 - Real.exp (-(720 / 400)) ∧ 1 - Real.exp (-(720 / 400)) < 0.8348 := by
  sorry

theorem resting_rate_not_identifiable {ω V₀ : ℝ} (hω : 0 < ω) (hV : 0 < V₀) (hV' : V₀ < 2.5) :
    ∃ ω' V₀' : ℝ, (ω', V₀') ≠ (ω, V₀) ∧ 0 < ω' ∧ 0 < V₀' ∧ V₀' < 2.5 ∧
      ω' * (1 + 0.25 * 0.1) * (1 - 0.4 * V₀') = ω * (1 + 0.25 * 0.1) * (1 - 0.4 * V₀) := by
  sorry

end Wyrd.Limits
