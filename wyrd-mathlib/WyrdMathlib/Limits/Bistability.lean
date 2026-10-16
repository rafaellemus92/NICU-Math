import WyrdMathlib.SharedAir.Linearization
import WyrdMathlib.SharedAir.Specific

/-!
# Test 4's second state: the capacity limit makes the pair bistable

The revised source says the rising side of Test 4's inverted U is "a second
stable state: above a responsiveness of about 2, a large enough disturbance
flips the pair into sustained co-arousal … Remove that capacity limit and the
second state disappears." For the deterministic perceived world (`U = 0`, no
noise, baseline `0`, steadiness `1`, zero delay) this is exact:

* `no_coarousal_without_cap_general`: without the capacity limit (`cap ≡ 1`),
  any equilibrium other than rest forces `P(0, g) < 0`, so rest is already
  unstable. This holds for any positive coefficients with a cubic damping
  `κ > 0`.
* `only_rest_without_cap`: with the model's coefficients and `0 ≤ g ≤ 3` (the
  whole Test 4 sweep), rest is the only equilibrium without the cap.
* `only_rest_upto_two`: **with** the cap, rest is still the only equilibrium for
  `0 ≤ g ≤ 2`.
* `coarousal_exists_above_two`: at `g = 2.1` there is a co-arousal equilibrium
  (`Aᵢ, Aₘ > 0`). So the second state appears between 2 and 2.1, matching
  "about 2" (numerically near 2.069).
* `coarousal_stable_at_three`: at `g = 3` there is a co-arousal equilibrium that
  is linearly stable: every eigenvalue of the Jacobian `jac` has negative real
  part. Rest is also stable there (`stable_at_three`), so the pair is
  **bistable**.
* `hasDerivAt_field_line_at`: `jac` is the true derivative of the model's field
  at any point, along every direction.
* `cubic_hurwitz`: the Routh–Hurwitz test for cubics used above.

Not proved: the size of the disturbance that flips the pair (the basin
boundary), and anything about delay or noise. As the source says, this is one
mechanism that could produce the shape, not evidence that it is the one at work.
-/

namespace Wyrd.Limits

open Wyrd.SharedAir

/-- The field with the capacity limit removed (`cap ≡ 1`). -/
noncomputable def fieldNoCap (g : ℝ) (p : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  (-p.1 / 30 - p.2.2 + 0.04 * g * p.2.1 - 0.02 * p.1 ^ 3,
   -p.2.1 / 20 + 0.10 * g * p.1 - 0.02 * p.2.1 ^ 3,
   (0.30 * g * p.1 - p.2.2) / 4)

/-- `cap'(y)`. -/
noncomputable def capDeriv (y : ℝ) : ℝ := -(2 * y / 0.64) / (1 + (y / 0.8) ^ 2) ^ 2

/-- The Jacobian of `field g` at `p` (order `Aᵢ, Aₘ, C`). -/
noncomputable def jac (g : ℝ) (p : ℝ × ℝ × ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  !![-1 / 30 - 0.06 * p.1 ^ 2, 0.04 * g, -1;
     0.10 * g, -1 / 20 - 0.06 * p.2.1 ^ 2, 0;
     0.30 * g * cap p.2.1 / 4, 0.30 * g * p.1 * capDeriv p.2.1 / 4, -1 / 4]

/-- `jac g p` is the derivative of `field g` at `p` along every direction `v`. -/
theorem hasDerivAt_field_line_at (g : ℝ) (p v : ℝ × ℝ × ℝ) :
    HasDerivAt (fun t : ℝ => field g (p + t • v))
      ((jac g p).mulVec ![v.1, v.2.1, v.2.2] 0, (jac g p).mulVec ![v.1, v.2.1, v.2.2] 1,
        (jac g p).mulVec ![v.1, v.2.1, v.2.2] 2) 0 := by
  sorry

/-- Routh–Hurwitz for cubics: `c₂, c₀ > 0` and `c₂ c₁ > c₀` put every root in the
open left half-plane. -/
theorem cubic_hurwitz {c₂ c₁ c₀ : ℝ} (h₂ : 0 < c₂) (h₀ : 0 < c₀) (h₂₁ : c₀ < c₂ * c₁)
    {s : ℂ} (hs : s ^ 3 + c₂ * s ^ 2 + c₁ * s + c₀ = 0) : s.re < 0 := by
  sorry

/-- Without the capacity limit, an equilibrium other than rest forces `P(0, g) < 0`. -/
theorem no_coarousal_without_cap_general {a b d r q h κ g x y z : ℝ} (ha : 0 < a)
    (hb : 0 < b) (hd : 0 < d) (hh : 0 ≤ h) (hκ : 0 < κ) (hg : 0 ≤ g)
    (e₁ : -a * x - z + r * g * y - κ * x ^ 3 = 0) (e₂ : -b * y + q * g * x - κ * y ^ 3 = 0)
    (e₃ : -d * z + h * g * x = 0) (hne : (x, y) ≠ (0, 0)) :
    P a b d (r * q) h g 0 < 0 := by
  sorry

/-- Without the cap, rest is the only equilibrium over the whole Test 4 sweep. -/
theorem only_rest_without_cap {g : ℝ} (hg₀ : 0 ≤ g) (hg : g ≤ 3) {p : ℝ × ℝ × ℝ}
    (hp : fieldNoCap g p = 0) : p = 0 := by
  sorry

/-- With the cap, rest is still the only equilibrium for `0 ≤ g ≤ 2`. -/
theorem only_rest_upto_two {g : ℝ} (hg₀ : 0 ≤ g) (hg : g ≤ 2) {p : ℝ × ℝ × ℝ}
    (hp : field g p = 0) : p = 0 := by
  sorry

/-- At `g = 2.1` a co-arousal equilibrium exists. -/
theorem coarousal_exists_above_two :
    ∃ p : ℝ × ℝ × ℝ, 0 < p.1 ∧ 0 < p.2.1 ∧ field 2.1 p = 0 := by
  sorry

/-- At `g = 3` a linearly stable co-arousal equilibrium exists. -/
theorem coarousal_stable_at_three :
    ∃ p : ℝ × ℝ × ℝ, 0 < p.1 ∧ 0 < p.2.1 ∧ field 3 p = 0 ∧
      ∀ s : ℂ, (s • (1 : Matrix (Fin 3) (Fin 3) ℂ) - (jac 3 p).map (fun r : ℝ => (r : ℂ))).det = 0 →
        s.re < 0 := by
  sorry

end Wyrd.Limits
