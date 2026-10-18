# physiology/ — neonatal cardiopulmonary modelling

> Compartmental and reduced-order models of neonatal respiration and
> circulation. The ambition is a scaffold for teaching, scenario
> exploration (PDA, BPD, PPHN, periodic breathing), and — eventually,
> with separate clinical validation and privacy safeguards — a
> clinician's workbench. Not now, and not without that validation.

Read [`../RESEARCH.md`](../RESEARCH.md) first.

## Structure

```
physiology/
├── README.md       # this file
├── CLAIMS.md       # tiered claim ledger
└── references/     # per-paper summaries with equation notes
```

## Clinical caveat (always)

Nothing in this folder is validated for patient care. Every scenario
model is a research instrument. Any clinical use requires separate
validation, approved data handling, and the clinician's judgment.

Say so explicitly in any UI copy, docstring, or README that a
clinician might read.

## Current scope

- **Two-compartment respiratory model** (planned, PR #7). The simplest
  demonstration that identical aggregate compliance can mask different
  distributions of local time constants τ_i = R_i C_i, producing
  different passive-emptying responses. The physiology analogue of the
  Navier–Stokes "reduced state doesn't determine evolution" claim.
- **Cardiopulmonary coupling.** Pressures, geometry, compliance,
  transmural distinctions. Grounded in reviews catalogued under
  `references/`.
- **PDA and BPD scenario models** (future). Separate branches; each
  with its own pre-registered scope.

## Dependencies

```sh
pip install numpy scipy matplotlib pytest
```

Heavier scenario work (e.g. compartmental systems with stochastic
inputs) states dependencies at the module level.

## References folder

`references/` holds short per-paper summaries: citation, central
claim, and any equations we rely on with units checked. Format:

```
references/
├── bronicki_2016_cardiopulmonary_interactions.md
├── mohr_2015_periodic_breathing_preterm.md
├── fultz_2019_sleep_csf_oscillations.md
└── ...
```

Each note states: what the paper measures, what it establishes versus
hypothesizes, and (where we build on it) which model file consumes
which equation.

## Voice

Clinical and physiological statements stay strict. The mythological
layer belongs in prose about the research arc, not in a dosing
discussion or a flow diagram.
