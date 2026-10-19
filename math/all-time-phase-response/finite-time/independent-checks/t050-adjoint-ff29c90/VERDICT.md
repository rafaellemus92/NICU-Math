# Audit of the T = 1/2 adjoint certificate (ff29c90e)

Auditor: Claude, session "Navier Stokes-Speech", 19 October 2026. This is an AI audit, not human refereeing or
formal verification. The first input was the single bundle `nicu-t050-adjoint-certificate-v1-2026-10-19-ff29c90.zip`
(SHA-256 b3e19ce0…a58143a). All 60 files listed in its MANIFEST.json match, and all 60 are byte-identical to the
reconstructed commit (see VERDICT_ADDENDUM.md). Audited head: ff29c90e139ab34241d09070aa9316106f5247a1.
I made no edits to the audited sources, did no merges, called no reviewers and ran no simulations. The only
computations were postprocessing of stored enclosures, about 7 s per full set.

Revision of 19 October 2026 (preserved version):
- the sensitivity figures are now stated as one-at-a-time hypotheticals, not error allowances;
- the checker now records unrounded intermediates, and the reconciliation with the committed bound is added
  (section B2);
- paths refer to this folder.

Claim audited: H_b(1/2) ≥ 0.00328934052060975 · b² for every 0 < |b| ≤ 0.003, with a = c = d = 1, ν = 1/28 and
φ = 37/100 (t050-adjoint/PROOF.md lines 13 and 176–177).

## Verdict

**Not disproved.** I found no error in the reduction from the inherited enclosures to the claimed inequality. I
re-derived the adjoint lemma and its constants from the equations. I reproduced the final comparison with independent
code in different arithmetic (40-digit directed decimal intervals, not mpmath):

    C ≤ 848.2334460880,  β²C ≤ 0.0076341010148,  J2 ≥ 0.010923441604609,  H_b(1/2)/b² ≥ 0.0032893405898 > 0.

The committed C ≤ 848.2334537777 and H/b² ≥ 0.0032893405206 are slightly more conservative than mine. The whole
difference comes from one place: the committed gradient term uses ε₁(T) rounded up to 5 significant digits
(section B2). The claimed constant is therefore valid as stated.

The claim is **conditional**. The rigorous statement requires every inherited enclosure to be a valid bound in its
stated direction; nothing below relaxes that. Three of them were computed from the 546 MB trajectory arrays and could
not be recomputed from the bundle:
- the source-hull row bounds U_i;
- the base Laplacian bound G;
- the endpoint energy E.

The validated residual enclosures for t ∈ (1/4, 1/2] come from the T = 1/2 validator run. The addendum shows that
code to be the reviewed T = 1/4 code with horizon constants changed; the run itself still needs the arrays to replay.

As a **hypothetical sensitivity test** (section 8 of the log), I changed one input at a time with all others held
fixed. This is not an allowed error and not evidence that any input is wrong. The final comparison would remain
positive under:
- a 2.45 % increase of all U_i;
- a 2.34 % increase of G;
- a decrease of 0.00329 in E's lower end.

These inputs carry the least slack. By the same test, the nonself term could rise 52 %, ∫N² by a factor of about 9,
and the strain constant to about 2500.

## A. Arguments checked analytically, from the equations

References are to t050-adjoint/PROOF.md (P) and t050-tightening/DERIVATION.md (D).

1. **Adjoint equation, signs, time reversal (P lines 22–37).** L_U X = X_t − νΔX + P[(U·∇)X + (X·∇)U]. Transport is
   skew. ⟨(X·∇)U, Z⟩ = ⟨X, (∇U)ᵀZ⟩ with ((∇U)ᵀZ)_j = Σ_i ∂_jU_i Z_i. So L_U*Z = 0 is
   −Z_t = νΔZ + P[(U·∇)Z − (∇U)ᵀZ]. With Z divergence-free and X(0) = 0, d⟨X,Z⟩/dt = ⟨F, ∇Z⟩ for L_U X = −P div F.
   In τ = T − t the problem is forward and dissipative. Z(T) = −ΔU(T) produces ⟨−ΔU(T), X(T)⟩. The self bound is an
   absolute value, so it uses only the magnitude of the terminal datum, never its sign.
