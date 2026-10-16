import Wyrd.MinimalTable0
import Wyrd.MinimalTable1
import Wyrd.MinimalTable2
import Wyrd.MinimalTable3

/-!
# 4296 is the smallest pangram sum

The theorem combines four facts:

* `lower_bound`: every pangram has `N ≥ 1352`;
* `sum_even`: every pangram has `N` even;
* the tables cover every even `N` from 1352 to 4294 (`tables_cover`), and every
  row passes the search check (`tables_ok`);
* `checkEntry_sound`: a passing row means no pangram has that sum.
-/

set_option maxRecDepth 100000

namespace Wyrd

def tables : List (Nat × List Nat) := table0 ++ table1 ++ table2 ++ table3

theorem tables_ok : tables.all checkEntry = true := by
  simp only [tables, List.all_append, table0_ok, table1_ok, table2_ok, table3_ok, Bool.and_self]

/-- The tables list exactly the sums 1352, 1354, …, 4294. -/
theorem tables_cover : tables.map Prod.fst = (List.range 1472).map (fun i => 1352 + 2 * i) := by
  decide +kernel

/-- **No pangram has a sum below 4296.** -/
theorem no_smaller_pangram {N : Nat} (hN : N < 4296) (ps : List (Nat × Nat)) :
    ¬ IsPangram N ps := by
  intro h
  have h1 := lower_bound h
  have h2 := sum_even h
  -- Find the row for `N`.
  have hmem : N ∈ tables.map Prod.fst := by
    rw [tables_cover]
    exact List.mem_map.mpr ⟨(N - 1352) / 2, List.mem_range.mpr (by omega), by omega⟩
  obtain ⟨⟨N', Lb⟩, hrow, hN'⟩ := List.mem_map.mp hmem
  simp only at hN'
  subst hN'
  exact checkEntry_sound (by omega) (List.all_eq_true.mp tables_ok _ hrow) ps h

/-- **4296 is the smallest sum of a five-pair prime pangram.** A pangram exists
at 4296, and none exists below it. -/
theorem smallest_pangram_sum :
    (∃ ps, IsPangram 4296 ps) ∧ ∀ N < 4296, ∀ ps, ¬ IsPangram N ps :=
  ⟨pangram_exists, fun _ hN ps => no_smaller_pangram hN ps⟩

end Wyrd
