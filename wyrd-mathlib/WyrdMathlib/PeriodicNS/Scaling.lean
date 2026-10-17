import WyrdMathlib.PeriodicNS.SignFlip

/-!
# Spatial rescaling: no universal power law with `2a + 4b < 3`

Rescale every spatial argument of `v` by an integer `k ≥ 1`:

  `v_k = (sin(k y), sin(k z), cos(k x) − cos(k x + k y))`.

It is divergence-free (`div_vScaled`); `2π`-periodicity and smoothness are clear
from the definition for integer `k` and are not stated separately. Each derivative brings a
factor `k`, and an average over the period cube is unchanged. So, exactly
(`quantities_vScaled`):

  `E = 1`,  `Z = 5k²/4`,  `D = 7k⁴/2`,  `S = k³/4`.

For any real exponents `a, b`,

  `S / (Z^a D^b) = (1/4) / ((5/4)^a (7/2)^b) · k^(3 − 2a − 4b)` (`ratio_vScaled`).

**Consequence** (`no_power_law_bound`). Fix the energy `E = 1`, the viscosity
and the domain. No inequality `S ≤ C Z^a D^b` with `2a + 4b < 3` holds for all
smooth periodic divergence-free fields, whatever the constant `C`. In
particular `S ≤ C Z^0.75 D^0.2` fails (`fitted_law_fails`): the ratio grows like
`k^0.7`. A law fitted to particular trajectories may still describe them; it
cannot be a universal estimate. The classical estimate `S ≤ c Z^{3/4} D^{3/4}`
(Calderón–Zygmund plus Gagliardo–Nirenberg; standard, not formalised here) has
`2a + 4b = 9/2 ≥ 3` and is not contradicted by this family.

Suggested by ChatGPT as a test of a fitted exponent law; proved here.
-/

namespace Wyrd.PeriodicNS

open Real

/-- `v` with every spatial argument multiplied by `k`. -/
noncomputable def vScaled (k : ℕ) : Field :=
  ⟨fun _ y _ => sin (k * y), fun _ _ z => sin (k * z),
   fun x y _ => cos (k * x) - cos (k * x + k * y)⟩

theorem vScaled_one : vScaled 1 = v := by
  simp [vScaled, v]

theorem div_vScaled (k : ℕ) (x y z : ℝ) : (vScaled k).div x y z = 0 := by
  -- every component is independent of its own coordinate
  simp [Field.div, dx, dy, dz, vScaled]

/-! ### Helpers: the derivatives of `v_k` (each brings a factor `k`) -/

/-- The vorticity of `v_k`. -/
private lemma Scaling_curl (k : ℕ) :
    (vScaled k).curl.u1 = (fun x y z => k * sin (k * x + k * y) - k * cos (k * z)) ∧
      (vScaled k).curl.u2 = (fun x y _ => k * sin (k * x) - k * sin (k * x + k * y)) ∧
      (vScaled k).curl.u3 = (fun _ y _ => -(k * cos (k * y))) := by
  refine ⟨?_, ?_, ?_⟩ <;> funext x y z <;>
    simp (disch := fun_prop) [Field.curl, dx, dy, dz, vScaled] <;> ring

/-- The velocity gradient entries of `v_k`. -/
private lemma Scaling_grad (k : ℕ) :
    dx (vScaled k).u1 = (fun _ _ _ => 0) ∧ dy (vScaled k).u1 = (fun _ y _ => k * cos (k * y)) ∧
      dz (vScaled k).u1 = (fun _ _ _ => 0) ∧
    dx (vScaled k).u2 = (fun _ _ _ => 0) ∧ dy (vScaled k).u2 = (fun _ _ _ => 0) ∧
      dz (vScaled k).u2 = (fun _ _ z => k * cos (k * z)) ∧
    dx (vScaled k).u3 = (fun x y _ => -(k * sin (k * x)) + k * sin (k * x + k * y)) ∧
      dy (vScaled k).u3 = (fun x y _ => k * sin (k * x + k * y)) ∧
      dz (vScaled k).u3 = (fun _ _ _ => 0) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> funext x y z <;>
    simp (disch := fun_prop) [dx, dy, dz, vScaled] <;> ring

