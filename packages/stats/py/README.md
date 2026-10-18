# stats — numpy twin of sgrounds/lib/piano/*.ts

Shared numerical helpers for the fluids and physiology research tracks,
twinned with the TypeScript modules in the sgrounds piano trainer. Both
languages consume the JSON vectors under
[`../vectors/`](../vectors/); any disagreement surfaces as a failing
pytest or vitest run.

See [`../README.md`](../README.md) for the twin-implementation strategy
and [`../../../RESEARCH.md`](../../../RESEARCH.md) for the convergence
thesis these modules serve.

## Install

```sh
pip install -e packages/stats/py
pytest -q packages/stats/py/tests/
```

Requires numpy ≥ 1.24, Python ≥ 3.10. Test suite finishes in under a
second.

## Modules

| Module | Public API | TypeScript twin |
|---|---|---|
| `stats.fft` | `fft_in_place`, `ifft_in_place`, `next_pow2` | `fftInPlace`, `ifftInPlace` in `sgrounds/lib/piano/hilbert.ts` |
| `stats.hilbert` | `analytic_signal`, `instantaneous_phase`, `instantaneous_amplitude`, `onset_density`, `unwrap_phase` | `sgrounds/lib/piano/hilbert.ts` |
| `stats.kuramoto` | `order_parameter`, `order_parameter_series`, `kuramoto_from_onsets`, `live_frame`, `live_phase_from_onsets`, `KuramotoFrame` | `sgrounds/lib/piano/kuramoto.ts` |

Pythonic naming (`snake_case`); same semantics as the TS. Non-finite
phases are skipped by `order_parameter` (NaN = "oscillator has no data
yet"); zero-mean subtraction inside `onset_density` prevents DC
swamping the Hilbert phase estimate on sparse spike trains.

## The shared JSON vectors

Each file under [`../vectors/`](../vectors/) has the same schema:

```json
{
  "schema_version": 1,
  "module": "<name>",
  "tolerance": <float>,
  "cases": [
    { "name": "...", "input": {...}, "expected": {...} },
    ...
  ]
}
```

The Python test suite loads each file through `tests/conftest.py`'s
`load_vector(name)` helper. The TypeScript twin's test suite will load
the identical file through its own loader when it's mirrored into
`../ts/` in a follow-up PR.

**Protocol for adding a case:**

1. Add `{"name": "...", "input": {...}, "expected": {...}}` to the
   relevant vector file.
2. Run `pytest -q packages/stats/py/tests/` here.
3. Run `vitest run` in the sgrounds repo once its TS tests consume
   this vector too.
4. If either side fails, **do not change the vector** — fix the
   implementation. The vector is the shared definition; the code
   is the implementation.

## What's not here (yet)

- `stats.welch` — Welch PSD + log-log slope fit (currently in TS at
  `sgrounds/lib/piano/onsetPSD.ts`). Follow-up PR.
- `stats.pitch_histogram` — duration-weighted pitch-class histogram.
  Mostly interesting from the piano trainer side; port when needed.
- `stats.stationary_phase` — currently in `fluids/stationary_phase.py`
  because it was built for the fluids track first. Candidate for
  migration here once a second user needs it.

## Caveat

`fft_in_place` is kept as a direct line-for-line twin of the TS
implementation specifically so the two language implementations agree
bit-for-bit on the shared vectors. For performance-critical work,
`numpy.fft.fft` is a few orders of magnitude faster — use it directly
unless twin agreement is the point.
