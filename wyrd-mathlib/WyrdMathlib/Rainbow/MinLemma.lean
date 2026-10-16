import Mathlib.Analysis.Calculus.Deriv.MeanValue

/-!
# A calculus lemma: falling then rising means a strict minimum

If `f` is continuous on `[a, b]`, its derivative is negative on `(a, c)` and
positive on `(c, b)`, then `c` is the unique minimum point of `f` on `[a, b]`.
-/

namespace Wyrd.Rainbow

/-- Falling on `(a, c)` and rising on `(c, b)`: `c` beats every other point of `[a, b]`. -/
theorem lt_of_deriv_sign {f : ℝ → ℝ} {a b c : ℝ} (hac : a ≤ c) (hcb : c ≤ b)
    (hf : ContinuousOn f (Set.Icc a b))
    (hneg : ∀ x ∈ Set.Ioo a c, deriv f x < 0) (hpos : ∀ x ∈ Set.Ioo c b, 0 < deriv f x) :
    ∀ x ∈ Set.Icc a b, x ≠ c → f c < f x := by
  -- On `[a, c]` the function falls strictly (negative derivative inside).
  have hanti : StrictAntiOn f (Set.Icc a c) :=
    strictAntiOn_of_deriv_neg (convex_Icc a c) (hf.mono (Set.Icc_subset_Icc_right hcb))
      (fun x hx => hneg x (by simpa [interior_Icc] using hx))
  -- On `[c, b]` the function rises strictly (positive derivative inside).
  have hmono : StrictMonoOn f (Set.Icc c b) :=
    strictMonoOn_of_deriv_pos (convex_Icc c b) (hf.mono (Set.Icc_subset_Icc_left hac))
      (fun x hx => hpos x (by simpa [interior_Icc] using hx))
  intro x hx hxc
  rcases lt_or_gt_of_ne hxc with hlt | hgt
  -- Left of `c`: falling from `x` down to `c`.
  · exact hanti ⟨hx.1, hlt.le⟩ ⟨hac, le_rfl⟩ hlt
  -- Right of `c`: rising from `c` up to `x`.
  · exact hmono ⟨le_rfl, hcb⟩ ⟨hgt.le, hx.2⟩ hgt

/-- The same, as Mathlib's `IsMinOn`. -/
theorem isMinOn_of_deriv_sign {f : ℝ → ℝ} {a b c : ℝ} (hac : a ≤ c) (hcb : c ≤ b)
    (hf : ContinuousOn f (Set.Icc a b))
    (hneg : ∀ x ∈ Set.Ioo a c, deriv f x < 0) (hpos : ∀ x ∈ Set.Ioo c b, 0 < deriv f x) :
    IsMinOn f (Set.Icc a b) c := by
  -- Every other point has a strictly larger value; `c` itself ties.
  refine isMinOn_iff.mpr fun x hx => ?_
  rcases eq_or_ne x c with rfl | hxc
  · exact le_rfl
  · exact (lt_of_deriv_sign hac hcb hf hneg hpos x hx hxc).le

end Wyrd.Rainbow
