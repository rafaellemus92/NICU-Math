import Mathlib

/-!
# The 2:1 locking condition, for the averaged phase equation

After weak-forcing averaging, the phase difference obeys
`φ' = Δ − k sin φ` with detuning `Δ = ω − 2Ω` and `k = ε a₂/2`. This file proves
the exact statements for that averaged equation:

* it has an equilibrium exactly when `|Δ| ≤ k`;
* it has a *stable* equilibrium (where `−k cos φ < 0`) exactly when `|Δ| < k`.

That is the source's `|ω − 2Ω| < ε a₂/2`. It is exact for the averaged equation
only; for the full noisy, modulated population model it is a first-order
approximation. Also, for 2:1 locking the first circular moment can vanish even
under perfect locking (phases `0` and `π`). So a 2:1 index should use the second
harmonic (or analyse `θ − 2ψ` directly). The source does not give its index's
implementation, so this is a check to make, not a proven defect. The source's
`a₂ ≈ 0.19` matches `2e⁻² I₂(2) ≈ 0.18648` numerically; that value is not proved here.
-/

namespace Wyrd.SharedAir

open Complex

theorem averaged_equilibrium_iff {Δ k : ℝ} (hk : 0 < k) :
    (∃ φ : ℝ, Δ - k * Real.sin φ = 0) ↔ |Δ| ≤ k := by
  constructor
  · rintro ⟨φ, hφ⟩
    -- Δ = k sin φ and |sin φ| ≤ 1
    have hΔ : Δ = k * Real.sin φ := by linarith
    rw [hΔ, abs_mul, abs_of_pos hk]
    calc k * |Real.sin φ| ≤ k * 1 := by gcongr; exact Real.abs_sin_le_one φ
      _ = k := mul_one k
  · intro h
    have h1 : |Δ / k| ≤ 1 := by
      rw [abs_div, abs_of_pos hk, div_le_one hk]; exact h
    obtain ⟨h2, h3⟩ := abs_le.mp h1
    -- take φ = arcsin (Δ / k), so k sin φ = Δ
    refine ⟨Real.arcsin (Δ / k), ?_⟩
    rw [Real.sin_arcsin h2 h3]
    field_simp
    ring

theorem averaged_stable_equilibrium_iff {Δ k : ℝ} (hk : 0 < k) :
    (∃ φ : ℝ, Δ - k * Real.sin φ = 0 ∧ -(k * Real.cos φ) < 0) ↔ |Δ| < k := by
  constructor
  · rintro ⟨φ, hφ, hc⟩
    -- stability with k > 0 forces cos φ > 0
    have hcos : 0 < Real.cos φ := by
      by_contra hn
      have hn' : Real.cos φ ≤ 0 := not_lt.mp hn
      nlinarith [mul_nonpos_of_nonneg_of_nonpos hk.le hn']
    have hΔ : Δ = k * Real.sin φ := by linarith
    -- sin² φ = 1 - cos² φ < 1, so |sin φ| < 1
    have hsq : Real.sin φ ^ 2 < 1 := by
      nlinarith [Real.sin_sq_add_cos_sq φ]
    have hsin : |Real.sin φ| < 1 := (sq_lt_one_iff_abs_lt_one _).mp hsq
    rw [hΔ, abs_mul, abs_of_pos hk]
    calc k * |Real.sin φ| < k * 1 := by gcongr
      _ = k := mul_one k
  · intro h
    have h1 : |Δ / k| < 1 := by
      rw [abs_div, abs_of_pos hk, div_lt_one hk]; exact h
    obtain ⟨h2, h3⟩ := abs_lt.mp h1
    refine ⟨Real.arcsin (Δ / k), ?_, ?_⟩
    · rw [Real.sin_arcsin h2.le h3.le]
      field_simp
      ring
    · -- cos (arcsin x) = √(1 - x²) > 0 since x² < 1
      rw [Real.cos_arcsin]
      have hx : (Δ / k) ^ 2 < 1 := (sq_lt_one_iff_abs_lt_one _).mpr h1
      have hpos : 0 < Real.sqrt (1 - (Δ / k) ^ 2) := Real.sqrt_pos.mpr (by linarith)
      nlinarith

/-- Perfect 2:1 locking sampled at phases `0` and `π`: first moment `0`, second `1`. -/
theorem two_to_one_moments :
    (exp ((0 : ℝ) * I) + exp (Real.pi * I)) / 2 = 0 ∧
      (exp (2 * (0 : ℝ) * I) + exp (2 * Real.pi * I)) / 2 = 1 := by
  constructor
  · -- exp 0 = 1 and exp (π I) = -1
    push_cast
    rw [zero_mul, Complex.exp_zero, Complex.exp_pi_mul_I]
    norm_num
  · -- exp 0 = 1 and exp (2π I) = 1
    push_cast
    rw [mul_zero, zero_mul, Complex.exp_zero, Complex.exp_two_pi_mul_I]
    norm_num

end Wyrd.SharedAir
