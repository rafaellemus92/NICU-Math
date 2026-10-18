import WyrdMathlib.PeriodicNS.Averages

/-!
# Same spectrum, opposite enstrophy change

For amplitude `A`, the fields `±A v` have the same energy `A²`, enstrophy `5A²/4`,
dissipation `7A²/2`, and the same Fourier magnitude at every wave vector. But the
cubic stretching term flips sign: `S = ±A³/4`. So the enstrophy rate `S − νD`
from the standard balance is `A³/4 − 7νA²/2` for one and `−A³/4 − 7νA²/2` for the
other: of opposite signs once `A > 14ν`. With `A = 1`, `ν = 1/28` the rates are
`1/8` and `−3/8`.

What is proved: the right-hand side `S − νD` of the enstrophy balance is **not a
function** of `(E, Z, D, ν)` (`no_closure`), nor of the full list of Fourier
magnitudes `|û(k)|` plus `ν` (`no_spectral_closure`). The two fields share every
input but give `1/8` and `−3/8`.

Informal consequence, **not formalised**: no exact law `dZ/dt = Φ(E, Z, D, ν)`
holds for all smooth solutions. Reading it that way needs two standard facts
Lean does not have here: local existence of smooth solutions from `±A v`, and the
enstrophy balance `dZ/dt = S − νD` itself. Neither field is claimed to blow up.
-/

namespace Wyrd.PeriodicNS

open Real

/-- `∂/∂x` commutes with multiplication by a constant (no differentiability needed). -/
private lemma SignFlip_dx_smul (A : ℝ) (f : ℝ → ℝ → ℝ → ℝ) :
    dx (fun x y z => A * f x y z) = fun x y z => A * dx f x y z := by
  funext x y z; exact deriv_const_mul_field A

/-- `∂/∂y` commutes with multiplication by a constant. -/
private lemma SignFlip_dy_smul (A : ℝ) (f : ℝ → ℝ → ℝ → ℝ) :
    dy (fun x y z => A * f x y z) = fun x y z => A * dy f x y z := by
  funext x y z; exact deriv_const_mul_field A

/-- `∂/∂z` commutes with multiplication by a constant. -/
private lemma SignFlip_dz_smul (A : ℝ) (f : ℝ → ℝ → ℝ → ℝ) :
    dz (fun x y z => A * f x y z) = fun x y z => A * dz f x y z := by
  funext x y z; exact deriv_const_mul_field A

/-- The curl is linear: `curl (A u) = A curl u`. -/
private lemma SignFlip_curl_smul (A : ℝ) (u : Field) : (u.smul A).curl = u.curl.smul A := by
  simp only [Field.curl, Field.smul, SignFlip_dx_smul, SignFlip_dy_smul, SignFlip_dz_smul,
    Field.mk.injEq]
  refine ⟨?_, ?_, ?_⟩ <;> funext x y z <;> ring

/-- Constants pull out of the average (`integral_const_mul` needs no integrability). -/
private lemma SignFlip_avg_eq_mul {f g : ℝ → ℝ → ℝ → ℝ} (c : ℝ)
    (h : ∀ x y z, f x y z = c * g x y z) : avg f = c * avg g := by
  have hf : f = fun x y z => c * g x y z := by funext x y z; exact h x y z
  subst hf
  unfold avg
  simp only [intervalIntegral.integral_const_mul]
  ring

private lemma SignFlip_energy_smul (A : ℝ) (u : Field) : (u.smul A).energy = A ^ 2 * u.energy := by
  unfold Field.energy
  rw [SignFlip_avg_eq_mul (A ^ 2)
    (g := fun x y z => u.u1 x y z ^ 2 + u.u2 x y z ^ 2 + u.u3 x y z ^ 2)
    (fun x y z => by simp only [Field.smul]; ring)]
  ring

private lemma SignFlip_gradSq_smul (A : ℝ) (u : Field) : (u.smul A).gradSq = A ^ 2 * u.gradSq := by
  unfold Field.gradSq
  rw [SignFlip_avg_eq_mul (A ^ 2)
    (g := fun x y z =>
      dx u.u1 x y z ^ 2 + dy u.u1 x y z ^ 2 + dz u.u1 x y z ^ 2 +
      dx u.u2 x y z ^ 2 + dy u.u2 x y z ^ 2 + dz u.u2 x y z ^ 2 +
      dx u.u3 x y z ^ 2 + dy u.u3 x y z ^ 2 + dz u.u3 x y z ^ 2)
    (fun x y z => by
      simp only [Field.smul, SignFlip_dx_smul, SignFlip_dy_smul, SignFlip_dz_smul]; ring)]

