import Mathlib

/-!
# Ratios other than n:1

The Shared Air model's locking index looks for 2:1 and 3:1. Prenatal recordings
(van Leeuwen and colleagues) found brief 3:2, 5:3 and 4:3 epochs. Two exact facts
about what a harmonic index and the model's forcing can and cannot see.

**1. A harmonic index counts bands, not ratios.** Under perfect `n:m` locking
(`n` infant beats per `m` maternal cycles, `gcd(n, m) = 1`), mom's phase at
successive infant beats steps by `2π m/n`. Over one full locking cycle, the
`k`-th harmonic index `|⟨exp(i k ψⱼ)⟩|` is `1` if `n ∣ k` and `0` otherwise
(`lockIndex_eq_one`, `lockIndex_eq_zero`). So:

* no harmonic index can tell 3:2 from 3:1 (`three_two_looks_like_three_one`);
* 5:3 and 4:3 are invisible to the 2nd and 3rd harmonics (`five_three_hidden`,
  `four_three_hidden`);
* a perfect 2:1 lock has first-harmonic index 0 (`two_one_needs_second_harmonic`).

The ratio itself has to come from the beat rates, not from the index.

**2. First-order forcing through `sin θ` only produces n:1 tongues.** In the
model each maternal beat pushes each infant cell by `−ε P(ψ) sin θ`. To first
order in `ε` (standard averaging theory, not formalised here), locking near
`n:m` is decided by the average of the forcing along
the unperturbed `n:m` orbit `θ = n s + a`, `ψ = m s + b`. For **every**
continuous `2π`-periodic `P`, forcing through the `l`-th harmonic `sin(l θ)`
averages to zero unless `m ∣ l n` (`resonant_average_vanishes`). With the
model's `sin θ` (`l = 1`) and coprime `n, m > 1`, the average vanishes
(`model_forcing_misses_n_m`), while an n:1 average need not vanish
(`n_one_average`, shown for a test `P = cos(n ψ)`; for the model's own `P` it
needs the Fourier coefficient `e⁻² Iₙ(2) ≠ 0`, true but not formalised). A
first-order 3:2 tongue needs the second harmonic of the infant phase in the
coupling, and 5:3 the third (`second_harmonic_reaches_three_two`,
`third_harmonic_reaches_five_three`, again with test `P = cos 3ψ`, `cos 5ψ`).
Otherwise n:m locking is a higher-order effect in `ε`.

These are statements about the equations and an idealised, noise-free lock, not
about any recording.
-/

namespace Wyrd.Limits

open Complex Real

/-- The `k`-th harmonic locking index over one full `n:m` cycle. Mom's phase at the
`j`-th infant beat is `ψ₀ + 2π m j / n`. -/
noncomputable def lockIndex (k n m : ℕ) (ψ₀ : ℝ) : ℝ :=
  ‖(∑ j ∈ Finset.range n,
      Complex.exp ((((k : ℝ) * (ψ₀ + 2 * π * (m : ℝ) * (j : ℝ) / (n : ℝ)) : ℝ) : ℂ) * I)) /
    (n : ℂ)‖

private lemma lim_term (k n m : ℕ) (ψ₀ : ℝ) (j : ℕ) :
    Complex.exp ((((k : ℝ) * (ψ₀ + 2 * π * (m : ℝ) * (j : ℝ) / (n : ℝ)) : ℝ) : ℂ) * I) =
      Complex.exp (((k * ψ₀ : ℝ) : ℂ) * I) *
        Complex.exp (((2 * π * ((k * m : ℕ) : ℝ) / (n : ℝ) : ℝ) : ℂ) * I) ^ j := by
  rw [← Complex.exp_nat_mul, ← Complex.exp_add]
  congr 1
  push_cast
  ring

