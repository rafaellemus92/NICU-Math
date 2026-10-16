import Mathlib

/-!
# Which world is real: what the bedside conditions can identify

The source: "Real life may mix them; the tests are built so a mixture could be
taken apart." This file makes that exact for one response measured in different
bedside conditions (for example, the change in infant heart rate with contact).

A condition switches two paths on or off. The **perceived** path needs mom
present and awake. The **contact** path needs skin-to-skin. The **alike** part
(shared room, shared build) is present in every condition. In the additive
model

  `response = r + p · perceived + q · contact`,

`r` is the alike part, `p` the perceived part and `q` the physical part.

* `alike_explains_any_one_condition`: any result in a single condition is
  reproduced exactly by the pure alike world.
* `two_conditions_never_enough`: for any two conditions, some nonzero mixture
  gives zero response in both.
* `additive_recover`, `additive_identified`: three conditions identify the
  mixture: bedside awake, skin-to-skin awake, skin-to-skin asleep. The sleeping
  mother is what separates `p` from `q`.
* `three_conditions_miss_interaction`, `four_conditions_identify_interaction`:
  if the paths interact (`+ i · perceived · contact`), those three are not
  enough. Adding mom apart (out of the room, or at the bedside asleep)
  completes the 2 × 2 design and identifies everything.

What mathematics cannot do is pick the numbers: `r, p, q, i` come only from
recordings. Additivity itself is an assumption, and the interaction model is the
first relaxation of it.
-/

namespace Wyrd.Limits

/-- A bedside condition: is the perceived path on (`1`) or off (`0`), and is the
contact path on or off? -/
structure Cond where
  perceived : ℝ
  contact : ℝ

/-- The additive response. -/
def resp (r p q : ℝ) (c : Cond) : ℝ := r + p * c.perceived + q * c.contact

/-- The response with an interaction term. -/
def respI (r p q i : ℝ) (c : Cond) : ℝ :=
  r + p * c.perceived + q * c.contact + i * c.perceived * c.contact

/-- Mom at the bedside, awake, no skin-to-skin. -/
def bedsideAwake : Cond := ⟨1, 0⟩
/-- Skin-to-skin, mom awake. -/
def skinAwake : Cond := ⟨1, 1⟩
/-- Skin-to-skin, mom asleep. -/
def skinAsleep : Cond := ⟨0, 1⟩
/-- Mom apart: out of the room, or at the bedside asleep. -/
def apart : Cond := ⟨0, 0⟩

/-- Any single-condition result is reproduced exactly by the pure alike world. -/
theorem alike_explains_any_one_condition (r p q : ℝ) (c : Cond) :
    resp (resp r p q c) 0 0 c = resp r p q c := by
  sorry

/-- Two conditions never identify the mixture. -/
theorem two_conditions_never_enough (c₁ c₂ : Cond) :
    ∃ r p q : ℝ, (r, p, q) ≠ (0, 0, 0) ∧ resp r p q c₁ = 0 ∧ resp r p q c₂ = 0 := by
  sorry

/-- Three conditions recover each part explicitly. -/
theorem additive_recover (r p q : ℝ) :
    p = resp r p q skinAwake - resp r p q skinAsleep ∧
    q = resp r p q skinAwake - resp r p q bedsideAwake ∧
    r = resp r p q bedsideAwake + resp r p q skinAsleep - resp r p q skinAwake := by
  sorry

/-- Three conditions identify the additive mixture. -/
theorem additive_identified {r p q r' p' q' : ℝ}
    (h₁ : resp r p q bedsideAwake = resp r' p' q' bedsideAwake)
    (h₂ : resp r p q skinAwake = resp r' p' q' skinAwake)
    (h₃ : resp r p q skinAsleep = resp r' p' q' skinAsleep) :
    r = r' ∧ p = p' ∧ q = q' := by
  sorry

/-- With an interaction, the same three conditions cannot tell `(1, −1, −1, 1)`
from nothing at all; mom apart can. -/
theorem three_conditions_miss_interaction :
    respI 1 (-1) (-1) 1 bedsideAwake = respI 0 0 0 0 bedsideAwake ∧
    respI 1 (-1) (-1) 1 skinAwake = respI 0 0 0 0 skinAwake ∧
    respI 1 (-1) (-1) 1 skinAsleep = respI 0 0 0 0 skinAsleep ∧
    respI 1 (-1) (-1) 1 apart ≠ respI 0 0 0 0 apart := by
  sorry

/-- The full 2 × 2 design identifies the mixture with interaction. -/
theorem four_conditions_identify_interaction {r p q i r' p' q' i' : ℝ}
    (h₁ : respI r p q i bedsideAwake = respI r' p' q' i' bedsideAwake)
    (h₂ : respI r p q i skinAwake = respI r' p' q' i' skinAwake)
    (h₃ : respI r p q i skinAsleep = respI r' p' q' i' skinAsleep)
    (h₄ : respI r p q i apart = respI r' p' q' i' apart) :
    r = r' ∧ p = p' ∧ q = q' ∧ i = i' := by
  sorry

end Wyrd.Limits
