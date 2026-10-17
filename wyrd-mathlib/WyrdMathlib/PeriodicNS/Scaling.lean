import WyrdMathlib.PeriodicNS.SignFlip

/-!
# Spatial rescaling: no universal power law with `2a + 4b < 3`

Rescale every spatial argument of `v` by an integer `k ≥ 1`:

  `v_k = (sin(k y), sin(k z), cos(k x) − cos(k x + k y))`.

It stays `2π`-periodic, smooth and divergence-free. Each derivative brings a
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
  sorry

theorem div_vScaled (k : ℕ) (x y z : ℝ) : (vScaled k).div x y z = 0 := by
  sorry

theorem quantities_vScaled {k : ℕ} (hk : 0 < k) :
    (vScaled k).energy = 1 ∧ (vScaled k).enstrophy = 5 * (k : ℝ) ^ 2 / 4 ∧
      (vScaled k).palin = 7 * (k : ℝ) ^ 4 / 2 ∧ (vScaled k).stretching = (k : ℝ) ^ 3 / 4 := by
  sorry

theorem ratio_vScaled {k : ℕ} (hk : 0 < k) (a b : ℝ) :
    (vScaled k).stretching / ((vScaled k).enstrophy ^ a * (vScaled k).palin ^ b) =
      1 / 4 / ((5 / 4 : ℝ) ^ a * (7 / 2 : ℝ) ^ b) * (k : ℝ) ^ (3 - 2 * a - 4 * b) := by
  sorry

theorem no_power_law_bound {a b : ℝ} (hab : 2 * a + 4 * b < 3) (C : ℝ) :
    ∃ k : ℕ, 0 < k ∧
      C * ((vScaled k).enstrophy ^ a * (vScaled k).palin ^ b) < (vScaled k).stretching := by
  sorry

theorem fitted_law_fails (C : ℝ) :
    ∃ k : ℕ, 0 < k ∧
      C * ((vScaled k).enstrophy ^ (0.75 : ℝ) * (vScaled k).palin ^ (0.2 : ℝ)) <
        (vScaled k).stretching := by
  sorry

end Wyrd.PeriodicNS
