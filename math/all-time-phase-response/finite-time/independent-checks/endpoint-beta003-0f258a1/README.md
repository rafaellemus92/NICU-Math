# Audit of endpoint-beta003 (codex/endpoint-beta003-tightening at 0f258a1)

Audited commit `0f258a1add2b9e339d6c28f3599c43c4ad8241c3`, base `6757dcb7655387a09666c7928c0099516188ee38`.
Claude, session "Navier Stokes-Speech", 19 October 2026. AI audit artifacts, not proofs or human refereeing.
Run against a scratch checkout of 0f258a1 (LFS disabled), with `<FT>` its `math/all-time-phase-response/finite-time`:

    python3 -B independent_beta003.py <FT> <fresh dir>     # about 2 s; writes <fresh dir>/independent_beta003.log
    python3 -I -B divergence_form_check.py                # about 1 s

**independent_beta003.py** recomputes the whole scalar chain from the primitive certified inputs, on the
parent's decimal intervals (constants.py, 40 digits, directed rounding) instead of check.py's mpmath, and
without reading the parent's stored totals: the J2 lower end, D_w,j and I_inf,j, N_r,j and E_r,j, the three
nonself parts, d1, d2, the new d_div, C_new and the final margin. Every input is hash-checked first. Result
(`results/independent_beta003.log`): every value equals results/candidate.json to the printed digits;
H_b(1/4)/b² ≥ 0.004804904671503767 at |b| = 0.003, so the claimed 0.004804904671503 is a valid lower
bound; the cell weights f_i are not monotone by themselves, so the suffix majorant is needed.

**divergence_form_check.py** tests, on random band-limited fields whose products the grid resolves exactly,
the normalization and signs of the divergence-form step: Leray projection and z-average drop against a
divergence-free z-independent X; the integration by parts sign; the chain
|⟨W⊗W, ∇X⟩| ≤ ‖mean W⊗W‖‖∇X‖ ≤ ‖W⊗W‖‖∇X‖ ≤ max|W|‖W‖‖∇X‖ with normalized norms (no volume or component
factor); skew transport. Binary64 floating point: a check of the algebra, not a certificate.

Inspected, not run: check.py and test_check.py (they import mpmath, which is not installed here).
