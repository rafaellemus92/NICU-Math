# wyrd — machine-checked proofs

A [Lean 4](https://lean-lang.org) project that proves facts about the prime
pangram from [`../coupled_prime26_pangram.py`](../coupled_prime26_pangram.py).
Here no step is taken on trust: the Lean kernel checks every inference.

## What is proved

| Theorem | Statement | File |
|---|---|---|
| `decode_encode` | Decoding a name gives back the number | `Wyrd/Encoding.lean` |
| `encode_injective` | Different numbers get different names | `Wyrd/Encoding.lean` |
| `solution_names` | The five pairs are named `UKR TEP DB NMF YL AQV SH CWZ IJ OGX` | `Wyrd/Pangram.lean` |
| `solution_isPangram` | Those ten numbers are prime, each pair sums to 4296, and every letter appears exactly once | `Wyrd/Pangram.lean` |
| `lower_bound` | **Any** five-pair prime pangram has sum ≥ 1352 | `Wyrd/Pangram.lean` |

`Audit.lean` prints the axioms each theorem rests on. They are only Lean's
standard ones: no `sorry` (an unfinished proof) and no `native_decide`
(trusting compiled code instead of the kernel). CI fails if either appears.

What's next is in [`ROADMAP.md`](ROADMAP.md).

## Running it

**Without installing anything:** push a change. The *Lean proofs* GitHub
Action rebuilds everything and runs the audit. A green check means every proof
was accepted. You can also paste a file into <https://live.lean-lang.org>.

**On a computer:**

```sh
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
cd experiments/wyrd
lake build                 # checks every proof (~10 s)
lake env lean Audit.lean   # lists the axioms used
```

For editing, use VS Code with the *Lean 4* extension. Put the cursor inside a
proof to see the goal that is still open.

## How to read a proof

- `theorem name : statement := by tactics`: the tactics transform the goal
  until nothing is left.
- `omega` settles linear arithmetic over whole numbers, including `/` and `%`
  by constants. Most of the arithmetic here is done by it.
- `decide +kernel` makes the kernel evaluate a true/false computation, such as
  trial division up to 4243. It is slow but fully trusted.
- `simp` rewrites with known lemmas. `induction` and pattern-matching
  definitions (`| [] => … | d :: ds => …`) are proof by induction.

## Notes

- This uses core Lean only, with no Mathlib, so it builds in seconds. Mathlib
  (Lean's maths library) will be needed for deeper number theory. Adding it is
  one line in `lakefile.toml`.
- `IsPrime` is defined here because core Lean has none. `primeB_sound` proves
  that the fast checker agrees with the definition.
