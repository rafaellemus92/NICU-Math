# Endpoint sign of H_b(T): derivation of the first-stage enclosure (scripts/sign_enclosure.py)

Status: new derivation, pending one independent review. Fixed scope, not to be changed after results:
a = c = d = 1, ν = 1/28, φ = 37/100, T = 1/4, β = 3/1000, and the target is the sign of

    H_b(T) := Z(u_b(T)) − Z(U(T)) − b² e^{−2νT}/4      for every 0 < |b| ≤ β,

with Z(f) = ½‖∇f‖² on the normalized 2π-torus. The term b² e^{−2νT}/4 is the enstrophy of the
initial perturbation b sin z e_y under pure heat decay (|k| = 1). Inputs are files at f4fe230 under
`finite-time/`; no trajectory is read by this stage.

## 0. Decomposition

With q₁, q₂ the first and second b-coefficients (q₂ = half the second derivative), V := z-mean of q₂,
E := ½‖∇q₁(T)‖², M := ⟨−ΔU(T), V(T)⟩, Z2 := E + M, R_Z := Z(u_b) − Z(U) − b² Z2 (all at t = T):

    H_b/b² = J2 + R_Z/b²,      J2 := Z2 − e^{−2νT}/4 = (E − e^{−2νT}/4) + M.               (0)

J2 does not depend on b. E is enclosed in z2-endpoint/results/endpoint.json (exact rational endpoint
sum and the inherited H¹ error ε₁).

## 1. Time-weighted propagator for the mean field (new)

V solves L_U V = −F, V(0) = 0, F := z-mean of P[(q₁·∇)q₁]; V and F have zero spatial mean
(source-only-hull NOTE §1). Pairing with V, using ⟨(U·∇)V, V⟩ = 0, |⟨(V·∇)U, V⟩| ≤ m₁(t)‖V‖² with
m₁(t) ≥ ‖∇U(t)‖_∞, and Poincaré ‖∇V‖ ≥ ‖V‖:

    d⁺/dt ‖V‖ ≤ (m₁(t) − ν)‖V‖ + ‖F(t)‖,   so   ‖V(T)‖ ≤ ∫₀ᵀ exp(∫ₛᵀ (m₁ − ν)) ‖F(s)‖ ds.     (1)

Cells I_ℓ = [ℓΔ, (ℓ+1)Δ], Δ = 1/1000, ℓ = 0..249. The parent's analytic bound
m₁(t) = (α(t)² + γ² + γ₁(t)²)^{1/2}, α = |a|e^{−νt}, γ = |c| + |d| = 2, γ₁ = |d| + |a|γE₁(t) = 1 + 2E₁(t),
E₁(t) = (1 − e^{−νt})/ν, has α decreasing and E₁ increasing, so on I_j

    m₁(t) ≤ m₁,j := (e^{−2νjΔ} + 4 + (1 + 2E₁((j+1)Δ))²)^{1/2},   and  m₁,j > ν.

For s ∈ I_ℓ the integrand m₁ − ν is positive on [ℓΔ, T], hence
∫ₛᵀ (m₁ − ν) ≤ Σ_{j ≥ ℓ} (m₁,j − ν)Δ =: τ_ℓ, and τ_ℓ ≤ τ₀. Splitting F = F_N + (F − F_N), with
U_ℓ ≥ sup_{I_ℓ} ‖F_N‖ the rigorous hull bounds of source-only-hull/results/full.json and
ΔF ≥ ∫₀ᵀ ‖F − F_N‖ (source-only-hull NOTE, ΔF = T(n₁ε₀ + pε₁) + C_A ε₁ (Tδ)^{1/2}):

    ‖V(T)‖ ≤ Σ_ℓ e^{τ_ℓ} Δ U_ℓ + e^{τ₀} ΔF.                                             (2)

The q₁ error forcing enters only through the total ΔF, multiplied by the largest factor e^{τ₀}; no
per-cell split of ΔF and no per-cell use of the cumulative dissipation δ is made. Then

    |M| ≤ G ‖V(T)‖,   G ≥ ‖ΔU(T)‖ (z2-endpoint/results/endpoint.json, base_true_laplacian_upper).   (3)

The source-only-hull note instead used ‖V(T)‖ ≤ e^{(M₁−ν)T}(L_N + ΔF) with the constant M₁ = m₁ at T.

## 2. Enclosure of J2

    J2 ∈ [E_lo − e^{−2νT}/4 − |M|_up,  E_hi − e^{−2νT}/4 + |M|_up].                           (4)

## 3. One-sided remainder (positive direction)

Exact identity (route-b-dissipation NOTE §4), with w = v − b q₁, r = w − b² q₂, r̄ its z-mean:

    R_Z = ⟨−ΔU, r̄⟩ + b⟨∇q₁, ∇r⟩ + ½‖∇w‖².                                                (5)

With ‖r̄(T)‖ ≤ b⁴ N̄, ‖∇r(T)‖ ≤ |b|³ E_r, ‖∇q₁(T)‖ ≤ S, ‖∇w(T)‖ ≤ b² K (route-b-tightening
time_refinement.final.json at λ = 10⁶; S, K from absorption-b003 chain.json), valid for every |b| ≤ β:

    R_Z ≥ −b⁴ C_one,  C_one := G' N̄ + S E_r     (the last term of (5) is ≥ 0 and is dropped),
    |R_Z| ≤ b⁴ C_end, C_end := G' N̄ + S E_r + K²/2,   G' = 1.8534 ≥ G.                       (6)

## 4. Consequences

    J2_lo − b² C_one ≤ H_b/b² ≤ J2_hi + b² C_end,     0 < |b| ≤ β.                          (7)

If J2_lo > 0 then H_b > 0 for every 0 < |b| < b* := (J2_lo/C_one)^{1/2}, strictly, provided b* ≤ β
so that (6) applies. The fixed target needs J2_lo > β² C_one. At b = 0, H_b = 0.

## Inherited assumptions

The absorption certificate at 419e6c3 (ε₀, ε₁, δ, ε_W, S, N_w, K, Lemma M, closure); the parent note
at cd9c9f0 (C_A, analytic base-flow bounds, (I1)–(I6), mean-zero Agmon); the Route B and tightening
derivations and the endpoint enclosure as audited at f4fe230; the source-only hull enclosure; IEEE
binary64 round-to-nearest with gradual underflow in NumPy; correct Python decimal and mpmath interval
arithmetic.
