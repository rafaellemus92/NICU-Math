import Wyrd.Parity
import Wyrd.MinimalData

/-!
# Toward minimality: a search that is proved complete

Goal: no pangram has a sum below 4296. Already known: `N ≥ 1352`
(`lower_bound`) and `N` is even (`sum_even`). That leaves the 1,472 even sums
`1352, 1354, …, 4294`. For each one, a search shows no pangram exists. This
file defines the search and proves the key fact about it:

> if a pangram with sum `N` existed, the search would find it (`ec_complete`).

So when the search finds nothing, there is nothing (`checkEntry_sound`).

The search is designed for Lean's kernel, which is slow and remembers nothing.
That's why the data in `MinimalData.lean` is precomputed, and why
`MinimalTable*.lean` stores each sum's candidate list. Every piece of that data
is re-checked here or there, so none of it has to be trusted.

## The search

For a sum `N`, a *candidate* is a pair `p < N - p` of possible primes whose
names share no letter. Its *block* is the list of letters in both names.
`ec C used k` asks: can `k` more blocks from `C` cover every letter not in
`used`, with no letter used twice? It always looks at the **lowest** letter `l`
not yet covered. Some block must cover `l`, so it tries each block that
contains `l` and recurses. That keeps the search small.
-/

namespace Wyrd

/-! ## Step 1: candidate primes -/

/-- Fast "no repeated element" check. -/
def nodupB : List Nat → Bool
  | [] => true
  | x :: xs => !xs.contains x && nodupB xs

theorem nodupB_iff : ∀ l : List Nat, nodupB l = true ↔ l.Nodup
  | [] => by simp [nodupB]
  | x :: xs => by
    simp [nodupB, List.nodup_cons, nodupB_iff xs]

