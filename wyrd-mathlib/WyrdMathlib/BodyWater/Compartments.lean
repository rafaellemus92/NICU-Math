import Mathlib.Tactic

/-!
# Body water: compartments and the dilution principle

Water is the largest part of the body. It splits into intracellular water (ICW)
and extracellular water (ECW), and ECW splits into interstitial fluid and
plasma. Each volume is measured by **indicator dilution**: give a dose `I` of
a tracer that spreads through one compartment only, wait for it to mix, and
measure its plasma concentration `C`. Then the volume is `V = I / C`. The
tracers are D₂O or H₂¹⁸O for total body water, bromide or sucrose for ECW,
and Evans blue for plasma.

Source: *Body Composition in the Fetus and Newborn: Effects of Intrauterine
Growth Aberration* (abdominalkey.com), Table 2.1 and the formulas after it.

Educational model only. It is not for clinical dosing.
-/

namespace Wyrd.BodyWater

/-- A body's water partition (any consistent units, e.g. kg and L, since water is about 1 kg/L). -/
structure Body where
  weight : ℝ
  tbw : ℝ
  ecw : ℝ
  plasma : ℝ
  plasma_pos : 0 < plasma
  plasma_lt_ecw : plasma < ecw
  ecw_lt_tbw : ecw < tbw
  tbw_lt_weight : tbw < weight

namespace Body

/-- Intracellular water `= TBW − ECW`. -/
def icw (b : Body) : ℝ := b.tbw - b.ecw

/-- Interstitial water `= ECW − plasma`. -/
def interstitial (b : Body) : ℝ := b.ecw - b.plasma

/-- Solids `= weight − TBW`. -/
def solids (b : Body) : ℝ := b.weight - b.tbw

/-- The four parts add back up to the body weight, and each part is positive. -/
theorem weight_decomposition (b : Body) :
    b.weight = b.solids + b.icw + b.interstitial + b.plasma ∧
      0 < b.solids ∧ 0 < b.icw ∧ 0 < b.interstitial ∧ 0 < b.plasma := by
  sorry

end Body

/-- **Dilution principle**: a dose `I` mixed into volume `V` has concentration
`I / V`, and the estimate `I / C` recovers `V`. -/
theorem dilution_recovers {I V : ℝ} (hI : 0 < I) (hV : 0 < V) : I / (I / V) = V := by
  sorry

/-- **Lost tracer inflates the estimate**: if a fraction `e` of the dose is lost
(excreted, or bound outside the compartment) before sampling, `I / C`
overstates the volume by the factor `1 / (1 - e)`. -/
theorem dilution_overestimate {I V e : ℝ} (hI : 0 < I) (hV : 0 < V) (he0 : 0 < e) (he1 : e < 1) :
    I / ((1 - e) * I / V) = V / (1 - e) ∧ V < I / ((1 - e) * I / V) := by
  sorry

/-- Blood volume from plasma volume and haematocrit: `BV = PV / (1 − Hct)`, and it
exceeds the plasma volume whenever there are any red cells. -/
theorem blood_volume {pv hct : ℝ} (hpv : 0 < pv) (h0 : 0 < hct) (h1 : hct < 1) :
    pv < pv / (1 - hct) ∧ pv / (1 - hct) * (1 - hct) = pv := by
  sorry

end Wyrd.BodyWater
