import WyrdMathlib.PeriodicNS.SignFlip

/-!
# The phase family: only a relative phase changes, and stretching follows it

From the uploaded `periodic_ns_lab_v1`: the family

  `v_φ = (sin y, sin z, cos x − cos(x + y + φ))`,  `v_0 = v`.

Background, not formalised: translating space can remove the phases of three of
the four plane waves, but not the relational phase `φ`, because the wave vector
`(1, 1, 0)` is the sum of `(1, 0, 0)` and `(0, 1, 0)`. Changing `φ` moves no Fourier magnitude (the
magnitudes are not formalised here). Proved:

* `div_vphi`, `vphi_zero`: every member is divergence-free, and `φ = 0` is `v`.
* `quantities_vphi`: `E = 1`, `Z = 5/4`, `D = 7/2` for **every** `φ`, while
  `S = cos φ / 4`.
* `quantities_vphi_smul`, `growth_iff`: for amplitude `A > 0`, `S − νD > 0`
  exactly when `cos φ > 14ν/A`.
* `zero_growth_at_pi_div_three`: at `A = 1`, `ν = 1/28`, `φ = π/3` gives `S − νD = 0`.
* `neg_v_translate`: the old sign-reversed field `−v` is `v_π` translated by
  `(π, π, π)`, so it is a member of the family.

As in `SignFlip.lean`, `S − νD` is the right-hand side of the standard enstrophy
balance. The balance itself, and any time evolution (the lab's `Z''(0)`,
high-shell growth and simulations), are not formalised.
-/

namespace Wyrd.PeriodicNS

open Real

/-- The phase family. -/
noncomputable def vphi (φ : ℝ) : Field :=
  ⟨fun _ y _ => sin y, fun _ _ z => sin z, fun x y _ => cos x - cos (x + y + φ)⟩

theorem vphi_zero : vphi 0 = v := by
  simp [vphi, v]

theorem div_vphi (φ x y z : ℝ) : (vphi φ).div x y z = 0 := by
  simp [Field.div, dx, dy, dz, vphi]

/-- `d/ds cos (c + s + d) = -sin (c + s + d)` (simp handles `s + c + d` but not `c + s + d`). -/
private lemma PhaseFamily_deriv_cos_mid (c d t : ℝ) :
    deriv (fun s => cos (c + s + d)) t = -sin (c + t + d) := by
  have h : (fun s => cos (c + s + d)) = fun s => cos (s + (c + d)) := by funext s; ring_nf
  rw [h]; simp; ring_nf

/-- `d/ds sin (c + s + d) = cos (c + s + d)`. -/
private lemma PhaseFamily_deriv_sin_mid (c d t : ℝ) :
    deriv (fun s => sin (c + s + d)) t = cos (c + t + d) := by
  have h : (fun s => sin (c + s + d)) = fun s => sin (s + (c + d)) := by funext s; ring_nf
  rw [h]; simp; ring_nf

/-- The vorticity of `v_φ`. -/
private lemma PhaseFamily_curl (φ : ℝ) :
    (vphi φ).curl.u1 = (fun x y z => sin (x + y + φ) - cos z) ∧
      (vphi φ).curl.u2 = (fun x y _ => sin x - sin (x + y + φ)) ∧
      (vphi φ).curl.u3 = (fun _ y _ => -cos y) := by
  refine ⟨?_, ?_, ?_⟩ <;> funext x y z
  · simp [Field.curl, dx, dy, dz, vphi, PhaseFamily_deriv_cos_mid]
  · simp [Field.curl, dx, dy, dz, vphi, PhaseFamily_deriv_cos_mid]
    ring
  · simp [Field.curl, dx, dy, dz, vphi, PhaseFamily_deriv_cos_mid]

/-- The velocity gradient entries of `v_φ`. -/
private lemma PhaseFamily_grad (φ : ℝ) :
    dx (vphi φ).u1 = (fun _ _ _ => 0) ∧ dy (vphi φ).u1 = (fun _ y _ => cos y) ∧
      dz (vphi φ).u1 = (fun _ _ _ => 0) ∧
    dx (vphi φ).u2 = (fun _ _ _ => 0) ∧ dy (vphi φ).u2 = (fun _ _ _ => 0) ∧
      dz (vphi φ).u2 = (fun _ _ z => cos z) ∧
    dx (vphi φ).u3 = (fun x y _ => -sin x + sin (x + y + φ)) ∧
      dy (vphi φ).u3 = (fun x y _ => sin (x + y + φ)) ∧
      dz (vphi φ).u3 = (fun _ _ _ => 0) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> funext x y z <;>
    simp [dx, dy, dz, vphi, PhaseFamily_deriv_cos_mid]