/-- `n` has a divisor `d` with `2 ≤ d < n`, `d ≤ 65`. Every composite number
below 4295 has one, since `66² > 4295`. -/
def hasSmallDiv (n : Nat) : Bool := (List.range' 2 64).any fun d => d < n && n % d == 0

/-- `n` certainly can't be in a pangram: too small to be an odd prime, its name
repeats a letter, or it has a small divisor. -/
def rejectB (n : Nat) : Bool := n < 3 || !nodupB (encode n) || hasSmallDiv n

/-- A prime other than 2 with a repeat-free name is never rejected. -/
theorem rejectB_false {n : Nat} (hp : IsPrime n) (h2 : n ≠ 2) (hnd : (encode n).Nodup) :
    rejectB n = false := by
  have h3 : ¬ n < 3 := by have := hp.1; omega
  have hsd : hasSmallDiv n = false := by
    apply Bool.eq_false_iff.mpr
    intro hd
    simp only [hasSmallDiv, List.any_eq_true, List.mem_range'_1, Bool.and_eq_true,
      decide_eq_true_eq, beq_iff_eq] at hd
    obtain ⟨d, ⟨hd2, _⟩, hdn, hmod⟩ := hd
    rcases hp.2 d (Nat.dvd_of_mod_eq_zero hmod) with h | h <;> omega
  simp [rejectB, h3, (nodupB_iff _).mpr hnd, hsd]

/-- The data claims: every number below 4295 is in `VB` or is rejected. -/
theorem VB_complete : (List.range 4295).all (fun n => VB.testBit n || rejectB n) = true := by
  decide +kernel

theorem testBit_VB {n : Nat} (hn : n < 4295) (hp : IsPrime n) (h2 : n ≠ 2)
    (hnd : (encode n).Nodup) : VB.testBit n = true := by
  have := List.all_eq_true.mp VB_complete n (List.mem_range.mpr hn)
  simpa [rejectB_false hp h2 hnd] using this

/-- The list `V` is exactly the set bits of `VB`. -/
theorem V_eq : V = (List.range 4295).filter (fun n => VB.testBit n) := by decide +kernel

theorem mem_V {n : Nat} (hn : n < 4295) (hb : VB.testBit n = true) : n ∈ V := by
  rw [V_eq]; exact List.mem_filter.mpr ⟨List.mem_range.mpr hn, hb⟩

/-! ## Step 2: fast names -/

/-- The packed name of `n`, 16 bits taken from `NT`. -/
def entry (n : Nat) : Nat := (NT >>> (16 * n)) % 65536

/-- Unpack up to three letters, 5 bits each, stored as code + 1 (0 ends the name).
Written without recursion because the kernel evaluates that much faster. -/
def unpack3 (x : Nat) : List Nat :=
  cond (x % 32 == 0) [] <|
  cond (x / 32 % 32 == 0) [x % 32 - 1] <|
  cond (x / 1024 % 32 == 0) [x % 32 - 1, x / 32 % 32 - 1]
    [x % 32 - 1, x / 32 % 32 - 1, x / 1024 % 32 - 1]

def nameOf (n : Nat) : List Nat := unpack3 (entry n)

theorem nameOf_all : (List.range 4295).all (fun n => nameOf n == encode n) = true := by
  decide +kernel

/-- The table agrees with `encode` everywhere below 4295. -/
theorem nameOf_eq {n : Nat} (hn : n < 4295) : nameOf n = encode n := by
  have := List.all_eq_true.mp nameOf_all n (List.mem_range.mpr hn)
  simpa using this

/-! ## Step 3: candidates and the search -/

/-- Candidates for sum `N`, each packed as `entry p + 65536 · entry (N - p)`. -/
def cands (N : Nat) : List Nat :=
  V.filterMap fun p =>
    cond (decide (2 * p < N) && VB.testBit (N - p) && nodupB (nameOf p ++ nameOf (N - p)))
      (some (entry p + 65536 * entry (N - p))) none

/-- The letters of a packed candidate. -/
def unblock (x : Nat) : List Nat := unpack3 (x % 65536) ++ unpack3 (x / 65536)

theorem unblock_pack (p q : Nat) :
    unblock (entry p + 65536 * entry q) = nameOf p ++ nameOf q := by
  have h : entry p < 65536 := Nat.mod_lt _ (by decide)
  have h1 : (entry p + 65536 * entry q) % 65536 = entry p := by omega
  have h2 : (entry p + 65536 * entry q) / 65536 = entry q := by omega
  simp only [unblock, nameOf, h1, h2]

/-- Can `k` more blocks from `C` exactly cover the letters missing from `used`? -/
def ec (C : List (List Nat)) : List Nat → Nat → Bool
  | used, 0 => used.length == 26
  | used, k + 1 =>
    match (List.range 26).find? (fun i => !used.contains i) with
    | none => false
    | some l => C.any fun c => c.contains l && c.all (fun x => !used.contains x) && ec C (used ++ c) k

/-- One table row `(N, Lb)` passes if `Lb` is exactly the candidate list for `N`
and the search over it finds nothing. -/
def checkEntry (e : Nat × List Nat) : Bool :=
  cands e.1 == e.2 && !ec (e.2.map unblock) [] 5

/-! ## Step 4: the search is complete -/

/-- **If `k` non-empty blocks `S` exactly cover what `used` is missing, and
every block of `S` is (a rearrangement of) one in `C`, then `ec` returns
`true`.**

By induction on `k`. Since `used` plus the blocks of `S` is a rearrangement of
`0…25`, there are no repeats. Let `l` be the lowest missing letter. Some block
`s ∈ S` contains `l`, and its copy `c ∈ C` contains `l` and avoids `used`, so
`ec` tries `c`. Then the induction hypothesis applies to `used ++ c` and the
other `k - 1` blocks. -/
theorem ec_complete (C : List (List Nat)) :
    ∀ (k : Nat) (used : List Nat) (S : List (List Nat)),
      S.length = k → (∀ s ∈ S, s ≠ [] ∧ ∃ c ∈ C, c.Perm s) →
      (used ++ S.flatten).Perm (List.range 26) → ec C used k = true
  | 0, used, S, hlen, _, hperm => by
    have hS : S = [] := List.eq_nil_of_length_eq_zero hlen
    subst hS
    simp only [List.flatten_nil, List.append_nil] at hperm
    simp [ec, hperm.length_eq]
  | k + 1, used, S, hlen, hS, hperm => by
    have hnd : (used ++ S.flatten).Nodup := hperm.nodup_iff.mpr List.nodup_range
    have hdisj := (List.nodup_append.mp hnd).2.2
    unfold ec
    split
    next hnone =>
      -- Every letter is in `used`, but `S` has a non-empty block: a repeat.
      exfalso
      obtain ⟨s, hs⟩ : ∃ s, s ∈ S := by
        cases S with
        | nil => simp at hlen
        | cons s _ => exact ⟨s, List.mem_cons_self ..⟩
      obtain ⟨x, hx⟩ := List.exists_mem_of_ne_nil s (hS s hs).1
      have hxflat : x ∈ S.flatten := List.mem_flatten.mpr ⟨s, hs, hx⟩
      have hxr : x ∈ List.range 26 := hperm.subset (List.mem_append_right _ hxflat)
      have hxu : x ∈ used := by
        have := List.find?_eq_none.mp hnone x hxr
        simpa [List.contains_iff_mem] using this
      exact hdisj x hxu x hxflat rfl
    next l hl =>
      have hlu : l ∉ used := by
        have := List.find?_some hl
        simpa [List.contains_iff_mem] using this
      have hlflat : l ∈ S.flatten := by
        rcases List.mem_append.mp (hperm.symm.subset (List.mem_of_find?_eq_some hl)) with h | h
        · exact absurd h hlu
        · exact h
      obtain ⟨s, hs, hls⟩ := List.mem_flatten.mp hlflat
      obtain ⟨_, c, hc, hcs⟩ := hS s hs
      rw [List.any_eq_true]
      refine ⟨c, hc, ?_⟩
      simp only [Bool.and_eq_true]
      refine ⟨⟨List.contains_iff_mem.mpr (hcs.symm.subset hls), ?_⟩, ?_⟩
      · rw [List.all_eq_true]
        intro x hx
        have hxflat : x ∈ S.flatten := List.mem_flatten.mpr ⟨s, hs, hcs.subset hx⟩
        have : x ∉ used := fun hxu => hdisj x hxu x hxflat rfl
        simpa [List.contains_iff_mem] using this
      · apply ec_complete C k (used ++ c) (S.erase s)
        · rw [List.length_erase_of_mem hs]; omega
        · exact fun t ht => hS t (List.mem_of_mem_erase ht)
        · have h1 : S.flatten.Perm (s ++ (S.erase s).flatten) := by
            simpa using (List.perm_cons_erase hs).flatten
          have h2 : ((used ++ c) ++ (S.erase s).flatten).Perm (used ++ S.flatten) := by
            rw [List.append_assoc]
            exact List.Perm.append_left _ ((hcs.append_right _).trans h1.symm)
          exact h2.trans hperm

/-! ## Step 5: every pangram pair is a candidate -/

/-- A candidate in sorted order `p < q`. -/
theorem mem_cands {N p q : Nat} (hN : N ≤ 4294) (hs : p + q = N) (hlt : p < q)
    (hp : IsPrime p) (hq : IsPrime q) (hp2 : p ≠ 2) (hq2 : q ≠ 2)
    (hnd : (encode p ++ encode q).Nodup) :
    ∃ x ∈ cands N, unblock x = encode p ++ encode q := by
  have hpn : (encode p).Nodup := (List.nodup_append.mp hnd).1
  have hqn : (encode q).Nodup := (List.nodup_append.mp hnd).2.1
  have hNp : N - p = q := by omega
  have hnp : nameOf p = encode p := nameOf_eq (by omega)
  have hnq : nameOf q = encode q := nameOf_eq (by omega)
  refine ⟨entry p + 65536 * entry q, ?_, by rw [unblock_pack, hnp, hnq]⟩
  apply List.mem_filterMap.mpr
  refine ⟨p, mem_V (by omega) (testBit_VB (by omega) hp hp2 hpn), ?_⟩
  have hcond : 2 * p < N := by omega
  simp [hNp, hcond, testBit_VB (show q < 4295 by omega) hq hq2 hqn, hnp, hnq,
    (nodupB_iff _).mpr hnd]

/-- Every pair in a pangram shows up among the candidates, in one order or the other. -/
theorem pair_in_cands {N : Nat} {ps : List (Nat × Nat)} (h : IsPangram N ps) (hN : N ≤ 4294)
    (pq : Nat × Nat) (hpq : pq ∈ ps) :
    ∃ x ∈ cands N, (unblock x).Perm (encode pq.1 ++ encode pq.2) := by
  -- Facts about the pair.
  have hblock : (encode pq.1 ++ encode pq.2).Nodup := by
    refine List.Nodup.sublist ?_ (nodup_letters h)
    rw [letters, List.flatMap_def]
    exact List.sublist_flatten_of_mem (List.mem_map.mpr ⟨pq, hpq, rfl⟩)
  have hmem1 : pq.1 ∈ primesOf ps := List.mem_flatMap.mpr ⟨pq, hpq, by simp⟩
  have hmem2 : pq.2 ∈ primesOf ps := List.mem_flatMap.mpr ⟨pq, hpq, by simp⟩
  have h21 : pq.1 ≠ 2 := fun e => two_not_mem h (e ▸ hmem1)
  have h22 : pq.2 ≠ 2 := fun e => two_not_mem h (e ▸ hmem2)
  have hne := pair_ne ps (primes_nodup h) pq hpq
  have hs := h.sums pq hpq
  obtain ⟨hp1, hp2⟩ := h.primes pq hpq
  rcases Nat.lt_or_gt_of_ne hne with hlt | hgt
  · obtain ⟨x, hx, hu⟩ := mem_cands hN hs hlt hp1 hp2 h21 h22 hblock
    exact ⟨x, hx, hu ▸ List.Perm.refl _⟩
  · -- Stored the other way round: same letters, swapped names.
    obtain ⟨x, hx, hu⟩ := mem_cands hN (by omega) hgt hp2 hp1 h22 h21
      (List.perm_append_comm.nodup_iff.mp hblock)
    exact ⟨x, hx, hu ▸ List.perm_append_comm⟩

/-- **If a table row for `N` passes, there is no pangram with sum `N`.** -/
theorem checkEntry_sound {N : Nat} {Lb : List Nat} (hN : N ≤ 4294)
    (hc : checkEntry (N, Lb) = true) (ps : List (Nat × Nat)) : ¬ IsPangram N ps := by
  intro h
  simp only [checkEntry, Bool.and_eq_true, beq_iff_eq, Bool.not_eq_true'] at hc
  obtain ⟨hL, hec⟩ := hc
  subst hL
  have := ec_complete ((cands N).map unblock) 5 [] (ps.map fun pq => encode pq.1 ++ encode pq.2)
    (by simp [h.five]) ?_ ?_
  · rw [this] at hec; contradiction
  · intro s hs
    obtain ⟨pq, hpq, rfl⟩ := List.mem_map.mp hs
    refine ⟨?_, ?_⟩
    · have := encode_ne_nil (n := pq.1) (by have := (h.primes pq hpq).1.1; omega)
      simp [this]
    · obtain ⟨x, hx, hperm⟩ := pair_in_cands h hN pq hpq
      exact ⟨unblock x, List.mem_map.mpr ⟨x, hx, rfl⟩, hperm⟩
  · have : (ps.map fun pq => encode pq.1 ++ encode pq.2).flatten = letters ps := by
      simp [letters, List.flatMap_def]
    rw [List.nil_append, this]
    exact h.alphabet

end Wyrd