private lemma lim_geom_zero (p q : ℕ) (hq : 0 < q) (h : ¬ q ∣ p) :
    ∑ j ∈ Finset.range q,
      Complex.exp (((2 * π * (p : ℝ) / (q : ℝ) : ℝ) : ℂ) * I) ^ j = 0 := by
  have hqR : (q : ℝ) ≠ 0 := by positivity
  have hπ : π ≠ 0 := Real.pi_ne_zero
  have hζq : Complex.exp (((2 * π * (p : ℝ) / (q : ℝ) : ℝ) : ℂ) * I) ^ q = 1 := by
    rw [← Complex.exp_nat_mul]
    have hqC : (q : ℂ) ≠ 0 := by exact_mod_cast hqR
    have : ((q : ℂ) * (((2 * π * (p : ℝ) / (q : ℝ) : ℝ) : ℂ) * I)) =
        (p : ℂ) * (2 * π * I) := by
      push_cast
      field_simp
    rw [this, Complex.exp_nat_mul_two_pi_mul_I]
  have hζ1 : Complex.exp (((2 * π * (p : ℝ) / (q : ℝ) : ℝ) : ℂ) * I) ≠ 1 := by
    intro h1
    rw [Complex.exp_eq_one_iff] at h1
    obtain ⟨N, hN⟩ := h1
    have h3 : (((2 * π * (p : ℝ) / (q : ℝ) : ℝ) : ℂ)) * I = (((N : ℝ) * (2 * π) : ℝ) : ℂ) * I := by
      rw [hN]; push_cast; ring
    have h2 : (2 * π * (p : ℝ) / (q : ℝ)) = (N : ℝ) * (2 * π) :=
      Complex.ofReal_injective (mul_right_cancel₀ Complex.I_ne_zero h3)
    have h4 : (p : ℝ) = N * q := by
      calc (p : ℝ) = (2 * π * (p : ℝ) / (q : ℝ)) * q / (2 * π) := by field_simp
        _ = N * (2 * π) * q / (2 * π) := by rw [h2]
        _ = N * q := by field_simp
    have h5 : (p : ℤ) = N * q := by exact_mod_cast h4
    exact h (Int.natCast_dvd_natCast.mp ⟨N, by rw [h5]; ring⟩)
  rw [geom_sum_eq hζ1, hζq, sub_self, zero_div]

private lemma lim_sin_sum (θ : ℝ) (p q : ℕ) (hq : 0 < q) (h : ¬ q ∣ p) :
    ∑ j ∈ Finset.range q, Real.sin (θ + j * (2 * π * (p : ℝ) / (q : ℝ))) = 0 := by
  have e : ∀ j : ℕ, Real.sin (θ + j * (2 * π * (p : ℝ) / (q : ℝ))) =
      (Complex.exp ((θ : ℂ) * I) *
        Complex.exp (((2 * π * (p : ℝ) / (q : ℝ) : ℝ) : ℂ) * I) ^ j).im := by
    intro j
    rw [← Complex.exp_nat_mul, ← Complex.exp_add,
      show (θ : ℂ) * I + (j : ℂ) * (((2 * π * (p : ℝ) / (q : ℝ) : ℝ) : ℂ) * I) =
        ((θ + j * (2 * π * (p : ℝ) / (q : ℝ)) : ℝ) : ℂ) * I by push_cast; ring,
      Complex.exp_ofReal_mul_I_im]
  rw [Finset.sum_congr rfl (fun j _ => e j), ← Complex.im_sum, ← Finset.mul_sum,
    lim_geom_zero p q hq h, mul_zero, Complex.zero_im]

private lemma lim_sin_cos (c : ℕ) (hc : 0 < c) (A B : ℝ) :
    ∫ s in (0 : ℝ)..2 * π, Real.sin (c * s + A) * Real.cos (c * s + B) =
      π * Real.sin (A - B) := by
  have hcR : (c : ℝ) ≠ 0 := by positivity
  have key : ∀ x : ℝ, Real.sin (c * x + A) * Real.cos (c * x + B) =
      (Real.sin (2 * c * x + (A + B)) + Real.sin (A - B)) / 2 := by
    intro x
    have h1 := Real.sin_add (c * x + A) (c * x + B)
    have h2 := Real.sin_sub (c * x + A) (c * x + B)
    rw [show (c * x + A) + (c * x + B) = 2 * (c : ℝ) * x + (A + B) by ring] at h1
    rw [show (c * x + A) - (c * x + B) = A - B by ring] at h2
    rw [h1, h2]
    ring
  have hderiv : ∀ x ∈ Set.uIcc (0 : ℝ) (2 * π),
      HasDerivAt (fun x => -Real.cos (2 * c * x + (A + B)) / (4 * c) + x * Real.sin (A - B) / 2)
        (Real.sin (c * x + A) * Real.cos (c * x + B)) x := by
    intro x _
    rw [key x]
    have h1 : HasDerivAt (fun x : ℝ => 2 * (c : ℝ) * x + (A + B)) (2 * c) x := by
      simpa using ((hasDerivAt_id x).const_mul (2 * (c : ℝ))).add_const (A + B)
    have h2 := (h1.cos).neg.div_const (4 * (c : ℝ))
    have h3 := ((hasDerivAt_id x).mul_const (Real.sin (A - B))).div_const 2
    convert h2.add h3 using 1
    · funext y
      simp only [Pi.add_apply, Pi.neg_apply, id]
    · field_simp
      ring
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv
    (by apply Continuous.intervalIntegrable; fun_prop)]
  have : Real.cos (2 * c * (2 * π) + (A + B)) = Real.cos (A + B) := by
    rw [show 2 * (c : ℝ) * (2 * π) + (A + B) = (A + B) + ((2 * c : ℕ) : ℝ) * (2 * π) by
      push_cast; ring, Real.cos_add_nat_mul_two_pi]
  simp only [this, mul_zero, zero_add]
  field_simp
  ring