2. **Pressure and Leray (P lines 89–92, 109–121).** Z has k_z = 0. P acts as the 2D projector on h and as the identity
   on v. The curl removes the gradient part. Components of (∇U)ᵀZ: x gives w_x v; y gives σ_y h1 + w_y v; z gives 0.
   This yields v_τ = νΔv + σv_x and h_τ = νΔh + P₂[σh_x − e_y σ_y h1 − v∇w]. η_τ has homogeneous part σ η_x − 2σ_y ∂_x h1
   and forcing w_x v_y − w_y v_x. I derived each term by hand.
3. **Preserved Fourier supports.** q₁ lives on k_z = ±1, q₂ on {0, ±2}, U and Z on k_z = 0. v has k_x = ±1 and h has
   k_x ∈ {0, ±2} (terminal data k_x = 0, forcing ±1 × ±1, coefficients depending on y only). The mean of
   B(q₁, q₂) vanishes by parity, which gives P's mean equation and the X/Y split.
4. **Wiener moments (P lines 53–81).** The shift coefficients are e^{−νt}/2 per neighbour, and
   (|m+1|^j + |m−1|^j)/2 ≤ (|m|+1)^j gives D⁺M_j ≤ Σ binom(j,l) M_l. Initial moments (2,1,1,1) from
   W(y,0) = 1 − e^{i(y+φ)}. The polynomial majorants solve the cooperative system with equality (checked symbolically).
   The real-harmonic normalization adds no factor 2.
5. **Vertical and vorticity bounds, and 274 (P lines 94–145).** B₀(0) ≤ M₀ + M₂ and B₁(0) ≤ M₁ + M₃ give
   B₀ ≤ 275/18 and B₁ ≤ 1225/36. The Biot–Savart factor max |k_x k_y|/(k_x²+k_y²) = 1/2 is attained at |k_x| = |k_y| = 2.
   Then L′ ≤ 3L + F, L(0) ≤ e^{−νT} ≤ 1, F ≤ 8875/54, L ≤ 18155/81, and ‖∇h‖_F ≤ Σ|k||ĥ| = L. Finally
   ‖sym ∇Z‖_op ≤ ‖∇Z‖_F ≤ L + B₀ + B₁ = 88595/324 < 274. The majorants are increasing, so the bound holds uniformly on
   [0, 1/2]. With the exact Taylor bound for e^{1/2} instead of 5/3, the same chain gives 237.38.
6. **Pairing (P lines 38–46).** F = z-average of W_b⊗W_b is symmetric positive semidefinite, and ∇Z does not depend
   on z. So |⟨F, ∇Z⟩| ≤ ‖sym∇Z‖_op,∞ · avg tr F = ‖sym∇Z‖ · ‖W_b‖². Averages are normalized, so there is no volume
   factor. Z(T) = −ΔU(T) already carries the observable, so no factor G belongs on this term.
7. **Normalization and powers of b.** u_b = U + bq₁ + w and r = w − b²q₂. Expanding gives
   H_b = b²J2 + ⟨−ΔU, r̄⟩ + b⟨∇q₁,∇r⟩ + ½‖∇w‖², with J2 = ½‖∇q₁‖² − e^{−2νT}/4 + ⟨−ΔU, q̄₂⟩. Each remaining piece
   scales as b⁴: r̄ = b⁴(X + Y) with W_b = w/b² and R = r/b³, and b⟨∇q₁,∇r⟩ = b⁴⟨∇q₁,∇R⟩. Dropping ½‖∇w‖² ≥ 0 gives
   H/b² ≥ J2_lo − b²C ≥ J2_lo − β²C, with β² = 9·10⁻⁶.
8. **Structural strain μ = m₁/√3 (D §1).** ∇U has only the three off-diagonal entries A, B, C, so S is traceless and
   ‖S‖_op ≤ √(2/3)‖S‖_F = √((A²+B²+C²)/3). This needs m₁ ≥ √(sup A² + sup B² + sup C²). That is how m₁ is defined:
   absorb_chain.py `base()`, `m1_hi = sqrt(al² + g² + g1²)`.
