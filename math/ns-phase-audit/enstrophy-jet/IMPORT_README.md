> Historical PR15 record from a9aaf1f, referring to source 77916bb.
> Dates, passes, pending-review language and paths below describe that session.
> Use [README.md](README.md) for current scratch-only commands and
> [the correction review](../../../docs/reconciliation/CORRECTIONS.md) for fresh checks.

# navier-stokes-jet

Exact Taylor series in time of the enstrophy (mean-square vorticity) for a one-parameter family
of 3D Navier–Stokes flows on the periodic cube, with no forcing:

    u(x, 0) = (sin y, sin z, cos x − cos(x + y + φ)),   viscosity ν.

ChatGPT's package `periodic_ns_lab_v2` (not included in the original standalone import) claimed that the enstrophy first depends
on cos 2φ at order t⁶, with coefficient −6487/1555200 for every ν. This folder checks that claim
with three independent programs. It extends the series to t¹⁴, with every coefficient an exact
polynomial in ν, and explains its structure with two selection rules. It also measures how far
in time the series can be trusted: not far. **Read `RESULTS.md` for the findings and their limits.**

## Import status and overlap

Selective import from `claude/breath-rhythm-ns-jet` at
`77916bb51ea88ea6e1b2cddd2cd6e9309993383f`. See
[IMPORT.md](IMPORT.md) for provenance, historical PR15 validation and runtime estimates.
All supplied `results/` logs and tables are **historical source artifacts**, not
new runs. The mathematical argument is a **non-refereed sketch**. No rigorous
Taylor remainder, finite-time optimum conclusion or series-divergence theorem
is established. No clinical or speech model is implemented here.

The same phase family, lower-order coefficients and selection-rule argument
already live in the adjacent `../audit_v2/`. Orders 13–14 and these reproduction tools
are incremental; orders 0–12 are retained within the complete reference table
so the checks can run. The overlap test compares both stored E and Z exactly,
normalizing trailing polynomial zeros; it does not regenerate order 12.

## Files

| File | Purpose |
|---|---|
| `taylor_exact.py` | exact jet, ν kept as a symbol (python-flint); writes the series JSON |
| `exact_single_nu.py` | independent exact jet at one rational ν (different form of the equation) |
| `float_check.py` | independent float FFT jet; compares every coefficient with `results/series.json` |
| `ljet.py`, `decompose.py` | leaf-labelled jet; which Fourier interactions build each coefficient |
| `leaf_check.py` | term-by-term check of the selection rules |
| `show_series.py` | prints the t⁶, t⁷, t⁸ polynomials, checks the rules, shows partial sums |
| `long_jet.py` | float jet to t⁴⁰, to see how the coefficients grow |
| `tests/test_jet.py` | fast pytest suite |
| `results/series.json` | c[n, m](ν) for n ≤ 14: Z = Σ c[n,m](ν) tⁿ e^{imφ} (cosine coefficient = 2c) |
| `results/*.log`, `*.txt`, `*.json` | outputs of the scripts above |
| Source `results/earlier_runs/` | Not recopied; see the pinned source links in RESULTS.md |

## Historical run recipes (scratch copy only)

From this folder (Python 3.11 or later; tested on 3.13):

    python3 -m pip install numpy python-flint pytest  # isolated environment; no manifest added
    python3 -m pytest -q tests                    # source checks plus import failure/overlap controls
    python3 show_series.py                        # t^6, t^7, t^8 in readable form, < 1 s
    python3 show_series.py --all                  # + rule checks and partial sums (results/series_summary.txt)

Historical source runtimes below are not current-machine estimates; see IMPORT.md.
Full order-14/40 regeneration is deferred. Commands for a separately budgeted run:

    python3 taylor_exact.py 8                     # 2 s; writes results/series_n8.json
    python3 taylor_exact.py 14                    # 10.5 min; writes results/series_n14.json,
                                                  # which matches results/series.json except timings
    python3 exact_single_nu.py 1/28 8 --series results/series.json   # 4 s; 0 mismatches
    python3 float_check.py                        # 16 s; results/float_check.log
    python3 decompose.py                          # 3 s; results/decompose.log, decompose.json
    python3 leaf_check.py 9                       # 21 s; results/leaf_check.log
    python3 long_jet.py                           # 2.5 min, about 2 GB RAM; results/long_jet.json

`show_series.py` needs only the standard library. The others need `python-flint` (exact
rational polynomials) or `numpy`.

## Credits

The φ-family, the simulations and the t⁶ claim come from ChatGPT's package `periodic_ns_lab_v2`.
The code here was written by Claude agents and shares no code with that package.

## Comparison failure contract

`exact_single_nu.py --series ...` returns nonzero for an exact mismatch or a
missing requested order. `float_check.py` returns nonzero when the worst error
exceeds **1e-10**, normalized by the largest exact coefficient in each order.
This fixed regression tolerance allows accumulated float64 FFT/convolution and
cancellation error (historical maximum 6.5e-13 through 14); it is not a certified
roundoff bound. Nonfinite data fail. Phase/grid resolution and missing orders
are rejected rather than silently reducing coverage. Negative controls perturb
the order-zero coefficient by 1e-6 and exercise missing orders and nonfinite values.
