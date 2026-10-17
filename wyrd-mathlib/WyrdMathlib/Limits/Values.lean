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

private lemma lt_rpow_inv_of_pow_lt' {a x : ℝ} {n : ℕ} (ha : 0 ≤ a) (hn : n ≠ 0)
    (h : a ^ n < x) : a < x ^ ((n : ℝ)⁻¹) := by
  have hpos : (0 : ℝ) < (n : ℝ)⁻¹ := inv_pos.mpr (Nat.cast_pos.mpr (Nat.pos_of_ne_zero hn))
  calc a = (a ^ n) ^ ((n : ℝ)⁻¹) := (Real.pow_rpow_inv_natCast ha hn).symm
    _ < x ^ ((n : ℝ)⁻¹) := Real.rpow_lt_rpow (pow_nonneg ha n) h hpos

private lemma rpow_inv_lt_of_lt_pow' {a x : ℝ} {n : ℕ} (hx : 0 ≤ x) (ha : 0 ≤ a) (hn : n ≠ 0)
    (h : x < a ^ n) : x ^ ((n : ℝ)⁻¹) < a := by
  have hpos : (0 : ℝ) < (n : ℝ)⁻¹ := inv_pos.mpr (Nat.cast_pos.mpr (Nat.pos_of_ne_zero hn))
  calc x ^ ((n : ℝ)⁻¹) < (a ^ n) ^ ((n : ℝ)⁻¹) := Real.rpow_lt_rpow hx h hpos
    _ = a := Real.pow_rpow_inv_natCast ha hn

theorem q10_per_degree :
    1.082 < (2.2 : ℝ) ^ (1 / 10 : ℝ) ∧ (2.2 : ℝ) ^ (1 / 10 : ℝ) < 1.0821 := by
  have e : (1 / 10 : ℝ) = ((10 : ℕ) : ℝ)⁻¹ := by norm_num
  rw [e]
  constructor
  · exact lt_rpow_inv_of_pow_lt' (by norm_num) (by norm_num) (by norm_num)
  · exact rpow_inv_lt_of_lt_pow' (by norm_num) (by norm_num) (by norm_num) (by norm_num)

theorem chest_warmth_rate :
    1.0279 < (2.2 : ℝ) ^ (0.035 : ℝ) ∧ (2.2 : ℝ) ^ (0.035 : ℝ) < 1.0281 := by
  have e : (2.2 : ℝ) ^ (0.035 : ℝ) = ((2.2 : ℝ) ^ (7 : ℕ)) ^ (((200 : ℕ) : ℝ)⁻¹) := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul (by norm_num : (0 : ℝ) ≤ 2.2)]
    congr 1
    norm_num
  rw [e]
  constructor
  · exact lt_rpow_inv_of_pow_lt' (by norm_num) (by norm_num) (by norm_num)
  · exact rpow_inv_lt_of_lt_pow' (by positivity) (by norm_num) (by norm_num) (by norm_num)

theorem chest_warmth_bpm :
    3.9 < 140 * ((2.2 : ℝ) ^ (0.035 : ℝ) - 1) ∧ 140 * ((2.2 : ℝ) ^ (0.035 : ℝ) - 1) < 3.94 := by
  obtain ⟨h1, h2⟩ := chest_warmth_rate
  constructor <;> linarith

/-- `T(t) = T_c (1 − e^(−t/400))` solves `T' = (T_c − T)/400` with `T(0) = 0`. -/
theorem warming_solution (Tc t : ℝ) :
    HasDerivAt (fun s => Tc * (1 - Real.exp (-s / 400)))
      ((Tc - Tc * (1 - Real.exp (-t / 400))) / 400) t ∧
    Tc * (1 - Real.exp (-0 / 400)) = 0 := by
  constructor
  · have h1 : HasDerivAt (fun s : ℝ => -s / 400) (-1 / 400) t :=
      (hasDerivAt_id' (x := t)).neg.div_const 400
    have h2 := ((h1.exp).const_sub 1).const_mul Tc
    convert h2 using 1
    ring
  · simp

theorem warming_after_twelve_minutes :
    0.8346 < 1 - Real.exp (-(720 / 400)) ∧ 1 - Real.exp (-(720 / 400)) < 0.8348 := by
  have hb := Real.exp_bound (x := -0.9) (by rw [abs_le]; constructor <;> norm_num) (n := 10)
    (by norm_num)
  rw [abs_le] at hb
  obtain ⟨hl, hu⟩ := hb
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial] at hl hu
  norm_num at hl hu
  have h1 : Real.exp (-0.9) ≤ 0.40657 := by linarith
  have h2 : 0.40656 ≤ Real.exp (-0.9) := by linarith
  have hy : 0 ≤ Real.exp (-0.9) := (Real.exp_pos _).le
  have e : Real.exp (-(720 / 400)) = Real.exp (-0.9) ^ 2 := by
    rw [sq, ← Real.exp_add]
    norm_num
  rw [e]
  constructor
  · nlinarith [mul_le_mul h1 h1 hy (by norm_num)]
  · nlinarith [mul_le_mul h2 h2 (by norm_num) hy]

theorem resting_rate_not_identifiable {ω V₀ : ℝ} (hω : 0 < ω) (hV : 0 < V₀) (hV' : V₀ < 2.5) :
    ∃ ω' V₀' : ℝ, (ω', V₀') ≠ (ω, V₀) ∧ 0 < ω' ∧ 0 < V₀' ∧ V₀' < 2.5 ∧
      ω' * (1 + 0.25 * 0.1) * (1 - 0.4 * V₀') = ω * (1 + 0.25 * 0.1) * (1 - 0.4 * V₀) := by
  have hk : 0 < 1 - 0.4 * V₀ := by linarith
  have hk' : 0 < 1 - 0.4 * (V₀ / 2) := by linarith
  refine ⟨ω * (1 - 0.4 * V₀) / (1 - 0.4 * (V₀ / 2)), V₀ / 2, ?_, ?_, ?_, ?_, ?_⟩
  · intro h
    simp only [Prod.mk.injEq] at h
    linarith [h.2]
  · exact div_pos (mul_pos hω hk) hk'
  · linarith
  · linarith
  · rw [div_mul_eq_mul_div, div_mul_eq_mul_div, div_eq_iff hk'.ne']
    ring

end Wyrd.Limits
