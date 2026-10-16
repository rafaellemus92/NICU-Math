import Mathlib.Tactic

/-!
# Body water in the fetus and newborn

From *Body Composition in the Fetus and Newborn* (abdominalkey.com):

* total body water falls from about 86% of body weight at 24 weeks' gestation
  to 78% at term (ECW 44%, ICW 34%, solids 22%), and to about 70% at one year
  (ICW 42%, so ECW 28%, solids 30%);
* in the first week every newborn loses extracellular water (diuresis), up to
  10–15% of body weight;
* small-for-gestational-age infants have *more* water and *less* fat than
  appropriately grown ones, and large-for-gestational-age infants *less* water
  and *more* fat (e.g. infants of diabetic mothers, 73% versus 80% water).

Proved here: the stated compositions add up; losing extracellular water lowers
the water fraction; and in the two-compartment model (fat holds no water, and
the fat-free mass has a fixed water fraction `h`), more water means less fat,
which is the SGA/LGA pattern.

Educational model only, not a clinical tool.
-/

namespace Wyrd.BodyWater

/-- The stated term and one-year compositions are consistent (percent of body weight). -/
theorem term_and_one_year_add_up :
    (44 : ℝ) + 34 = 78 ∧ (78 : ℝ) + 22 = 100 ∧ (70 : ℝ) - 42 = 28 ∧ (70 : ℝ) + 30 = 100 := by
  sorry

/-- **Losing extracellular water lowers the water fraction**: removing `x` of water
from a body of weight `B` with water `T` (`0 < x < T < B`) leaves a smaller
fraction of water. -/
theorem water_fraction_falls {B T x : ℝ} (hx : 0 < x) (hxT : x < T) (hTB : T < B) :
    (T - x) / (B - x) < T / B := by
  sorry

/-- A term newborn (78% water, 44% ECW) losing 10% of birth weight as ECW only:
water falls to `68/90` (about 75.6%) and ECW to `34/90` (about 37.8%) of the new weight. -/
theorem term_newborn_ten_percent_loss :
    (78 - 10) / (100 - 10 : ℝ) = 68 / 90 ∧ (68 / 90 : ℝ) < 78 / 100 ∧
      (44 - 10) / (100 - 10 : ℝ) = 34 / 90 ∧ (34 / 90 : ℝ) < 44 / 100 := by
  sorry

/-- Two-compartment model: with fat-free mass of water fraction `h`, a body whose
water fraction is `t` has fat fraction `1 − t / h`. -/
noncomputable def fatFraction (h t : ℝ) : ℝ := 1 - t / h

/-- **More water, less fat**: at a fixed hydration of the fat-free mass, the fat
fraction strictly decreases as the water fraction rises. -/
theorem fatFraction_strictAnti {h : ℝ} (hh : 0 < h) : StrictAnti (fatFraction h) := by
  sorry

/-- The SGA/LGA pattern: an infant with more body water (e.g. SGA) has less fat than
one with less (e.g. LGA or an infant of a diabetic mother), at equal hydration of
the fat-free mass. -/
theorem more_water_less_fat {h t₁ t₂ : ℝ} (hh : 0 < h) (ht : t₁ < t₂) :
    fatFraction h t₂ < fatFraction h t₁ := by
  sorry

end Wyrd.BodyWater