9. **Gradient term (t050-self-gradient).** ⟨∇q₁,∇R⟩ ≤ ‖Δq_N(T)‖‖R(T)‖ + ‖∇e(T)‖‖∇R(T)‖ ≤ ‖Δq_N‖N_r + ε₁E_r.
10. **Endpoint versus interval, and uniformity.** The inequality is asserted only at T = 1/2 (P line 15). The time
    integrals use per-cell bounds on all of [0, T]. Every envelope is nondecreasing in |b| (b enters only through
    b n₁, b² C_A² δ, b n₂, β), so the b = 0.003 values cover 0 < |b| ≤ 0.003. Negative b changes only signs, not norms.
    b = 0 is excluded and H₀ = 0.
11. **Nonself (D §3; the selected "cross" form).** Young's inequality absorbs ⟨F, ∇Y⟩ into ν‖∇Y‖², leaving rate 2μ.
    ‖q⊗R + R⊗q‖ ≤ 2‖q‖_∞‖R‖ with ‖e‖_∞ ≤ C_A‖Δe‖. The ‖Δe‖ factor is handled by Minkowski plus summation by parts
    against the cumulative δ. The direct form's steps check out as well.

## B. Calculations reproduced (`checker/independent_t050.py`, `results/independent_t050.log`)

| quantity | committed | reproduced |
|---|---|---|
| 88595/324 < 274 | exact | exact (Fractions) |
| ∫N² | 0.16413420599391970609… | the same exact fraction |
| J2 lower end | 0.01092344160460902489419775544737079360 | 0.0109234416046090248941977554473707935 (40-digit, directed) |
| Ahat(10⁶), D_w(T), I_∞(T) | tr_remainder.repaired | identical to 30 digits; Ahat from my own lattice histogram |
| N_r(T), E_r(T), D_r(T), direct, cross | candidate-v2 | identical to 30 digits; all 500 per-cell N_r and E_r within 10⁻³⁰ |
| nonself (cross) | 343.0839870273641 | 343.0839870273641 |
| C | 848.2334537777 | 848.2334460880 (full-precision ε₁) |
| H/b² | 0.0032893405206098 | 0.0032893405898171 |

The inputs were also reproduced upstream, from the validated enclosures:
- `checker/make_t050_variant.py` derives the T = 1/2 per-cell chain from the reviewed absorb_chain.py (sha 0984e22c),
  regenerated through the reviewed make_chain_percell.py (output sha 0af7b93e). It changes exactly two lines: the
  horizon 0.25 → 0.5 in the interval constant and in the scope assertion.
- Run on the T = 1/2 validated.json, it reproduces **all 500 rows** of chain_percell.json byte for byte
  (`results/chain_percell_t050_rerun.json`). It also reproduces chain.json's K, N_w, ε₀, ε₁, δ, S₁ and the closure:
  conditions A, B1, B2 hold, with lhs_A ≤ 3.3599·10⁻³ < 4.3906·10⁻³. So the T = 1/2 closure and every per-cell
  envelope follow from validated.json through reviewed code.
- `checker/compare_t025.py` (`results/compare_t025.log`): on cells 1–250, the T = 1/2 validated.json and per-cell
  table are byte-identical to the reviewed T = 1/4 files on this branch (validator 2d295236, per-cell sha 795e3a7b).
  Their conventions, approximation and initial-data records are also identical.
- E and G were recomputed from the stored exact fractions. E = ½(‖∇q_N‖ ± ε₁)². G = ‖ΔU_N(T)‖ + √(2/27)·ε_W(T); the
  √(2/27) is the maximum over n of the conversion from the weighted (2+n²)³ norm to the L² Laplacian norm, at n = 1.
- The global Lemma B cap from bounds.review.json is below K_i² in **0 of 500 cells**, so that file has no effect on
  D_w.

### B2. Reconciling the small difference in the final bound (unrounded values)

`results/independent_t050.json` keeps every intermediate at the checker's full working precision: 40-digit decimal
endpoints with directed rounding, not display-rounded.
- `intermediates` holds E, G, V and its three parts, J2, Ahat, D_w, I_∞, N_r, E_r, J_r and D_r at T, the direct and
  cross parts, ‖Δq_N‖, ∫N² and both ε roundings.
