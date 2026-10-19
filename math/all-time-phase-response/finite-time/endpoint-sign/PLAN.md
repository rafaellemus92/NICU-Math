# Preregistration: time-resolved one-sided remainder at T = 1/4 (written before any run of it)

Target, fixed: the sign of H_b(T) for every 0 < |b| ≤ β = 3/1000, at a = c = d = 1, ν = 1/28,
φ = 37/100, T = 1/4. Decision rule, fixed: the positive sign is certified for the whole range iff

    J2_lo > β² · C_one,TR,                                                              (D)

with J2_lo the lower endpoint from DERIVATION.md Section 2 (variant B, recomputed in the script),
and C_one,TR the one-sided constant below, minimized over the preregistered list
λ ∈ {10², 10⁴, 10⁵, 10⁶, 10⁷} and over the two preregistered self-term bounds (d1), (d2); each
member of these finite families is a valid upper bound, so their minimum is. If (D) fails, report
the two sides of (D) exactly and stop. No other parameter, amplitude or target is changed.

Gate: run only after the independent review of DERIVATION.md Sections 1–4 finds no blocking or major
defect. Numerical cap: five minutes in total for this stage (chain rerun plus postprocessing), hard
timeouts on every process. New output files only; nothing existing is overwritten.

## Inputs (all at f4fe230; no trajectory reads)

- Per-cell chain values, from a generated copy of absorb_chain.py that differs only in paths and in
  logging every cell with exact decimal upper endpoints (scripts/make_chain_percell.py documents the
  four textual patches). Its rows at every 50th cell must equal the committed chain.json log, and
  its final values must equal chain.json; otherwise stop. For cell j (t ∈ I_j = [j/1000,(j+1)/1000]):
  m₁,j, m₂,j (analytic, α at the left endpoint, E₁, E₂ at the right), ε₀,j, ε₁,j, δ_j (cumulative
  ∫₀^{t_{j+1}} ‖Δe‖²), σ_j, N_j ≥ ‖w(t)‖/b², K_j ≥ ‖∇w(t)‖/b² for all t ≤ t_{j+1}. By Lemma M of
  absorption-b003 these bound the quantities for every |b| ≤ β.
- validated.json cell sups p_j, n₁,j, n₂,j. The Lemma B cap g(t) with the global constants exactly as
  route-b-tightening/time_refinement.py. D_r(λ) from time_refinement.final.json (a valid global bound
  on ∫₀ᵀ ‖Δr‖²/b⁶). G and E from z2-endpoint/results/endpoint.json. S = S1 of chain.json.

## Formulas (all quantities scaled as in route-b-dissipation; Δ = 1/1000)

A. Cumulative retained dissipation, from integrating (W)/b⁴ on [0, t_{j+1}] with y(0) = 0 and
   dropping ½y(t_{j+1}) ≥ 0: with Y_i = min(K_i², g(t_{i+1})), a_i = 2m₁,i + 2βn₁,i,
   c_i = (m₂,i + βn₂,i)N_i, q = 2β²C_A²/ν,

       D_w,j = (8/ν)[ Σ_{i≤j} (a_i Y_i + c_i Y_i^{1/2} + (4/ν)σ_i²) Δ + (q K_j² + (4/ν)C_A² ε₁,j²) δ_j ].

   The error-dissipation terms use the cumulative δ_j against the largest K_j, ε₁,j; no cell
   increment of δ or of D_w is ever formed.
B. I∞,j = Â_λ (λ Σ_{i≤j} N_i² Δ + D_w,j) ≥ ∫₀^{t_{j+1}} ‖W‖_∞², Â_λ as in route-b-tightening (B).
C. With E(i,j) = exp(Σ_{k=i..j}(m₁,k − ν)Δ), A_i = p_i K_i + n₁,i N_i, h_i = ε₁,i + βK_i:

       N_r,j = Σ_{i≤j} E(i,j) A_i Δ + C_A E(0,j) K_j (t_{j+1} δ_j)^{1/2} + (Σ_{i≤j} E(i,j)² h_i² Δ)^{1/2} I∞,j^{1/2}.

D. With Q(i,j) = exp(Σ_{k=i..j}(4m₁,k + 1)Δ), Minkowski in L²(Q ds), and a summation by parts
   against the cumulative I∞ with the smallest nonincreasing majorant φ_i = max_{i≤k≤j} Q(k,j)h_k²:

       E_r,j² = Σ_{i≤j} Q(i,j) m₂,i² N_r,i² Δ
                + (1/ν)[ (Σ_{i≤j} Q(i,j)A_i²Δ)^{1/2} + (Q(0,j)C_A²K_j²δ_j)^{1/2} + (Abel_j)^{1/2} ]²,
       Abel_j = φ_j I∞,j + Σ_{i<j} (φ_i − φ_{i+1}) I∞,i.

E. With P_i = exp(Σ_{k≥i}(m₁,k − ν)Δ):

       N̄ = Σ_i P_i (p_i E_r,i + n₁,i N_r,i)Δ + C_A max_i(P_i E_r,i)(Tδ_T)^{1/2}
           + C_A max_i(P_i ε₁,i)(T D_r)^{1/2} + min(d1, d2),
       d1 = (Σ_i P_i² K_i² Δ)^{1/2} I∞,T^{1/2},   d2 = (Σ_i P_i K_i² Δ)^{1/2} (Σ_i P_i X_i bound by summation by parts)^{1/2}.

F. C_one,TR = G N̄ + S E_r,249.  Two-sided C_end,TR = C_one,TR + K_T²/2 is reported for the upper side.

## Implementation checks before the decision

1. Collapse check: the same formulas with every per-cell input and weight replaced by its global
   value, I∞,j by the global I∞ of route-b-tightening, and the per-cell N_r,i, E_r,i by their values
   at T before they are reused, must reproduce route-b-tightening's N_r, E_r, N̄
   (time_refinement.final.json) for each λ.
2. Synthetic checks of the cell sums: a geometric closed form for the E-weighted sum, and the
   summation by parts against a direct sum on synthetic nonnegative data.
3. Monotonicity: every time-resolved quantity at T is at most its global counterpart.

## Status

Sections A–F are a new derivation that the single reviewer of this round does not cover; any
decision from them is conditional and pending its own independent review.

Status update, recorded after the run without changing the preregistered text above: sections A–F
and tr_remainder.py were independently reviewed once and accepted conditionally (REVIEW.md §2).
