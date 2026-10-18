import Mathlib

/-!
# Periodic velocity fields: the quantities in the enstrophy balance

A velocity field on the `2π`-periodic cube is given by its three components.
With `ω = ∇ × u` and `⟨·⟩` the normalised average over `[0, 2π]³`:

* energy `E = ½⟨|u|²⟩`;
* enstrophy `Z = ½⟨|ω|²⟩`;
* `D = ⟨|∇ω|²⟩` (vorticity-gradient dissipation);
* vortex stretching `S = ⟨ω · ((ω · ∇) u)⟩ = ⟨Σᵢⱼ ωᵢ (∂ⱼ uᵢ) ωⱼ⟩`.

For smooth solutions of the unforced Navier–Stokes equations on the torus, the
standard enstrophy balance is `dZ/dt = S − ν D` (curl the equation, dot with `ω`,
integrate; transport vanishes by incompressibility and periodicity). That
identity needs Navier–Stokes solution theory and is **not** formalised here.
These files compute the right-hand side exactly for explicit fields.

All derivatives are Lean's `deriv`, taken one coordinate at a time, so nothing
is hand-entered.

`Field` here shadows Mathlib's `Field` class and `v` is a short public name, so
refer to them as `Wyrd.PeriodicNS.Field` and `Wyrd.PeriodicNS.v` rather than
opening the namespace.
-/

namespace Wyrd.PeriodicNS

open Real

/-- A velocity field given by its three components. -/
structure Field where
  u1 : ℝ → ℝ → ℝ → ℝ
  u2 : ℝ → ℝ → ℝ → ℝ
  u3 : ℝ → ℝ → ℝ → ℝ

/-- `∂/∂x`. -/
noncomputable def dx (f : ℝ → ℝ → ℝ → ℝ) : ℝ → ℝ → ℝ → ℝ :=
  fun x y z => deriv (fun s => f s y z) x

/-- `∂/∂y`. -/
noncomputable def dy (f : ℝ → ℝ → ℝ → ℝ) : ℝ → ℝ → ℝ → ℝ :=
  fun x y z => deriv (fun s => f x s z) y

/-- `∂/∂z`. -/
noncomputable def dz (f : ℝ → ℝ → ℝ → ℝ) : ℝ → ℝ → ℝ → ℝ :=
  fun x y z => deriv (fun s => f x y s) z

namespace Field

/-- Divergence. -/
noncomputable def div (u : Field) : ℝ → ℝ → ℝ → ℝ :=
  fun x y z => dx u.u1 x y z + dy u.u2 x y z + dz u.u3 x y z

/-- Curl (vorticity). -/
noncomputable def curl (u : Field) : Field :=
  ⟨fun x y z => dy u.u3 x y z - dz u.u2 x y z,
   fun x y z => dz u.u1 x y z - dx u.u3 x y z,
   fun x y z => dx u.u2 x y z - dy u.u1 x y z⟩

/-- Scaling by an amplitude. -/
def smul (A : ℝ) (u : Field) : Field :=
  ⟨fun x y z => A * u.u1 x y z, fun x y z => A * u.u2 x y z, fun x y z => A * u.u3 x y z⟩

end Field

/-- Normalised average over the period cube `[0, 2π]³`. -/
noncomputable def avg (f : ℝ → ℝ → ℝ → ℝ) : ℝ :=
  (∫ x in (0 : ℝ)..2 * π, ∫ y in (0 : ℝ)..2 * π, ∫ z in (0 : ℝ)..2 * π, f x y z) / (2 * π) ^ 3

namespace Field

/-- Energy `E = ½⟨|u|²⟩`. -/
noncomputable def energy (u : Field) : ℝ :=
  avg (fun x y z => u.u1 x y z ^ 2 + u.u2 x y z ^ 2 + u.u3 x y z ^ 2) / 2

/-- Enstrophy `Z = ½⟨|ω|²⟩`. -/
noncomputable def enstrophy (u : Field) : ℝ := u.curl.energy

/-- `⟨|∇u|²⟩`: the sum of the averages of all nine squared partial derivatives. -/
noncomputable def gradSq (u : Field) : ℝ :=
  avg (fun x y z =>
    dx u.u1 x y z ^ 2 + dy u.u1 x y z ^ 2 + dz u.u1 x y z ^ 2 +
    dx u.u2 x y z ^ 2 + dy u.u2 x y z ^ 2 + dz u.u2 x y z ^ 2 +
    dx u.u3 x y z ^ 2 + dy u.u3 x y z ^ 2 + dz u.u3 x y z ^ 2)

/-- `D = ⟨|∇ω|²⟩`, with no factor `½` (so the balance reads `dZ/dt = S − νD`). -/
noncomputable def palin (u : Field) : ℝ := u.curl.gradSq

/-- Vortex stretching `S = ⟨Σᵢⱼ ωᵢ (∂ⱼ uᵢ) ωⱼ⟩`. -/
noncomputable def stretching (u : Field) : ℝ :=
  avg (fun x y z =>
    u.curl.u1 x y z * (dx u.u1 x y z * u.curl.u1 x y z + dy u.u1 x y z * u.curl.u2 x y z +
      dz u.u1 x y z * u.curl.u3 x y z) +
    u.curl.u2 x y z * (dx u.u2 x y z * u.curl.u1 x y z + dy u.u2 x y z * u.curl.u2 x y z +
      dz u.u2 x y z * u.curl.u3 x y z) +
    u.curl.u3 x y z * (dx u.u3 x y z * u.curl.u1 x y z + dy u.u3 x y z * u.curl.u2 x y z +
      dz u.u3 x y z * u.curl.u3 x y z))

end Field

/-- Fourier coefficient on the period cube, wave vector `k ∈ ℤ³`. -/
noncomputable def coeff (f : ℝ → ℝ → ℝ → ℝ) (k : ℤ × ℤ × ℤ) : ℂ :=
  (∫ x in (0 : ℝ)..2 * π, ∫ y in (0 : ℝ)..2 * π, ∫ z in (0 : ℝ)..2 * π,
    (f x y z : ℂ) * Complex.exp (-((k.1 * x + k.2.1 * y + k.2.2 * z : ℝ) : ℂ) * Complex.I)) /
    (2 * π) ^ 3

end Wyrd.PeriodicNS