/-- The vorticity gradient entries of `v_k`. -/
private lemma Scaling_grad_curl (k : ℕ) :
    dx (vScaled k).curl.u1 = (fun x y _ => k ^ 2 * cos (k * x + k * y)) ∧
      dy (vScaled k).curl.u1 = (fun x y _ => k ^ 2 * cos (k * x + k * y)) ∧
      dz (vScaled k).curl.u1 = (fun _ _ z => k ^ 2 * sin (k * z)) ∧
    dx (vScaled k).curl.u2 = (fun x y _ => k ^ 2 * cos (k * x) - k ^ 2 * cos (k * x + k * y)) ∧
      dy (vScaled k).curl.u2 = (fun x y _ => -(k ^ 2 * cos (k * x + k * y))) ∧
      dz (vScaled k).curl.u2 = (fun _ _ _ => 0) ∧
    dx (vScaled k).curl.u3 = (fun _ _ _ => 0) ∧
      dy (vScaled k).curl.u3 = (fun _ y _ => k ^ 2 * sin (k * y)) ∧
      dz (vScaled k).curl.u3 = (fun _ _ _ => 0) := by
  obtain ⟨c1, c2, c3⟩ := Scaling_curl k
  rw [c1, c2, c3]
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> funext x y z <;>
    simp (disch := fun_prop) [dx, dy, dz] <;> ring

/-! ### Helpers: triple integrals of trigonometric polynomials -/

/-- The unnormalised iterated integral over `[0, 2π]³` (so `avg f = Scaling_I3 f / (2π)³`). -/
private noncomputable def Scaling_I3 (f : ℝ → ℝ → ℝ → ℝ) : ℝ :=
  ∫ x in (0 : ℝ)..2 * π, ∫ y in (0 : ℝ)..2 * π, ∫ z in (0 : ℝ)..2 * π, f x y z

/-- Additivity of the iterated integral on jointly continuous integrands: each partial
integral is continuous in the remaining variables (parametric integrals), hence integrable. -/
private lemma Scaling_I3_add {f g : ℝ → ℝ → ℝ → ℝ}
    (hf : Continuous fun p : ℝ × ℝ × ℝ => f p.1 p.2.1 p.2.2)
    (hg : Continuous fun p : ℝ × ℝ × ℝ => g p.1 p.2.1 p.2.2) :
    Scaling_I3 (fun x y z => f x y z + g x y z) = Scaling_I3 f + Scaling_I3 g := by
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
  unfold Scaling_I3
  simp only [e1, e2]
  exact intervalIntegral.integral_add (cx f hf) (cx g hg)

/-- One-dimensional orthogonality: `∫₀^{2π} cos(d + n t) dt` vanishes for `n ≠ 0`
(antiderivative `sin(d + n t)/n` is `2π`-periodic). -/
private lemma Scaling_int_cos (n : ℤ) (d : ℝ) :
    ∫ t in (0 : ℝ)..2 * π, cos (d + n * t) = if n = 0 then 2 * π * cos d else 0 := by
  split_ifs with h
  · subst h; simp
  · have hn : (n : ℝ) ≠ 0 := Int.cast_ne_zero.mpr h
    have := intervalIntegral.integral_comp_add_mul (a := 0) (b := 2 * π) cos hn d
    rw [this, integral_cos]
    simp [sin_add_int_mul_two_pi]

private lemma Scaling_int_sin (n : ℤ) (d : ℝ) :
    ∫ t in (0 : ℝ)..2 * π, sin (d + n * t) = if n = 0 then 2 * π * sin d else 0 := by
  split_ifs with h
  · subst h; simp
  · have hn : (n : ℝ) ≠ 0 := Int.cast_ne_zero.mpr h
    have := intervalIntegral.integral_comp_add_mul (a := 0) (b := 2 * π) sin hn d
    rw [this, integral_sin]
    simp [cos_add_int_mul_two_pi]

/-- Triple orthogonality: integrate out `z`, then `y`, then `x`; a nonzero frequency kills the
integral at the first level where it appears. -/
private lemma Scaling_I3_cos (p q r : ℤ) :
    Scaling_I3 (fun x y z => cos (p * x + q * y + r * z)) =
      if (p, q, r) = (0, 0, 0) then (2 * π) ^ 3 else 0 := by
  unfold Scaling_I3
  simp only [Scaling_int_cos]
  by_cases hr : r = 0
  · subst hr
    simp only [ite_true, intervalIntegral.integral_const_mul, Scaling_int_cos]
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

