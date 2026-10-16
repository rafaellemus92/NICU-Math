import WyrdMathlib.SharedAir.Basic

/-!
# The dominant eigenvalue is real and lies above `-b`

For `g > 0`: `P(-b, g) < 0`, `P → ∞`, and `P` is strictly convex on `[-b, ∞)`
(because `d ≥ 3b − 2a`), so `P` has exactly one root `s(g)` in `(-b, ∞)`. Every
other root, real or complex, has real part at most `s(g)`: other real roots are
`≤ -b`, and a complex pair has real part `(-a - b - d - s(g))/2 < s(g)`.
-/

namespace Wyrd.SharedAir

theorem P_neg_b {a b d c h g : ℝ} (hp : Hyp a b d c h) (hg : 0 < g) : P a b d c h g (-b) < 0 := by
  sorry

/-- For `g > 0`, `P(·, g)` has exactly one real root in `(-b, ∞)`. -/
theorem existsUnique_root_gt {a b d c h g : ℝ} (hp : Hyp a b d c h) (hg : 0 < g) :
    ∃! s, -b < s ∧ P a b d c h g s = 0 := by
  sorry

/-- **Dominance**: if `s₀ > -b` is a real root, every complex root has real part `≤ s₀`. -/
theorem re_le_of_root {a b d c h g : ℝ} (hp : Hyp a b d c h) (hg : 0 < g) {s₀ : ℝ}
    (hs₀ : -b < s₀) (hP : P a b d c h g s₀ = 0) :
    ∀ z : ℂ, Pc a b d c h g z = 0 → z.re ≤ s₀ := by
  sorry

end Wyrd.SharedAir
