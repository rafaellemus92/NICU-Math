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
  -- `P(-b) = -c g² (d - b)` and `d - b ≥ 2 (b - a) > 0`.
  have hbd : 0 < d - b := by linarith [hp.d_ge, hp.a_lt_b]
  have hcg : 0 < c * g ^ 2 := mul_pos hp.c_pos (pow_pos hg 2)
  have : P a b d c h g (-b) = -(c * g ^ 2 * (d - b)) := by unfold P; ring
  rw [this]
  exact neg_neg_of_pos (mul_pos hcg hbd)

/-- Strict convexity on `[-b, ∞)` in three-point form: since `P(-b) < 0`, `P` cannot
have two distinct roots in `(-b, ∞)`. -/
private lemma Dominant_no_two_roots {a b d c h g s₁ s₂ : ℝ} (hp : Hyp a b d c h) (hg : 0 < g)
    (h1 : -b < s₁) (h12 : s₁ < s₂) (hP1 : P a b d c h g s₁ = 0) (hP2 : P a b d c h g s₂ = 0) :
    False := by
  -- Second divided difference of the monic cubic `P` on `-b, s₁, s₂` is `s₁ + s₂ + a + d`.
  have key : (s₂ - s₁) * P a b d c h g (-b) + (s₁ + b) * P a b d c h g s₂
      - (s₂ + b) * P a b d c h g s₁ = (s₂ - s₁) * (s₁ + b) * (s₂ + b) * (s₁ + s₂ + a + d) := by
    unfold P; ring
  rw [hP1, hP2] at key
  have hneg : (s₂ - s₁) * P a b d c h g (-b) < 0 :=
    mul_neg_of_pos_of_neg (by linarith) (P_neg_b hp hg)
  -- `s₁ + s₂ + a + d > -2b + a + (3b - 2a) = b - a > 0`.
  have hpos : 0 < (s₂ - s₁) * (s₁ + b) * (s₂ + b) * (s₁ + s₂ + a + d) := by
    have e1 : 0 < s₂ - s₁ := by linarith
    have e2 : 0 < s₁ + b := by linarith
    have e3 : 0 < s₂ + b := by linarith
    have e4 : 0 < s₁ + s₂ + a + d := by linarith [hp.d_ge, hp.a_lt_b]
    positivity
  linarith

/-- For `g > 0`, `P(·, g)` has exactly one real root in `(-b, ∞)`. -/
theorem existsUnique_root_gt {a b d c h g : ℝ} (hp : Hyp a b d c h) (hg : 0 < g) :
    ∃! s, -b < s ∧ P a b d c h g s = 0 := by
  have ha := hp.a_pos
  have hab := hp.a_lt_b
  have hbd : b < d := by linarith [hp.d_ge]
  have hcg : 0 < c * g ^ 2 := mul_pos hp.c_pos (pow_pos hg 2)
  have hhg : 0 < h * g := mul_pos hp.h_pos hg
  -- A point where `P` is positive: `S = 1 + c g²`, so `(S + a)(S + b) > S² ≥ S > c g²`.
  set S : ℝ := 1 + c * g ^ 2 with hS
  have hSpos : 0 < P a b d c h g S := by
    have h1 : c * g ^ 2 < (S + a) * (S + b) := by nlinarith
    have h2 : 0 < (S + d) * ((S + a) * (S + b) - c * g ^ 2) :=
      mul_pos (by linarith) (by linarith)
    have h3 : 0 < h * g * (S + b) := mul_pos hhg (by linarith)
    have : P a b d c h g S = (S + d) * ((S + a) * (S + b) - c * g ^ 2) + h * g * (S + b) := by
      unfold P; ring
    rw [this]; linarith
  have hcont : Continuous (P a b d c h g) := by unfold P; fun_prop
  -- Intermediate value theorem on `[-b, S]`.
  obtain ⟨s, ⟨hs1, -⟩, hs⟩ := intermediate_value_Ioo (by linarith) hcont.continuousOn
    (show (0 : ℝ) ∈ Set.Ioo (P a b d c h g (-b)) (P a b d c h g S) from ⟨P_neg_b hp hg, hSpos⟩)
  refine ⟨s, ⟨hs1, hs⟩, ?_⟩
  rintro t ⟨ht1, ht⟩
  rcases lt_trichotomy t s with hlt | heq | hgt
  · exact (Dominant_no_two_roots hp hg ht1 hlt ht hs).elim
  · exact heq
  · exact (Dominant_no_two_roots hp hg hs1 hgt hs ht).elim

/-- **Dominance**: if `s₀ > -b` is a real root, every complex root has real part `≤ s₀`. -/
theorem re_le_of_root {a b d c h g : ℝ} (hp : Hyp a b d c h) (hg : 0 < g) {s₀ : ℝ}
    (hs₀ : -b < s₀) (hP : P a b d c h g s₀ = 0) :
    ∀ z : ℂ, Pc a b d c h g z = 0 → z.re ≤ s₀ := by
  intro z hz
  -- Coefficients of the quotient `P(z) = (z - s₀) (z² + B z + C) + P(s₀)`.
  set B : ℝ := s₀ + a + b + d with hB
  set C : ℝ := s₀ ^ 2 + (a + b + d) * s₀ + (a * b + a * d + b * d + h * g - c * g ^ 2) with hC
  have hfac : Pc a b d c h g z = (z - s₀) * (z ^ 2 + B * z + C) + (P a b d c h g s₀ : ℂ) := by
    simp only [hB, hC, Pc, P]; push_cast; ring
  rw [hfac, hP, Complex.ofReal_zero, add_zero] at hz
  rcases mul_eq_zero.mp hz with h0 | hQ
  · -- `z = s₀`
    have : z = s₀ := sub_eq_zero.mp h0
    rw [this, Complex.ofReal_re]
  · -- The quadratic factor vanishes: split into real and imaginary parts.
    have hre := congrArg Complex.re hQ
    have him := congrArg Complex.im hQ
    simp only [Complex.add_re, Complex.add_im, Complex.mul_re, Complex.mul_im, pow_two,
      Complex.ofReal_re, Complex.ofReal_im, Complex.zero_re, Complex.zero_im] at hre him
    set x := z.re
    set y := z.im
    -- Imaginary part: `y (2x + B) = 0`.
    have hy : y * (2 * x + B) = 0 := by linarith
    rcases mul_eq_zero.mp hy with hy0 | hx
    · -- Real root `x`: then `P(x) = 0`, and convexity forbids `x > s₀`.
      rw [hy0] at hre
      have hPx : P a b d c h g x = 0 := by
        have : P a b d c h g x = (x - s₀) * (x ^ 2 + B * x + C) + P a b d c h g s₀ := by
          simp only [hB, hC, P]; ring
        rw [this, hP]
        have : x ^ 2 + B * x + C = 0 := by nlinarith
        rw [this]; ring
      by_contra hlt
      exact Dominant_no_two_roots hp hg hs₀ (not_le.mp hlt) hP hPx
    · -- Complex pair: `x = -(s₀ + a + b + d)/2 ≤ s₀` since `3 s₀ + a + b + d > b - a > 0`.
      linarith [hp.d_ge, hp.a_lt_b]

end Wyrd.SharedAir