private lemma Scaling_I3_sin (p q r : ℤ) :
    Scaling_I3 (fun x y z => sin (p * x + q * y + r * z)) = 0 := by
  unfold Scaling_I3
  simp only [Scaling_int_sin]
  by_cases hr : r = 0
  · subst hr
    simp only [ite_true, intervalIntegral.integral_const_mul, Scaling_int_sin]
    by_cases hq : q = 0
    · subst hq
      by_cases hp : p = 0
      · subst hp; simp
      · simp [hp]
    · simp [hq]
  · simp [hr]

/-- One Fourier mode `a cos(k·x) + b sin(k·x)` with `m = (a, b, k)`, `k ∈ ℤ³`. -/
private noncomputable def Scaling_tm (m : ℝ × ℝ × ℤ × ℤ × ℤ) (x y z : ℝ) : ℝ :=
  m.1 * cos (m.2.2.1 * x + m.2.2.2.1 * y + m.2.2.2.2 * z) +
    m.2.1 * sin (m.2.2.1 * x + m.2.2.2.1 * y + m.2.2.2.2 * z)

/-- A trigonometric polynomial: a finite list of modes. -/
private noncomputable def Scaling_tp (L : List (ℝ × ℝ × ℤ × ℤ × ℤ)) (x y z : ℝ) : ℝ :=
  (L.map fun m => Scaling_tm m x y z).sum

/-- Its constant Fourier coefficient. -/
private noncomputable def Scaling_c0 (L : List (ℝ × ℝ × ℤ × ℤ × ℤ)) : ℝ :=
  (L.map fun m => if m.2.2 = (0, 0, 0) then m.1 else 0).sum

private lemma Scaling_tm_cont (m : ℝ × ℝ × ℤ × ℤ × ℤ) :
    Continuous fun p : ℝ × ℝ × ℝ => Scaling_tm m p.1 p.2.1 p.2.2 := by
  unfold Scaling_tm; fun_prop

private lemma Scaling_tp_cont (L : List (ℝ × ℝ × ℤ × ℤ × ℤ)) :
    Continuous fun p : ℝ × ℝ × ℝ => Scaling_tp L p.1 p.2.1 p.2.2 := by
  induction L with
  | nil => simp only [Scaling_tp, List.map_nil, List.sum_nil]; exact continuous_const
  | cons m L ih =>
    simp only [Scaling_tp, List.map_cons, List.sum_cons] at ih ⊢
    exact (Scaling_tm_cont m).add ih

private lemma Scaling_I3_tm (m : ℝ × ℝ × ℤ × ℤ × ℤ) :
    Scaling_I3 (Scaling_tm m) = (2 * π) ^ 3 * (if m.2.2 = (0, 0, 0) then m.1 else 0) := by
  obtain ⟨a, b, p, q, r⟩ := m
  have hc : Continuous fun w : ℝ × ℝ × ℝ => a * cos (p * w.1 + q * w.2.1 + r * w.2.2) := by
    fun_prop
  have hs : Continuous fun w : ℝ × ℝ × ℝ => b * sin (p * w.1 + q * w.2.1 + r * w.2.2) := by
    fun_prop
  have e := Scaling_I3_add (f := fun x y z => a * cos (p * x + q * y + r * z))
    (g := fun x y z => b * sin (p * x + q * y + r * z)) hc hs
  unfold Scaling_tm
  simp only
  rw [e]
  have ec : Scaling_I3 (fun x y z => a * cos (p * x + q * y + r * z)) =
      a * Scaling_I3 (fun x y z => cos (p * x + q * y + r * z)) := by
    simp only [Scaling_I3, intervalIntegral.integral_const_mul]
  have es : Scaling_I3 (fun x y z => b * sin (p * x + q * y + r * z)) =
      b * Scaling_I3 (fun x y z => sin (p * x + q * y + r * z)) := by
    simp only [Scaling_I3, intervalIntegral.integral_const_mul]
  rw [ec, es, Scaling_I3_cos, Scaling_I3_sin]
  split_ifs <;> ring