/-- If the number of bands divides the harmonic, the index is `1`. -/
theorem lockIndex_eq_one {k n m : ℕ} (hn : 0 < n) (h : n ∣ k) (ψ₀ : ℝ) :
    lockIndex k n m ψ₀ = 1 := by
  unfold lockIndex
  rw [Finset.sum_congr rfl (fun j _ => lim_term k n m ψ₀ j), ← Finset.mul_sum]
  obtain ⟨t, rfl⟩ := h
  have hnR : (n : ℝ) ≠ 0 := by positivity
  have hnC : (n : ℂ) ≠ 0 := by exact_mod_cast hnR
  have hζ : Complex.exp (((2 * π * ((n * t * m : ℕ) : ℝ) / (n : ℝ) : ℝ) : ℂ) * I) = 1 := by
    rw [show (((2 * π * ((n * t * m : ℕ) : ℝ) / (n : ℝ) : ℝ) : ℂ) * I) =
      ((t * m : ℕ) : ℂ) * (2 * π * I) by push_cast; field_simp]
    exact Complex.exp_nat_mul_two_pi_mul_I _
  rw [hζ]
  simp only [one_pow, Finset.sum_const, Finset.card_range, nsmul_eq_mul, mul_one]
  rw [mul_div_assoc, div_self hnC, mul_one, Complex.norm_exp_ofReal_mul_I]

/-- Otherwise (for coprime `n, m`) the index is exactly `0`. -/
theorem lockIndex_eq_zero {k n m : ℕ} (hn : 0 < n) (hcop : Nat.Coprime n m) (h : ¬ n ∣ k)
    (ψ₀ : ℝ) : lockIndex k n m ψ₀ = 0 := by
  unfold lockIndex
  rw [Finset.sum_congr rfl (fun j _ => lim_term k n m ψ₀ j), ← Finset.mul_sum,
    lim_geom_zero (k * m) n hn (fun hd => h (hcop.dvd_of_dvd_mul_right hd))]
  simp

/-- Every harmonic index reads a 3:2 lock exactly as it reads a 3:1 lock. -/
theorem three_two_looks_like_three_one (k : ℕ) (ψ₀ : ℝ) :
    lockIndex k 3 2 ψ₀ = lockIndex k 3 1 ψ₀ := by
  by_cases h : 3 ∣ k
  · rw [lockIndex_eq_one (by norm_num) h, lockIndex_eq_one (by norm_num) h]
  · rw [lockIndex_eq_zero (by norm_num) (by norm_num) h,
      lockIndex_eq_zero (by norm_num) (by norm_num) h]

/-- A perfect 5:3 lock is invisible to the 2nd and 3rd harmonics; the 5th sees it. -/
theorem five_three_hidden (ψ₀ : ℝ) :
    lockIndex 2 5 3 ψ₀ = 0 ∧ lockIndex 3 5 3 ψ₀ = 0 ∧ lockIndex 5 5 3 ψ₀ = 1 := by
  refine ⟨lockIndex_eq_zero (by norm_num) (by norm_num) (by norm_num) ψ₀,
    lockIndex_eq_zero (by norm_num) (by norm_num) (by norm_num) ψ₀,
    lockIndex_eq_one (by norm_num) (dvd_refl 5) ψ₀⟩

