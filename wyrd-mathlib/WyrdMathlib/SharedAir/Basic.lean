import Mathlib

/-!
# Shared Air feedback systems: definitions and the completed square

The linearised three-variable feedback system (zero delay)

  `x' = -a x - z + r g y`,  `y' = -b y + q g x`,  `z' = -d z + h g x`

has two loops: `x → z → -x` is negative feedback of strength `∝ g`, and
`x → y → x` is positive feedback of round-trip strength `∝ g²` (with `c = r q`).
Its characteristic polynomial is

  `P(s, g) = (s + a)(s + b)(s + d) + h g (s + b) - c g² (s + d)`.

Standing hypotheses (`Hyp`): `0 < a < b`, `d ≥ 3b − 2a`, `c, h > 0`. These are
sufficient, not necessary.

Source of the equations: the "Perceived" world of the *Shared Air* model,
linearised at zero input, zero noise, baseline 0 and steadiness 1. This is a
mathematical statement about that linearisation, not a biological claim.
-/

namespace Wyrd.SharedAir

/-- The standing hypotheses on the coefficients. -/
structure Hyp (a b d c h : ℝ) : Prop where
  a_pos : 0 < a
  a_lt_b : a < b
  d_ge : 3 * b - 2 * a ≤ d
  c_pos : 0 < c
  h_pos : 0 < h

/-- Characteristic polynomial, real variable. -/
def P (a b d c h g s : ℝ) : ℝ :=
  (s + a) * (s + b) * (s + d) + h * g * (s + b) - c * g ^ 2 * (s + d)

/-- Characteristic polynomial, complex variable (real coefficients). -/
def Pc (a b d c h g : ℝ) (z : ℂ) : ℂ :=
  (z + a) * (z + b) * (z + d) + h * g * (z + b) - c * g ^ 2 * (z + d)

theorem Pc_ofReal (a b d c h g s : ℝ) : Pc a b d c h g (s : ℂ) = (P a b d c h g s : ℂ) := by
  sorry

/-- The system matrix: rows are `x', y', z'`. -/
def sysMatrix (a b d r q h g : ℝ) : Matrix (Fin 3) (Fin 3) ℂ :=
  !![(-a : ℂ), r * g, -1; q * g, -b, 0; h * g, 0, -d]

/-- **The eigenvalue equation is `P = 0`**: `det(z·I − M) = P(z)` with `c = r q`. -/
theorem det_charMatrix (a b d r q h g : ℝ) (z : ℂ) :
    (z • (1 : Matrix (Fin 3) (Fin 3) ℂ) - sysMatrix a b d r q h g).det = Pc a b d (r * q) h g z := by
  sorry

/-- The envelope `H(s) = (s + a)(s + d)² + h²/(4c) · (s + b)`. -/
noncomputable def H (a b d c h s : ℝ) : ℝ := (s + a) * (s + d) ^ 2 + h ^ 2 / (4 * c) * (s + b)

/-- The gain that completes the square, `G(s) = h/(2c) · (s + b)/(s + d)`. -/
noncomputable def G (b d c h s : ℝ) : ℝ := h / (2 * c) * ((s + b) / (s + d))

/-- **Completing the square in the gain**:
`P(s, g) = (s + b)/(s + d) · H(s) − c (s + d) (g − G(s))²`. -/
theorem complete_square {a b d c h g s : ℝ} (hc : c ≠ 0) (hs : s + d ≠ 0) :
    P a b d c h g s = (s + b) / (s + d) * H a b d c h s - c * (s + d) * (g - G b d c h s) ^ 2 := by
  sorry

/-- Under `Hyp`, `b < d` (so `s + d > 0` whenever `s > -b`). -/
theorem Hyp.b_lt_d {a b d c h : ℝ} (hp : Hyp a b d c h) : b < d := by
  sorry

theorem H_neg_b {a b d c h : ℝ} (hp : Hyp a b d c h) : H a b d c h (-b) < 0 := by
  sorry

theorem H_neg_a {a b d c h : ℝ} (hp : Hyp a b d c h) : 0 < H a b d c h (-a) := by
  sorry

/-- `H` is strictly increasing on `(-b, ∞)`. -/
theorem H_strictMonoOn {a b d c h : ℝ} (hp : Hyp a b d c h) :
    StrictMonoOn (H a b d c h) (Set.Ioi (-b)) := by
  sorry

/-- **`H` has exactly one root in `(-b, -a)`**: this is `s*`, the best achievable
dominant eigenvalue. -/
theorem existsUnique_root_H {a b d c h : ℝ} (hp : Hyp a b d c h) :
    ∃! s, s ∈ Set.Ioo (-b) (-a) ∧ H a b d c h s = 0 := by
  sorry

end Wyrd.SharedAir