/-- The vorticity gradient entries of `v_φ`. -/
private lemma PhaseFamily_grad_curl (φ : ℝ) :
    dx (vphi φ).curl.u1 = (fun x y _ => cos (x + y + φ)) ∧
      dy (vphi φ).curl.u1 = (fun x y _ => cos (x + y + φ)) ∧
      dz (vphi φ).curl.u1 = (fun _ _ z => sin z) ∧
    dx (vphi φ).curl.u2 = (fun x y _ => cos x - cos (x + y + φ)) ∧
      dy (vphi φ).curl.u2 = (fun x y _ => -cos (x + y + φ)) ∧
      dz (vphi φ).curl.u2 = (fun _ _ _ => 0) ∧
    dx (vphi φ).curl.u3 = (fun _ _ _ => 0) ∧ dy (vphi φ).curl.u3 = (fun _ y _ => sin y) ∧
      dz (vphi φ).curl.u3 = (fun _ _ _ => 0) := by
  obtain ⟨c1, c2, c3⟩ := PhaseFamily_curl φ
  rw [c1, c2, c3]
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> funext x y z <;>
    simp [dx, dy, dz, PhaseFamily_deriv_sin_mid]

/-! ### Helpers: triple integrals of trigonometric polynomials -/

/-- The unnormalised iterated integral over `[0, 2π]³` (so `avg f = PhaseFamily_I3 f / (2π)³`). -/
private noncomputable def PhaseFamily_I3 (f : ℝ → ℝ → ℝ → ℝ) : ℝ :=
  ∫ x in (0 : ℝ)..2 * π, ∫ y in (0 : ℝ)..2 * π, ∫ z in (0 : ℝ)..2 * π, f x y z

/-- Additivity of the iterated integral on jointly continuous integrands: each partial
integral is continuous in the remaining variables (parametric integrals), hence integrable. -/
private lemma PhaseFamily_I3_add {f g : ℝ → ℝ → ℝ → ℝ}
    (hf : Continuous fun p : ℝ × ℝ × ℝ => f p.1 p.2.1 p.2.2)
    (hg : Continuous fun p : ℝ × ℝ × ℝ => g p.1 p.2.1 p.2.2) :
    PhaseFamily_I3 (fun x y z => f x y z + g x y z) = PhaseFamily_I3 f + PhaseFamily_I3 g := by
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
  unfold PhaseFamily_I3
  simp only [e1, e2]
  exact intervalIntegral.integral_add (cx f hf) (cx g hg)

/-- One-dimensional orthogonality: `∫₀^{2π} cos(d + n t) dt` vanishes for `n ≠ 0`
(antiderivative `sin(d + n t)/n` is `2π`-periodic). -/
private lemma PhaseFamily_int_cos (n : ℤ) (d : ℝ) :
    ∫ t in (0 : ℝ)..2 * π, cos (d + n * t) = if n = 0 then 2 * π * cos d else 0 := by
  split_ifs with h
  · subst h; simp
  · have hn : (n : ℝ) ≠ 0 := Int.cast_ne_zero.mpr h
    have := intervalIntegral.integral_comp_add_mul (a := 0) (b := 2 * π) cos hn d
    rw [this, integral_cos]
    simp [sin_add_int_mul_two_pi]

private lemma PhaseFamily_int_sin (n : ℤ) (d : ℝ) :
    ∫ t in (0 : ℝ)..2 * π, sin (d + n * t) = if n = 0 then 2 * π * sin d else 0 := by
  split_ifs with h
  · subst h; simp
  · have hn : (n : ℝ) ≠ 0 := Int.cast_ne_zero.mpr h
    have := intervalIntegral.integral_comp_add_mul (a := 0) (b := 2 * π) sin hn d
    rw [this, integral_sin]
    simp [cos_add_int_mul_two_pi]

