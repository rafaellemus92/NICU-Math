import Mathlib

/-!
# Clay alternatives (B) and (D): the quantifiers

(Here "(D)" is Clay's breakdown alternative, not the dissipation `D` of `Field.lean`.)

Abstractly: `Smooth u₀ f` means "the solution from data `u₀` with force `f`
exists and stays smooth for all time"; the zero force is admissible.

* **B**: for every admissible `u₀`, `Smooth u₀ 0`.
* **D**: there exist admissible `u₀` and an admissible force `f` with `¬ Smooth u₀ f`.

Then `¬B → D` (take `f = 0`), but `D` does **not** imply `¬B`: a forced breakdown
is not an unforced one. The model `Smooth u₀ f := (f = 0)` satisfies both B and D.
-/

namespace Wyrd.PeriodicNS

/-- Alternative B. -/
def AltB {Data Force : Type*} (admD : Data → Prop) (zero : Force) (Smooth : Data → Force → Prop) : Prop :=
  ∀ u₀, admD u₀ → Smooth u₀ zero

/-- Alternative D. -/
def AltD {Data Force : Type*} (admD : Data → Prop) (admF : Force → Prop) (Smooth : Data → Force → Prop) : Prop :=
  ∃ u₀ f, admD u₀ ∧ admF f ∧ ¬ Smooth u₀ f

/-- An unforced counterexample to B is a counterexample of type D. -/
theorem not_B_implies_D {Data Force : Type*} (admD : Data → Prop) (admF : Force → Prop) (zero : Force)
    (hzero : admF zero) (Smooth : Data → Force → Prop) :
    ¬ AltB admD zero Smooth → AltD admD admF Smooth := by
  intro hB
  -- A failure of B gives admissible data that is not smooth under the zero force.
  unfold AltB at hB
  push Not at hB
  obtain ⟨u₀, hu₀, hns⟩ := hB
  exact ⟨u₀, zero, hu₀, hzero, hns⟩

/-- **D does not imply ¬B**: a model where both hold (two data-free forces, `0` and `1`;
smooth exactly when unforced). -/
theorem D_and_B_consistent :
    AltB (fun _ : Unit => True) (0 : ℕ) (fun _ f => f = 0) ∧
      AltD (fun _ : Unit => True) (fun f : ℕ => f ≤ 1) (fun _ f => f = 0) := by
  -- B: the unforced solution is smooth by definition; D: the force `1` breaks it.
  exact ⟨fun _ _ => rfl, ⟨(), 1, trivial, le_refl _, one_ne_zero⟩⟩

end Wyrd.PeriodicNS
