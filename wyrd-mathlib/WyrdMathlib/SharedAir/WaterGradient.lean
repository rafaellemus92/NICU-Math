import Mathlib

/-!
# Passive water exchange is a gradient flow: it settles and cannot oscillate

`m` cells with water volumes `vᵢ`, fixed effective osmoles `nᵢ` inside and `n_E`
outside, closed total water `W` (so outside water is `V_E = W − Σ vᵢ`), and
transport coefficients `Kᵢ`:

  `vᵢ' = Kᵢ (nᵢ/vᵢ − n_E/V_E)`.

The free energy `F = −Σ nᵢ log vᵢ − n_E log V_E` decreases along every
trajectory at the rate `Σ Kᵢ (nᵢ/vᵢ − n_E/V_E)²`. It is constant only at the
unique equilibrium, `vᵢ = W nᵢ/(n_E + Σ nⱼ)`, which is the osmotic split of
`BodyWater/Osmotic.lean`. Also, two configurations with the same totals can
move differently: the aggregate does not determine its own change.

(Global convergence follows by standard Lyapunov arguments; it is not
formalised here.)
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
  sorry

/-- The dissipation rate is never positive. -/
theorem dissipation_nonpos {m : ℕ} {K n : Fin m → ℝ} {nE W : ℝ} (v : Fin m → ℝ)
    (hK : ∀ i, 0 ≤ K i) : -(∑ i, K i * (n i / v i - nE / VE W v) ^ 2) ≤ 0 := by
  sorry

/-- With positive transport, the rate is zero exactly when every cell is at the
outside osmolality. -/
theorem dissipation_eq_zero_iff {m : ℕ} {K n : Fin m → ℝ} {nE W : ℝ} (v : Fin m → ℝ)
    (hK : ∀ i, 0 < K i) :
    (∑ i, K i * (n i / v i - nE / VE W v) ^ 2) = 0 ↔ ∀ i, n i / v i = nE / VE W v := by
  sorry

/-- **The equilibrium is unique**: equal osmolalities force `vᵢ = W nᵢ/(n_E + Σ nⱼ)`. -/
theorem equilibrium_eq {m : ℕ} {n : Fin m → ℝ} {nE W : ℝ} {v : Fin m → ℝ}
    (hn : ∀ i, 0 < n i) (hnE : 0 < nE) (hv : ∀ i, 0 < v i) (hE : 0 < VE W v)
    (heq : ∀ i, n i / v i = nE / VE W v) :
    ∀ i, v i = W * n i / (nE + ∑ j, n j) := by
  sorry

/-- **Same totals, different movement**: two cells with `n = (1, 1)`, `n_E = 2`,
`W = 4`, `K = (1, 1)`. Configurations `(1, 1)` and `(1/2, 3/2)` have the same total
cell water and outside water, but total inflow `0` versus `2/3`. -/
theorem aggregate_counterexample :
    (∑ i, ![(1 : ℝ), 1] i) = ∑ i, ![(1 / 2 : ℝ), 3 / 2] i ∧
      VE 4 ![(1 : ℝ), 1] = VE 4 ![(1 / 2 : ℝ), 3 / 2] ∧
      (∑ i, flux ![1, 1] ![1, 1] 2 4 ![(1 : ℝ), 1] i) = 0 ∧
      (∑ i, flux ![1, 1] ![1, 1] 2 4 ![(1 / 2 : ℝ), 3 / 2] i) = 2 / 3 := by
  sorry

end Wyrd.SharedAir