/-- Triple orthogonality: integrate out `z`, then `y`, then `x`; a nonzero frequency kills the
integral at the first level where it appears. -/
private lemma PhaseFamily_I3_cos (p q r : ℤ) :
    PhaseFamily_I3 (fun x y z => cos (p * x + q * y + r * z)) =
      if (p, q, r) = (0, 0, 0) then (2 * π) ^ 3 else 0 := by
  unfold PhaseFamily_I3
  simp only [PhaseFamily_int_cos]
  by_cases hr : r = 0
  · subst hr
    simp only [ite_true, intervalIntegral.integral_const_mul, PhaseFamily_int_cos]
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

private lemma PhaseFamily_I3_sin (p q r : ℤ) :
    PhaseFamily_I3 (fun x y z => sin (p * x + q * y + r * z)) = 0 := by
  unfold PhaseFamily_I3
  simp only [PhaseFamily_int_sin]
  by_cases hr : r = 0
  · subst hr
    simp only [ite_true, intervalIntegral.integral_const_mul, PhaseFamily_int_sin]
    by_cases hq : q = 0
    · subst hq
      by_cases hp : p = 0
      · subst hp; simp
      · simp [hp]
    · simp [hq]
  · simp [hr]

/-- One Fourier mode `a cos(k·x) + b sin(k·x)` with `m = (a, b, k)`, `k ∈ ℤ³`. -/
private noncomputable def PhaseFamily_tm (m : ℝ × ℝ × ℤ × ℤ × ℤ) (x y z : ℝ) : ℝ :=
  m.1 * cos (m.2.2.1 * x + m.2.2.2.1 * y + m.2.2.2.2 * z) +
    m.2.1 * sin (m.2.2.1 * x + m.2.2.2.1 * y + m.2.2.2.2 * z)

/-- A trigonometric polynomial: a finite list of modes. -/
private noncomputable def PhaseFamily_tp (L : List (ℝ × ℝ × ℤ × ℤ × ℤ)) (x y z : ℝ) : ℝ :=
  (L.map fun m => PhaseFamily_tm m x y z).sum

/-- Its constant Fourier coefficient. -/
private noncomputable def PhaseFamily_c0 (L : List (ℝ × ℝ × ℤ × ℤ × ℤ)) : ℝ :=
  (L.map fun m => if m.2.2 = (0, 0, 0) then m.1 else 0).sum

private lemma PhaseFamily_tm_cont (m : ℝ × ℝ × ℤ × ℤ × ℤ) :
    Continuous fun p : ℝ × ℝ × ℝ => PhaseFamily_tm m p.1 p.2.1 p.2.2 := by
  unfold PhaseFamily_tm; fun_prop

private lemma PhaseFamily_tp_cont (L : List (ℝ × ℝ × ℤ × ℤ × ℤ)) :
    Continuous fun p : ℝ × ℝ × ℝ => PhaseFamily_tp L p.1 p.2.1 p.2.2 := by
  induction L with
  | nil => simp only [PhaseFamily_tp, List.map_nil, List.sum_nil]; exact continuous_const
  | cons m L ih =>
    simp only [PhaseFamily_tp, List.map_cons, List.sum_cons] at ih ⊢
    exact (PhaseFamily_tm_cont m).add ih

private lemma PhaseFamily_I3_tm (m : ℝ × ℝ × ℤ × ℤ × ℤ) :
    PhaseFamily_I3 (PhaseFamily_tm m) = (2 * π) ^ 3 * (if m.2.2 = (0, 0, 0) then m.1 else 0) := by
  obtain ⟨a, b, p, q, r⟩ := m
  have hc : Continuous fun w : ℝ × ℝ × ℝ => a * cos (p * w.1 + q * w.2.1 + r * w.2.2) := by
    fun_prop
  have hs : Continuous fun w : ℝ × ℝ × ℝ => b * sin (p * w.1 + q * w.2.1 + r * w.2.2) := by
    fun_prop
  have e := PhaseFamily_I3_add (f := fun x y z => a * cos (p * x + q * y + r * z))
    (g := fun x y z => b * sin (p * x + q * y + r * z)) hc hs
  unfold PhaseFamily_tm
  simp only
  rw [e]
  have ec : PhaseFamily_I3 (fun x y z => a * cos (p * x + q * y + r * z)) =
      a * PhaseFamily_I3 (fun x y z => cos (p * x + q * y + r * z)) := by
    simp only [PhaseFamily_I3, intervalIntegral.integral_const_mul]
  have es : PhaseFamily_I3 (fun x y z => b * sin (p * x + q * y + r * z)) =
      b * PhaseFamily_I3 (fun x y z => sin (p * x + q * y + r * z)) := by
    simp only [PhaseFamily_I3, intervalIntegral.integral_const_mul]
  rw [ec, es, PhaseFamily_I3_cos, PhaseFamily_I3_sin]
  split_ifs <;> ring

