import Mathlib

/-!
# Passive water exchange: free energy is a strict Lyapunov function

`m` cells with water volumes `vᵢ`, fixed effective osmoles `nᵢ` inside and `n_E`
outside, closed total water `W` (so outside water is `V_E = W − Σ vᵢ`), and
transport coefficients `Kᵢ`:

  `vᵢ' = Kᵢ (nᵢ/vᵢ − n_E/V_E)`.

The free energy `F = −Σ nᵢ log vᵢ − n_E log V_E` decreases along every
trajectory at the rate `Σ Kᵢ (nᵢ/vᵢ − n_E/V_E)²`. It is constant only at the
unique equilibrium, `vᵢ = W nᵢ/(n_E + Σ nⱼ)`, which is the osmotic split of
`BodyWater/Osmotic.lean`. Also, two configurations with the same totals can
move differently: the aggregate does not determine its own change.

Global convergence, and so the absence of sustained oscillations, follows by
standard Lyapunov arguments. Neither is formalised here; what is proved is the
dissipation identity, its sign, when it vanishes, and that the equilibrium
exists (`equilibrium_exists`) and is unique (`equilibrium_eq`).
-/

namespace Wyrd.SharedAir

/-- Extracellular water. -/
def VE {m : ℕ} (W : ℝ) (v : Fin m → ℝ) : ℝ := W - ∑ i, v i

/-- Water flux into cell `i`. -/
noncomputable def flux {m : ℕ} (K n : Fin m → ℝ) (nE W : ℝ) (v : Fin m → ℝ) (i : Fin m) : ℝ :=
  K i * (n i / v i - nE / VE W v)

/-- Free energy. -/
noncomputable def freeEnergy {m : ℕ} (n : Fin m → ℝ) (nE W : ℝ) (v : Fin m → ℝ) : ℝ :=
  -(∑ i, n i * Real.log (v i)) - nE * Real.log (VE W v)

