import Mathlib.Tactic

/-!
# Body water: serum sodium, Adrogué–Madias and the free-water deficit

Edelman's relation approximates serum sodium by
`Na ≈ (exchangeable Na + K) / TBW`. Write `S` for the exchangeable Na + K (mmol)
and `W` for the total body water (L), so the model sodium is `S / W`. Two
bedside formulas follow algebraically from this simplified model:

* **Adrogué–Madias**: infusing `v` litres with Na + K concentration `c` changes
  serum sodium by `v · (c − Na) / (W + v)`. For one litre that is
  `(c − Na) / (TBW + 1)`.
* **Free-water deficit**: adding `W · (Na / 140 − 1)` litres of free water
  brings model sodium down to 140.

**For small patients, do not scale the per-litre form.** It assumes the volume
given is one litre. Scaling it down linearly to a small volume
*underestimates* the model change by the factor `(W + 1)/(W + v)`
(`per_litre_scaling_underestimates`). That is negligible for an adult
(`W ≈ 42 L`), but for a 3 kg term newborn (`W ≈ 2.3 L`) given 10 mL the true
model change is about 42% larger (`newborn_scaling_example`).

**These give a model total, never a rate.** Correcting sodium too fast is
dangerous: raising it too quickly in chronic hyponatraemia risks osmotic
demyelination, and lowering it too quickly in chronic hypernatraemia risks
cerebral oedema and seizures, including in infants with hypernatraemic
dehydration. Real changes can exceed the prediction, e.g. when urine output
rises. Rates come from local protocols and repeated sodium measurements.

Every limitation of the model carries over:
* Edelman's relation also has an intercept and slope.
* The model ignores ongoing losses (including high insensible water loss in
  preterm infants), urine output and regulation.
* Using an adult water fraction (about 0.6) for a newborn (about 0.78 at term,
  about 0.86 at 24 weeks) underestimates `W`, which overstates the change per
  volume and understates the free-water deficit.

These are proofs about a model, for understanding. They are **not** a dosing
tool.
-/

namespace Wyrd.BodyWater

/-- Model serum sodium (Edelman): exchangeable `Na + K` over total body water. -/
noncomputable def serumNa (S W : ℝ) : ℝ := S / W

/-- **Adrogué–Madias, general volume**: after infusing `v` litres at concentration
`c`, serum sodium changes by `v · (c − Na) / (W + v)`. -/
theorem adrogue_madias {S W v c : ℝ} (hW : 0 < W) (hv : 0 ≤ v) :
    serumNa (S + v * c) (W + v) - serumNa S W = v * (c - serumNa S W) / (W + v) := by
  unfold serumNa
  have h1 : W ≠ 0 := hW.ne'
  -- the new volume `W + v` is positive, so it is a legal denominator
  have h2 : W + v ≠ 0 := by linarith
  field_simp
  ring

/-- **Adrogué–Madias, per litre**: `ΔNa = (c − Na) / (TBW + 1)`. -/
theorem adrogue_madias_one_litre {S W c : ℝ} (hW : 0 < W) :
    serumNa (S + c) (W + 1) - serumNa S W = (c - serumNa S W) / (W + 1) := by
  -- specialise the general formula to `v = 1`; `simp` turns `1 * c` into `c`
  have h := adrogue_madias (S := S) (c := c) hW zero_le_one
  simpa using h

/-- A smaller body changes more per litre: a fluid more concentrated than serum
raises sodium further in a smaller patient. (`smaller_body_bigger_change_abs`
covers both directions.) -/
theorem smaller_body_bigger_change {S₁ S₂ W₁ W₂ c : ℝ} (h₁ : 0 < W₁) (hW : W₁ < W₂)
    (hNa : serumNa S₁ W₁ = serumNa S₂ W₂) (hc : serumNa S₁ W₁ < c) :
    serumNa (S₂ + c) (W₂ + 1) - serumNa S₂ W₂ < serumNa (S₁ + c) (W₁ + 1) - serumNa S₁ W₁ := by
  -- both changes are `(c − Na) / (W + 1)` with the same `Na`
  rw [adrogue_madias_one_litre h₁, adrogue_madias_one_litre (h₁.trans hW), ← hNa]
  -- positive numerator over a larger denominator is smaller
  exact div_lt_div_of_pos_left (sub_pos.mpr hc) (by linarith) (by linarith)

