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
  have hn' : (0 : ℝ) < n := by exact_mod_cast hn
  set Y : Ω → ℝ := ∑ i ∈ Finset.range n, X i with hY
  have hYapp : ∀ ω, Y ω = ∑ i ∈ Finset.range n, X i ω := fun ω => by
    simp [hY, Finset.sum_apply]
  have hYmem : MemLp Y 2 μ := memLp_finsetSum' _ (fun i _ => hX i)
  set S : Ω → ℝ := fun ω => (n : ℝ)⁻¹ * Y ω with hS
  have hSmem : MemLp S 2 μ := hYmem.const_mul _
  have hYvar : variance Y μ = n * σ2 := by
    rw [hY, IndepFun.variance_sum (fun i _ => hX i)
      (fun i _ j _ hij => hind hij)]
    simp [hvar]
  have hSvar : variance S μ = σ2 / n := by
    rw [hS, variance_const_mul, hYvar]
    field_simp
  have hYmean : μ[Y] = n * m := by
    have : (fun ω => Y ω) = fun ω => ∑ i ∈ Finset.range n, X i ω := funext hYapp
    rw [show μ[Y] = ∫ ω, Y ω ∂μ from rfl, this,
      integral_finsetSum _ (fun i _ => (hX i).integrable one_le_two)]
    simp [hmean]
  have hSmean : μ[S] = m := by
    rw [hS, integral_const_mul, hYmean]
    field_simp
  have hset : {ω | t ≤ |(∑ i ∈ Finset.range n, X i ω) / n - m|} =
      {ω | t ≤ |S ω - μ[S]|} := by
    ext ω
    rw [hSmean]
    show t ≤ |(∑ i ∈ Finset.range n, X i ω) / n - m| ↔ t ≤ |(n : ℝ)⁻¹ * Y ω - m|
    rw [hYapp, div_eq_inv_mul]
  rw [hset]
  refine (meas_ge_le_variance_div_sq hSmem ht).trans (le_of_eq ?_)
  rw [hSvar, div_div]

theorem sessions_enough {Ω : Type*} [MeasurableSpace Ω] {μ : Measure Ω}
    [IsProbabilityMeasure μ] {X : ℕ → Ω → ℝ} {m σ2 Δ δ : ℝ} {n : ℕ} (hn : 0 < n)
    (hΔ : 0 < Δ) (hδ : 0 < δ) (hX : ∀ i, MemLp (X i) 2 μ)
    (hind : Pairwise fun i j => IndepFun (X i) (X j) μ)
    (hmean : ∀ i, μ[X i] = m) (hvar : ∀ i, variance (X i) μ = σ2)
    (hN : 4 * σ2 / (δ * Δ ^ 2) ≤ n) :
    μ {ω | Δ / 2 ≤ |(∑ i ∈ Finset.range n, X i ω) / n - m|} ≤ ENNReal.ofReal δ := by
  have hn' : (0 : ℝ) < n := by exact_mod_cast hn
  refine (sessions_chebyshev hn (half_pos hΔ) hX hind hmean hvar).trans
    (ENNReal.ofReal_le_ofReal ?_)
  have h1 : 4 * σ2 ≤ n * (δ * Δ ^ 2) := by
    rw [div_le_iff₀ (by positivity)] at hN
    linarith
  rw [div_le_iff₀ (by positivity)]
  nlinarith

end Wyrd.Limits
