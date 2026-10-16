import Mathlib.Analysis.Calculus.Deriv.MeanValue

/-!
# A calculus lemma: falling then rising means a strict minimum

If `f` is continuous on `[a, b]`, its derivative is negative on `(a, c)` and
positive on `(c, b)`, then `c` is the unique minimum point of `f` on `[a, b]`.
-/

namespace Wyrd.Rainbow

theorem lt_of_deriv_sign {f : ℝ → ℝ} {a b c : ℝ} (hac : a ≤ c) (hcb : c ≤ b)
    (hf : ContinuousOn f (Set.Icc a b))
    (hneg : ∀ x ∈ Set.Ioo a c, deriv f x < 0) (hpos : ∀ x ∈ Set.Ioo c b, 0 < deriv f x) :
    ∀ x ∈ Set.Icc a b, x ≠ c → f c < f x := by
  sorry

theorem isMinOn_of_deriv_sign {f : ℝ → ℝ} {a b c : ℝ} (hac : a ≤ c) (hcb : c ≤ b)
    (hf : ContinuousOn f (Set.Icc a b))
    (hneg : ∀ x ∈ Set.Ioo a c, deriv f x < 0) (hpos : ∀ x ∈ Set.Ioo c b, 0 < deriv f x) :
    IsMinOn f (Set.Icc a b) c := by
  sorry

end Wyrd.Rainbow