- `comparisons.*.parts` holds the self term, G·nonself, the gradient, C and β²C for each variant.
- `percell` holds μ, P, U, the 2μ weight, D_w, I_∞, N_r, E_r, J_r and D_r for all 500 cells.
- `reconciliation` holds the differences below.

Full precision: ε₁(T) = 4.8004447567422908…·10⁻⁴ and ε_W(T) = 2.2080488611760210…·10⁻⁴ (chain row 500).
Committed convention: chain.json's upper roundings ε₁ = 4.8005E-4 and ε_W = 2.2081E-4.

| run | E lower end used | G used | gradient term | H/b² lower bound |
|---|---|---|---|---|
| committed (certificate-v1.json, self-gradient candidate-v1.json) | 0.38664510832974714882 (stored) | 2.05359614654874380021 (stored) | 98.70472763338865139 | 0.00328934052060975298 |
| mine, committed convention throughout (own E, G and gradient with rounded ε) | 0.38664510832974714882 | 2.05359614654874380021 | 98.70472763338865139 | 0.00328934052060975298 |
| mine, as certified: stored E and G, full-precision ε₁ in the gradient | 0.38664510832974714882 (stored) | 2.05359614654874380021 (stored) | 98.70471994368531390 | 0.00328934058981708302 |
| mine, full precision throughout (own E, G and gradient) | 0.38664511318766918182 | 2.05359614515692130249 | 98.70471994368531390 | 0.00328934554318898841 |

- **Committed convention.** My independent code reproduces the committed E, E_hi and G to all 40 printed digits,
  and the committed H/b² to within 5.3·10⁻³⁸ (40-digit versus 55-digit endpoints).
- **As certified.** This row differs from the committed bound by +6.920733·10⁻¹¹, which is β² · 7.689703·10⁻⁶,
  exactly the change in the gradient term ε₁·E_r(T) from rounding ε₁ up. This is the difference quoted in the
  Verdict.
- **Full precision throughout.** Also using full-precision ε in E and G adds a further +4.95·10⁻⁹, through J2
  (E lower end +4.86·10⁻⁹, G −1.39·10⁻⁹).
- All four are valid lower bounds; the committed one is the most conservative.

## C. Inherited, not verified

The rigorous claim needs each of these to be a valid bound. The hypothetical sensitivities from the Verdict section
are repeated for orientation only.
- **validated.json** (validator d849ec96, numerics ad8e4fb8, arrays W 17 MB and Q 529 MB). Cells 251–500 are new.
  Cells 1–250 equal the reviewed T = 1/4 output. Platform assumptions: binary64, round-to-nearest, no FMA.
- **Source-only hull U_i** (full.json, script 33e69640, reads Q_nodes). One-at-a-time sensitivity: 2.45 %.
- **Endpoint fractions** for ‖∇q_N(T)‖² and ‖Δw_N(T)‖² (z2-endpoint, script 160789cf). One-at-a-time sensitivity:
  2.34 % for G, 0.00329 absolute for E.
- **‖Δq_N(T)‖ = 1.2187793** (evaluate.py reads Q_nodes). Not needed: see gap 2.
- **C_A = 4.06707921080** (parent lattice certificate).
- The **R-source estimate and envelopes A–F** (endpoint-sign) and Lemma W1/W2 per-cell coverage. The formulas were
  audited earlier at T = 1/4; here they are re-implemented, not re-derived.
- **Standard facts** assumed as stated in P lines 31–33 and 70–74: smoothness and uniqueness of U and Z, the Galerkin
  limit for the Wiener inequalities, and that Python's decimal module is correct.

## D. Dependencies the first bundle omitted

The four-part package resolves all of these except the arrays; see VERDICT_ADDENDUM.md.
1. The producers of the T = 1/2 artifacts: validator d849ec96, numerics ad8e4fb8, source hull 33e69640, z2-endpoint
   160789cf. Also chain_percell.py 9d338c69, per-cell verifier 29f750b9, tr_remainder b193c13b, route-b bounds
   a5aadad5 and time_refinement c2586f5d; these five are reproduced or bypassed above.
