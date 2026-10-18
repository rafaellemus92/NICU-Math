import WyrdMathlib.PeriodicNS.Example

/-!
# The exact averages for the example field

Genuine integrals over `[0, 2π]³`: `E = 1`, `Z = 5/4`, `D = 7/2`, `S = 1/4`, and
`⟨|∇v|²⟩ = 5/2`.
-/

namespace Wyrd.PeriodicNS

open Real

/-! ### Helpers: triple integrals of trigonometric polynomials -/

/-- The unnormalised iterated integral over `[0, 2π]³` (so `avg f = Averages_I3 f / (2π)³`). -/
private noncomputable def Averages_I3 (f : ℝ → ℝ → ℝ → ℝ) : ℝ :=
  ∫ x in (0 : ℝ)..2 * π, ∫ y in (0 : ℝ)..2 * π, ∫ z in (0 : ℝ)..2 * π, f x y z

/-- Additivity of the iterated integral on jointly continuous integrands: each partial
integral is continuous in the remaining variables (parametric integrals), hence integrable. -/
private lemma Averages_I3_add {f g : ℝ → ℝ → ℝ → ℝ}
    (hf : Continuous fun p : ℝ × ℝ × ℝ => f p.1 p.2.1 p.2.2)
    (hg : Continuous fun p : ℝ × ℝ × ℝ => g p.1 p.2.1 p.2.2) :
    Averages_I3 (fun x y z => f x y z + g x y z) = Averages_I3 f + Averages_I3 g := by
  have cz : ∀ (h : ℝ → ℝ → ℝ → ℝ), (Continuous fun p : ℝ × ℝ × ℝ => h p.1 p.2.1 p.2.2) →
      ∀ x y, IntervalIntegrable (fun z => h x y z) MeasureTheory.volume 0 (2 * π) := by
    intro h hh x y
    exact (hh.comp (by fun_prop : Continuous fun z : ℝ => (x, y, z))).intervalIntegrable _ _
  have cy : ∀ (h : ℝ → ℝ → ℝ → ℝ), (Continuous fun p : ℝ × ℝ × ℝ => h p.1 p.2.1 p.2.2) →
      ∀ x, IntervalIntegrable (fun y => ∫ z in (0 : ℝ)..2 * π, h x y z)
        MeasureTheory.volume 0 (2 * π) := by
    intro h hh x
    apply Continuous.intervalIntegrable
    apply intervalIntegral.continuous_parametric_intervalIntegral_of_continuous'
      (f := fun y z => h x y z)
    exact hh.comp (by fun_prop : Continuous fun q : ℝ × ℝ => (x, q.1, q.2))
  have cx : ∀ (h : ℝ → ℝ → ℝ → ℝ), (Continuous fun p : ℝ × ℝ × ℝ => h p.1 p.2.1 p.2.2) →
      IntervalIntegrable (fun x => ∫ y in (0 : ℝ)..2 * π, ∫ z in (0 : ℝ)..2 * π, h x y z)
        MeasureTheory.volume 0 (2 * π) := by
    intro h hh
    apply Continuous.intervalIntegrable
    apply intervalIntegral.continuous_parametric_intervalIntegral_of_continuous'
      (f := fun x y => ∫ z in (0 : ℝ)..2 * π, h x y z)
    apply intervalIntegral.continuous_parametric_intervalIntegral_of_continuous'
      (f := fun (q : ℝ × ℝ) z => h q.1 q.2 z)
    exact hh.comp (by fun_prop : Continuous fun w : (ℝ × ℝ) × ℝ => (w.1.1, w.1.2, w.2))
  have e1 : ∀ x y, ∫ z in (0 : ℝ)..2 * π, (f x y z + g x y z) =
      (∫ z in (0 : ℝ)..2 * π, f x y z) + ∫ z in (0 : ℝ)..2 * π, g x y z :=
    fun x y => intervalIntegral.integral_add (cz f hf x y) (cz g hg x y)
  have e2 : ∀ x, ∫ y in (0 : ℝ)..2 * π,
      ((∫ z in (0 : ℝ)..2 * π, f x y z) + ∫ z in (0 : ℝ)..2 * π, g x y z) =
      (∫ y in (0 : ℝ)..2 * π, ∫ z in (0 : ℝ)..2 * π, f x y z) +
        ∫ y in (0 : ℝ)..2 * π, ∫ z in (0 : ℝ)..2 * π, g x y z :=
    fun x => intervalIntegral.integral_add (cy f hf x) (cy g hg x)
  unfold Averages_I3
  simp only [e1, e2]
  exact intervalIntegral.integral_add (cx f hf) (cx g hg)

