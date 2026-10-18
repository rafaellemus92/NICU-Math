import WyrdMathlib.Rainbow.Bow
import WyrdMathlib.Rainbow.Primary
import WyrdMathlib.Rainbow.Secondary

/-!
# Alexander's dark band

The sky between the two bows is visibly darker. It was described by Alexander
of Aphrodisias around 200 AD. Here is why, for water (`n = 4/3`):

* the bow angle is the *extreme* exit angle. Every ray that reflects once
  inside the drop leaves at most at the primary bow's angle, under 43°, so
  that light lies **inside** the primary bow;
* every ray that reflects twice leaves at least at the secondary bow's angle,
  over 50°, so that light lies **outside** the secondary bow;
* so no light with one or two internal reflections lands between 43° and 50°.

Angles are measured from the antisolar point (the shadow of your head).
-/

namespace Wyrd.Rainbow

open Real

/-- **Light reflected once lies inside the primary bow**: every such ray leaves
at less than 43° from the antisolar point. -/
theorem primary_light_inside {i : ℝ} (hi : i ∈ Set.Icc 0 (π / 2)) :
    π - dev 1 (4 / 3) i < 43 * π / 180 := by
  -- The bow is the minimum of the deviation, so it is the maximum of `π - D`.
  have hmin := isMinOn_iff.mp
    (dev_isMinOn (n := 4 / 3) (k := 1) (by norm_num) le_rfl (by norm_num)) i hi
  have := primary_bow_water.2
  linarith

/-- **Light reflected twice lies outside the secondary bow**: every such ray
leaves at more than 50° from the antisolar point. -/
theorem secondary_light_outside {i : ℝ} (hi : i ∈ Set.Icc 0 (π / 2)) :
    50 * π / 180 < dev 2 (4 / 3) i - π := by
  -- The bow is the minimum of the deviation, so it is the minimum of `D - π`.
  have hmin := isMinOn_iff.mp
    (dev_isMinOn (n := 4 / 3) (k := 2) (by norm_num) (by norm_num) (by norm_num)) i hi
  have := secondary_bow_water.1
  linarith

/-- **Alexander's dark band**: no ray with one or two internal reflections
leaves at an angle between 43° and 50°. -/
theorem alexander_dark_band {i θ : ℝ} (hi : i ∈ Set.Icc 0 (π / 2))
    (hθ : 43 * π / 180 ≤ θ ∧ θ ≤ 50 * π / 180) :
    π - dev 1 (4 / 3) i ≠ θ ∧ dev 2 (4 / 3) i - π ≠ θ := by
  have h1 := primary_light_inside hi
  have h2 := secondary_light_outside hi
  constructor <;> intro h <;> linarith [hθ.1, hθ.2]

end Wyrd.Rainbow
