import Mathlib

/-!
# Why a fixed Fourier cutoff cannot settle the question

In an exact unforced, Leray-projected (divergence-free) Fourier–Galerkin
truncation keeping wave vectors `|k| ≤ K`, energy
`E_K = ½ Σ |û_k|²` does not increase, and the enstrophy is `Z_K = ½ Σ |k|² |û_k|²`.
So `Z_K(t) ≤ K² E_K(t) ≤ K² E_K(0)`: bounded for each fixed `K`, but the bound
grows without limit as `K → ∞`. This file proves the inequality step.
-/

namespace Wyrd.PeriodicNS

/-- `Σ |k|² aₖ ≤ K² Σ aₖ` when every retained `|k|² ≤ K²` and `aₖ ≥ 0`. -/
theorem cutoff_bound {ι : Type*} (s : Finset ι) (k2 a : ι → ℝ) {K : ℝ}
    (hk : ∀ i ∈ s, k2 i ≤ K ^ 2) (ha : ∀ i ∈ s, 0 ≤ a i) :
    ∑ i ∈ s, k2 i * a i ≤ K ^ 2 * ∑ i ∈ s, a i := by
  -- bound each term `k2 i * a i ≤ K² * a i`, then pull `K²` out of the sum
  calc ∑ i ∈ s, k2 i * a i ≤ ∑ i ∈ s, K ^ 2 * a i :=
        Finset.sum_le_sum fun i hi => mul_le_mul_of_nonneg_right (hk i hi) (ha i hi)
    _ = K ^ 2 * ∑ i ∈ s, a i := by rw [Finset.mul_sum]

/-- With non-increasing energy, enstrophy stays below `K²` times the initial energy. -/
theorem galerkin_enstrophy_bound {ι : Type*} (s : Finset ι) (k2 : ι → ℝ) {K : ℝ}
    (a a₀ : ι → ℝ) (hk : ∀ i ∈ s, k2 i ≤ K ^ 2) (ha : ∀ i ∈ s, 0 ≤ a i)
    (henergy : ∑ i ∈ s, a i ≤ ∑ i ∈ s, a₀ i) :
    (∑ i ∈ s, k2 i * a i) / 2 ≤ K ^ 2 * ((∑ i ∈ s, a₀ i) / 2) := by
  have h1 := cutoff_bound s k2 a hk ha
  -- energy decay, scaled by the nonnegative factor `K²`
  have h2 : K ^ 2 * ∑ i ∈ s, a i ≤ K ^ 2 * ∑ i ∈ s, a₀ i :=
    mul_le_mul_of_nonneg_left henergy (sq_nonneg K)
  linarith

end Wyrd.PeriodicNS
