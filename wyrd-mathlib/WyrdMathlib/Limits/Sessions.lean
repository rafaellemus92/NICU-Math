import Mathlib

/-!
# How many sessions: a distribution-free bound

The source says the model shows "roughly how many sessions it might take". A
simulation estimates that for its own noise. Chebyshev's inequality gives a
guarantee that holds for **any** session-to-session distribution with the
stated variance: no normality and no fitted model.

* `sessions_chebyshev`: for `n` pairwise independent sessions with common mean
  `m` and variance `σ²`, the session average is off by at least `t` with
  probability at most `σ² / (n t²)`.
* `sessions_enough`: suppose two worlds predict means `Δ` apart and the
  decision rule picks the nearer one. Its error probability is at most `δ`
  once `n ≥ 4σ² / (δ Δ²)`.

The bound is conservative, and the inputs `σ²` and `Δ` have to come from data or
from a model. Mathematics supplies only the conversion.
-/

namespace Wyrd.Limits

open MeasureTheory ProbabilityTheory

theorem sessions_chebyshev {Ω : Type*} [MeasurableSpace Ω] {μ : Measure Ω}
    [IsProbabilityMeasure μ] {X : ℕ → Ω → ℝ} {m σ2 t : ℝ} {n : ℕ} (hn : 0 < n)
    (ht : 0 < t) (hX : ∀ i, MemLp (X i) 2 μ)
    (hind : Pairwise fun i j => IndepFun (X i) (X j) μ)
    (hmean : ∀ i, μ[X i] = m) (hvar : ∀ i, variance (X i) μ = σ2) :
    μ {ω | t ≤ |(∑ i ∈ Finset.range n, X i ω) / n - m|} ≤
      ENNReal.ofReal (σ2 / (n * t ^ 2)) := by
  sorry

theorem sessions_enough {Ω : Type*} [MeasurableSpace Ω] {μ : Measure Ω}
    [IsProbabilityMeasure μ] {X : ℕ → Ω → ℝ} {m σ2 Δ δ : ℝ} {n : ℕ} (hn : 0 < n)
    (hΔ : 0 < Δ) (hδ : 0 < δ) (hX : ∀ i, MemLp (X i) 2 μ)
    (hind : Pairwise fun i j => IndepFun (X i) (X j) μ)
    (hmean : ∀ i, μ[X i] = m) (hvar : ∀ i, variance (X i) μ = σ2)
    (hN : 4 * σ2 / (δ * Δ ^ 2) ≤ n) :
    μ {ω | Δ / 2 ≤ |(∑ i ∈ Finset.range n, X i ω) / n - m|} ≤ ENNReal.ofReal δ := by
  sorry

end Wyrd.Limits
