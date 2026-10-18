# navier-stokes-jet

Exact Taylor series in time of the enstrophy (mean-square vorticity) for a one-parameter family
of 3D Navier–Stokes flows on the periodic cube, with no forcing:

    u(x, 0) = (sin y, sin z, cos x − cos(x + y + φ)),   viscosity ν.

ChatGPT's package `periodic_ns_lab_v2` (not included) claimed that the enstrophy first depends
on cos 2φ at order t⁶, with coefficient −6487/1555200 for every ν. This folder checks that claim
with three independent programs. It extends the series to t¹⁴, with every coefficient an exact
polynomial in ν, and explains its structure with two selection rules. It also measures how far
in time the series can be trusted: not far. **Read `RESULTS.md` for the findings and their limits.**

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
| `results/earlier_runs/` | logs from earlier runs that needed ChatGPT's package (see its README) |

## How to run

From this folder (Python 3.11 or later; tested on 3.13):

    pip install -r requirements.txt
    python3 -m pytest -q tests                    # 12 tests, about 4 s
    python3 show_series.py                        # t^6, t^7, t^8 in readable form, < 1 s
    python3 show_series.py --all                  # + rule checks and partial sums (results/series_summary.txt)

Regenerate or cross-check the results (times on one core of the machine used here):

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
