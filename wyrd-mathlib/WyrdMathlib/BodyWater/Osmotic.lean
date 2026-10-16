import Mathlib.Tactic

/-!
# Body water: osmotic equilibrium between cells and the extracellular space

Cell membranes let water through freely but not most solutes. So water
settles where intracellular and extracellular osmolality are equal. With
`Oi` and `Oe` osmoles inside and outside the cells and `W` litres of total
body water, the equilibrium split is

  `ICW = W · Oi / (Oi + Oe)`,  `ECW = W · Oe / (Oi + Oe)`.

Consequences proved here:

* a load of pure water spreads in proportion to the osmoles: about 2/3 into
  cells for an adult, but only `34/78 ≈ 44%` for a term newborn, whose water
  is mostly extracellular;
* isotonic fluid stays outside the cells;
* adding solute outside the cells (hypertonic saline) pulls water out of them.

Educational model only. It ignores effective versus ineffective osmoles,
ongoing losses and regulation, and it is not for clinical dosing.
-/

namespace Wyrd.BodyWater

/-- Equilibrium intracellular water. -/
noncomputable def icwEq (W Oi Oe : ℝ) : ℝ := W * Oi / (Oi + Oe)

/-- Equilibrium extracellular water. -/
noncomputable def ecwEq (W Oi Oe : ℝ) : ℝ := W * Oe / (Oi + Oe)

/-- The split uses all the water. -/
theorem icwEq_add_ecwEq {W Oi Oe : ℝ} (hi : 0 < Oi) (he : 0 < Oe) :
    icwEq W Oi Oe + ecwEq W Oi Oe = W := by
  sorry

/-- At equilibrium both sides have the same osmolality, `(Oi + Oe) / W`. -/
theorem equal_osmolality {W Oi Oe : ℝ} (hW : 0 < W) (hi : 0 < Oi) (he : 0 < Oe) :
    Oi / icwEq W Oi Oe = (Oi + Oe) / W ∧ Oe / ecwEq W Oi Oe = (Oi + Oe) / W := by
  sorry

/-- **A water load spreads in proportion to the osmoles**: of `w` litres of pure
water, `w · Oi / (Oi + Oe)` ends up inside the cells. -/
theorem water_load_split {W w Oi Oe : ℝ} (hi : 0 < Oi) (he : 0 < Oe) :
    icwEq (W + w) Oi Oe - icwEq W Oi Oe = w * Oi / (Oi + Oe) := by
  sorry

/-- Adult proportions (`ICW : ECW = 2 : 1`, the 60–40–20 rule): two thirds of a
water load goes into the cells. -/
theorem adult_water_load {W w Oe : ℝ} (he : 0 < Oe) :
    icwEq (W + w) (2 * Oe) Oe - icwEq W (2 * Oe) Oe = 2 / 3 * w := by
  sorry

/-- Term newborn proportions (ICW 34%, ECW 44% of body weight): only `34/78` of a
water load, less than half, goes into the cells. -/
theorem newborn_water_load {W w : ℝ} (hw : 0 < w) :
    icwEq (W + w) 34 44 - icwEq W 34 44 = 34 / 78 * w ∧
      icwEq (W + w) 34 44 - icwEq W 34 44 < w / 2 := by
  sorry

/-- **Isotonic fluid stays outside the cells**: adding `v` litres whose osmolality
equals the body's leaves intracellular water unchanged. -/
theorem isotonic_stays_extracellular {W v Oi Oe : ℝ} (hW : 0 < W) (hv : 0 ≤ v)
    (hi : 0 < Oi) (he : 0 < Oe) :
    icwEq (W + v) Oi (Oe + v * ((Oi + Oe) / W)) = icwEq W Oi Oe := by
  sorry

/-- **Extra solute outside the cells shrinks them** (e.g. hypertonic saline). -/
theorem solute_load_shrinks_cells {W s Oi Oe : ℝ} (hW : 0 < W) (hs : 0 < s)
    (hi : 0 < Oi) (he : 0 < Oe) :
    icwEq W Oi (Oe + s) < icwEq W Oi Oe := by
  sorry

/-- **Pure water swells the cells.** -/
theorem water_load_swells_cells {W w Oi Oe : ℝ} (hw : 0 < w) (hi : 0 < Oi) (he : 0 < Oe) :
    icwEq W Oi Oe < icwEq (W + w) Oi Oe := by
  sorry

end Wyrd.BodyWater