/-- The integral of a trigonometric polynomial is `(2π)³` times its constant coefficient. -/
private lemma PhaseFamily_I3_tp (L : List (ℝ × ℝ × ℤ × ℤ × ℤ)) :
    PhaseFamily_I3 (PhaseFamily_tp L) = (2 * π) ^ 3 * PhaseFamily_c0 L := by
  induction L with
  | nil => simp [PhaseFamily_I3, PhaseFamily_tp, PhaseFamily_c0]
  | cons m L ih =>
    have e := PhaseFamily_I3_add (PhaseFamily_tm_cont m) (PhaseFamily_tp_cont L)
    have hfun : PhaseFamily_tp (m :: L) =
        fun x y z => PhaseFamily_tm m x y z + PhaseFamily_tp L x y z := by
      funext x y z; simp only [PhaseFamily_tp, List.map_cons, List.sum_cons]
    rw [hfun, e, ih, PhaseFamily_I3_tm]
    simp only [PhaseFamily_c0, List.map_cons, List.sum_cons]
    ring

/-- The average of a function that agrees pointwise with a trigonometric polynomial is its
constant coefficient. -/
private lemma PhaseFamily_avg_eq {f : ℝ → ℝ → ℝ → ℝ} (L : List (ℝ × ℝ × ℤ × ℤ × ℤ))
    (h : ∀ x y z, f x y z = PhaseFamily_tp L x y z) : avg f = PhaseFamily_c0 L := by
  have hf : f = PhaseFamily_tp L := by funext x y z; exact h x y z
  have hpi : (2 * π) ^ 3 ≠ 0 := pow_ne_zero _ (by positivity)
  rw [avg, hf]
  change PhaseFamily_I3 (PhaseFamily_tp L) / _ = _
  rw [PhaseFamily_I3_tp]
  field_simp

/-- Reduction of `sin³` modulo `sin² + cos² = 1`, used to normalise polynomial identities. -/
private lemma PhaseFamily_sin_cube (t : ℝ) : sin t ^ 3 = sin t - sin t * cos t ^ 2 := by
  have := sin_sq_add_cos_sq t
  linear_combination sin t * this

