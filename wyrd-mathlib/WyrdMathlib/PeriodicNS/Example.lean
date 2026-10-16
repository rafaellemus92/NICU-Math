import WyrdMathlib.PeriodicNS.Field

/-!
# An explicit divergence-free periodic field

`v(x, y, z) = (sin y, sin z, cos x − cos(x + y))`. Each component is independent
of its own coordinate, so `div v = 0`. It is smooth, `2π`-periodic in every
variable, depends on all three coordinates, and its vorticity is
`ω = (sin(x + y) − cos z, sin x − sin(x + y), −cos y)`.
-/

namespace Wyrd.PeriodicNS

open Real

/-- The example field. -/
noncomputable def v : Field :=
  ⟨fun _ y _ => sin y, fun _ _ z => sin z, fun x y _ => cos x - cos (x + y)⟩

/-- **Divergence-free.** -/
theorem div_v (x y z : ℝ) : v.div x y z = 0 := by
  sorry

/-- **The vorticity.** -/
theorem curl_v :
    v.curl.u1 = (fun x y z => sin (x + y) - cos z) ∧
      v.curl.u2 = (fun x y _ => sin x - sin (x + y)) ∧
      v.curl.u3 = (fun _ y _ => -cos y) := by
  sorry

/-- The velocity gradient (Jacobian) entries. -/
theorem grad_v :
    dx v.u1 = (fun _ _ _ => 0) ∧ dy v.u1 = (fun _ y _ => cos y) ∧ dz v.u1 = (fun _ _ _ => 0) ∧
    dx v.u2 = (fun _ _ _ => 0) ∧ dy v.u2 = (fun _ _ _ => 0) ∧ dz v.u2 = (fun _ _ z => cos z) ∧
    dx v.u3 = (fun x y _ => -sin x + sin (x + y)) ∧ dy v.u3 = (fun x y _ => sin (x + y)) ∧
      dz v.u3 = (fun _ _ _ => 0) := by
  sorry

/-- The vorticity gradient entries. -/
theorem grad_curl_v :
    dx v.curl.u1 = (fun x y _ => cos (x + y)) ∧ dy v.curl.u1 = (fun x y _ => cos (x + y)) ∧
      dz v.curl.u1 = (fun _ _ z => sin z) ∧
    dx v.curl.u2 = (fun x y _ => cos x - cos (x + y)) ∧ dy v.curl.u2 = (fun x y _ => -cos (x + y)) ∧
      dz v.curl.u2 = (fun _ _ _ => 0) ∧
    dx v.curl.u3 = (fun _ _ _ => 0) ∧ dy v.curl.u3 = (fun _ y _ => sin y) ∧
      dz v.curl.u3 = (fun _ _ _ => 0) := by
  sorry

/-- `v` is smooth. -/
theorem v_smooth :
    ContDiff ℝ ⊤ (fun p : ℝ × ℝ × ℝ => (v.u1 p.1 p.2.1 p.2.2, v.u2 p.1 p.2.1 p.2.2, v.u3 p.1 p.2.1 p.2.2)) := by
  sorry

/-- `v` is `2π`-periodic in each coordinate. -/
theorem v_periodic (x y z : ℝ) :
    v.u1 (x + 2 * π) y z = v.u1 x y z ∧ v.u1 x (y + 2 * π) z = v.u1 x y z ∧ v.u1 x y (z + 2 * π) = v.u1 x y z ∧
    v.u2 (x + 2 * π) y z = v.u2 x y z ∧ v.u2 x (y + 2 * π) z = v.u2 x y z ∧ v.u2 x y (z + 2 * π) = v.u2 x y z ∧
    v.u3 (x + 2 * π) y z = v.u3 x y z ∧ v.u3 x (y + 2 * π) z = v.u3 x y z ∧ v.u3 x y (z + 2 * π) = v.u3 x y z := by
  sorry

end Wyrd.PeriodicNS