/-- One-dimensional orthogonality: `∫₀^{2π} cos(d + n t) dt` vanishes for `n ≠ 0`
(antiderivative `sin(d + n t)/n` is `2π`-periodic). -/
private lemma Averages_int_cos (n : ℤ) (d : ℝ) :
    ∫ t in (0 : ℝ)..2 * π, cos (d + n * t) = if n = 0 then 2 * π * cos d else 0 := by
  split_ifs with h
  · subst h; simp
  · have hn : (n : ℝ) ≠ 0 := Int.cast_ne_zero.mpr h
    have := intervalIntegral.integral_comp_add_mul (a := 0) (b := 2 * π) cos hn d
    rw [this, integral_cos]
    simp [sin_add_int_mul_two_pi]

private lemma Averages_int_sin (n : ℤ) (d : ℝ) :
    ∫ t in (0 : ℝ)..2 * π, sin (d + n * t) = if n = 0 then 2 * π * sin d else 0 := by
  split_ifs with h
  · subst h; simp
  · have hn : (n : ℝ) ≠ 0 := Int.cast_ne_zero.mpr h
    have := intervalIntegral.integral_comp_add_mul (a := 0) (b := 2 * π) sin hn d
    rw [this, integral_sin]
    simp [cos_add_int_mul_two_pi]

/-- Triple orthogonality: integrate out `z`, then `y`, then `x`; a nonzero frequency kills the
integral at the first level where it appears. -/
private lemma Averages_I3_cos (p q r : ℤ) :
    Averages_I3 (fun x y z => cos (p * x + q * y + r * z)) =
      if (p, q, r) = (0, 0, 0) then (2 * π) ^ 3 else 0 := by
  unfold Averages_I3
  simp only [Averages_int_cos]
  by_cases hr : r = 0
  · subst hr
    simp only [ite_true, intervalIntegral.integral_const_mul, Averages_int_cos]
    by_cases hq : q = 0
    · subst hq
      by_cases hp : p = 0
      · subst hp; simp; ring
      · simp [hp]
        -- `sin (2πp) = 0` for integer `p`
        rw [show (p : ℝ) * (2 * π) = ((2 * p : ℤ) : ℝ) * π by push_cast; ring]
        exact sin_int_mul_pi _
    · simp [hq]
  · simp [hr]

private lemma Averages_I3_sin (p q r : ℤ) :
    Averages_I3 (fun x y z => sin (p * x + q * y + r * z)) = 0 := by
  unfold Averages_I3
  simp only [Averages_int_sin]
  by_cases hr : r = 0
  · subst hr
    simp only [ite_true, intervalIntegral.integral_const_mul, Averages_int_sin]
    by_cases hq : q = 0
    · subst hq
      by_cases hp : p = 0
      · subst hp; simp
      · simp [hp]
    · simp [hq]
  · simp [hr]

/-- One Fourier mode `a cos(k·x) + b sin(k·x)` with `m = (a, b, k)`, `k ∈ ℤ³`. -/
private noncomputable def Averages_tm (m : ℝ × ℝ × ℤ × ℤ × ℤ) (x y z : ℝ) : ℝ :=
  m.1 * cos (m.2.2.1 * x + m.2.2.2.1 * y + m.2.2.2.2 * z) +
    m.2.1 * sin (m.2.2.1 * x + m.2.2.2.1 * y + m.2.2.2.2 * z)

