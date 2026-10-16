import Mathlib

/-!
# Same synchrony, different future: phase moments do not close

For `m` identical phase oscillators with mean-field coupling, in the frame
rotating at the common frequency, `θⱼ' = K · Im(Z₁ e^{−iθⱼ}) = K r sin(ψ − θⱼ)`,
where `Z₁ = r e^{iψ} = (1/m) Σ e^{iθⱼ}`. Then exactly

  `Z₁' = (K/2) (Z₁ − conj(Z₁) Z₂)`,  `Z₂ = (1/m) Σ e^{2iθⱼ}`.

So `Z₁`'s future depends on `Z₂`. Two four-cell configurations with the same
`Z₁ = 1/2` (same synchrony `R = 1/2`) have `Z₁' = K/4` and `Z₁' = 0`. Repeating
each six times gives 24 cells, the model's pacemaker count.
-/

namespace Wyrd.SharedAir

open Complex

/-- First phase moment. -/
noncomputable def Z1 {m : ℕ} (θ : Fin m → ℝ) : ℂ := (∑ j, exp (θ j * I)) / m

/-- Second phase moment. -/
noncomputable def Z2 {m : ℕ} (θ : Fin m → ℝ) : ℂ := (∑ j, exp (2 * θ j * I)) / m

/-- Mean-field velocity in the rotating frame. -/
noncomputable def vel (K : ℝ) {m : ℕ} (θ : Fin m → ℝ) (j : Fin m) : ℝ :=
  K * (Z1 θ * exp (-(θ j * I))).im

/-- It is the Kuramoto form `K r sin(ψ − θⱼ)` when `Z₁ = r e^{iψ}`. -/
theorem vel_eq_sin (K : ℝ) {m : ℕ} (θ : Fin m → ℝ) (j : Fin m) {r ψ : ℝ}
    (hZ : Z1 θ = r * exp (ψ * I)) : vel K θ j = K * r * Real.sin (ψ - θ j) := by
  unfold vel
  -- `r e^{iψ} e^{-iθⱼ} = r e^{i(ψ - θⱼ)}`, whose imaginary part is `r sin(ψ - θⱼ)`
  have h : (ψ : ℂ) * I + -(θ j * I) = ((ψ - θ j : ℝ) : ℂ) * I := by push_cast; ring
  rw [hZ, mul_assoc, ← Complex.exp_add, h, Complex.im_ofReal_mul, Complex.exp_ofReal_mul_I_im]
  ring

/-- The rate of change of `Z₁` implied by the velocities. -/
noncomputable def Z1dot (K : ℝ) {m : ℕ} (θ : Fin m → ℝ) : ℂ :=
  (∑ j, I * vel K θ j * exp (θ j * I)) / m

