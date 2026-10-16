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
  simp [field, cap]

/-- **Linearisation**: along every direction `v`, the field's derivative at the
origin is the linear system applied to `v`. -/
theorem hasDerivAt_field_line (g : ℝ) (v : ℝ × ℝ × ℝ) :
    HasDerivAt (fun t : ℝ => field g (t • v)) (linField g v) 0 := by
  obtain ⟨v1, v2, v3⟩ := v
  -- rewrite the map along the line as an explicit triple of real functions of `t`
  have hfun : (fun t : ℝ => field g (t • (v1, v2, v3))) = fun t =>
      (-(t * v1) / 30 - t * v3 + 0.04 * g * (t * v2) - 0.02 * (t * v1) ^ 3,
       -(t * v2) / 20 + 0.10 * g * (t * v1) - 0.02 * (t * v2) ^ 3,
       (0.30 * g * (t * v1) * cap (t * v2) - t * v3) / 4) := by
    funext t; simp [field, Prod.smul_mk, smul_eq_mul]
  rw [hfun]
  have h1 : HasDerivAt (fun t : ℝ => t * v1) v1 0 := by
    simpa using (hasDerivAt_id (0:ℝ)).mul_const v1
  have h2 : HasDerivAt (fun t : ℝ => t * v2) v2 0 := by
    simpa using (hasDerivAt_id (0:ℝ)).mul_const v2
  have h3 : HasDerivAt (fun t : ℝ => t * v3) v3 0 := by
    simpa using (hasDerivAt_id (0:ℝ)).mul_const v3
  -- `cap (t * v2)` is differentiable: it is the inverse of a never-vanishing polynomial
  have hden : HasDerivAt (fun t : ℝ => 1 + (t * v2 / 0.8) ^ 2)
      (2 * (0 * v2 / 0.8) ^ 1 * (v2 / 0.8)) 0 := by
    have := ((h2.div_const 0.8).pow 2).const_add 1
    simpa using this
  have hcap : HasDerivAt (fun t : ℝ => cap (t * v2))
      (-(2 * (0 * v2 / 0.8) ^ 1 * (v2 / 0.8)) / (1 + (0 * v2 / 0.8) ^ 2) ^ 2) 0 := by
    have := hden.inv (by positivity)
    convert this using 1
    funext t; simp [cap, one_div]
  show HasDerivAt _ (-v1 / 30 - v3 + g / 25 * v2, -v2 / 20 + g / 10 * v1,
    -v3 / 4 + 3 * g / 40 * v1) 0
  refine HasDerivAt.prodMk ?_ (HasDerivAt.prodMk ?_ ?_)
  · convert (((h1.neg.div_const 30).sub h3).add (h2.const_mul (0.04 * g))).sub
      ((h1.pow 3).const_mul 0.02) using 1
    -- the cubic term has zero derivative at the origin, and `0.04 = 1/25`
    rw [show (0.04:ℝ) = 1 / 25 by norm_num]
    simp only [zero_mul, ne_eq, Nat.add_one_sub_one, OfNat.ofNat_ne_zero, not_false_eq_true,
      zero_pow, mul_zero]
    ring
  · convert ((h2.neg.div_const 20).add (h1.const_mul (0.10 * g))).sub
      ((h2.pow 3).const_mul 0.02) using 1
    -- the cubic term has zero derivative at the origin, and `0.10 = 1/10`
    rw [show (0.10:ℝ) = 1 / 10 by norm_num]
    simp only [zero_mul, ne_eq, Nat.add_one_sub_one, OfNat.ofNat_ne_zero, not_false_eq_true,
      zero_pow, mul_zero]
    ring
  · convert ((((h1.const_mul (0.30 * g)).mul hcap).sub h3).div_const 4) using 1
    -- product rule at the origin: `cap 0 = 1` and the second summand carries a factor `0`
    rw [show (0.30:ℝ) = 3 / 10 by norm_num]
    simp only [cap, zero_mul, zero_div, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true, zero_pow,
      add_zero, div_one, mul_one, mul_zero]
    ring

end Wyrd.SharedAir