2. The trajectory arrays W_nodes.npy and Q_nodes.npy (still excluded by design).
3. extension-t050/README.md and resource-amendment/README.md, with the reviews cited in docs/HANDOFF.md.
4. The history behind base commit 221ddd79.

## E. Gaps and proposed repairs (none falsifies the claim)

1. **The margin rests on array-derived enclosures that cannot be recomputed from the bundle** (sections C and D;
   P lines 172–173, D §2). Repair:
   - ship the endpoint slices Q_nodes[25000] (3×21×21 complex, about 21 KB) and W_nodes[25000] (43 complex), so E, G
     and ‖Δq_N(T)‖ can be recomputed exactly without the full array;
   - keep the producing scripts and reviews with the result (the package now does this).
2. **‖Δq_N(T)‖ needs no array read** (P line 166). The validated bound ‖Δq‖ ≤ (1/√2)Σ|k̃|²|Q̂| ≤ sup_abshessq(T)/√2 =
   5.27694 (k̃ = (k_x, k_y, 1), from the reviewed validator's conventions) gives C ≤ 1174.67 and H/b² ≥ 0.000351 > 0.
   Repair: record this as a fallback.
3. **Per-cell coverage is not cited** (P line 162: "uniformly bound ‖W_b‖ by N_i on each of 500 cells"). It holds
   because the recursion asserts nonnegative cell rates and uses nondecreasing ε₁ and δ (absorption NOTE, Lemma W1).
   Repair: cite it.
4. **Dead dependency.** bounds.review.json enters only through an inactive cap. Repair: say so, or drop it.
5. **Slack is uneven.** By the one-at-a-time sensitivity test, the self term is no longer the limiting piece; U_i, G
   and E are. Future reviews of enclosure validity should concentrate there.
6. **Use full-precision envelopes where they are available** (new, minor). The 5-significant-digit roundings of ε₁
   and ε_W are valid upper roundings, so the committed bound is correct. Using the full chain values would move the
   bound by +6.9·10⁻¹¹ (section B2). No action is needed for validity.

## Files and commands

    VERDICT.md, VERDICT_ADDENDUM.md        the two reports
    checker/independent_t050.py            main re-derivation (exact Fractions + 40-digit directed decimals)
    checker/make_t050_variant.py           two-line T = 1/2 variant of the reviewed per-cell chain
    checker/compare_t025.py                identity checks against the reviewed T = 1/4 files
    checker/reassemble_own.py              own reassembly of the four-part package (VERDICT_ADDENDUM.md)
    results/independent_t050.{log,json}            run on the first bundle (with unrounded intermediates)
    results/independent_t050_on_ff29c90.{log,json} the same run on the reconstructed commit (identical apart from wall time)
    results/chain_percell_t050_rerun.{json,log}    per-cell chain from validated.json
    results/compare_t025.log

Here FT = this branch's math/all-time-phase-response/finite-time. BUNDLE = the finite-time folder of either the
extracted first bundle or the reconstructed ff29c90 checkout. ART = BUNDLE/extension-t050/resource-amendment/artifacts.

    cd checker
    python3 -I -B independent_t050.py $BUNDLE $FT <fresh>.json > <fresh>.log
    # per-cell chain: scratch folder X holding copies of $FT/constants.py, $FT/results/lattice_sums.log,
    # $FT/absorption-b003/absorb_chain.py and $FT/endpoint-sign/scripts/make_chain_percell.py at the same
    # relative paths, plus checker/make_t050_variant.py at its root:
    (cd X && python3 -I -B endpoint-sign/scripts/make_chain_percell.py && python3 -I -B make_t050_variant.py)
    (cd X/endpoint-sign/scripts && python3 -I -B chain_percell_t050.py --numerics $ART/absorption-b003/results/validated.json --json <fresh>.json)
    # comparison: folder REF with t025_chain_percell.json = $FT/endpoint-sign/results/chain_percell.json
    # and t025_validated.json = $FT/absorption-b003/results/validated.json
    python3 -I -B compare_t025.py $ART REF <chain rerun json>
