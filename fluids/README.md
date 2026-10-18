# fluids/ — Navier–Stokes research track

> Mathematical fluid dynamics work. The target is a controlled estimate
> that would advance the 3D Navier–Stokes global-regularity question.
> The method is to study **which organizational properties of a flow
> are not captured by its summary statistics**, and whether those
> properties can be bounded by the flow's own evolution.

Read [`../RESEARCH.md`](../RESEARCH.md) first for context.

This is a proposal scaffold from PR #5. `exact/`, `numerical/` and their
tests are planned, not present. PR #6 is separate; no mathematical result is
established by importing this scaffold. No claim to solve global regularity.

## Planned structure

```
fluids/
├── README.md           # this file
├── CLAIMS.md           # tiered research-claim ledger (read before editing)
├── exact/              # deterministic, reproducible exact-computation artifacts
└── numerical/          # pre-registered simulation studies with saved outputs
```

Tests live under the top-level [`../tests/`](../tests/) and are run
with `pytest -q`.

## What's in here

**Exact computations** (`exact/`) — exact-arithmetic or symbolic
constructions whose claim can be verified by running the script. Each
has:

- a Python module that constructs the object(s) under study,
- a pytest module that checks the stated calculation; approximate checks remain numerical evidence, and
- a short README explaining the claim and why it matters.

Example target: a pair of divergence-free periodic flows with
identical Fourier magnitudes (and therefore identical energy,
enstrophy, dissipation measure, and total helicity) but different
rates of change of vortex stretching. Encodes "the reduced state does
not determine its own evolution" as a one-command verification.

**Numerical studies** (`numerical/`) — simulations with pre-registered
hypotheses, saved seeds, train/test splits where applicable, and
held-out metrics. Each has:

- a `plan.md` naming the hypothesis **before** any run,
- the simulation code,
- saved input/output artifacts (small; large arrays as `.npz`),
- a short results report that reports what happened, including null
  results.

## Future test convention

```sh
# From repo root
python -m venv .venv && source .venv/bin/activate
pip install numpy scipy pytest
pytest -q tests/fluids
```

There are no executable tests under `tests/fluids` yet; this command is not a
validation result. Do not install research dependencies for application smoke tests.

Any script with heavier dependencies (matplotlib for plots,
sympy for algebra) states them at the top of its module.

## Related in-tree

- `../math/hou-luo-1d/hou-luo/` — adaptive-mesh 1D Hou-Luo inviscid singularity
  tracking. Companion inviscid blow-up candidate; preserved in main.
- `../packages/stats/` — planned shared diagnostics (Hilbert, Welch PSD,
  Kuramoto, FFT); implementation/cross-language verification is not present here.

## Voice

Prose may reach for the mythology (a Loki-moment, wyrd across runs);
theorem statements, numerics, and figure captions do not.
