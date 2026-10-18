# Logs from earlier runs

These are raw output files from the analysis sessions that produced this folder (16 October 2026).
They back numbers in `RESULTS.md` that cannot be regenerated from this folder alone, because
the scripts that made them ran ChatGPT's package `periodic_ns_lab_v2` or read its simulation
output, and those scripts are not kept here. The package itself, including
`periodic_ns_lab_v2/results/refine_p01_N64/diagnostics.csv`, is now in the repository as
[`../../../../inputs/periodic_ns_lab_v2_audit.zip`](../../../../inputs/periodic_ns_lab_v2_audit.zip).
Long scratch-directory paths inside the logs were shortened to `<nslab>` or `<scratchpad>`;
nothing else was edited.

Two later checks, made on 18 October 2026 while merging this folder, are kept with their
scripts: `fixed_dt_L2.py` (needs the unzipped package; its path is the first argument) and
`rot_passive_split.py` (self-contained).

"Audit" below means this folder's own earlier audit, not the lab-v2 audit in
[`../../../audit_v2/AUDIT.md`](../../../audit_v2/AUDIT.md), which covers the same ground in its
§3 (verdict tables) and §6 (items B1–B8).

| File | What it shows | Made by |
|---|---|---|
| `audit_pytest.txt` | the package's own test suite: 27 passed | audit, running the package's tests |
| `audit_crossing.txt` | sign change of d²Z/dφ²(T,0) between T = 1.76 and 1.77 on 24³, 32³, 48³; cubic-interpolated crossing times; independent finite differences | audit |
| `audit_symmetry.txt` | phase-reflection and time-reversal identities, checked numerically | audit |
| `audit_selection_rule.txt` | with sin z scaled by ε: harmonics 2–4 vanish at ε = 0; c[6,2]/ε² is constant (Laurent) | audit (float jet) |
| `audit_ranking32.log` | Z(2), Z(4) for the three candidate phases on 32³: the package's solver and an independent solver | audit |
| `audit_opt_fd_24.log` | finite-difference check of the Newton stationary point φ* = 0.971073 at 24³ | audit |
| `audit_field48_64.log` | regenerated 48³ vs 64³ full-field differences at φ = 0.971073, with the package's code. Its `rel_Z` values are the package's mixed-step numbers (200 fixed steps at 48³ against 240 adaptive steps at 64³); at fixed dt the T = 2 value is 5.3541e-8, not 5.4675e-8 (AUDIT.md §5.5, item B4) | audit |
| `audit_node_parity.txt` | interpolation of the package's 7 exact viscosity nodes: degree and parity checks for n ≤ 6 | audit |
| `audit_csv_audit.txt` | energy monotonicity in 45 trajectories; recomputed comparison tables; the 33-phase sweep. Its relative-Z rows are recomputed from the package's own CSV, so the 48³, T = 2 rows carry the same time-step mismatch (AUDIT.md item B4) | audit |
| `structure_growth.log` | float jet to t^40 compared with the package's 64³ simulation at ν = 1/28, φ = 0.97107 | structure analysis |
| `structure_leaf_check11.log` | the same term-by-term checks as `leaf_check.py`, run to n = 11 (257 s) | structure analysis |
| `reconcile_exact_vs_float.log` | exact series vs float jets at 25 viscosities, n ≤ 14 | reconciliation |
| `reconcile_compare_nodes.log` | `exact_single_nu.py` at 12 new rational ν, n ≤ 11, vs the exact polynomials: 0 mismatches | reconciliation |
| `reconcile_check_claims.log` | recomputation of side numbers (t^6 polynomials at ν = 1/28, t^7 table, factorizations) | reconciliation |
| `exact_run14.log` | timings of the original `taylor_exact.py` run to order 14 | exact computation |
| `float_rk4_check.json` | RK4 time integration at ν = 1/28 minus the jet: residual matches the next Taylor term | float computation |
| `fixed_dt_L2.log` | 48³ vs 64³ at φ = 0.971073 with fixed RK4 steps dt = 0.005 on both grids: Z at T = 2 and 4, and full-field rel_L2 1.382058e-04 (T = 2) and 2.993808e-04 (T = 4), the same digits as the mixed-step `audit_field48_64.log` | `fixed_dt_L2.py`, running the package's solver (about 15 min) |
| `rot_passive_split.log` | c[6, 2] in rotational form P[a × curl b]: the same total −6487/3110400, but the passive share ("d never in the velocity slot") is −23/28800, 38.3%, against 83.5% in the advective form of `../decompose.log` | `rot_passive_split.py`, exact arithmetic (6 s) |
