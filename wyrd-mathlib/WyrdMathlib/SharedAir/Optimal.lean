import WyrdMathlib.SharedAir.Dominant

/-!
# A unique finite optimal coupling, and the exact stability range

Recovery speed is the **spectral rate** `ρ(g) = −max Re(eigenvalues)`. With `s*`
the root of `H` in `(-b, -a)` and `g* = G(s*)`:

1. for every `g ≥ 0` some eigenvalue has real part `≥ s*`, so `ρ(g) ≤ −s*`;
2. for every `g ≥ 0` with `g ≠ g*`, some eigenvalue has real part `> s*`;
3. at `g = g*` every eigenvalue has real part `≤ s*`.

So `g*` is the **unique** maximiser of `ρ`, and it is finite and positive.
Stronger coupling eventually destabilises: the equilibrium is stable (all real
parts negative) exactly when `g < g_c`.
-/

namespace Wyrd.SharedAir

/-- **Unique finite optimal coupling.** -/
theorem optimal_coupling {a b d c h : ℝ} (hp : Hyp a b d c h) {s₀ : ℝ}
    (hs₀ : s₀ ∈ Set.Ioo (-b) (-a)) (hH : H a b d c h s₀ = 0) :
    0 < G b d c h s₀ ∧
      (∀ g, 0 ≤ g → ∃ s : ℝ, s₀ ≤ s ∧ P a b d c h g s = 0) ∧
      (∀ g, 0 ≤ g → g ≠ G b d c h s₀ → ∃ s : ℝ, s₀ < s ∧ P a b d c h g s = 0) ∧
      (∀ z : ℂ, Pc a b d c h (G b d c h s₀) z = 0 → z.re ≤ s₀) := by
  sorry

/-- The critical coupling: the positive root of `P(0, g) = a b d + h b g − c d g²`. -/
noncomputable def gc (a b d c h : ℝ) : ℝ :=
  (h * b + Real.sqrt (h ^ 2 * b ^ 2 + 4 * a * b * c * d ^ 2)) / (2 * c * d)

theorem P_zero (a b d c h g : ℝ) : P a b d c h g 0 = a * b * d + h * b * g - c * d * g ^ 2 := by
  sorry

/-- At `g = g_c` there is a zero eigenvalue. -/
theorem P_gc {a b d c h : ℝ} (hp : Hyp a b d c h) : P a b d c h (gc a b d c h) 0 = 0 := by
  sorry

/-- For `g ≥ 0`: `P(0, g) > 0` exactly when `g < g_c`. -/
theorem P_zero_pos_iff {a b d c h g : ℝ} (hp : Hyp a b d c h) (hg : 0 ≤ g) :
    0 < P a b d c h g 0 ↔ g < gc a b d c h := by
  sorry

/-- **Exact stability range**: for `g ≥ 0`, every eigenvalue has negative real part
if and only if `g < g_c`. -/
theorem stable_iff {a b d c h g : ℝ} (hp : Hyp a b d c h) (hg : 0 ≤ g) :
    (∀ z : ℂ, Pc a b d c h g z = 0 → z.re < 0) ↔ g < gc a b d c h := by
  sorry

end Wyrd.SharedAir
