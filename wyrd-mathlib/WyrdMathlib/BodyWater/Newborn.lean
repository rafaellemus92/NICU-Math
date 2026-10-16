import Mathlib.Tactic

/-!
# Body water in the fetus and newborn

From *Body Composition in the Fetus and Newborn* (abdominalkey.com):

* total body water falls from about 86% of body weight at 24 weeks' gestation
  to 78% at term (ECW 44%, ICW 34%, solids 22%), and to about 70% at one year
  (ICW 42%, so ECW 28%, solids 30%);
* in the first week newborns lose extracellular water through a physiologic
  diuresis. The source gives a *maximum* of 10–15% of body weight, mostly
  reflecting preterm and very-low-birth-weight infants. That is not a target or
  a normal threshold: in term (especially breastfed) infants a loss near 10%
  usually prompts evaluation (feeding, sodium, hypernatraemic dehydration).
  Early weight loss also includes insensible losses, meconium and catabolism,
  not only ECW. The source stresses daily weights: too little loss (fluid
  overload, linked in VLBW infants to PDA and BPD) and too much loss both
  carry risk;
* term small-for-gestational-age infants generally have *more* water and *less*
  fat than appropriately grown ones (one study of extremely preterm infants,
  25–30 weeks, found the opposite). Large-for-gestational-age infants have more
  fat and, by indirect evidence, less water; direct data are sparse (one D₂O
  study of 7 infants of diabetic mothers, not all LGA, 1430–3495 g, found 73%
  versus 80% water compared with infants of non-diabetic mothers).

Proved here: the stated compositions add up; losing extracellular water lowers
the water fraction; and in the two-compartment model (fat holds no water, the
fat-free mass has a fixed water fraction `h`), more water means less fat, which
is *consistent with* the SGA/LGA pattern.

The fat model is **qualitative only**. Fat-free-mass hydration is about 80% at
birth, higher in preterm infants and possibly in SGA infants (whose ECW is
expanded), and falls toward about 73% in adults. Do not use `fatFraction` with
an adult `h`, or to estimate a newborn's fat from the water percentages above:
`t = 0.78` with `h = 0.73` even gives a negative fat fraction.

Educational model only, not a clinical tool.
-/

namespace Wyrd.BodyWater

/-- The stated term and one-year compositions are consistent (percent of body weight). -/
theorem term_and_one_year_add_up :
    (44 : ℝ) + 34 = 78 ∧ (78 : ℝ) + 22 = 100 ∧ (70 : ℝ) - 42 = 28 ∧ (70 : ℝ) + 30 = 100 := by
  norm_num

/-- **Losing extracellular water lowers the water fraction**: removing `x` of water
from a body of weight `B` with water `T` (`0 < x < T < B`) leaves a smaller
fraction of water. -/
theorem water_fraction_falls {B T x : ℝ} (hx : 0 < x) (hxT : x < T) (hTB : T < B) :
    (T - x) / (B - x) < T / B := by
  -- cross-multiply: (T - x)·B < T·(B - x) ⇔ x·T < x·B
  rw [div_lt_div_iff₀ (by linarith) (by linarith)]
  nlinarith [mul_pos hx (sub_pos.2 hTB)]

/-- A term newborn (78% water, 44% ECW) losing 10% of birth weight as ECW only:
water falls to `68/90` (about 75.6%) and ECW to `34/90` (about 37.8%) of the new weight. -/
theorem term_newborn_ten_percent_loss :
    (78 - 10) / (100 - 10 : ℝ) = 68 / 90 ∧ (68 / 90 : ℝ) < 78 / 100 ∧
      (44 - 10) / (100 - 10 : ℝ) = 34 / 90 ∧ (34 / 90 : ℝ) < 44 / 100 := by
  norm_num

/-- Two-compartment model: with fat-free mass of water fraction `h`, a body whose
water fraction is `t` has fat fraction `1 − t / h`. -/
noncomputable def fatFraction (h t : ℝ) : ℝ := 1 - t / h

/-- **More water, less fat**: at a fixed hydration of the fat-free mass, the fat
fraction strictly decreases as the water fraction rises. -/
theorem fatFraction_strictAnti {h : ℝ} (hh : 0 < h) : StrictAnti (fatFraction h) := by
  intro a b hab
  unfold fatFraction
  -- dividing by the positive hydration `h` preserves the order
  have : a / h < b / h := by gcongr
  linarith

/-- Consistent with the SGA/LGA pattern: an infant with more body water (e.g. a term
SGA infant) has less fat than one with less (e.g. an LGA infant), *if* their
fat-free masses are equally hydrated, which may not hold for SGA infants. -/
theorem more_water_less_fat {h t₁ t₂ : ℝ} (hh : 0 < h) (ht : t₁ < t₂) :
    fatFraction h t₂ < fatFraction h t₁ := by
  exact fatFraction_strictAnti hh ht

end Wyrd.BodyWater