private lemma SignFlip_stretching_smul (A : ℝ) (u : Field) :
    (u.smul A).stretching = A ^ 3 * u.stretching := by
  unfold Field.stretching
  rw [SignFlip_curl_smul]
  rw [SignFlip_avg_eq_mul (A ^ 3)
    (g := fun x y z =>
      u.curl.u1 x y z * (dx u.u1 x y z * u.curl.u1 x y z + dy u.u1 x y z * u.curl.u2 x y z +
        dz u.u1 x y z * u.curl.u3 x y z) +
      u.curl.u2 x y z * (dx u.u2 x y z * u.curl.u1 x y z + dy u.u2 x y z * u.curl.u2 x y z +
        dz u.u2 x y z * u.curl.u3 x y z) +
      u.curl.u3 x y z * (dx u.u3 x y z * u.curl.u1 x y z + dy u.u3 x y z * u.curl.u2 x y z +
        dz u.u3 x y z * u.curl.u3 x y z))
    (fun x y z => by
      simp only [Field.smul, SignFlip_dx_smul, SignFlip_dy_smul, SignFlip_dz_smul]; ring)]

/-- Fourier coefficients are linear: a real constant pulls out. -/
private lemma SignFlip_coeff_const_mul (c : ℝ) (f : ℝ → ℝ → ℝ → ℝ) (k : ℤ × ℤ × ℤ) :
    coeff (fun x y z => c * f x y z) k = (c : ℂ) * coeff f k := by
  unfold coeff
  simp only [Complex.ofReal_mul, mul_assoc, intervalIntegral.integral_const_mul]
  ring

/-- **The quantities of `A v`.** -/
theorem quantities_smul (A : ℝ) :
    (v.smul A).energy = A ^ 2 ∧ (v.smul A).enstrophy = 5 * A ^ 2 / 4 ∧
      (v.smul A).palin = 7 * A ^ 2 / 2 ∧ (v.smul A).stretching = A ^ 3 / 4 := by
  -- each quantity scales by a power of `A`; then plug in the values for `v`
  obtain ⟨hE, hZ, hD, hS, -⟩ := quantities_v
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [SignFlip_energy_smul, hE]; ring
  · rw [Field.enstrophy, SignFlip_curl_smul, SignFlip_energy_smul, ← Field.enstrophy, hZ]; ring
  · rw [Field.palin, SignFlip_curl_smul, SignFlip_gradSq_smul, ← Field.palin, hD]; ring
  · rw [SignFlip_stretching_smul, hS]; ring

/-- With `A = 1`, `ν = 1/28`: enstrophy rates `1/8` for `v` and `−3/8` for `−v`. -/
theorem rates :
    (v.smul 1).stretching - 1 / 28 * (v.smul 1).palin = 1 / 8 ∧
      (v.smul (-1)).stretching - 1 / 28 * (v.smul (-1)).palin = -3 / 8 := by
  obtain ⟨-, -, hD1, hS1⟩ := quantities_smul 1
  obtain ⟨-, -, hD2, hS2⟩ := quantities_smul (-1)
  rw [hD1, hS1, hD2, hS2]
  constructor <;> norm_num

/-- **Opposite signs** whenever `A > 14ν > 0`. -/
theorem opposite_signs {A ν : ℝ} (hν : 0 < ν) (hA : 14 * ν < A) :
    0 < (v.smul A).stretching - ν * (v.smul A).palin ∧
      (v.smul (-A)).stretching - ν * (v.smul (-A)).palin < 0 := by
  obtain ⟨-, -, hD1, hS1⟩ := quantities_smul A
  obtain ⟨-, -, hD2, hS2⟩ := quantities_smul (-A)
  rw [hD1, hS1, hD2, hS2]
  have hA0 : 0 < A := by linarith
  have hA2 : 0 < A ^ 2 := by positivity
  have hA3 : 0 < A ^ 3 := by positivity
  constructor
  · -- `A³/4 − 7νA²/2 = (A²/4)(A − 14ν)`
    have := mul_pos hA2 (sub_pos.2 hA)
    nlinarith
  · -- `−A³/4 − 7νA²/2`: both terms negative
    have := mul_pos hν hA2
    nlinarith