/-- **Free-water deficit**: in the model, if sodium is above 140, adding
`W · (Na / 140 − 1)` litres of free water (in practice enteral water or hypotonic
fluid, never pure water IV) brings model sodium to 140. A total, not a rate:
see the warning in the module doc. -/
theorem free_water_deficit {S W : ℝ} (hW : 0 < W) (hNa : 140 < serumNa S W) :
    serumNa S (W + W * (serumNa S W / 140 - 1)) = 140 ∧ 0 < W * (serumNa S W / 140 - 1) := by
  unfold serumNa at *
  -- `S = (S / W) * W` with both factors positive
  have hS : 0 < S := by
    have : 0 < S / W := by linarith
    have := mul_pos this hW
    rwa [div_mul_cancel₀ S hW.ne'] at this
  constructor
  · -- the corrected volume is `S / 140`, and `S / (S / 140) = 140`
    have : W + W * (S / W / 140 - 1) = S / 140 := by
      field_simp
      ring
    rw [this]
    field_simp
  · apply mul_pos hW
    -- `S / W > 140` gives `S / W / 140 > 1`
    have : 1 < S / W / 140 := by rw [lt_div_iff₀ (by norm_num)]; linarith
    linarith

/-- **A smaller body moves sodium further, in either direction**: for the same
starting sodium and the same litre of fluid, more or less concentrated than
serum, the size of the change is larger when total body water is smaller. -/
theorem smaller_body_bigger_change_abs {S₁ S₂ W₁ W₂ c : ℝ} (h₁ : 0 < W₁) (hW : W₁ < W₂)
    (hNa : serumNa S₁ W₁ = serumNa S₂ W₂) (hc : c ≠ serumNa S₁ W₁) :
    |serumNa (S₂ + c) (W₂ + 1) - serumNa S₂ W₂| <
      |serumNa (S₁ + c) (W₁ + 1) - serumNa S₁ W₁| := by
  -- both changes are `(c − Na) / (W + 1)` with the same `Na`
  rw [adrogue_madias_one_litre h₁, adrogue_madias_one_litre (h₁.trans hW), ← hNa,
    abs_div, abs_div, abs_of_pos (by linarith : (0 : ℝ) < W₂ + 1),
    abs_of_pos (by linarith : (0 : ℝ) < W₁ + 1)]
  -- the same positive size `|c − Na|` over a larger denominator is smaller
  exact div_lt_div_of_pos_left (abs_pos.mpr (sub_ne_zero.mpr hc)) (by linarith) (by linarith)

/-- The exact model change is the linearly scaled per-litre figure times
`(W + 1) / (W + v)`. -/
theorem per_litre_scaling_ratio {S W v c : ℝ} (hW : 0 < W) (hv : 0 ≤ v) :
    serumNa (S + v * c) (W + v) - serumNa S W =
      (W + 1) / (W + v) * (v * ((c - serumNa S W) / (W + 1))) := by
  rw [adrogue_madias hW hv]
  have h1 : W + 1 ≠ 0 := by linarith
  have h2 : W + v ≠ 0 := by linarith
  field_simp

/-- **Scaling the per-litre formula down underestimates the model change**: for
less than a litre of fluid more concentrated than serum, the exact model change
`v · (c − Na) / (W + v)` exceeds `v` times the per-litre figure. -/
theorem per_litre_scaling_underestimates {S W v c : ℝ} (hW : 0 < W) (hv0 : 0 < v) (hv1 : v < 1)
    (hc : serumNa S W < c) :
    v * ((c - serumNa S W) / (W + 1)) < serumNa (S + v * c) (W + v) - serumNa S W := by
  rw [adrogue_madias hW hv0.le, mul_div_assoc]
  -- the same positive numerator over the smaller denominator `W + v < W + 1`
  exact mul_lt_mul_of_pos_left
    (div_lt_div_of_pos_left (sub_pos.mpr hc) (by linarith) (by linarith)) hv0

/-- A 3 kg term newborn (`W ≈ 0.78 · 3 = 2.34 L`) given 10 mL: the exact model change
is more than 1.42 times the scaled per-litre figure. -/
theorem newborn_scaling_example : (142 : ℝ) / 100 < (2.34 + 1) / (2.34 + 0.01) := by
  norm_num

end Wyrd.BodyWater
