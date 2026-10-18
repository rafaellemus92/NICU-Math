# enstrophy-jet

Exact Taylor series in time of the enstrophy (mean-square vorticity) for a one-parameter family
of 3D Navier–Stokes flows on the periodic cube, with no forcing:

    u(x, 0) = (sin y, sin z, cos x − cos(x + y + φ)),   viscosity ν.

ChatGPT's package `periodic_ns_lab_v2` (stored in this repository as
[`../../inputs/periodic_ns_lab_v2_audit.zip`](../../inputs/periodic_ns_lab_v2_audit.zip)) claimed
that the enstrophy first depends on cos 2φ at order t⁶, with coefficient −6487/1555200 (cosine form;
Laurent −6487/3110400) for every ν. This folder checks that claim with three independent programs.
It extends the series to t¹⁴, with every coefficient an exact polynomial in ν, and explains its
structure with two selection rules. It also measures how far in time the series can be trusted:
not far. **Read `RESULTS.md` for the findings and their limits.**

This folder was made in a separate session (October 2026; it was first called
`navier-stokes-jet/`) and shares no code with the lab-v2 audit next to it,
[`../audit_v2/AUDIT.md`](../audit_v2/AUDIT.md). The two exact series agree entry for entry
through n = 12 (`compare_audit_v2.py`); this one goes on to n = 14.

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
| `compare_audit_v2.py` | checks `results/series.json` against `../audit_v2/exact/z12_unit.json` (n ≤ 12) |
| `tests/test_jet.py` | fast pytest suite |
| `results/series.json` | Laurent c\[n, m\](ν) for n ≤ 14: Z = Σ c\[n,m\](ν) tⁿ e^{imφ} (cosine coefficient = 2c) |
| `results/*.log`, `*.txt`, `*.json` | outputs of the scripts above |
| `results/earlier_runs/` | logs from earlier runs that used ChatGPT's package (see its README) |

## How to run

Run everything from this folder (`cd math/ns-phase-audit/enstrophy-jet` from the repository
root). Python 3.11 or later; tested on 3.13.

    pip install -r requirements.txt
    python3 -m pytest -q tests                    # 12 tests, about 4 s
    python3 show_series.py                        # t^6, t^7, t^8 in readable form, < 1 s
    python3 show_series.py --all > results/series_summary.txt   # + rule checks and partial sums
    python3 compare_audit_v2.py > results/compare_audit_v2.log   # < 1 s

Regenerate or cross-check the results (times on one core of the machine used here):

    python3 taylor_exact.py 8                     # 2 s; writes results/series_n8.json
    python3 taylor_exact.py 14                    # 10.5 min; writes results/series_n14.json,
                                                  # which matches results/series.json except timings
    python3 exact_single_nu.py 1/28 8 --series results/series.json   # 4 s; 0 mismatches
    python3 float_check.py > results/float_check.log   # 16 s
    python3 decompose.py                          # 3 s; results/decompose.log, decompose.json
    python3 leaf_check.py 9 > results/leaf_check.log   # 21 s
    python3 long_jet.py                           # 2.5 min, about 2 GB RAM; results/long_jet.json

`show_series.py` and `compare_audit_v2.py` need only the standard library. The others need
`python-flint` (exact rational polynomials) or `numpy`; the tests need `pytest`.

## Credits

The φ-family, the simulations and the t⁶ claim come from ChatGPT's package `periodic_ns_lab_v2`.
The code here was written by Claude agents and shares no code with that package or with
`../audit_v2/`.