theorem quantities_vphi (φ : ℝ) :
    (vphi φ).energy = 1 ∧ (vphi φ).enstrophy = 5 / 4 ∧ (vphi φ).palin = 7 / 2 ∧
      (vphi φ).stretching = cos φ / 4 := by
  obtain ⟨c1, c2, c3⟩ := PhaseFamily_curl φ
  obtain ⟨g1, g2, g3, g4, g5, g6, g7, g8, g9⟩ := PhaseFamily_grad φ
  obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9⟩ := PhaseFamily_grad_curl φ
  refine ⟨?_, ?_, ?_, ?_⟩
  -- As in `Averages.lean`: each integrand equals an explicit trigonometric polynomial whose
  -- coefficients now depend on `φ`; the average is its constant coefficient.
  -- |u|² = 2 + (oscillating modes), so E = 1
  · unfold Field.energy
    rw [PhaseFamily_avg_eq
      [(2, 0, 0, 0, 0), (-1/2, 0, 0, 0, 2), (-cos φ, sin φ, 0, 1, 0), (-1/2, 0, 0, 2, 0),
      (1/2, 0, 2, 0, 0), (-cos φ, sin φ, 2, 1, 0),
      (1/2 * cos (2 * φ), -1/2 * sin (2 * φ), 2, 2, 0)]]
    · norm_num [PhaseFamily_c0]
    · intro x y z
      simp only [vphi, PhaseFamily_tp, PhaseFamily_tm, List.map_cons, List.map_nil,
        List.sum_cons, List.sum_nil]
      push_cast
      simp only [zero_mul, mul_zero, add_zero, zero_add, one_mul, neg_mul, Real.cos_add,
        Real.sin_add, Real.cos_two_mul, Real.sin_two_mul,
        Real.cos_zero, Real.sin_zero]
      ring_nf
      simp only [Real.sin_sq]
      ring_nf
  -- |ω|² = 5/2 + (oscillating modes), so Z = 5/4
  · unfold Field.enstrophy Field.energy
    rw [PhaseFamily_avg_eq
      [(5/2, 0, 0, 0, 0), (1/2, 0, 0, 0, 2), (-cos φ, sin φ, 0, 1, 0), (1/2, 0, 0, 2, 0),
      (-sin φ, -cos φ, 1, 1, -1), (-sin φ, -cos φ, 1, 1, 1), (-1/2, 0, 2, 0, 0),
      (cos φ, -sin φ, 2, 1, 0), (-cos (2 * φ), sin (2 * φ), 2, 2, 0)]]
    · norm_num [PhaseFamily_c0]
    · intro x y z
      simp only [c1, c2, c3, PhaseFamily_tp, PhaseFamily_tm, List.map_cons, List.map_nil,
        List.sum_cons, List.sum_nil]
      push_cast
      simp only [zero_mul, mul_zero, add_zero, zero_add, one_mul, neg_mul, Real.cos_add,
        Real.sin_add, Real.cos_neg, Real.sin_neg, Real.cos_two_mul, Real.sin_two_mul,
        Real.cos_zero, Real.sin_zero]
      ring_nf
      simp only [Real.sin_sq]
      ring_nf
  -- |∇ω|² = 7/2 + (oscillating modes)
  · unfold Field.palin Field.gradSq
    rw [PhaseFamily_avg_eq
      [(7/2, 0, 0, 0, 0), (-1/2, 0, 0, 0, 2), (-cos φ, sin φ, 0, 1, 0), (-1/2, 0, 0, 2, 0),
      (1/2, 0, 2, 0, 0), (-cos φ, sin φ, 2, 1, 0),
      (2 * cos (2 * φ), -2 * sin (2 * φ), 2, 2, 0)]]
    · norm_num [PhaseFamily_c0]
    · intro x y z
      simp only [h1, h2, h3, h4, h5, h6, h7, h8, h9, PhaseFamily_tp, PhaseFamily_tm,
        List.map_cons, List.map_nil, List.sum_cons, List.sum_nil]
      push_cast
      simp only [zero_mul, mul_zero, add_zero, zero_add, one_mul, neg_mul, Real.cos_add,
        Real.sin_add, Real.cos_two_mul, Real.sin_two_mul,
        Real.cos_zero, Real.sin_zero]
      ring_nf
      simp only [Real.sin_sq]
      ring_nf
  -- ω·(ω·∇)u = cos y (sin x − sin(x+y+φ)) (sin(x+y+φ) − 3 cos z) = cos φ / 4 + (oscillating modes)
  · unfold Field.stretching
    rw [PhaseFamily_avg_eq
      [(1/4 * cos φ, 0, 0, 0, 0), (-1/2, 0, 0, 1, 0), (1/4 * cos φ, -1/4 * sin φ, 0, 2, 0),
      (0, -3/4, 1, -1, -1), (0, -3/4, 1, -1, 1),
      (3/4 * sin φ, 3/4 * cos φ, 1, 0, -1), (3/4 * sin φ, 3/4 * cos φ, 1, 0, 1),
      (0, -3/4, 1, 1, -1), (0, -3/4, 1, 1, 1),
      (3/4 * sin φ, 3/4 * cos φ, 1, 2, -1), (3/4 * sin φ, 3/4 * cos φ, 1, 2, 1),
      (-1/4 * cos φ, 1/4 * sin φ, 2, 0, 0), (1/4 * cos (2 * φ), -1/4 * sin (2 * φ), 2, 1, 0),
      (-1/4 * cos φ, 1/4 * sin φ, 2, 2, 0), (1/4 * cos (2 * φ), -1/4 * sin (2 * φ), 2, 3, 0)]]
    · norm_num [PhaseFamily_c0]
      ring
    · intro x y z
      simp only [c1, c2, c3, g1, g2, g3, g4, g5, g6, g7, g8, g9,
        PhaseFamily_tp, PhaseFamily_tm, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil]
      push_cast
      simp only [zero_mul, mul_zero, add_zero, zero_add, one_mul, neg_mul, Real.cos_add,
        Real.sin_add, Real.cos_neg, Real.sin_neg, Real.cos_two_mul, Real.sin_two_mul,
        Real.cos_three_mul, Real.sin_three_mul, Real.cos_zero, Real.sin_zero]
      ring_nf
      simp only [Real.sin_sq, PhaseFamily_sin_cube]
      ring_nf

