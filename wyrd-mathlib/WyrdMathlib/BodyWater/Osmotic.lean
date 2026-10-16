import Mathlib.Tactic

/-!
# Body water: osmotic equilibrium between cells and the extracellular space

Cell membranes let water through freely but not most solutes. So water
settles where intracellular and extracellular *effective* osmolality (tonicity)
are equal. With `Oi` and `Oe` effective osmoles inside and outside the cells
(solutes that cannot cross the cell membrane, e.g. potassium inside and
sodium outside) and `W` litres of total body water, the equilibrium split is

  `ICW = W · Oi / (Oi + Oe)`,  `ECW = W · Oe / (Oi + Oe)`.

Consequences proved here:

* a load of free water spreads in proportion to the effective osmoles: about
  2/3 into the cells for an adult, but only `34/78 ≈ 43.6%` of the load for a
  term newborn, whose water is mostly extracellular;
* isotonic fluid whose solute stays outside the cells (e.g. 0.9% saline) does
  not change cell water. Outside the cells is not the same as inside the
  vessels: most of it moves to the interstitium;
* adding effective solute outside the cells (hypertonic saline, mannitol)
  pulls water out of them.

Iso-*osmolar* is not iso-*tonic*. Dextrose solutions are iso-osmolar in the bag,
but once the glucose is taken up and metabolised they act as free water and
mostly enter the cells, which is why dextrose-based maintenance fluids can
lower sodium. Permeant solutes such as urea do not shift water.

Educational model only. `Oi` and `Oe` must be effective osmoles, and the model
ignores ongoing losses and regulation. It is not for clinical dosing.
-/

namespace Wyrd.BodyWater

/-- Equilibrium intracellular water, for effective osmoles `Oi` (inside) and `Oe` (outside). -/
noncomputable def icwEq (W Oi Oe : ℝ) : ℝ := W * Oi / (Oi + Oe)

/-- Equilibrium extracellular water, for effective osmoles `Oi` (inside) and `Oe` (outside). -/
noncomputable def ecwEq (W Oi Oe : ℝ) : ℝ := W * Oe / (Oi + Oe)

/-- The split uses all the water. -/
theorem icwEq_add_ecwEq {W Oi Oe : ℝ} (hi : 0 < Oi) (he : 0 < Oe) :
    icwEq W Oi Oe + ecwEq W Oi Oe = W := by
  unfold icwEq ecwEq
  have h : Oi + Oe ≠ 0 := by positivity
  -- combine over the common denominator `Oi + Oe`
  field_simp

/-- At equilibrium both sides have the same osmolality, `(Oi + Oe) / W`. -/
theorem equal_osmolality {W Oi Oe : ℝ} (hW : 0 < W) (hi : 0 < Oi) (he : 0 < Oe) :
    Oi / icwEq W Oi Oe = (Oi + Oe) / W ∧ Oe / ecwEq W Oi Oe = (Oi + Oe) / W := by
  unfold icwEq ecwEq
  have hs : 0 < Oi + Oe := by positivity
  constructor
  · field_simp
  · field_simp

/-- **A water load spreads in proportion to the osmoles**: of `w` litres of pure
water, `w · Oi / (Oi + Oe)` ends up inside the cells. -/
theorem water_load_split {W w Oi Oe : ℝ} (hi : 0 < Oi) (he : 0 < Oe) :
    icwEq (W + w) Oi Oe - icwEq W Oi Oe = w * Oi / (Oi + Oe) := by
  unfold icwEq
  have h : Oi + Oe ≠ 0 := by positivity
  rw [← sub_div]
  ring

/-- Adult proportions (`ICW : ECW = 2 : 1`, the 60–40–20 rule): two thirds of a
water load goes into the cells. -/
theorem adult_water_load {W w Oe : ℝ} (he : 0 < Oe) :
    icwEq (W + w) (2 * Oe) Oe - icwEq W (2 * Oe) Oe = 2 / 3 * w := by
  unfold icwEq
  have h : Oe ≠ 0 := he.ne'
  field_simp
  ring

/-- Term newborn proportions (ICW 34%, ECW 44% of body weight): only `34/78` of a
water load, less than half, goes into the cells. -/
theorem newborn_water_load {W w : ℝ} (hw : 0 < w) :
    icwEq (W + w) 34 44 - icwEq W 34 44 = 34 / 78 * w ∧
      icwEq (W + w) 34 44 - icwEq W 34 44 < w / 2 := by
  have h1 : icwEq (W + w) 34 44 - icwEq W 34 44 = 34 / 78 * w := by
    unfold icwEq
    ring
  -- `34/78 < 1/2` and `w > 0`
  refine ⟨h1, ?_⟩
  rw [h1]
  linarith

/-- **Isotonic fluid stays outside the cells**: adding `v` litres of fluid whose
*effective* osmolality equals the body's, with all its solute staying outside the
cells (e.g. 0.9% saline), leaves intracellular water unchanged. This does not
apply to iso-osmolar dextrose, which acts as free water once the glucose is
metabolised. -/
theorem isotonic_stays_extracellular {W v Oi Oe : ℝ} (hW : 0 < W) (hv : 0 ≤ v)
    (hi : 0 < Oi) (he : 0 < Oe) :
    icwEq (W + v) Oi (Oe + v * ((Oi + Oe) / W)) = icwEq W Oi Oe := by
  unfold icwEq
  have hs : 0 < Oi + Oe := by positivity
  -- the new osmole total is `(Oi + Oe) * (W + v) / W`
  have hd : Oi + (Oe + v * ((Oi + Oe) / W)) = (Oi + Oe) * (W + v) / W := by
    field_simp
    ring
  have hWv : 0 < W + v := by linarith
  rw [hd]
  field_simp

/-- **Extra effective solute outside the cells shrinks them** (e.g. hypertonic
saline or mannitol; not urea, which crosses cell membranes). -/
theorem solute_load_shrinks_cells {W s Oi Oe : ℝ} (hW : 0 < W) (hs : 0 < s)
    (hi : 0 < Oi) (he : 0 < Oe) :
    icwEq W Oi (Oe + s) < icwEq W Oi Oe := by
  unfold icwEq
  -- same numerator, larger denominator
  apply div_lt_div_of_pos_left (by positivity) (by positivity)
  linarith

/-- **Free water swells the cells.** -/
theorem water_load_swells_cells {W w Oi Oe : ℝ} (hw : 0 < w) (hi : 0 < Oi) (he : 0 < Oe) :
    icwEq W Oi Oe < icwEq (W + w) Oi Oe := by
  have h := water_load_split (W := W) (w := w) hi he
  have hp : 0 < w * Oi / (Oi + Oe) := by positivity
  linarith

end Wyrd.BodyWater
