# fluids/ — Navier–Stokes research track

> Mathematical fluid dynamics work. The target is a controlled estimate
> that would advance the 3D Navier–Stokes global-regularity question.
> The method is to study **which organizational properties of a flow
> are not captured by its summary statistics**, and whether those
> properties can be bounded by the flow's own evolution.

Read [`../RESEARCH.md`](../RESEARCH.md) first for context.

## Structure

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

**Exact computations** (`exact/`) — closed-form or short-numeric
constructions whose claim can be verified by running the script. Each
has:

- a Python module that constructs the object(s) under study,
- a pytest module that asserts the claim's numerical content, and
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

## Running

```sh
# From repo root
python -m venv .venv && source .venv/bin/activate
pip install numpy scipy pytest
pytest -q tests/fluids
```

Any script with heavier dependencies (matplotlib for plots,
sympy for algebra) states them at the top of its module.

## Related in-tree

- `../hou-luo/` — adaptive-mesh 1D Hou-Luo inviscid singularity
  tracking. Companion inviscid blow-up candidate; separate open PR.
- `../packages/stats/` — shared math library (Hilbert, Welch PSD,
  Kuramoto, FFT) used by both fluids experiments and the piano
  trainer in sgrounds.

## Voice

Prose may reach for the mythology (a Loki-moment, wyrd across runs);
theorem statements, numerics, and figure captions do not.
