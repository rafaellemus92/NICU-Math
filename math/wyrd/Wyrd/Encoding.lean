/-!
# The coupled base-26 encoding

Every positive number gets a name made of letters A–Z:

* write the number in base 26, digits `d₀ d₁ d₂ …` counted from the units place;
* replace each digit by `aⱼ = (dⱼ + dⱼ₋₁) mod 26` (and `a₀ = d₀`);
* read the result back most-significant first, using 0 = A, …, 25 = Z.

The main result here is `decode_encode`: decoding a name always gives back the
original number. So the encoding is injective (`encode_injective`), which means
two different primes can never share a name.

We work with letter *codes* (numbers 0–25) rather than characters. `name`
renders the codes as a `String` for display.
-/

namespace Wyrd

/-! ## Base-26 digits -/

/-- Base-26 digits of `n`, least significant first. `fuel` bounds the recursion;
`digits` below always passes enough fuel. (Plain structural recursion on fuel
lets the Lean kernel evaluate this, which `decide` needs later.) -/
def digitsAux : Nat → Nat → List Nat
  | 0, _ => []
  | fuel + 1, n => if n = 0 then [] else n % 26 :: digitsAux fuel (n / 26)

/-- Base-26 digits of `n`, least significant first. `digits 0 = []`. -/
def digits (n : Nat) : List Nat := digitsAux n n

/-- Read a list of base-26 digits (least significant first) back into a number. -/
def ofDigits : List Nat → Nat
  | [] => 0
  | d :: ds => d + 26 * ofDigits ds

theorem ofDigits_digitsAux : ∀ fuel n, n ≤ fuel → ofDigits (digitsAux fuel n) = n
  | 0, n, h => by simp [digitsAux, ofDigits]; omega
  | fuel + 1, n, h => by
    by_cases hn : n = 0
    · simp [digitsAux, hn, ofDigits]
    · simp only [digitsAux, hn, ite_false, ofDigits]
      rw [ofDigits_digitsAux fuel (n / 26) (by omega)]
      omega

/-- Digits followed by `ofDigits` is the identity. -/
theorem ofDigits_digits (n : Nat) : ofDigits (digits n) = n :=
  ofDigits_digitsAux n n (Nat.le_refl n)

theorem digitsAux_lt : ∀ fuel n, ∀ d ∈ digitsAux fuel n, d < 26
  | 0, _, d, h => by simp [digitsAux] at h
  | fuel + 1, n, d, h => by
    by_cases hn : n = 0
    · simp [digitsAux, hn] at h
    · simp only [digitsAux, hn, ite_false, List.mem_cons] at h
      rcases h with h | h
      · omega
      · exact digitsAux_lt fuel (n / 26) d h

/-- Every base-26 digit is less than 26. -/
theorem digits_lt (n : Nat) : ∀ d ∈ digits n, d < 26 := digitsAux_lt n n

theorem length_digitsAux_le : ∀ k fuel n, n < 26 ^ k → (digitsAux fuel n).length ≤ k
  | k, 0, n, _ => by simp [digitsAux]
  | 0, fuel + 1, n, h => by
    have : n = 0 := by simp at h; omega
    simp [digitsAux, this]
  | k + 1, fuel + 1, n, h => by
    by_cases hn : n = 0
    · simp [digitsAux, hn]
    · simp only [digitsAux, hn, ite_false, List.length_cons]
      have : n / 26 < 26 ^ k := by rw [Nat.pow_succ] at h; omega
      have := length_digitsAux_le k fuel (n / 26) this
      omega

/-- A number below `26 ^ k` has at most `k` base-26 digits. -/
theorem length_digits_le {n k : Nat} (h : n < 26 ^ k) : (digits n).length ≤ k :=
  length_digitsAux_le k n n h

/-! ## Coupling neighbouring digits -/

/-- Replace each digit by (digit + previous digit) mod 26. `prev` is the digit
to the right of the current one (0 at the units place). -/
def couple (prev : Nat) : List Nat → List Nat
  | [] => []
  | d :: ds => (d + prev) % 26 :: couple d ds

/-- Undo `couple`: subtract the previously recovered digit, mod 26. -/
def uncouple (prev : Nat) : List Nat → List Nat
  | [] => []
  | a :: as => ((a + 26 - prev) % 26) :: uncouple ((a + 26 - prev) % 26) as

theorem uncouple_couple :
    ∀ (ds : List Nat) (prev : Nat), prev < 26 → (∀ d ∈ ds, d < 26) →
      uncouple prev (couple prev ds) = ds
  | [], _, _, _ => rfl
  | d :: ds, prev, hp, hds => by
    have hd : d < 26 := hds d (List.mem_cons_self ..)
    have key : ((d + prev) % 26 + 26 - prev) % 26 = d := by omega
    simp only [couple, uncouple, key]
    rw [uncouple_couple ds d hd (fun x hx => hds x (List.mem_cons_of_mem _ hx))]

theorem length_couple : ∀ (ds : List Nat) (prev : Nat), (couple prev ds).length = ds.length
  | [], _ => rfl
  | _ :: ds, _ => by simp [couple, length_couple ds]

theorem couple_lt : ∀ (ds : List Nat) (prev : Nat), ∀ a ∈ couple prev ds, a < 26
  | [], _, a, h => by simp [couple] at h
  | d :: ds, prev, a, h => by
    simp only [couple, List.mem_cons] at h
    rcases h with h | h
    · omega
    · exact couple_lt ds d a h

/-! ## Names -/

/-- The letter codes (0 = A … 25 = Z) of `n`'s name, most significant first. -/
def encode (n : Nat) : List Nat := (couple 0 (digits n)).reverse

/-- Turn letter codes back into a number. -/
def decode (codes : List Nat) : Nat := ofDigits (uncouple 0 codes.reverse)

/-- **Decoding undoes encoding.** -/
theorem decode_encode (n : Nat) : decode (encode n) = n := by
  simp only [decode, encode, List.reverse_reverse]
  rw [uncouple_couple (digits n) 0 (by decide) (digits_lt n), ofDigits_digits]

/-- **Different numbers get different names.** -/
theorem encode_injective {a b : Nat} (h : encode a = encode b) : a = b := by
  rw [← decode_encode a, h, decode_encode]

/-- A name has exactly as many letters as the number has base-26 digits. -/
theorem length_encode (n : Nat) : (encode n).length = (digits n).length := by
  simp [encode, length_couple]

/-- Every letter code is a real letter (0–25). -/
theorem encode_lt (n : Nat) : ∀ a ∈ encode n, a < 26 := by
  intro a h
  simp only [encode, List.mem_reverse] at h
  exact couple_lt _ _ a h

/-- Numbers below 676 = 26² have names of at most two letters. -/
theorem length_encode_le_two {n : Nat} (h : n < 676) : (encode n).length ≤ 2 := by
  rw [length_encode]; exact length_digits_le (k := 2) h

/-- Numbers below 17576 = 26³ have names of at most three letters. -/
theorem length_encode_le_three {n : Nat} (h : n < 17576) : (encode n).length ≤ 3 := by
  rw [length_encode]; exact length_digits_le (k := 3) h

/-- Render a name as a string, for display. -/
def name (n : Nat) : String :=
  String.ofList ((encode n).map fun k => Char.ofNat (65 + k))

end Wyrd
