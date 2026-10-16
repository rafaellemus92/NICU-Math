import WyrdMathlib.SharedAir.Optimal
import WyrdMathlib.SharedAir.Delay

/-!
# The Shared Air coefficients

`a = 1/30`, `b = 1/20`, `d = 1/4` (relaxation rates), `r = 1/25`, `q = 1/10`
(so `c = 1/250`), `h = 3/40`. Then

* `P(s, g) = (s + 1/30)(s + 1/20)(s + 1/4) + 3g/40 (s + 1/20) − g²/250 (s + 1/4)`;
* the optimal coupling is `g* ≈ 0.0803559`, with dominant eigenvalue `s* ≈ −0.0482709`;
* the equilibrium is stable exactly for `g < 15/8 + √2265/24 ≈ 3.858`, and unstable
  above it for every delay.

These values inherit the model's illustrative coefficients. They are not
biological estimates.
-/

namespace Wyrd.SharedAir

theorem hyp_sharedAir : Hyp (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) := by
  constructor <;> norm_num

/-- The model's matrix uses `r = 1/25`, `q = 1/10`, so `c = r q = 1/250`. -/
theorem c_sharedAir : (1 / 25 : ℝ) * (1 / 10) = 1 / 250 := by
  norm_num

theorem H_sharedAir (s : ℝ) :
    H (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) s =
      (s + 1 / 30) * (s + 1 / 4) ^ 2 + 45 / 128 * (s + 1 / 20) := by
  -- `h² / (4c) = (9/1600) / (4/250) = 45/128`
  unfold H
  norm_num

theorem G_sharedAir (s : ℝ) :
    G (1 / 20) (1 / 4) (1 / 250) (3 / 40) s = 75 / 8 * ((s + 1 / 20) / (s + 1 / 4)) := by
  -- `h / (2c) = (3/40) / (2/250) = 75/8`
  unfold G
  norm_num

theorem gc_sharedAir : gc (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) = 15 / 8 + Real.sqrt 2265 / 24 := by
  unfold gc
  -- the discriminant is `9/640000 + 1/600000 = 151/9600000 = 2265 · (1/12000)²`
  have hD : ((3 : ℝ) / 40) ^ 2 * (1 / 20) ^ 2 + 4 * (1 / 30) * (1 / 20) * (1 / 250) * (1 / 4) ^ 2
      = 2265 * (1 / 12000) ^ 2 := by norm_num
  rw [hD, Real.sqrt_mul (by norm_num), Real.sqrt_sq (by norm_num)]
  ring

/-- **The optimum, numerically**: the best dominant eigenvalue `s*` lies in
`(−0.048271, −0.048270)` and the optimal gain `g* = G(s*)` in `(0.08035, 0.08036)`. -/
theorem optimum_bounds {s : ℝ} (hs : s ∈ Set.Ioo (-(1 / 20) : ℝ) (-(1 / 30)))
    (hH : H (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) s = 0) :
    -0.048271 < s ∧ s < -0.04827 ∧
      0.08035 < G (1 / 20) (1 / 4) (1 / 250) (3 / 40) s ∧
      G (1 / 20) (1 / 4) (1 / 250) (3 / 40) s < 0.08036 := by
  have hmono := H_strictMonoOn hyp_sharedAir
  obtain ⟨hs1, hs2⟩ := hs
  have hsI : s ∈ Set.Ioi (-(1 / 20 : ℝ)) := hs1
  -- tight bracket: `H(-0.048270930) < 0 = H(s) < H(-0.048270910)`, and `H` is strictly increasing
  have hlo : (-0.048270930 : ℝ) < s :=
    (hmono.lt_iff_lt (by norm_num [Set.mem_Ioi]) hsI).mp (by rw [hH, H_sharedAir]; norm_num)
  have hhi : s < (-0.048270910 : ℝ) :=
    (hmono.lt_iff_lt hsI (by norm_num [Set.mem_Ioi])).mp (by rw [hH, H_sharedAir]; norm_num)
  have hpos : 0 < s + 1 / 4 := by linarith
  refine ⟨by linarith, by linarith, ?_, ?_⟩
  · -- clear the positive denominator; the resulting inequality is linear in `s`
    rw [G_sharedAir, ← mul_div_assoc, lt_div_iff₀ hpos]
    linarith
  · rw [G_sharedAir, ← mul_div_assoc, div_lt_iff₀ hpos]
    linarith

/-- The critical coupling is about `3.858`. -/
theorem gc_bounds : 3.858 < gc (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) ∧
    gc (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) < 3.8581 := by
  rw [gc_sharedAir]
  -- `47.592 < √2265 < 47.593` (note `15/8 + 47.592/24 = 3.858` exactly)
  have h1 : (47.592 : ℝ) < Real.sqrt 2265 := by
    rw [Real.lt_sqrt (by norm_num)]; norm_num
  have h2 : Real.sqrt 2265 < 47.593 := by
    rw [Real.sqrt_lt' (by norm_num)]; norm_num
  constructor <;> linarith

/-- Coupling `g = 3` (the top of the model's own sweep) is still stable. -/
theorem stable_at_three :
    ∀ z : ℂ, Pc (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) 3 z = 0 → z.re < 0 := by
  exact (stable_iff hyp_sharedAir (by norm_num : (0 : ℝ) ≤ 3)).mpr (by linarith [gc_bounds.1])

/-- **Above the critical coupling the equilibrium is unstable for every delay.** -/
theorem unstable_every_delay {g τ : ℝ} (hg : 15 / 8 + Real.sqrt 2265 / 24 < g) (hτ : 0 ≤ τ) :
    ∃ s : ℝ, 0 < s ∧ Dd (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) g τ s = 0 := by
  have hr0 : 0 ≤ Real.sqrt 2265 := Real.sqrt_nonneg _
  have hr2 : Real.sqrt 2265 ^ 2 = 2265 := Real.sq_sqrt (by norm_num)
  have hg0 : 0 ≤ g := by linarith
  -- `P(0, g) = 1/2400 + 3g/800 - g²/1000 = -(1/1000) (g - g_c) (g - g')` with
  -- `g_c, g' = 15/8 ± √2265/24`; both factors are positive for `g > g_c`.
  have hP : P (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) g 0 < 0 := by
    rw [P_zero]
    have e1 : 0 < g - (15 / 8 + Real.sqrt 2265 / 24) := by linarith
    have e2 : 0 < g - (15 / 8 - Real.sqrt 2265 / 24) := by linarith
    nlinarith [mul_pos e1 e2]
  exact delay_unstable (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    hg0 hτ hP

end Wyrd.SharedAir