/-- A perfect 4:3 lock is invisible to the 2nd and 3rd harmonics; the 4th sees it. -/
theorem four_three_hidden (ψ₀ : ℝ) :
    lockIndex 2 4 3 ψ₀ = 0 ∧ lockIndex 3 4 3 ψ₀ = 0 ∧ lockIndex 4 4 3 ψ₀ = 1 := by
  refine ⟨lockIndex_eq_zero (by norm_num) (by norm_num) (by norm_num) ψ₀,
    lockIndex_eq_zero (by norm_num) (by norm_num) (by norm_num) ψ₀,
    lockIndex_eq_one (by norm_num) (dvd_refl 4) ψ₀⟩

/-- A perfect 2:1 lock has first-harmonic index `0` and second-harmonic index `1`. -/
theorem two_one_needs_second_harmonic (ψ₀ : ℝ) :
    lockIndex 1 2 1 ψ₀ = 0 ∧ lockIndex 2 2 1 ψ₀ = 1 := by
  refine ⟨lockIndex_eq_zero (by norm_num) (by norm_num) (by norm_num) ψ₀,
    lockIndex_eq_one (by norm_num) (dvd_refl 2) ψ₀⟩

/-- **First-order averages vanish off resonance**: for every continuous
`2π`-periodic `P`, forcing through `sin(l θ)` along the `n:m` orbit averages to
zero unless `m ∣ l n`. -/
theorem resonant_average_vanishes {P : ℝ → ℝ} (hP : Continuous P)
    (hper : Function.Periodic P (2 * π)) {l n m : ℕ} (hm : 0 < m) (h : ¬ m ∣ l * n)
    (a b : ℝ) :
    ∫ s in (0 : ℝ)..2 * π, Real.sin (l * (n * s + a)) * P (m * s + b) = 0 := by
  set F : ℝ → ℝ := fun s => Real.sin (l * (n * s + a)) * P (m * s + b) with hF
  have hFc : Continuous F := by
    simp only [hF]
    fun_prop
  have hFper : Function.Periodic F (2 * π) := by
    intro s
    simp only [hF]
    have e1 : (l : ℝ) * (n * (s + 2 * π) + a) =
        l * (n * s + a) + ((l * n : ℕ) : ℝ) * (2 * π) := by push_cast; ring
    have e2 : (m : ℝ) * (s + 2 * π) + b = (m * s + b) + (m : ℝ) * (2 * π) := by ring
    rw [e1, e2, Real.sin_add_nat_mul_two_pi, hper.nat_mul m]
  have hmR : (m : ℝ) ≠ 0 := by positivity
  have hshift : ∀ j : ℕ, ∫ s in (0 : ℝ)..2 * π, F (s + 2 * π * j / m) =
      ∫ s in (0 : ℝ)..2 * π, F s := by
    intro j
    rw [intervalIntegral.integral_comp_add_right, zero_add, add_comm (2 * π),
      hFper.intervalIntegral_add_eq _ 0, zero_add]
  have hpoint : ∀ s : ℝ, ∑ j ∈ Finset.range m, F (s + 2 * π * j / m) = 0 := by
    intro s
    have e : ∀ j : ℕ, F (s + 2 * π * j / m) =
        Real.sin (l * (n * s + a) + j * (2 * π * ((l * n : ℕ) : ℝ) / m)) * P (m * s + b) := by
      intro j
      simp only [hF]
      have e1 : (l : ℝ) * (n * (s + 2 * π * j / m) + a) =
          l * (n * s + a) + j * (2 * π * ((l * n : ℕ) : ℝ) / m) := by push_cast; ring
      have e2 : (m : ℝ) * (s + 2 * π * j / m) + b = (m * s + b) + (j : ℝ) * (2 * π) := by
        field_simp; ring
      rw [e1, e2, hper.nat_mul j]
    rw [Finset.sum_congr rfl (fun j _ => e j), ← Finset.sum_mul, lim_sin_sum _ _ _ hm h,
      zero_mul]
  have hint : ∀ j ∈ Finset.range m, IntervalIntegrable (fun s => F (s + 2 * π * j / m))
      MeasureTheory.volume 0 (2 * π) :=
    fun j _ => (hFc.comp (continuous_id.add continuous_const)).intervalIntegrable _ _
  have key : (m : ℝ) * ∫ s in (0 : ℝ)..2 * π, F s = 0 := by
    calc (m : ℝ) * ∫ s in (0 : ℝ)..2 * π, F s
        = ∑ j ∈ Finset.range m, ∫ s in (0 : ℝ)..2 * π, F (s + 2 * π * j / m) := by
          rw [Finset.sum_congr rfl (fun j _ => hshift j), Finset.sum_const, Finset.card_range,
            nsmul_eq_mul]
      _ = ∫ s in (0 : ℝ)..2 * π, ∑ j ∈ Finset.range m, F (s + 2 * π * j / m) :=
          (intervalIntegral.integral_finsetSum hint).symm
      _ = 0 := by simp [hpoint]
  exact (mul_eq_zero.mp key).resolve_left hmR

