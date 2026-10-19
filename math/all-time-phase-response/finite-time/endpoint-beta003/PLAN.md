# Preregistered divergence-form mean self-term check

Owner Codex; branch codex/endpoint-beta003-tightening. Exact base
6757dcb7655387a09666c7928c0099516188ee38. Independent audit
87fa0e39ac51d8fd63b110af60e88c2f0e606109 inspected read-only.
Written before executing new numerical postprocessing. Preserve all prior files.

Fixed target: H_b(T)=Z(u_b(T))-Z(U(T))-b² exp(-2nu T)/4 >0 for every
0<|b|<=beta=3/1000, a=c=d=1, nu=1/28, phi=37/100, T=1/4.
Normalized torus norms and inherited smoothness/closure/Lemma M, analytic base
bounds, q1/endpoint/source hull certificates, Route B support cancellations,
weighted Fourier inequality and audited endpoint-sign A–F are assumed.
Correct interval arithmetic and inherited IEEE assumptions remain trusted.

Compare routes without assuming M positive:
1. Selected: improve only the mean self-forcing contribution to the quartic
remainder, using its divergence form and existing cumulative I_infty envelopes.
2. Alternative: improve M's lower bound enough to exceed the exact threshold
beta² C_old -(E_lo-free). Existing norm-only hulls do not record signed source
or adjoint pairings. Report this threshold; do not assume a full q2 or adjoint
solve is necessary, and do not launch one. If route1 fails, report its gap.

Selected inequality: write W=w/b² and let X solve the linear mean equation
L_U X=-P div overline(W tensor W), X(0)=0. It is z-independent and solenoidal.
Periodicity, Leray orthogonality and Jensen give
  (||X||²)'/2+nu||grad X||²
     <= m1||X||²+||W|| ||W||_infty ||grad X||
     <= m1||X||²+nu||grad X||²+||W||²||W||_infty²/(4nu).
Consequently ||X(T)|| <= d_div, where
  d_div² = (1/(2nu)) integral_0^T exp(2 integral_s^T m1) N(s)² ||W(s)||_infty² ds.
For cell i use inclusive positive-rate weights Q_i=exp(2 sum_{k>=i} m1,k Delta),
f_i=Q_i N_i², its nonincreasing majorant phi_i=max_{k>=i} f_k, and
  d_div² <= [phi_last I_last + sum_i(phi_i-phi_{i+1}) I_i]/(2nu).
I_j bounds cumulative integral_0^{t_{j+1}} ||W||_infty². Never difference I_j,
D_w,j or delta_j to infer cell dissipation. Linear decomposition allows adding
this self-solution norm to unchanged nonself terms in Nbar.

Use lambda=1000000 only (already selected in the reviewed parent), unchanged
N_r,E_r, smooth, err_adv, err_grad and J2_lo. Form
C_new = G*(smooth+err_adv+err_grad+min(d1,d2,d_div)) + S E_r.
Do not obtain nonself bounds by subtracting one upper bound from another;
read each named nonself component directly. Positive final ||grad w||²/2 is
retained in the exact identity, then dropped only for this sufficient lower bound.
Acceptance: lower(J2_lo-beta² upper(C_new))>0 using directed interval arithmetic.
Safe outward display is separate; no nearest-rounded cutoff governs decisions.
If it fails, preserve output and report unresolved target, not negative H_b.
If it improves C, request exactly one focused independent proof/code review,
no recursive review, and fix confirmed defects while preserving failed outputs.

Inputs: committed endpoint-sign/results/chain_percell.json,
tr_remainder.repaired.json, absorption-b003 chain.json/validated.json,
route-b-dissipation bounds.review.json, route-b-tightening time_refinement.final.json,
z2-endpoint endpoint.json. Pin exact hashes before import/evaluation. Recompute
only D_w and I_infty cumulative sequences from A–B; check their final endpoints
against the parent and use its already audited remaining components. No array
loads, LFS, DNS, q2/adjoint evolution, full validator, downloads or new dependencies.
At most300 seconds aggregate numerical runtime, hard timeout<=60 seconds/process.
Include exact arithmetic toy checks for divergence energy/Young coefficient,
weighted Abel bound and mandatory majorant. Output exclusive-create with hashes.
Local commit only; root-required HANDOFF/research-index updates allowed.
