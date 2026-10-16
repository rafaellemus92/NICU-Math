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
  have hn0 : 0 < n := by linarith
  -- dividing a positive sine by a larger index gives a smaller ratio
  have hlt : sin i / n' < sin i / n := div_lt_div_of_pos_left hi hn0 hnn'
  -- both ratios are valid sines: `0 < sin i / n' < sin i / n ≤ sin i ≤ 1`
  have hlo : -1 ≤ sin i / n' := by
    have : 0 < sin i / n' := div_pos hi (by linarith)
    linarith
  have hhi : sin i / n ≤ 1 := by
    rw [div_le_iff₀ hn0]; nlinarith [sin_le_one i]
  -- and `arcsin` is strictly increasing on `[-1, 1]`
  exact arcsin_lt_arcsin hlo hlt hhi

/-- At a fixed entry angle, the deviation grows with the index. -/
theorem dev_lt_dev {k : ℕ} {n n' i : ℝ} (hn : 1 ≤ n) (hnn' : n < n') (hi : 0 < sin i) :
    dev k n i < dev k n' i := by
  -- the refraction term enters with the negative coefficient `-2(k+1)`
  have h := refr_lt_refr hn hnn' hi
  have hk : (0 : ℝ) < (k : ℝ) + 1 := by positivity
  unfold dev
  nlinarith

/-- **The bow's deviation grows with the index.** -/
theorem bowDev_lt {k : ℕ} {n n' : ℝ} (hk : 1 ≤ k) (hn : 1 < n) (hnn' : n < n') (hn' : n' < k + 1) :
    dev k n (bowIncidence k n) < dev k n' (bowIncidence k n') := by
  -- the larger index's bow angle `i'` lies in `(0, π/2)`, so `sin i' > 0`
  have hmem := bowIncidence_mem (hn.trans hnn') hk hn'
  have hsin : 0 < sin (bowIncidence k n') :=
    sin_pos_of_pos_of_lt_pi hmem.1 (by linarith [pi_pos, hmem.2])
  -- at index `n` the bow is the minimum over `[0, π/2]`, in particular below `D(i')`
  have hmin := isMinOn_iff.mp (dev_isMinOn hn hk (hnn'.trans hn')) (bowIncidence k n')
    ⟨hmem.1.le, hmem.2.le⟩
  -- and at the fixed angle `i'` the deviation grows from `n` to `n'`
  exact hmin.trans_lt (dev_lt_dev hn.le hnn' hsin)

theorem bowDev_strictMonoOn {k : ℕ} (hk : 1 ≤ k) :
    StrictMonoOn (fun n => dev k n (bowIncidence k n)) (Set.Ioo 1 (k + 1)) := by
  intro a ha b hb hab
  exact bowDev_lt hk ha.1 hab hb.2

/-- The primary bow's angle shrinks as the index grows. -/
theorem primary_angle_strictAntiOn :
    StrictAntiOn (fun n => π - dev 1 n (bowIncidence 1 n)) (Set.Ioo 1 2) := by
  intro a ha b hb hab
  -- `k = 1`: the bound `n < 2` is `n < 1 + 1`
  have hb2 : b < ((1 : ℕ) : ℝ) + 1 := by push_cast; linarith [hb.2]
  have := bowDev_lt le_rfl ha.1 hab hb2
  simp only
  linarith

/-- The secondary bow's angle grows as the index grows. -/
theorem secondary_angle_strictMonoOn :
    StrictMonoOn (fun n => dev 2 n (bowIncidence 2 n) - π) (Set.Ioo 1 3) := by
  intro a ha b hb hab
  -- `k = 2`: the bound `n < 3` is `n < 2 + 1`
  have hb3 : b < ((2 : ℕ) : ℝ) + 1 := by push_cast; linarith [hb.2]
  have := bowDev_lt (by norm_num) ha.1 hab hb3
  simp only
  linarith

/-- **Colour order**: if red has the smaller index, red lies outside violet in
the primary bow and inside violet in the secondary bow. -/
theorem colour_order {nRed nViolet : ℝ} (h1 : 1 < nRed) (h2 : nRed < nViolet) (h3 : nViolet < 2) :
    π - dev 1 nViolet (bowIncidence 1 nViolet) < π - dev 1 nRed (bowIncidence 1 nRed) ∧
      dev 2 nRed (bowIncidence 2 nRed) - π < dev 2 nViolet (bowIncidence 2 nViolet) - π := by
  -- both indices lie in `(1, 2) ⊆ (1, 3)`
  refine ⟨primary_angle_strictAntiOn ⟨h1, by linarith⟩ ⟨h1.trans h2, h3⟩ h2,
    secondary_angle_strictMonoOn ⟨h1, by linarith⟩ ⟨h1.trans h2, by linarith⟩ h2⟩

end Wyrd.Rainbow
