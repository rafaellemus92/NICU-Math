import Mathlib

/-!
# The conditional regularity route: Grönwall with a variable rate

If `dZ/dt ≤ a(t) Z(t)`, then `Z(t) ≤ Z(0) · exp(∫₀ᵗ a)`. For Navier–Stokes, a
uniform estimate `S ≤ (1 − δ) ν D + a(t) Z` with `∫₀ᵀ a < ∞` controlled
independently would therefore bound the enstrophy on `[0, T]`. That estimate is
the missing piece, and is **not** proved; this file proves only the Grönwall step.
-/

namespace Wyrd.PeriodicNS

/-- **Grönwall's inequality, variable coefficient.** -/
theorem gronwall_variable {Z Z' a : ℝ → ℝ} (ha : Continuous a)
    (hZ : ∀ t, HasDerivAt Z (Z' t) t) (hle : ∀ t, 0 ≤ t → Z' t ≤ a t * Z t)
    {t : ℝ} (ht : 0 ≤ t) :
    Z t ≤ Z 0 * Real.exp (∫ s in (0 : ℝ)..t, a s) := by
  -- `A u = ∫₀ᵘ a`, with `A' = a` by the fundamental theorem of calculus.
  set A : ℝ → ℝ := fun u => ∫ s in (0 : ℝ)..u, a s with hAdef
  have hA : ∀ u, HasDerivAt A (a u) u := fun u =>
    (ha.integral_hasStrictDerivAt 0 u).hasDerivAt
  -- The integrating factor: `g = Z · exp(−A)`.
  set g : ℝ → ℝ := fun u => Z u * Real.exp (-A u) with hgdef
  have hg : ∀ u, HasDerivAt g (Z' u * Real.exp (-A u) + Z u * (Real.exp (-A u) * (-a u))) u :=
    fun u => (hZ u).mul ((hA u).neg.exp)
  -- `g' = (Z' − a Z) exp(−A) ≤ 0` on `[0, ∞)`, so `g` is antitone there.
  have hanti : AntitoneOn g (Set.Ici 0) := by
    refine antitoneOn_of_hasDerivWithinAt_nonpos (convex_Ici 0)
      (fun u _ => (hg u).continuousAt.continuousWithinAt)
      (fun u _ => (hg u).hasDerivWithinAt) ?_
    intro u hu
    rw [interior_Ici] at hu
    have h1 := hle u (le_of_lt hu)
    have h2 := Real.exp_pos (-A u)
    nlinarith
  have hgt : g t ≤ g 0 := hanti (Set.mem_Ici.mpr le_rfl) (Set.mem_Ici.mpr ht) ht
  have hA0 : A 0 = 0 := by simp [hAdef]
  simp only [hgdef, hA0, neg_zero, Real.exp_zero, mul_one] at hgt
  -- Multiply back by `exp(A t) > 0`.
  have hE := Real.exp_pos (A t)
  have key : Z t = Z t * Real.exp (-A t) * Real.exp (A t) := by
    rw [mul_assoc, ← Real.exp_add, neg_add_cancel, Real.exp_zero, mul_one]
  calc Z t = Z t * Real.exp (-A t) * Real.exp (A t) := key
    _ ≤ Z 0 * Real.exp (A t) := mul_le_mul_of_nonneg_right hgt hE.le

/-- The enstrophy step: if `S ≤ (1 − δ) ν D + a Z` with `δ ≥ 0` and `D ≥ 0`, then
`S − ν D ≤ a Z`. -/
theorem stretching_estimate_step {S D Zv a ν δ : ℝ} (hν : 0 ≤ ν) (hδ : 0 ≤ δ) (hD : 0 ≤ D)
    (h : S ≤ (1 - δ) * ν * D + a * Zv) : S - ν * D ≤ a * Zv := by
  -- `δ ν D ≥ 0`, and `S − ν D ≤ a Z − δ ν D`.
  have h1 : 0 ≤ δ * ν * D := mul_nonneg (mul_nonneg hδ hν) hD
  nlinarith

end Wyrd.PeriodicNS
