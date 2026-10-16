import Mathlib

/-!
# The linear system is the linearisation of the Shared Air equations

The "Perceived" equations, with input `U = 0`, no noise, baseline `A₀ = 0`,
steadiness `1` and no delay, are (`x = Aᵢ`, `y = Aₘ`, `z = C`):

* `x' = −x/30 − z + 0.04 g y − 0.02 x³`
* `y' = −y/20 + 0.10 g x − 0.02 y³`
* `z' = (0.30 g x · cap(y) − z)/4`, `cap(y) = 1/(1 + (y/0.8)²)`.

The origin is an equilibrium, and the derivative there along any direction is the
linear system in `Basic.lean` with `a = 1/30, b = 1/20, d = 1/4, r = 1/25,
q = 1/10, h = 3/40`.
-/

namespace Wyrd.SharedAir

/-- Response capacity. -/
noncomputable def cap (y : ℝ) : ℝ := 1 / (1 + (y / 0.8) ^ 2)

/-- The nonlinear vector field (zero input, zero noise, zero delay). -/
noncomputable def field (g : ℝ) (p : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  (-p.1 / 30 - p.2.2 + 0.04 * g * p.2.1 - 0.02 * p.1 ^ 3,
   -p.2.1 / 20 + 0.10 * g * p.1 - 0.02 * p.2.1 ^ 3,
   (0.30 * g * p.1 * cap p.2.1 - p.2.2) / 4)

/-- The linear system. -/
noncomputable def linField (g : ℝ) (p : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  (-p.1 / 30 - p.2.2 + g / 25 * p.2.1,
   -p.2.1 / 20 + g / 10 * p.1,
   -p.2.2 / 4 + 3 * g / 40 * p.1)

theorem field_zero (g : ℝ) : field g 0 = 0 := by
  sorry

/-- **Linearisation**: along every direction `v`, the field's derivative at the
origin is the linear system applied to `v`. -/
theorem hasDerivAt_field_line (g : ℝ) (v : ℝ × ℝ × ℝ) :
    HasDerivAt (fun t : ℝ => field g (t • v)) (linField g v) 0 := by
  sorry

end Wyrd.SharedAir