/-! ### Helpers: scaling by an amplitude (as in `SignFlip.lean`) -/

/-- `∂/∂x` commutes with multiplication by a constant (no differentiability needed). -/
private lemma PhaseFamily_dx_smul (A : ℝ) (f : ℝ → ℝ → ℝ → ℝ) :
    dx (fun x y z => A * f x y z) = fun x y z => A * dx f x y z := by
  funext x y z; exact deriv_const_mul_field A

/-- `∂/∂y` commutes with multiplication by a constant. -/
private lemma PhaseFamily_dy_smul (A : ℝ) (f : ℝ → ℝ → ℝ → ℝ) :
    dy (fun x y z => A * f x y z) = fun x y z => A * dy f x y z := by
  funext x y z; exact deriv_const_mul_field A

/-- `∂/∂z` commutes with multiplication by a constant. -/
private lemma PhaseFamily_dz_smul (A : ℝ) (f : ℝ → ℝ → ℝ → ℝ) :
    dz (fun x y z => A * f x y z) = fun x y z => A * dz f x y z := by
  funext x y z; exact deriv_const_mul_field A

/-- The curl is linear: `curl (A u) = A curl u`. -/
private lemma PhaseFamily_curl_smul (A : ℝ) (u : Field) : (u.smul A).curl = u.curl.smul A := by
  simp only [Field.curl, Field.smul, PhaseFamily_dx_smul, PhaseFamily_dy_smul,
    PhaseFamily_dz_smul, Field.mk.injEq]
  refine ⟨?_, ?_, ?_⟩ <;> funext x y z <;> ring

/-- Constants pull out of the average (`integral_const_mul` needs no integrability). -/
private lemma PhaseFamily_avg_eq_mul {f g : ℝ → ℝ → ℝ → ℝ} (c : ℝ)
    (h : ∀ x y z, f x y z = c * g x y z) : avg f = c * avg g := by
  have hf : f = fun x y z => c * g x y z := by funext x y z; exact h x y z
  subst hf
  unfold avg
  simp only [intervalIntegral.integral_const_mul]
  ring

private lemma PhaseFamily_energy_smul (A : ℝ) (u : Field) :
    (u.smul A).energy = A ^ 2 * u.energy := by
  unfold Field.energy
  rw [PhaseFamily_avg_eq_mul (A ^ 2)
    (g := fun x y z => u.u1 x y z ^ 2 + u.u2 x y z ^ 2 + u.u3 x y z ^ 2)
    (fun x y z => by simp only [Field.smul]; ring)]
  ring

private lemma PhaseFamily_gradSq_smul (A : ℝ) (u : Field) :
    (u.smul A).gradSq = A ^ 2 * u.gradSq := by
  unfold Field.gradSq
  rw [PhaseFamily_avg_eq_mul (A ^ 2)
    (g := fun x y z =>
      dx u.u1 x y z ^ 2 + dy u.u1 x y z ^ 2 + dz u.u1 x y z ^ 2 +
      dx u.u2 x y z ^ 2 + dy u.u2 x y z ^ 2 + dz u.u2 x y z ^ 2 +
      dx u.u3 x y z ^ 2 + dy u.u3 x y z ^ 2 + dz u.u3 x y z ^ 2)
    (fun x y z => by
      simp only [Field.smul, PhaseFamily_dx_smul, PhaseFamily_dy_smul, PhaseFamily_dz_smul]; ring)]