/-- The integral of a trigonometric polynomial is `(2π)³` times its constant coefficient. -/
private lemma Scaling_I3_tp (L : List (ℝ × ℝ × ℤ × ℤ × ℤ)) :
    Scaling_I3 (Scaling_tp L) = (2 * π) ^ 3 * Scaling_c0 L := by
  induction L with
  | nil => simp [Scaling_I3, Scaling_tp, Scaling_c0]
  | cons m L ih =>
    have e := Scaling_I3_add (Scaling_tm_cont m) (Scaling_tp_cont L)
    have hfun : Scaling_tp (m :: L) = fun x y z => Scaling_tm m x y z + Scaling_tp L x y z := by
      funext x y z; simp only [Scaling_tp, List.map_cons, List.sum_cons]
    rw [hfun, e, ih, Scaling_I3_tm]
    simp only [Scaling_c0, List.map_cons, List.sum_cons]
    ring

/-- The average of a function that agrees pointwise with a trigonometric polynomial is its
constant coefficient. -/
private lemma Scaling_avg_eq {f : ℝ → ℝ → ℝ → ℝ} (L : List (ℝ × ℝ × ℤ × ℤ × ℤ))
    (h : ∀ x y z, f x y z = Scaling_tp L x y z) : avg f = Scaling_c0 L := by
  have hf : f = Scaling_tp L := by funext x y z; exact h x y z
  have hpi : (2 * π) ^ 3 ≠ 0 := pow_ne_zero _ (by positivity)
  rw [avg, hf]
  change Scaling_I3 (Scaling_tp L) / _ = _
  rw [Scaling_I3_tp]
  field_simp

/-- Reduction of `sin³` modulo `sin² + cos² = 1`, used to normalise polynomial identities. -/
private lemma Scaling_sin_cube (t : ℝ) : sin t ^ 3 = sin t - sin t * cos t ^ 2 := by
  have := sin_sq_add_cos_sq t
  linear_combination sin t * this

/-! ### Helpers: modes with wave vectors multiplied by `k` -/

/-- A mode with its coefficients multiplied by `c` and its wave vector by `k`. -/
private noncomputable def Scaling_sc (k : ℕ) (c : ℝ) (m : ℝ × ℝ × ℤ × ℤ × ℤ) :
    ℝ × ℝ × ℤ × ℤ × ℤ :=
  (c * m.1, c * m.2.1, (k : ℤ) * m.2.2.1, (k : ℤ) * m.2.2.2.1, (k : ℤ) * m.2.2.2.2)

private lemma Scaling_tm_sc (k : ℕ) (c : ℝ) (m : ℝ × ℝ × ℤ × ℤ × ℤ) (x y z : ℝ) :
    Scaling_tm (Scaling_sc k c m) x y z = c * Scaling_tm m (k * x) (k * y) (k * z) := by
  obtain ⟨a, b, p, q, r⟩ := m
  simp only [Scaling_tm, Scaling_sc]
  push_cast
  rw [show (k : ℝ) * p * x + k * q * y + k * r * z = p * (k * x) + q * (k * y) + r * (k * z) by
    ring]
  ring

private lemma Scaling_tp_sc (k : ℕ) (c : ℝ) (L : List (ℝ × ℝ × ℤ × ℤ × ℤ)) (x y z : ℝ) :
    Scaling_tp (L.map (Scaling_sc k c)) x y z = c * Scaling_tp L (k * x) (k * y) (k * z) := by
  induction L with
  | nil => simp [Scaling_tp]
  | cons m L ih =>
    simp only [Scaling_tp, List.map_cons, List.map_map, List.sum_cons] at ih ⊢
    rw [Function.comp_def] at ih ⊢
    rw [ih, Scaling_tm_sc]
    ring

