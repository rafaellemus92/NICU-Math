# packages/stats — shared math library

Twin TypeScript and Python implementations of the small numerical
toolkit used across the sgrounds piano trainer and this repo's
`fluids/` and `physiology/` tracks. **The definitions are shared via
JSON test vectors that both language implementations must pass;** the
code is twinned, not literally shared.

Read [`../../RESEARCH.md`](../../RESEARCH.md) for the convergence
thesis these functions serve.

## Layout

```
packages/stats/
├── README.md               # this file
├── py/                     # numpy canonical implementation
│   ├── stats/              # importable package
│   └── tests/              # per-module tests + shared-vector consumers
├── ts/                     # typescript twin (consumed by sgrounds/piano)
│   ├── src/
│   └── tests/
└── vectors/                # shared JSON test cases, source of truth
    ├── hilbert.json
    ├── kuramoto.json
    ├── welch.json
    └── onset_density.json
```

Each JSON vector file contains an array of `{input, expected}` cases.
Both the Python and TypeScript test suites load the same file and
assert their implementation's output matches `expected` to a shared
tolerance. If the two implementations disagree, the discrepancy is
visible on CI immediately.

## Modules

The first ports (from `sgrounds/lib/piano/*.ts`):

| Module | Purpose | Status |
|---|---|---|
| `fft` | radix-2 Cooley–Tukey FFT, in-place | **TS done, Py done** (shared vectors + 31 passing pytest cases) |
| `hilbert` | FFT-based analytic signal, instantaneous phase, envelope | **TS done, Py done** |
| `onset_density` | Gaussian-smoothed spike-train density (in `stats.hilbert`) | **TS done, Py done** |
| `kuramoto` | Order parameter r(t), mean phase, live-window helper | **TS done, Py done** |
| `welch` | Welch's PSD + log-log slope fit (for IOI power-law work) | TS done; Py pending (follow-up PR) |
| `stationary_phase` | ∫ B cos Ψ dt integration-by-parts helper for fluid-triad bounds | Py in `fluids/stationary_phase.py` (migration candidate) |

## Why both languages

- **TS** lives in-browser for the piano trainer (`sgrounds/app/piano`)
  and runs at ~20 Hz on the main thread for the live Kuramoto phasor.
- **Py** is where the numerics live for the fluids work (numpy, scipy,
  matplotlib) and for the Streamlit UI's post-processing.
- Keeping them twinned (shared vectors) means a formula change in one
  language forces the matching change in the other, or CI fails.

## Local use

### Python

```sh
cd packages/stats/py
pip install -e .
pytest -q
```

### TypeScript

The TS twin currently lives inside the sgrounds repo at
`sgrounds/lib/piano/`. A follow-up PR will mirror those files here
and have sgrounds import from `packages/stats/ts/` instead. Until
then, the TS "source of truth" is the sgrounds copy, with its tests
under `sgrounds/lib/piano/__tests__/`.

## Adding a vector

1. Add a new `{input, expected}` object to the relevant file under
   `vectors/`.
2. Run `pytest` here — the test loader will pick it up automatically.
3. Run the sgrounds piano trainer's `vitest run` — same contract.
4. If either side fails, do not change the vector; fix the
   implementation.

The vectors are the shared *definition*; the code is the
*implementation*. The definition wins.