/-- A trigonometric polynomial: a finite list of modes. -/
private noncomputable def Averages_tp (L : List (ℝ × ℝ × ℤ × ℤ × ℤ)) (x y z : ℝ) : ℝ :=
  (L.map fun m => Averages_tm m x y z).sum

/-- Its constant Fourier coefficient. -/
private noncomputable def Averages_c0 (L : List (ℝ × ℝ × ℤ × ℤ × ℤ)) : ℝ :=
  (L.map fun m => if m.2.2 = (0, 0, 0) then m.1 else 0).sum

private lemma Averages_tm_cont (m : ℝ × ℝ × ℤ × ℤ × ℤ) :
    Continuous fun p : ℝ × ℝ × ℝ => Averages_tm m p.1 p.2.1 p.2.2 := by
  unfold Averages_tm; fun_prop

private lemma Averages_tp_cont (L : List (ℝ × ℝ × ℤ × ℤ × ℤ)) :
    Continuous fun p : ℝ × ℝ × ℝ => Averages_tp L p.1 p.2.1 p.2.2 := by
  induction L with
  | nil => simp only [Averages_tp, List.map_nil, List.sum_nil]; exact continuous_const
  | cons m L ih =>
    simp only [Averages_tp, List.map_cons, List.sum_cons] at ih ⊢
    exact (Averages_tm_cont m).add ih

private lemma Averages_I3_tm (m : ℝ × ℝ × ℤ × ℤ × ℤ) :
    Averages_I3 (Averages_tm m) = (2 * π) ^ 3 * (if m.2.2 = (0, 0, 0) then m.1 else 0) := by
  obtain ⟨a, b, p, q, r⟩ := m
  have hc : Continuous fun w : ℝ × ℝ × ℝ => a * cos (p * w.1 + q * w.2.1 + r * w.2.2) := by
    fun_prop
  have hs : Continuous fun w : ℝ × ℝ × ℝ => b * sin (p * w.1 + q * w.2.1 + r * w.2.2) := by
    fun_prop
  have e := Averages_I3_add (f := fun x y z => a * cos (p * x + q * y + r * z))
    (g := fun x y z => b * sin (p * x + q * y + r * z)) hc hs
  unfold Averages_tm
  simp only
  rw [e]
  have ec : Averages_I3 (fun x y z => a * cos (p * x + q * y + r * z)) =
      a * Averages_I3 (fun x y z => cos (p * x + q * y + r * z)) := by
    simp only [Averages_I3, intervalIntegral.integral_const_mul]
  have es : Averages_I3 (fun x y z => b * sin (p * x + q * y + r * z)) =
      b * Averages_I3 (fun x y z => sin (p * x + q * y + r * z)) := by
    simp only [Averages_I3, intervalIntegral.integral_const_mul]
  rw [ec, es, Averages_I3_cos, Averages_I3_sin]
  split_ifs <;> ring

/-- The integral of a trigonometric polynomial is `(2π)³` times its constant coefficient. -/
private lemma Averages_I3_tp (L : List (ℝ × ℝ × ℤ × ℤ × ℤ)) :
    Averages_I3 (Averages_tp L) = (2 * π) ^ 3 * Averages_c0 L := by
  induction L with
  | nil => simp [Averages_I3, Averages_tp, Averages_c0]
  | cons m L ih =>
    have e := Averages_I3_add (Averages_tm_cont m) (Averages_tp_cont L)
    have hfun : Averages_tp (m :: L) = fun x y z => Averages_tm m x y z + Averages_tp L x y z := by
      funext x y z; simp only [Averages_tp, List.map_cons, List.sum_cons]
    rw [hfun, e, ih, Averages_I3_tm]
    simp only [Averages_c0, List.map_cons, List.sum_cons]
    ring