private lemma Scaling_c0_sc {k : ℕ} (hk : 0 < k) (c : ℝ) (L : List (ℝ × ℝ × ℤ × ℤ × ℤ)) :
    Scaling_c0 (L.map (Scaling_sc k c)) = c * Scaling_c0 L := by
  induction L with
  | nil => simp [Scaling_c0]
  | cons m L ih =>
    simp only [Scaling_c0, List.map_cons, List.map_map, List.sum_cons] at ih ⊢
    rw [Function.comp_def] at ih ⊢
    rw [ih]
    obtain ⟨a, b, p, q, r⟩ := m
    have hk' : (k : ℤ) ≠ 0 := by exact_mod_cast hk.ne'
    simp only [Scaling_sc, Prod.mk.injEq, mul_eq_zero, hk', false_or]
    split_ifs <;> ring

/-- The average of `f(x, y, z) = c · P(kx, ky, kz)` for a trigonometric polynomial `P` and an
integer `k ≥ 1` is `c` times the constant coefficient of `P`. -/
private lemma Scaling_avg_eq_scaled {f : ℝ → ℝ → ℝ → ℝ} {k : ℕ} (hk : 0 < k) (c : ℝ)
    (L : List (ℝ × ℝ × ℤ × ℤ × ℤ))
    (h : ∀ x y z, f x y z = c * Scaling_tp L (k * x) (k * y) (k * z)) :
    avg f = c * Scaling_c0 L := by
  rw [Scaling_avg_eq (L.map (Scaling_sc k c)) (fun x y z => by rw [h, Scaling_tp_sc]),
    Scaling_c0_sc hk]

theorem quantities_vScaled {k : ℕ} (hk : 0 < k) :
    (vScaled k).energy = 1 ∧ (vScaled k).enstrophy = 5 * (k : ℝ) ^ 2 / 4 ∧
      (vScaled k).palin = 7 * (k : ℝ) ^ 4 / 2 ∧ (vScaled k).stretching = (k : ℝ) ^ 3 / 4 := by
  obtain ⟨c1, c2, c3⟩ := Scaling_curl k
  obtain ⟨g1, g2, g3, g4, g5, g6, g7, g8, g9⟩ := Scaling_grad k
  obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9⟩ := Scaling_grad_curl k
  refine ⟨?_, ?_, ?_, ?_⟩
  -- Each integrand equals `k^j · P(kx, ky, kz)`, with `P` the trigonometric polynomial used for
  -- `v` in `Averages.lean` and `j` the number of derivatives; its average is `k^j` times the
  -- constant coefficient of `P` (`Scaling_avg_eq_scaled`). The pointwise identity is the one for
  -- `v` at `(X, Y, Z) = (kx, ky, kz)`, with the extra factors of `k` carried along.
  · unfold Field.energy
    rw [Scaling_avg_eq_scaled hk 1
      [(2, 0, 0, 0, 0), (-1/2, 0, 0, 0, 2), (-1, 0, 0, 1, 0), (-1/2, 0, 0, 2, 0),
      (1/2, 0, 2, 0, 0), (-1, 0, 2, 1, 0), (1/2, 0, 2, 2, 0)]]
    · norm_num [Scaling_c0]
    · intro x y z
      simp only [vScaled, Scaling_tp, Scaling_tm, List.map_cons, List.map_nil, List.sum_cons,
        List.sum_nil]
      push_cast
      generalize (k : ℝ) * x = X
      generalize (k : ℝ) * y = Y
      generalize (k : ℝ) * z = Z
      simp only [zero_mul, mul_zero, add_zero, zero_add, one_mul, neg_mul, Real.cos_add,
        Real.sin_add, Real.cos_two_mul, Real.sin_two_mul, Real.cos_zero, Real.sin_zero]
      ring_nf
      simp only [Real.sin_sq]
      ring_nf
  · unfold Field.enstrophy Field.energy
    rw [Scaling_avg_eq_scaled hk ((k : ℝ) ^ 2)
      [(5/2, 0, 0, 0, 0), (1/2, 0, 0, 0, 2), (-1, 0, 0, 1, 0), (1/2, 0, 0, 2, 0),
      (0, -1, 1, 1, -1), (0, -1, 1, 1, 1), (-1/2, 0, 2, 0, 0), (1, 0, 2, 1, 0), (-1, 0, 2, 2, 0)]]
    · norm_num [Scaling_c0]
      ring
    · intro x y z
      simp only [c1, c2, c3, Scaling_tp, Scaling_tm, List.map_cons, List.map_nil, List.sum_cons,
        List.sum_nil]
      push_cast
      generalize (k : ℝ) * x = X
      generalize (k : ℝ) * y = Y
      generalize (k : ℝ) * z = Z
      simp only [zero_mul, mul_zero, add_zero, zero_add, one_mul, neg_mul, Real.cos_add,
        Real.sin_add, Real.cos_neg, Real.sin_neg, Real.cos_two_mul, Real.sin_two_mul,
        Real.cos_zero, Real.sin_zero]
      ring_nf
      simp only [Real.sin_sq]
      ring_nf
  · unfold Field.palin Field.gradSq
    rw [Scaling_avg_eq_scaled hk ((k : ℝ) ^ 4)
      [(7/2, 0, 0, 0, 0), (-1/2, 0, 0, 0, 2), (-1, 0, 0, 1, 0), (-1/2, 0, 0, 2, 0),
      (1/2, 0, 2, 0, 0), (-1, 0, 2, 1, 0), (2, 0, 2, 2, 0)]]
    · norm_num [Scaling_c0]
      ring
    · intro x y z
      simp only [h1, h2, h3, h4, h5, h6, h7, h8, h9, Scaling_tp, Scaling_tm, List.map_cons,
        List.map_nil, List.sum_cons, List.sum_nil]
      push_cast
      generalize (k : ℝ) * x = X
      generalize (k : ℝ) * y = Y
      generalize (k : ℝ) * z = Z
      simp only [zero_mul, mul_zero, add_zero, zero_add, one_mul, neg_mul, Real.cos_add,
        Real.sin_add, Real.cos_two_mul, Real.sin_two_mul, Real.cos_zero, Real.sin_zero]
      ring_nf
      simp only [Real.sin_sq]
      ring_nf
  · unfold Field.stretching
    rw [Scaling_avg_eq_scaled hk ((k : ℝ) ^ 3)
      [(1/4, 0, 0, 0, 0), (-1/2, 0, 0, 1, 0), (1/4, 0, 0, 2, 0),
      (0, -3/4, 1, -1, -1), (0, -3/4, 1, -1, 1), (0, 3/4, 1, 0, -1), (0, 3/4, 1, 0, 1),
      (0, -3/4, 1, 1, -1), (0, -3/4, 1, 1, 1), (0, 3/4, 1, 2, -1), (0, 3/4, 1, 2, 1),
      (-1/4, 0, 2, 0, 0), (1/4, 0, 2, 1, 0), (-1/4, 0, 2, 2, 0), (1/4, 0, 2, 3, 0)]]
    · norm_num [Scaling_c0]
      ring
    · intro x y z
      simp only [c1, c2, c3, g1, g2, g3, g4, g5, g6, g7, g8, g9,
        Scaling_tp, Scaling_tm, List.map_cons, List.map_nil, List.sum_cons, List.sum_nil]
      push_cast
      generalize (k : ℝ) * x = X
      generalize (k : ℝ) * y = Y
      generalize (k : ℝ) * z = Z
      simp only [zero_mul, mul_zero, add_zero, zero_add, one_mul, neg_mul, Real.cos_add,
        Real.sin_add, Real.cos_neg, Real.sin_neg, Real.cos_two_mul, Real.sin_two_mul,
        Real.cos_three_mul, Real.sin_three_mul, Real.cos_zero, Real.sin_zero]
      ring_nf
      simp only [Real.sin_sq, Scaling_sin_cube]
      ring_nf

theorem ratio_vScaled {k : ℕ} (hk : 0 < k) (a b : ℝ) :
    (vScaled k).stretching / ((vScaled k).enstrophy ^ a * (vScaled k).palin ^ b) =
      1 / 4 / ((5 / 4 : ℝ) ^ a * (7 / 2 : ℝ) ^ b) * (k : ℝ) ^ (3 - 2 * a - 4 * b) := by
  obtain ⟨-, hZ, hD, hS⟩ := quantities_vScaled hk
  have hk' : (0 : ℝ) < k := by exact_mod_cast hk
  -- `(c kⁿ)^a = c^a k^(n a)` for `c, k > 0`
  have eZ : (5 * (k : ℝ) ^ 2 / 4) ^ a = (5 / 4 : ℝ) ^ a * (k : ℝ) ^ (2 * a) := by
    rw [show 5 * (k : ℝ) ^ 2 / 4 = 5 / 4 * (k : ℝ) ^ 2 by ring,
      Real.mul_rpow (by norm_num) (by positivity),
      show (2 : ℝ) * a = ((2 : ℕ) : ℝ) * a by norm_num, Real.rpow_natCast_mul hk'.le]
  have eD : (7 * (k : ℝ) ^ 4 / 2) ^ b = (7 / 2 : ℝ) ^ b * (k : ℝ) ^ (4 * b) := by
    rw [show 7 * (k : ℝ) ^ 4 / 2 = 7 / 2 * (k : ℝ) ^ 4 by ring,
      Real.mul_rpow (by norm_num) (by positivity),
      show (4 : ℝ) * b = ((4 : ℕ) : ℝ) * b by norm_num, Real.rpow_natCast_mul hk'.le]
  -- `k^(3 − 2a − 4b) = k³ / k^(2a) / k^(4b)`
  have eK : (k : ℝ) ^ (3 - 2 * a - 4 * b) = (k : ℝ) ^ 3 / (k : ℝ) ^ (2 * a) / (k : ℝ) ^ (4 * b) := by
    rw [Real.rpow_sub hk', Real.rpow_sub hk', show (3 : ℝ) = ((3 : ℕ) : ℝ) by norm_num,
      Real.rpow_natCast]
  rw [hS, hZ, hD, eZ, eD, eK]
  have h1 : (0 : ℝ) < (5 / 4 : ℝ) ^ a := Real.rpow_pos_of_pos (by norm_num) a
  have h2 : (0 : ℝ) < (7 / 2 : ℝ) ^ b := Real.rpow_pos_of_pos (by norm_num) b
  have h3 : (0 : ℝ) < (k : ℝ) ^ (2 * a) := Real.rpow_pos_of_pos hk' _
  have h4 : (0 : ℝ) < (k : ℝ) ^ (4 * b) := Real.rpow_pos_of_pos hk' _
  field_simp

theorem no_power_law_bound {a b : ℝ} (hab : 2 * a + 4 * b < 3) (C : ℝ) :
    ∃ k : ℕ, 0 < k ∧
      C * ((vScaled k).enstrophy ^ a * (vScaled k).palin ^ b) < (vScaled k).stretching := by
  set K : ℝ := 1 / 4 / ((5 / 4 : ℝ) ^ a * (7 / 2 : ℝ) ^ b) with hKdef
  have hK : 0 < K := by
    have h1 : (0 : ℝ) < (5 / 4 : ℝ) ^ a := Real.rpow_pos_of_pos (by norm_num) a
    have h2 : (0 : ℝ) < (7 / 2 : ℝ) ^ b := Real.rpow_pos_of_pos (by norm_num) b
    positivity
  -- `k^(3 − 2a − 4b) → ∞` along the positive integers
  have he : 0 < 3 - 2 * a - 4 * b := by linarith
  have ht : Filter.Tendsto (fun n : ℕ => (n : ℝ) ^ (3 - 2 * a - 4 * b)) Filter.atTop
      Filter.atTop := (tendsto_rpow_atTop he).comp tendsto_natCast_atTop_atTop
  obtain ⟨k, hk0, hkC⟩ :=
    ((Filter.eventually_gt_atTop 0).and (ht.eventually_gt_atTop (C / K))).exists
  refine ⟨k, hk0, ?_⟩
  obtain ⟨-, hZ, hD, -⟩ := quantities_vScaled hk0
  have hk' : (0 : ℝ) < k := by exact_mod_cast hk0
  have hP : 0 < (vScaled k).enstrophy ^ a * (vScaled k).palin ^ b := by
    rw [hZ, hD]
    exact mul_pos (Real.rpow_pos_of_pos (by positivity) a) (Real.rpow_pos_of_pos (by positivity) b)
  rw [← lt_div_iff₀ hP, ratio_vScaled hk0, ← hKdef]
  rw [div_lt_iff₀ hK] at hkC
  linarith

theorem fitted_law_fails (C : ℝ) :
    ∃ k : ℕ, 0 < k ∧
      C * ((vScaled k).enstrophy ^ (0.75 : ℝ) * (vScaled k).palin ^ (0.2 : ℝ)) <
        (vScaled k).stretching := by
  -- `2 · 0.75 + 4 · 0.2 = 2.3 < 3`
  exact no_power_law_bound (by norm_num) C

end Wyrd.PeriodicNS