/-- `Z1dot` really is the time derivative of `Z₁` along a trajectory. -/
theorem hasDerivAt_Z1 {m : ℕ} {θ : ℝ → Fin m → ℝ} {θ' : Fin m → ℝ} {t : ℝ}
    (h : ∀ j, HasDerivAt (fun s => θ s j) (θ' j) t) :
    HasDerivAt (fun s => Z1 (θ s)) ((∑ j, I * θ' j * exp (θ t j * I)) / m) t := by
  -- each term: `d/ds exp(θⱼ(s) i) = exp(θⱼ i) · (θ'ⱼ i)`
  have hj : ∀ j ∈ (Finset.univ : Finset (Fin m)),
      HasDerivAt (fun s => exp ((θ s j : ℂ) * I)) (exp ((θ t j : ℂ) * I) * ((θ' j : ℂ) * I)) t :=
    fun j _ => (((h j).ofReal_comp).mul_const I).cexp
  -- sum the terms, then divide by `m`
  have hs := (HasDerivAt.sum hj).div_const (m : ℂ)
  unfold Z1
  convert hs using 2
  · simp
  · refine Finset.sum_congr rfl fun j _ => ?_
    ring

/-- **The moment identity**: `Z₁' = (K/2)(Z₁ − conj(Z₁) Z₂)`. -/
theorem Z1dot_eq (K : ℝ) {m : ℕ} (θ : Fin m → ℝ) :
    Z1dot K θ = K / 2 * (Z1 θ - starRingEnd ℂ (Z1 θ) * Z2 θ) := by
  -- `m = 0`: every moment is `0 / 0 = 0`
  rcases Nat.eq_zero_or_pos m with rfl | hm
  · simp [Z1dot, Z1, Z2]
  -- per-cell identity: `i vⱼ e^{iθⱼ} = (K/2)(Z₁ − conj(Z₁) e^{2iθⱼ})`,
  -- using `Im w = (w − conj w)/(2i)` with `w = Z₁ e^{−iθⱼ}`
  have key : ∀ j, I * (vel K θ j : ℂ) * exp (θ j * I)
      = K / 2 * (Z1 θ - starRingEnd ℂ (Z1 θ) * exp (2 * θ j * I)) := by
    intro j
    have hc : starRingEnd ℂ (exp (-((θ j : ℂ) * I))) = exp ((θ j : ℂ) * I) := by
      rw [← Complex.exp_conj]; simp
    have hneg : exp (-((θ j : ℂ) * I)) = (exp ((θ j : ℂ) * I))⁻¹ := Complex.exp_neg _
    have h2 : exp (2 * (θ j : ℂ) * I) = exp ((θ j : ℂ) * I) * exp ((θ j : ℂ) * I) := by
      rw [← Complex.exp_add]; ring_nf
    have he : exp ((θ j : ℂ) * I) ≠ 0 := Complex.exp_ne_zero _
    unfold vel
    push_cast
    rw [Complex.im_eq_sub_conj, map_mul, hc, hneg, h2]
    field_simp
  have hm' : (m : ℂ) ≠ 0 := by exact_mod_cast hm.ne'
  unfold Z1dot
  simp_rw [key]
  -- sum: `Σ (K/2)(Z₁ − conj(Z₁) e^{2iθⱼ}) = (K/2)(m Z₁ − conj(Z₁) Σ e^{2iθⱼ})`
  rw [← Finset.mul_sum, Finset.sum_sub_distrib, ← Finset.mul_sum, Finset.sum_const,
    Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  unfold Z2
  generalize (∑ j, exp (2 * (θ j : ℂ) * I)) = S
  generalize Z1 θ = z
  field_simp

/-- Configuration A: phases `0, 0, π/2, −π/2`. -/
noncomputable def confA : Fin 4 → ℝ := ![0, 0, Real.pi / 2, -(Real.pi / 2)]

/-- Configuration B: phases `0, 0, 0, π`. -/
noncomputable def confB : Fin 4 → ℝ := ![0, 0, 0, Real.pi]

theorem moments_A : Z1 confA = 1 / 2 ∧ Z2 confA = 0 := by
  -- `e^{-iπ/2} = -i`, and the doubled phases are `0, 0, π, −π`
  have h1 : -((Real.pi : ℂ) / 2 * I) = -Real.pi / 2 * I := by ring
  have h2 : 2 * ((Real.pi : ℂ) / 2) * I = Real.pi * I := by ring
  constructor
  · simp [Z1, confA, Fin.sum_univ_four, h1]
    norm_num
  · simp [Z2, confA, Fin.sum_univ_four, h2]

theorem moments_B : Z1 confB = 1 / 2 ∧ Z2 confB = 1 := by
  constructor
  · simp [Z1, confB, Fin.sum_univ_four]
    norm_num
  · simp [Z2, confB, Fin.sum_univ_four]
    norm_num

/-- **Counterexample to closure**: the same first moment (so the same synchrony
`R = 1/2`) but different rates of change, `K/4` versus `0`. -/
theorem same_synchrony_different_future (K : ℝ) :
    Z1 confA = Z1 confB ∧ Z1dot K confA = K / 4 ∧ Z1dot K confB = 0 := by
  obtain ⟨hA1, hA2⟩ := moments_A
  obtain ⟨hB1, hB2⟩ := moments_B
  refine ⟨by rw [hA1, hB1], ?_, ?_⟩
  · rw [Z1dot_eq, hA1, hA2]; ring
  · -- `conj(1/2) = 1/2`
    have hc : starRingEnd ℂ (1 / 2 : ℂ) = 1 / 2 := by rw [map_div₀, map_one, map_ofNat]
    rw [Z1dot_eq, hB1, hB2, hc]; ring

/-- The 24-cell versions (each four-cell pattern repeated six times). -/
noncomputable def confA24 (j : Fin 24) : ℝ := confA ⟨j.val % 4, Nat.mod_lt _ (by norm_num)⟩

noncomputable def confB24 (j : Fin 24) : ℝ := confB ⟨j.val % 4, Nat.mod_lt _ (by norm_num)⟩

/-- A sum over 24 cells of a 4-periodic pattern is six copies of the 4-cell sum. -/
private lemma PhaseMoments_sum24 (g : Fin 4 → ℂ) :
    ∑ j : Fin 24, g ⟨j.val % 4, Nat.mod_lt _ (by norm_num)⟩ = 6 * ∑ j, g j := by
  simp [Fin.sum_univ_succ]
  ring

/-- Repeating a 4-cell pattern six times leaves both moments unchanged. -/
private lemma PhaseMoments_moments24 (c : Fin 4 → ℝ) :
    Z1 (fun j : Fin 24 => c ⟨j.val % 4, Nat.mod_lt _ (by norm_num)⟩) = Z1 c ∧
    Z2 (fun j : Fin 24 => c ⟨j.val % 4, Nat.mod_lt _ (by norm_num)⟩) = Z2 c := by
  constructor
  · unfold Z1
    rw [PhaseMoments_sum24 (fun k => exp (c k * I))]
    push_cast
    ring
  · unfold Z2
    rw [PhaseMoments_sum24 (fun k => exp (2 * c k * I))]
    push_cast
    ring

theorem same_synchrony_different_future_24 (K : ℝ) :
    Z1 confA24 = 1 / 2 ∧ Z1 confB24 = 1 / 2 ∧ Z1dot K confA24 = K / 4 ∧ Z1dot K confB24 = 0 := by
  -- the 24-cell moments equal the 4-cell ones; then use the moment identity
  obtain ⟨hA1, hA2⟩ := PhaseMoments_moments24 confA
  obtain ⟨hB1, hB2⟩ := PhaseMoments_moments24 confB
  have eA1 : Z1 confA24 = 1 / 2 := hA1.trans moments_A.1
  have eA2 : Z2 confA24 = 0 := hA2.trans moments_A.2
  have eB1 : Z1 confB24 = 1 / 2 := hB1.trans moments_B.1
  have eB2 : Z2 confB24 = 1 := hB2.trans moments_B.2
  refine ⟨eA1, eB1, ?_, ?_⟩
  · rw [Z1dot_eq, eA1, eA2]; ring
  · have hc : starRingEnd ℂ (1 / 2 : ℂ) = 1 / 2 := by rw [map_div₀, map_one, map_ofNat]
    rw [Z1dot_eq, eB1, eB2, hc]; ring

end Wyrd.SharedAir
