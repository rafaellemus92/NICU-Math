# fluids/exact/ — reproducible exact-computation artifacts

Each module here encodes one claim as a script whose output verifies
it. The sibling [`CLAIMS.md`](../CLAIMS.md) ledger carries the formal
statement and the convention for filing a claim in this tier.

## What's here

| Module | Claim | Test |
|---|---|---|
| [`phi_family.py`](phi_family.py) | For `u^φ = (sin y, sin z, cos x − cos(x+y+φ))`: ∇·u = 0, E is φ-independent, H = 0, and S(φ) = ¼ cos φ. | [`tests/fluids/test_phi_family.py`](../../tests/fluids/test_phi_family.py) |

## The φ-family claim, in one line

Two divergence-free 2π-periodic flows (`u^0` and `u^π`) with
**identical** Fourier magnitudes, energy, and total helicity have
**opposite-sign** vortex stretching:

```
S(0) = +¼        S(π) = −¼
```

So (E, H) does not determine S even in sign — the summary statistics
hide the phase organisation. This is the simplest instance of the
`RESEARCH.md` thesis in Navier–Stokes.

## Reproduce

```sh
# From repo root
python -m venv .venv && source .venv/bin/activate
pip install numpy pytest
python fluids/exact/phi_family.py        # prints the φ-sweep table
pytest -q tests/fluids/test_phi_family.py
```

Expected output for the sweep (abbreviated):

```
   phi/π            E              H              S      ¼cos(phi)      |div u|
   0.000     1.000000     -2.776e-17       0.250000       0.250000    0.000e+00
   0.500     1.000000      0.000e+00      -0.000000       0.000000    0.000e+00
   1.000     1.000000      2.776e-17      -0.250000      -0.250000    0.000e+00
   1.500     1.000000      5.551e-17      -0.000000      -0.000000    0.000e+00
   2.000     1.000000      0.000e+00       0.250000       0.250000    0.000e+00

max |E − E(0)|             = 0.000e+00
max |H|                    = 1.388e-16
max |S − ¼ cos φ|          = 1.110e-16
max |∇·u| (residual)       = 0.000e+00
```

The equalities hold at the floating-point roundoff level because the
field is a low-degree trigonometric polynomial and the FFT-based
spectral differentiation is exact on such inputs at the grid
resolution used (32³).

## What the claim does and doesn't say

- **It does say** the mapping (E, H, |û|²) ↦ S is not injective: there
  exist pairs of flows in this one-parameter family that agree on all
  three but differ in S. The dynamics therefore depend on information
  (phases) that the summary statistics discard.
- **It does not say** anything global about Navier–Stokes regularity.
  Stretching at `t = 0` is a snapshot; the full question concerns
  whether phase organisation can be sustained long enough to force
  blow-up. The φ-family is the simplest-possible counterexample to
  "summaries determine dynamics," not a theorem about the Clay
  problem.

The intended use is as a baseline that any future "summary ↦ dynamics"
reduction has to pass through — if a proposed reduced description
cannot distinguish `u^0` from `u^π`, it cannot predict S, and it will
not predict Ṡ either.

## Dependencies

`numpy` only for the module; `pytest` to run the test. The entire run
takes under a second on a laptop.