/-- The model's own forcing `P(ψ) = exp(2(cos ψ − 1)) − c` (any centring constant
`c`) through `sin θ` has zero first-order average along every `n:m` orbit with
coprime `n, m` and `m > 1`. -/
theorem model_forcing_misses_n_m {n m : ℕ} (hm : 1 < m) (hcop : Nat.Coprime n m)
    (c a b : ℝ) :
    ∫ s in (0 : ℝ)..2 * π,
      Real.sin (n * s + a) * (Real.exp (2 * (Real.cos (m * s + b) - 1)) - c) = 0 := by
  have hm0 : 0 < m := by omega
  have hnd : ¬ m ∣ 1 * n := by
    rw [one_mul]
    intro hd
    have h1 : m ∣ 1 := by
      have := Nat.dvd_gcd hd (dvd_refl m)
      rwa [Nat.Coprime.gcd_eq_one hcop] at this
    have := Nat.le_of_dvd one_pos h1
    omega
  have := resonant_average_vanishes (P := fun x => Real.exp (2 * (Real.cos x - 1)) - c)
    (by fun_prop) (by intro x; simp [Real.cos_add_two_pi]) hm0 hnd a b
  simpa using this

/-- An n:1 orbit picks up the `n`-th harmonic of `P`: here `P = cos(n ·)`. -/
theorem n_one_average {n : ℕ} (hn : 0 < n) (a b : ℝ) :
    ∫ s in (0 : ℝ)..2 * π, Real.sin (n * s + a) * Real.cos (n * (s + b)) =
      π * Real.sin (a - n * b) := by
  simp_rw [mul_add]
  exact lim_sin_cos n hn a (n * b)

/-- Coupling through `sin 2θ` reaches 3:2 at first order (with `P = cos 3ψ`). -/
theorem second_harmonic_reaches_three_two (a b : ℝ) :
    ∫ s in (0 : ℝ)..2 * π, Real.sin (2 * (3 * s + a)) * Real.cos (3 * (2 * s + b)) =
      π * Real.sin (2 * a - 3 * b) := by
  have e : ∀ s : ℝ, Real.sin (2 * (3 * s + a)) * Real.cos (3 * (2 * s + b)) =
      Real.sin (((6 : ℕ) : ℝ) * s + 2 * a) * Real.cos (((6 : ℕ) : ℝ) * s + 3 * b) := by
    intro s
    push_cast
    rw [show (2 : ℝ) * (3 * s + a) = 6 * s + 2 * a by ring,
      show (3 : ℝ) * (2 * s + b) = 6 * s + 3 * b by ring]
  rw [intervalIntegral.integral_congr (fun s _ => e s), lim_sin_cos 6 (by norm_num)]

/-- Coupling through `sin 3θ` reaches 5:3 at first order (with `P = cos 5ψ`). -/
theorem third_harmonic_reaches_five_three (a b : ℝ) :
    ∫ s in (0 : ℝ)..2 * π, Real.sin (3 * (5 * s + a)) * Real.cos (5 * (3 * s + b)) =
      π * Real.sin (3 * a - 5 * b) := by
  have e : ∀ s : ℝ, Real.sin (3 * (5 * s + a)) * Real.cos (5 * (3 * s + b)) =
      Real.sin (((15 : ℕ) : ℝ) * s + 3 * a) * Real.cos (((15 : ℕ) : ℝ) * s + 5 * b) := by
    intro s
    push_cast
    rw [show (3 : ℝ) * (5 * s + a) = 15 * s + 3 * a by ring,
      show (5 : ℝ) * (3 * s + b) = 15 * s + 5 * b by ring]
  rw [intervalIntegral.integral_congr (fun s _ => e s), lim_sin_cos 15 (by norm_num)]

end Wyrd.Limits