/-- **Identical Fourier magnitudes at every wave vector.** -/
theorem same_spectrum (A : ℝ) (k : ℤ × ℤ × ℤ) :
    ‖coeff (v.smul (-A)).u1 k‖ = ‖coeff (v.smul A).u1 k‖ ∧
      ‖coeff (v.smul (-A)).u2 k‖ = ‖coeff (v.smul A).u2 k‖ ∧
      ‖coeff (v.smul (-A)).u3 k‖ = ‖coeff (v.smul A).u3 k‖ := by
  -- `coeff (c f) = c · coeff f`, and `‖−A‖ = ‖A‖`
  refine ⟨?_, ?_, ?_⟩ <;>
    simp only [Field.smul, SignFlip_coeff_const_mul, norm_mul, Complex.norm_real, norm_neg]

/-- **`S − νD` is not a function of `(E, Z, D, ν)`**: `v` and `−v` share
`(E, Z, D) = (1, 5/4, 7/2)` but give `1/8` and `−3/8` at `ν = 1/28`. (Applying this to
solutions needs the unformalised enstrophy balance and local existence.) -/
theorem no_closure :
    ¬ ∃ Φ : ℝ → ℝ → ℝ → ℝ → ℝ, ∀ u ∈ ({v.smul 1, v.smul (-1)} : Set Field),
      u.stretching - 1 / 28 * u.palin = Φ u.energy u.enstrophy u.palin (1 / 28) := by
  rintro ⟨Φ, hΦ⟩
  have h1 := hΦ (v.smul 1) (Set.mem_insert _ _)
  have h2 := hΦ (v.smul (-1)) (Set.mem_insert_of_mem _ (Set.mem_singleton _))
  obtain ⟨e1, z1, p1, s1⟩ := quantities_smul 1
  obtain ⟨e2, z2, p2, s2⟩ := quantities_smul (-1)
  rw [e1, z1, p1, s1] at h1
  rw [e2, z2, p2, s2] at h2
  -- both members feed the same `(E, Z, D, ν) = (1, 5/4, 7/2, 1/28)` into `Φ`,
  -- but their rates are `1/8` and `−3/8`
  norm_num at h1 h2
  linarith

/-- **`S − νD` is not a function of the Fourier magnitudes either**: `v` and `−v` have
the same `|û(k)|` for every component and every wave vector `k`, yet different
`S − νD`. So any exact rule that sees only spectra, even all of them, loses the
phase information that decides the stretching. -/
theorem no_spectral_closure :
    ¬ ∃ Φ : ((ℤ × ℤ × ℤ) → ℝ × ℝ × ℝ) → ℝ → ℝ, ∀ u ∈ ({v.smul 1, v.smul (-1)} : Set Field),
      u.stretching - 1 / 28 * u.palin =
        Φ (fun k => (‖coeff u.u1 k‖, ‖coeff u.u2 k‖, ‖coeff u.u3 k‖)) (1 / 28) := by
  rintro ⟨Φ, hΦ⟩
  have h1 := hΦ (v.smul 1) (by simp)
  have h2 := hΦ (v.smul (-1)) (by simp)
  -- the two spectra agree at every wave vector
  have hspec : (fun k => (‖coeff (v.smul (-1)).u1 k‖, ‖coeff (v.smul (-1)).u2 k‖,
      ‖coeff (v.smul (-1)).u3 k‖)) =
      (fun k => (‖coeff (v.smul 1).u1 k‖, ‖coeff (v.smul 1).u2 k‖, ‖coeff (v.smul 1).u3 k‖)) := by
    funext k
    obtain ⟨a, b, c⟩ := same_spectrum 1 k
    simp only [Prod.mk.injEq]
    exact ⟨a, b, c⟩
  rw [hspec] at h2
  -- but the rates are `1/8` and `−3/8`
  obtain ⟨r1, r2⟩ := rates
  linarith

end Wyrd.PeriodicNS
