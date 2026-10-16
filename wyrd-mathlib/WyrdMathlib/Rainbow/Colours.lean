import WyrdMathlib.Rainbow.Bow

/-!
# Rainbow colours: why red is outside the primary bow and inside the secondary

The refractive index `n` of water is slightly larger for violet light than for
red (dispersion). Two simple facts then sort the colours:

1. at a fixed entry angle, a larger `n` bends the ray more, so the deviation
   `D` grows with `n` (`dev_lt_dev`);
2. the bow is the *minimum* of `D` over entry angles (`dev_isMinOn`). If every
   value grows, so does the minimum (`bowDev_lt`).

So the primary bow's angle `π - D` shrinks as `n` grows: violet sits inside,
red outside. The secondary bow's angle `D - π` grows: the order is reversed.
No derivative in `n` is needed.
-/

namespace Wyrd.Rainbow

open Real

/-- A larger index bends the ray more: the refraction angle shrinks as `n` grows. -/
theorem refr_lt_refr {n n' i : ℝ} (hn : 1 ≤ n) (hnn' : n < n') (hi : 0 < sin i) :
    refr n' i < refr n i := by
  sorry

/-- At a fixed entry angle, the deviation grows with the index. -/
theorem dev_lt_dev {k : ℕ} {n n' i : ℝ} (hn : 1 ≤ n) (hnn' : n < n') (hi : 0 < sin i) :
    dev k n i < dev k n' i := by
  sorry

/-- **The bow's deviation grows with the index.** -/
theorem bowDev_lt {k : ℕ} {n n' : ℝ} (hk : 1 ≤ k) (hn : 1 < n) (hnn' : n < n') (hn' : n' < k + 1) :
    dev k n (bowIncidence k n) < dev k n' (bowIncidence k n') := by
  sorry

theorem bowDev_strictMonoOn {k : ℕ} (hk : 1 ≤ k) :
    StrictMonoOn (fun n => dev k n (bowIncidence k n)) (Set.Ioo 1 (k + 1)) := by
  sorry

/-- The primary bow's angle shrinks as the index grows. -/
theorem primary_angle_strictAntiOn :
    StrictAntiOn (fun n => π - dev 1 n (bowIncidence 1 n)) (Set.Ioo 1 2) := by
  sorry

/-- The secondary bow's angle grows as the index grows. -/
theorem secondary_angle_strictMonoOn :
    StrictMonoOn (fun n => dev 2 n (bowIncidence 2 n) - π) (Set.Ioo 1 3) := by
  sorry

/-- **Colour order**: if red has the smaller index, red lies outside violet in
the primary bow and inside violet in the secondary bow. -/
theorem colour_order {nRed nViolet : ℝ} (h1 : 1 < nRed) (h2 : nRed < nViolet) (h3 : nViolet < 2) :
    π - dev 1 nViolet (bowIncidence 1 nViolet) < π - dev 1 nRed (bowIncidence 1 nRed) ∧
      dev 2 nRed (bowIncidence 2 nRed) - π < dev 2 nViolet (bowIncidence 2 nViolet) - π := by
  sorry

end Wyrd.Rainbow
