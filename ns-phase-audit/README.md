# Audit of the periodic Navier–Stokes phase lab

Independent checks of ChatGPT's `periodic_ns_lab_v2` package (not stored here). Also shipped as a ZIP for a direct comparison. Contents:

| Folder | What it is |
|---|---|
| `audit_v2/AUDIT.md` | **Start here.** The audit of `periodic_ns_lab_v2`: a PASS/FAIL/UNPROVEN table for every item of your `CLAUDE_HANDOFF.md` and every `RESULTS.md` headline. |
| `audit_v2/exact/` | An independent exact (rational) Taylor-series code with **symbolic ν** and general amplitudes, written without reading your code. Orders up to 12. |
| `audit_v2/float/` | An independent FFT/float Taylor-series code (double and long double), with DFTs in φ, ν and the amplitudes, up to order 12. |
| `audit_v2/dns/` | An independent pseudo-spectral DNS: fixed-dt RK4, the same cube cutoff `K = ⌊(N−1)/3⌋`, tangent (φ-variation) equations, N = 24…96. |
| `audit_v2/code_audit/` | Our checks run against your code: formal-ν jet, symmetry, generic variation checks, and the re-run script. |
| `audit_v2/xcheck/` | Cross-comparisons between the lines above and your outputs. |
| `checks_v1/nslab_check.py` | Our earlier FFT re-derivation of the v1 exact identities. |
| `../wyrd-mathlib/` | The Lean 4 + Mathlib project. `WyrdMathlib/PeriodicNS/` is the Navier–Stokes part. |

Repository: `github.com/rafaellemus92/sgrounds`, branch `claude/new-session-sbrl43`, folder `experiments/`.
It may be private; the user decides whether to share it.

## Same problem, same conventions

- Equation: unforced 3D incompressible NS on `[0,2π]³`.
- Averages: normalised volume averages.
- Quantities: `E = ½⟨|u|²⟩`, `Z = ½⟨|ω|²⟩`, `D = ⟨|∇ω|²⟩` and `S = ⟨ω·(ω·∇)u⟩`.
- Viscosity: `ν = 1/28`.
- Initial data: `u_φ = (sin y, sin z, cos x − cos(x+y+φ))`. The audit generalises it to amplitudes `(α sin y, β sin z, γ cos x − δ cos(x+y+φ))`.

Everything both sides compute agrees.

## New results beyond your package (details in `AUDIT.md` §4)

1. **Your order-6 identity is confirmed exactly, with ν kept symbolic.** `[t⁶] Z ∋ −(6487/1555200) cos 2φ`, and its ν¹…ν⁶ coefficients are identically 0. Your seven-node jets match ours by `Fraction` equality.
2. **Why the harmonic appears exactly at order 6, and why its coefficient is ν-free.** The proof is at the level of the Taylor recurrence:
   - **P1, a 2D-3C structure.** If `β = 0` (no `sin z` mode), the flow stays z-independent. The in-plane part is `α e^{−νt} sin y` exactly, and `u₃` evolves *linearly*, conserving `k_x`. Hence `Z` contains only `1, cos φ` at **every** order, so every harmonic `|m| ≥ 2` needs the `sin z` mode.
   - **P2, counting.**
     - Per-axis wave-vector balance gives `#α, #γ, #δ ≥ |m|` (each with the parity of `m`) and `#β` even; with P1, `#β ≥ 2`.
     - The grading is `amplitude degree + ν-power = n + 2`.
     - So `|m| ≥ 2` cannot appear before `n = 3|m|`. At that order it is ν-independent and proportional to `α^|m| β² γ^|m| δ^|m|`.
3. **Predictions from P2, all confirmed exactly:**
   - `[t⁷] cos 2φ = (207269/7257600) ν`: exactly linear in ν, so **zero for Euler**. This is the 7th-order polynomial.
   - `cos 3φ` first appears at `t⁹`: `z_{9,3} = −21381938959/211843247616000`, ν-free.
   - `cos 4φ` first appears at `t¹²`.
   - With `β = 0`, no `|m| ≥ 2` term occurs through order 16.
4. **Your item 8:** the order-6 value is a near-cancellation. The `{2,4}` pair contributes `+103/6912` and the `{3,3}` pair `−433/27648`; six shells contribute. No small interaction set explains the *value*, only its *existence and form*.
5. **Numerics reproduced independently, to about 8 decimals.** The 9th decimals depend on your CFL-adaptive RK4.
   - The curvature crossing at `T ≈ 1.764994` is robust in `N`, `dt` and `h`. Your linear-interpolant values run about `1.8e−5` early.
   - The `T = 2` optimum converges to `φ* ≈ 0.970364` (at 64³).
6. **Bugs and precision issues found:**
   - Bare `pytest -q` fails to collect two test files.
   - `--dt` is ignored in `optimize`.
   - `exact_viscosity_invariant.py` can overwrite the archived certificate.
   - Some counts are hard-coded.
   - Two CSVs have no generating script.
   - The 48³, T = 2 relative-Z rows are contaminated by a time-step mismatch (1–2.5%).

   No mathematical error and no wrong headline number was found.

## The Lean side

`../wyrd-mathlib/WyrdMathlib/PeriodicNS/` holds proved theorems about given fields at `t = 0`. It does not contain NS solution theory.

- **Proved, for `v = u_0`:** `E = 1`, `Z = 5/4`, `D = 7/2`, `S = 1/4`. Derivatives come from Lean `deriv`, and averages are genuine integrals.
- **Proved, sign flip:** `±A v` share `E`, `Z`, `D` and every Fourier magnitude, but `S = ±A³/4` (`no_closure`, `no_spectral_closure`).
- **Also proved:** a Galerkin cutoff bound, a variable-coefficient Grönwall lemma, and the Clay B/D quantifier logic.
- **Statements only, proofs in progress.** These files still contain `sorry` and are **not** part of the default build:
  - `PeriodicNS/PhaseFamily.lean`: `S(u_φ) = cos φ/4`, with `E, Z, D` independent of φ.
  - `PeriodicNS/PhaseSymmetry.lean`: your rotation-plus-translation map sends `u_φ` to `u_{−φ}`.
  - `PeriodicNS/SelectionRules.lean`: the arithmetic core of P2.
  - `Limits/*.lean`: a separate project on the Shared Air model's limits.

No time-dependent claim (Taylor jets, simulations) is a Lean theorem.

## Running

- Each `audit_v2/<line>/` script is run **from its own folder**, with python3 + numpy (sympy only for `code_audit/symmetry_sympy.py`).
- Scripts that read your package expect it at `./periodic_ns_lab_v2`, next to `audit_v2/`. Run them with `python3 -I`.
- The full command list is in `AUDIT.md` §8. Large re-run outputs and all `.npz` arrays are not included; the scripts regenerate them.

Lean: `cd ../wyrd-mathlib && lake exe cache get && lake build && lake env lean Audit.lean`. This needs Lean 4.35.0 and Mathlib v4.35.0, and `../wyrd` must sit next to it.

## Still open, on both sides

- A cutoff-uniform (continuum) estimate. `AUDIT.md` §7.1 gives the a-posteriori route that would turn the rankings into theorems.
- A remainder bound for the Taylor jet at `t = 2` or `t = 4`.
- A global optimality certificate in φ.
- A proof that the leading `|m|` coefficient is nonzero for `|m| ≥ 5`.
