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
  sorry

/-- The model's matrix uses `r = 1/25`, `q = 1/10`, so `c = r q = 1/250`. -/
theorem c_sharedAir : (1 / 25 : ℝ) * (1 / 10) = 1 / 250 := by
  sorry

theorem H_sharedAir (s : ℝ) :
    H (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) s =
      (s + 1 / 30) * (s + 1 / 4) ^ 2 + 45 / 128 * (s + 1 / 20) := by
  sorry

theorem G_sharedAir (s : ℝ) :
    G (1 / 20) (1 / 4) (1 / 250) (3 / 40) s = 75 / 8 * ((s + 1 / 20) / (s + 1 / 4)) := by
  sorry

theorem gc_sharedAir : gc (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) = 15 / 8 + Real.sqrt 2265 / 24 := by
  sorry

/-- **The optimum, numerically**: the best dominant eigenvalue `s*` lies in
`(−0.048271, −0.048270)` and the optimal gain `g* = G(s*)` in `(0.08035, 0.08036)`. -/
theorem optimum_bounds {s : ℝ} (hs : s ∈ Set.Ioo (-(1 / 20) : ℝ) (-(1 / 30)))
    (hH : H (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) s = 0) :
    -0.048271 < s ∧ s < -0.04827 ∧
      0.08035 < G (1 / 20) (1 / 4) (1 / 250) (3 / 40) s ∧
      G (1 / 20) (1 / 4) (1 / 250) (3 / 40) s < 0.08036 := by
  sorry

/-- The critical coupling is about `3.858`. -/
theorem gc_bounds : 3.858 < gc (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) ∧
    gc (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) < 3.8581 := by
  sorry

/-- Coupling `g = 3` (the top of the model's own sweep) is still stable. -/
theorem stable_at_three :
    ∀ z : ℂ, Pc (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) 3 z = 0 → z.re < 0 := by
  sorry

/-- **Above the critical coupling the equilibrium is unstable for every delay.** -/
theorem unstable_every_delay {g τ : ℝ} (hg : 15 / 8 + Real.sqrt 2265 / 24 < g) (hτ : 0 ≤ τ) :
    ∃ s : ℝ, 0 < s ∧ Dd (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) g τ s = 0 := by
  sorry

end Wyrd.SharedAir
