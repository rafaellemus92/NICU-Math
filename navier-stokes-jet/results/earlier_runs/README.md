# Logs from earlier runs

These are raw output files from the analysis sessions that produced this folder (16 October 2026).
They back numbers in `RESULTS.md` that cannot be regenerated from this folder alone, because
the scripts that made them run ChatGPT's package `periodic_ns_lab_v2` or read its simulation
output, and that package is not included here. Long scratch-directory paths inside the logs were
shortened to `<nslab>` or `<scratchpad>`; nothing else was edited.

| File | What it shows | Made by |
|---|---|---|
| `audit_pytest.txt` | the package's own test suite: 27 passed | audit, running the package's tests |
| `audit_crossing.txt` | sign change of d²Z/dφ²(T,0) between T = 1.76 and 1.77 on 24³, 32³, 48³; cubic-interpolated crossing times; independent finite differences | audit |
| `audit_symmetry.txt` | phase-reflection and time-reversal identities, checked numerically | audit |
| `audit_selection_rule.txt` | with sin z scaled by ε: harmonics 2–4 vanish at ε = 0; c[6,2]/ε² is constant | audit (float jet) |
| `audit_ranking32.log` | Z(2), Z(4) for the three candidate phases on 32³: the package's solver and an independent solver | audit |
| `audit_opt_fd_24.log` | finite-difference check of the Newton stationary point φ* = 0.971073 at 24³ | audit |
| `audit_field48_64.log` | regenerated 48³ vs 64³ full-field differences at φ = 0.971073 | audit |
| `audit_node_parity.txt` | interpolation of the package's 7 exact viscosity nodes: degree and parity checks for n ≤ 6 | audit |
| `audit_csv_audit.txt` | energy monotonicity in 45 trajectories; recomputed comparison tables; the 33-phase sweep | audit |
| `structure_growth.log` | float jet to t^40 compared with the package's 64³ simulation at ν = 1/28, φ = 0.97107 | structure analysis |
| `structure_leaf_check11.log` | the same term-by-term checks as `leaf_check.py`, run to n = 11 (257 s) | structure analysis |
| `reconcile_exact_vs_float.log` | exact series vs float jets at 25 viscosities, n ≤ 14 | reconciliation |
| `reconcile_compare_nodes.log` | `exact_single_nu.py` at 12 new rational ν, n ≤ 11, vs the exact polynomials: 0 mismatches | reconciliation |
| `reconcile_check_claims.log` | recomputation of side numbers (t^6 polynomials at ν = 1/28, t^7 table, factorizations) | reconciliation |
| `exact_run14.log` | timings of the original `taylor_exact.py` run to order 14 | exact computation |
| `float_rk4_check.json` | RK4 time integration at ν = 1/28 minus the jet: residual matches the next Taylor term | float computation |