private lemma PhaseFamily_stretching_smul (A : ℝ) (u : Field) :
    (u.smul A).stretching = A ^ 3 * u.stretching := by
  unfold Field.stretching
  rw [PhaseFamily_curl_smul]
  rw [PhaseFamily_avg_eq_mul (A ^ 3)
    (g := fun x y z =>
      u.curl.u1 x y z * (dx u.u1 x y z * u.curl.u1 x y z + dy u.u1 x y z * u.curl.u2 x y z +
        dz u.u1 x y z * u.curl.u3 x y z) +
      u.curl.u2 x y z * (dx u.u2 x y z * u.curl.u1 x y z + dy u.u2 x y z * u.curl.u2 x y z +
        dz u.u2 x y z * u.curl.u3 x y z) +
      u.curl.u3 x y z * (dx u.u3 x y z * u.curl.u1 x y z + dy u.u3 x y z * u.curl.u2 x y z +
        dz u.u3 x y z * u.curl.u3 x y z))
    (fun x y z => by
      simp only [Field.smul, PhaseFamily_dx_smul, PhaseFamily_dy_smul, PhaseFamily_dz_smul]; ring)]

theorem quantities_vphi_smul (A φ : ℝ) :
    ((vphi φ).smul A).energy = A ^ 2 ∧ ((vphi φ).smul A).enstrophy = 5 * A ^ 2 / 4 ∧
      ((vphi φ).smul A).palin = 7 * A ^ 2 / 2 ∧
      ((vphi φ).smul A).stretching = A ^ 3 * cos φ / 4 := by
  obtain ⟨hE, hZ, hD, hS⟩ := quantities_vphi φ
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [PhaseFamily_energy_smul, hE]; ring
  · rw [Field.enstrophy, PhaseFamily_curl_smul, PhaseFamily_energy_smul, ← Field.enstrophy, hZ]
    ring
  · rw [Field.palin, PhaseFamily_curl_smul, PhaseFamily_gradSq_smul, ← Field.palin, hD]; ring
  · rw [PhaseFamily_stretching_smul, hS]; ring

theorem growth_iff {A ν φ : ℝ} (hA : 0 < A) :
    0 < ((vphi φ).smul A).stretching - ν * ((vphi φ).smul A).palin ↔ 14 * ν / A < cos φ := by
  obtain ⟨-, -, hD, hS⟩ := quantities_vphi_smul A φ
  rw [hD, hS, div_lt_iff₀ hA]
  -- `A³ cos φ / 4 − 7νA²/2 = (A²/4)(A cos φ − 14ν)`
  rw [show A ^ 3 * cos φ / 4 - ν * (7 * A ^ 2 / 2) = A ^ 2 / 4 * (cos φ * A - 14 * ν) by ring,
    mul_pos_iff_of_pos_left (by positivity), sub_pos]

theorem zero_growth_at_pi_div_three :
    ((vphi (π / 3)).smul 1).stretching - 1 / 28 * ((vphi (π / 3)).smul 1).palin = 0 := by
  obtain ⟨-, -, hD, hS⟩ := quantities_vphi_smul 1 (π / 3)
  rw [hD, hS, Real.cos_pi_div_three]
  norm_num

theorem neg_v_translate (x y z : ℝ) :
    (v.smul (-1)).u1 x y z = (vphi π).u1 (x + π) (y + π) (z + π) ∧
      (v.smul (-1)).u2 x y z = (vphi π).u2 (x + π) (y + π) (z + π) ∧
      (v.smul (-1)).u3 x y z = (vphi π).u3 (x + π) (y + π) (z + π) := by
  -- `sin (t + π) = -sin t`, `cos (t + π) = -cos t`, and `x + π + (y + π) + π ≡ x + y + π (mod 2π)`
  refine ⟨?_, ?_, ?_⟩ <;> simp only [Field.smul, v, vphi]
  · rw [sin_add_pi]; ring
  · rw [sin_add_pi]; ring
  · rw [show x + π + (y + π) + π = (x + y + π) + 2 * π by ring, cos_add_two_pi, cos_add_pi,
      cos_add_pi]
    ring

end Wyrd.PeriodicNS
