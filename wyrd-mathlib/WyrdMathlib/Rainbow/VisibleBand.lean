import WyrdMathlib.Rainbow.Colours
import WyrdMathlib.Rainbow.SpectrumPrimary
import WyrdMathlib.Rainbow.SpectrumSecondary

/-!
# Alexander's dark band, for every visible colour

For every index between red (`1.331`) and violet (`1.343`), light reflected
once leaves at under 43° and light reflected twice at over 50°. Red is the
extreme colour at *both* edges, so the red bounds plus the colour ordering
cover the whole visible range.
-/

namespace Wyrd.Rainbow

open Real

/-- **Alexander's dark band holds for every visible colour.** -/
theorem dark_band_visible {n i : ℝ} (hn : n ∈ Set.Icc (1331 / 1000) (1343 / 1000))
    (hi : i ∈ Set.Icc 0 (π / 2)) :
    π - dev 1 n i < 43 * π / 180 ∧ 50 * π / 180 < dev 2 n i - π := by
  sorry

/-- In real water, red lies outside violet in the primary bow and inside it in
the secondary bow. -/
theorem water_colour_order :
    π - dev 1 (1343 / 1000) (bowIncidence 1 (1343 / 1000)) <
        π - dev 1 (1331 / 1000) (bowIncidence 1 (1331 / 1000)) ∧
      dev 2 (1331 / 1000) (bowIncidence 2 (1331 / 1000)) - π <
        dev 2 (1343 / 1000) (bowIncidence 2 (1343 / 1000)) - π := by
  sorry

end Wyrd.Rainbow