/-- The average of a function that agrees pointwise with a trigonometric polynomial is its
constant coefficient. -/
private lemma Averages_avg_eq {f : ℝ → ℝ → ℝ → ℝ} (L : List (ℝ × ℝ × ℤ × ℤ × ℤ))
    (h : ∀ x y z, f x y z = Averages_tp L x y z) : avg f = Averages_c0 L := by
  have hf : f = Averages_tp L := by funext x y z; exact h x y z
  have hpi : (2 * π) ^ 3 ≠ 0 := pow_ne_zero _ (by positivity)
  rw [avg, hf]
  change Averages_I3 (Averages_tp L) / _ = _
  rw [Averages_I3_tp]
  field_simp

/-- Reduction of `sin³` modulo `sin² + cos² = 1`, used to normalise polynomial identities. -/
private lemma Averages_sin_cube (t : ℝ) : sin t ^ 3 = sin t - sin t * cos t ^ 2 := by
  have := sin_sq_add_cos_sq t
  linear_combination sin t * this

/-- **The quantities of `v`.** -/
theorem quantities_v :
    v.energy = 1 ∧ v.enstrophy = 5 / 4 ∧ v.palin = 7 / 2 ∧ v.stretching = 1 / 4 ∧ v.gradSq = 5 / 2 := by
  obtain ⟨c1, c2, c3⟩ := curl_v
  obtain ⟨g1, g2, g3, g4, g5, g6, g7, g8, g9⟩ := grad_v
  obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9⟩ := grad_curl_v
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  -- Each integrand is rewritten (via `Example`) into explicit trigonometric form and shown to equal
  -- an explicit trigonometric polynomial; the average is then its constant coefficient.
  -- |v|² = 2 + (oscillating modes), so E = 1
  · unfold Field.energy
    rw [Averages_avg_eq
      [(2, 0, 0, 0, 0), (-1/2, 0, 0, 0, 2), (-1, 0, 0, 1, 0), (-1/2, 0, 0, 2, 0),
      (1/2, 0, 2, 0, 0), (-1, 0, 2, 1, 0), (1/2, 0, 2, 2, 0)]]
    · norm_num [Averages_c0]
    · intro x y z
      simp only [v, Averages_tp, Averages_tm, List.map_cons, List.map_nil, List.sum_cons,
        List.sum_nil]
      push_cast
      -- expand every mode into a polynomial in sin/cos of x, y, z
      simp only [zero_mul, mul_zero, add_zero, zero_add, one_mul, neg_mul, Real.cos_add,
        Real.sin_add, Real.cos_two_mul, Real.sin_two_mul, Real.cos_zero, Real.sin_zero]
      ring_nf
      -- reduce modulo sin² + cos² = 1; both sides then have the same normal form
      simp only [Real.sin_sq]
      ring_nf
  -- |ω|² = 5/2 + (oscillating modes), so Z = 5/4
  · unfold Field.enstrophy Field.energy
    rw [Averages_avg_eq
      [(5/2, 0, 0, 0, 0), (1/2, 0, 0, 0, 2), (-1, 0, 0, 1, 0), (1/2, 0, 0, 2, 0),
      (0, -1, 1, 1, -1), (0, -1, 1, 1, 1), (-1/2, 0, 2, 0, 0), (1, 0, 2, 1, 0), (-1, 0, 2, 2, 0)]]
    · norm_num [Averages_c0]
    · intro x y z
      simp only [c1, c2, c3, Averages_tp, Averages_tm, List.map_cons, List.map_nil, List.sum_cons,
        List.sum_nil]
      push_cast
      -- expand every mode into a polynomial in sin/cos of x, y, z
      simp only [zero_mul, mul_zero, add_zero, zero_add, one_mul, neg_mul, Real.cos_add,
        Real.sin_add, Real.cos_neg, Real.sin_neg, Real.cos_two_mul, Real.sin_two_mul,
        Real.cos_zero, Real.sin_zero]
      ring_nf
      -- reduce modulo sin² + cos² = 1; both sides then have the same normal form
      simp only [Real.sin_sq]
      ring_nf
  -- |∇ω|² = 7/2 + (oscillating modes)
  · unfold Field.palin Field.gradSq
    rw [Averages_avg_eq
      [(7/2, 0, 0, 0, 0), (-1/2, 0, 0, 0, 2), (-1, 0, 0, 1, 0), (-1/2, 0, 0, 2, 0),
      (1/2, 0, 2, 0, 0), (-1, 0, 2, 1, 0), (2, 0, 2, 2, 0)]]
    · norm_num [Averages_c0]
    · intro x y z
      simp only [h1, h2, h3, h4, h5, h6, h7, h8, h9, Averages_tp, Averages_tm, List.map_cons,
        List.map_nil, List.sum_cons, List.sum_nil]
      push_cast
      -- expand every mode into a polynomial in sin/cos of x, y, z
      simp only [zero_mul, mul_zero, add_zero, zero_add, one_mul, neg_mul, Real.cos_add,
        Real.sin_add, Real.cos_two_mul, Real.sin_two_mul, Real.cos_zero, Real.sin_zero]
      ring_nf
      -- reduce modulo sin² + cos² = 1; both sides then have the same normal form
      simp only [Real.sin_sq]
      ring_nf
  -- ω·(ω·∇)v = cos y (sin x − sin(x+y)) (sin(x+y) − 3 cos z) = 1/4 + (oscillating modes);
  -- the mode `(2, 3, 0)` needs the triple-angle formulas
  · unfold Field.stretching
    rw [Averages_avg_eq
      [(1/4, 0, 0, 0, 0), (-1/2, 0, 0, 1, 0), (1/4, 0, 0, 2, 0),
      (0, -3/4, 1, -1, -1), (0, -3/4, 1, -1, 1), (0, 3/4, 1, 0, -1), (0, 3/4, 1, 0, 1),
      (0, -3/4, 1, 1, -1), (0, -3/4, 1, 1, 1), (0, 3/4, 1, 2, -1), (0, 3/4, 1, 2, 1),
      (-1/4, 0, 2, 0, 0), (1/4, 0, 2, 1, 0), (-1/4, 0, 2, 2, 0), (1/4, 0, 2, 3, 0)]]
    · norm_num [Averages_c0]
    · intro x y z
      simp only [c1, c2, c3, g1, g2, g3, g4, g5, g6, g7, g8, g9,
        Averages_tp, Averages_tm, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil]
      push_cast
      -- expand every mode into a polynomial in sin/cos of x, y, z
      simp only [zero_mul, mul_zero, add_zero, zero_add, one_mul, neg_mul, Real.cos_add,
        Real.sin_add, Real.cos_neg, Real.sin_neg, Real.cos_two_mul, Real.sin_two_mul,
        Real.cos_three_mul, Real.sin_three_mul, Real.cos_zero, Real.sin_zero]
      ring_nf
      -- reduce modulo sin² + cos² = 1; both sides then have the same normal form
      simp only [Real.sin_sq, Averages_sin_cube]
      ring_nf
  -- |∇v|² = 5/2 + (oscillating modes)
  · unfold Field.gradSq
    rw [Averages_avg_eq
      [(5/2, 0, 0, 0, 0), (1/2, 0, 0, 0, 2), (-1, 0, 0, 1, 0), (1/2, 0, 0, 2, 0),
      (-1/2, 0, 2, 0, 0), (1, 0, 2, 1, 0), (-1, 0, 2, 2, 0)]]
    · norm_num [Averages_c0]
    · intro x y z
      simp only [g1, g2, g3, g4, g5, g6, g7, g8, g9, Averages_tp, Averages_tm, List.map_cons,
        List.map_nil, List.sum_cons, List.sum_nil]
      push_cast
      -- expand every mode into a polynomial in sin/cos of x, y, z
      simp only [zero_mul, mul_zero, add_zero, zero_add, one_mul, neg_mul, Real.cos_add,
        Real.sin_add, Real.cos_two_mul, Real.sin_two_mul, Real.cos_zero, Real.sin_zero]
      ring_nf
      -- reduce modulo sin² + cos² = 1; both sides then have the same normal form
      simp only [Real.sin_sq]
      ring_nf

end Wyrd.PeriodicNS
