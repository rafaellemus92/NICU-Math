import Mathlib.Tactic

/-!
# Body water: serum sodium, Adrogué–Madias and the free-water deficit

Edelman's relation approximates serum sodium by
`Na ≈ (exchangeable Na + K) / TBW`. Write `S` for the exchangeable Na + K (mmol)
and `W` for the total body water (L), so the model sodium is `S / W`. Two
bedside formulas follow from it exactly:

* **Adrogué–Madias**: infusing `v` litres with Na + K concentration `c` changes
  serum sodium by `v · (c − Na) / (W + v)`. For one litre that is
  `(c − Na) / (TBW + 1)`.
* **Free-water deficit**: adding `W · (Na / 140 − 1)` litres of water brings
  sodium down to 140.

Both inherit every limitation of the model: Edelman's relation also has an
intercept and slope, and the model ignores ongoing losses, urine output and
regulation. Neonatal water fractions differ from adult ones (see
`Newborn.lean`). These are proofs about a model, for understanding. They are
**not** a dosing tool; real correction needs repeated sodium measurements.
-/

namespace Wyrd.BodyWater

/-- Model serum sodium (Edelman): exchangeable `Na + K` over total body water. -/
noncomputable def serumNa (S W : ℝ) : ℝ := S / W

/-- **Adrogué–Madias, general volume**: after infusing `v` litres at concentration
`c`, serum sodium changes by `v · (c − Na) / (W + v)`. -/
theorem adrogue_madias {S W v c : ℝ} (hW : 0 < W) (hv : 0 ≤ v) :
    serumNa (S + v * c) (W + v) - serumNa S W = v * (c - serumNa S W) / (W + v) := by
  sorry

/-- **Adrogué–Madias, per litre**: `ΔNa = (c − Na) / (TBW + 1)`. -/
theorem adrogue_madias_one_litre {S W c : ℝ} (hW : 0 < W) :
    serumNa (S + c) (W + 1) - serumNa S W = (c - serumNa S W) / (W + 1) := by
  sorry

/-- A smaller body (less total water) changes more per litre: the same fluid moves
sodium further in a small patient. -/
theorem smaller_body_bigger_change {S₁ S₂ W₁ W₂ c : ℝ} (h₁ : 0 < W₁) (hW : W₁ < W₂)
    (hNa : serumNa S₁ W₁ = serumNa S₂ W₂) (hc : serumNa S₁ W₁ < c) :
    serumNa (S₂ + c) (W₂ + 1) - serumNa S₂ W₂ < serumNa (S₁ + c) (W₁ + 1) - serumNa S₁ W₁ := by
  sorry

/-- **Free-water deficit**: if sodium is above 140, adding `W · (Na / 140 − 1)` litres
of pure water brings it to exactly 140. -/
theorem free_water_deficit {S W : ℝ} (hW : 0 < W) (hNa : 140 < serumNa S W) :
    serumNa S (W + W * (serumNa S W / 140 - 1)) = 140 ∧ 0 < W * (serumNa S W / 140 - 1) := by
  sorry

end Wyrd.BodyWater