/-- **Dissipation**: along any trajectory obeying the flux law, `F` changes at rate
`−Σ Kᵢ (nᵢ/vᵢ − n_E/V_E)²`. -/
theorem hasDerivAt_freeEnergy {m : ℕ} {K n : Fin m → ℝ} {nE W t : ℝ} {v : ℝ → Fin m → ℝ}
    (hv : ∀ i, HasDerivAt (fun s => v s i) (flux K n nE W (v t) i) t)
    (hpos : ∀ i, 0 < v t i) (hE : 0 < VE W (v t)) :
    HasDerivAt (fun s => freeEnergy n nE W (v s))
      (-(∑ i, K i * (n i / v t i - nE / VE W (v t)) ^ 2)) t := by
  -- derivative of the cell term `Σ nᵢ log vᵢ`
  have h1 : HasDerivAt (fun s => ∑ i, n i * Real.log (v s i))
      (∑ i, n i * (flux K n nE W (v t) i / v t i)) t := by
    apply HasDerivAt.fun_sum
    intro i _
    exact ((hv i).log (hpos i).ne').const_mul (n i)
  -- derivative of the outside water `V_E = W − Σ vᵢ`
  have h2 : HasDerivAt (fun s => VE W (v s)) (-(∑ i, flux K n nE W (v t) i)) t := by
    have : HasDerivAt (fun s => ∑ i, v s i) (∑ i, flux K n nE W (v t) i) t :=
      HasDerivAt.fun_sum (fun i _ => hv i)
    simpa [VE] using this.const_sub W
  have h3 := h1.neg.sub ((h2.log hE.ne').const_mul nE)
  convert h3 using 1
  · funext s
    simp [freeEnergy]
  -- algebra: collect everything into one sum and substitute the flux law termwise
  rw [neg_div, mul_neg, sub_neg_eq_add, Finset.sum_div, Finset.mul_sum,
    ← Finset.sum_neg_distrib, ← Finset.sum_neg_distrib, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl (fun i _ => ?_)
  simp only [flux]
  ring

/-- The dissipation rate is never positive. -/
theorem dissipation_nonpos {m : ℕ} {K n : Fin m → ℝ} {nE W : ℝ} (v : Fin m → ℝ)
    (hK : ∀ i, 0 ≤ K i) : -(∑ i, K i * (n i / v i - nE / VE W v) ^ 2) ≤ 0 := by
  have : 0 ≤ ∑ i, K i * (n i / v i - nE / VE W v) ^ 2 :=
    Finset.sum_nonneg (fun i _ => mul_nonneg (hK i) (sq_nonneg _))
  linarith

/-- With positive transport, the rate is zero exactly when every cell is at the
outside osmolality. -/
theorem dissipation_eq_zero_iff {m : ℕ} {K n : Fin m → ℝ} {nE W : ℝ} (v : Fin m → ℝ)
    (hK : ∀ i, 0 < K i) :
    (∑ i, K i * (n i / v i - nE / VE W v) ^ 2) = 0 ↔ ∀ i, n i / v i = nE / VE W v := by
  rw [Finset.sum_eq_zero_iff_of_nonneg (fun i _ => mul_nonneg (hK i).le (sq_nonneg _))]
  constructor
  · intro h i
    -- `Kᵢ > 0`, so the square must vanish
    rcases mul_eq_zero.mp (h i (Finset.mem_univ i)) with h0 | h0
    · exact absurd h0 (hK i).ne'
    · exact sub_eq_zero.mp ((pow_eq_zero_iff two_ne_zero).mp h0)
  · intro h i _
    rw [h i, sub_self]
    ring

/-- **The equilibrium is unique**: equal osmolalities force `vᵢ = W nᵢ/(n_E + Σ nⱼ)`. -/
theorem equilibrium_eq {m : ℕ} {n : Fin m → ℝ} {nE W : ℝ} {v : Fin m → ℝ}
    (hn : ∀ i, 0 < n i) (hnE : 0 < nE) (hv : ∀ i, 0 < v i) (hE : 0 < VE W v)
    (heq : ∀ i, n i / v i = nE / VE W v) :
    ∀ i, v i = W * n i / (nE + ∑ j, n j) := by
  intro i
  set E := VE W v with hEdef
  -- each cell volume is `nⱼ / κ` with `κ = n_E / V_E`
  have hvi : ∀ j, v j = n j * E / nE := by
    intro j
    have h := heq j
    have hvj := (hv j).ne'
    have hEne := hE.ne'
    have hnEne := hnE.ne'
    field_simp at h ⊢
    linarith
  have hsum : ∑ j, v j = (∑ j, n j) * E / nE := by
    rw [Finset.sum_congr rfl (fun j _ => hvi j), ← Finset.sum_div, ← Finset.sum_mul]
  -- total water is outside plus inside
  have hW : W = E + ∑ j, v j := by simp [hEdef, VE]
  have hS : 0 < nE + ∑ j, n j := by
    have := Finset.sum_nonneg (fun j (_ : j ∈ Finset.univ) => (hn j).le)
    linarith
  have hSne := hS.ne'
  have hnEne := hnE.ne'
  rw [hW, hsum, hvi i]
  field_simp

/-- **Same totals, different movement**: two cells with `n = (1, 1)`, `n_E = 2`,
`W = 4`, `K = (1, 1)`. Configurations `(1, 1)` and `(1/2, 3/2)` have the same total
cell water and outside water, but total inflow `0` versus `2/3`. -/
theorem aggregate_counterexample :
    (∑ i, ![(1 : ℝ), 1] i) = ∑ i, ![(1 / 2 : ℝ), 3 / 2] i ∧
      VE 4 ![(1 : ℝ), 1] = VE 4 ![(1 / 2 : ℝ), 3 / 2] ∧
      (∑ i, flux ![1, 1] ![1, 1] 2 4 ![(1 : ℝ), 1] i) = 0 ∧
      (∑ i, flux ![1, 1] ![1, 1] 2 4 ![(1 / 2 : ℝ), 3 / 2] i) = 2 / 3 := by
  simp [VE, flux, Fin.sum_univ_two]
  norm_num

/-- **The equilibrium exists**: `vᵢ = W nᵢ/(n_E + Σ nⱼ)` gives positive volumes, positive
outside water, and zero flux into every cell. -/
theorem equilibrium_exists {m : ℕ} {K n : Fin m → ℝ} {nE W : ℝ} (hn : ∀ i, 0 < n i) (hnE : 0 < nE)
    (hW : 0 < W) :
    (∀ i, 0 < W * n i / (nE + ∑ j, n j)) ∧ 0 < VE W (fun i => W * n i / (nE + ∑ j, n j)) ∧
      ∀ i, flux K n nE W (fun i => W * n i / (nE + ∑ j, n j)) i = 0 := by
  sorry

end Wyrd.SharedAir
