# RESEARCH.md — NICU-Math

The authoritative research spine. Both AI collaborators (Claude and
Codex) read from this file and keep it in sync.

---

## 1. The convergence thesis

One research program, three tracks, one mathematical spine:

> **The summary doesn't determine the dynamics; the phase and
> distribution do.**

Everything in this repo is a variation on that claim.

| Track | Where it lives | What a "signature" looks like | What's hidden by summarizing |
|---|---|---|---|
| Mathematical fluid dynamics | `fluids/` | Energy, enstrophy, dissipation measure, total helicity, current stretching | How phase organization among triadic interactions evolves — captured by rate of change of stretching |
| Neonatal cardiopulmonary modelling | `physiology/` | Measured pressure, aggregate compliance, average flow, saturation | How compliance and resistance are *distributed*; where the delays sit in the feedback loop; sleep state |
| Shared instruments | `packages/stats/` | Mean, quantile, spectrum magnitudes | Phase; coupling; persistence of alignment |

The piano trainer in [sgrounds](https://github.com/rafaellemus92/sgrounds)
(`/piano`) is the simplest instance of the same instrument at N=2
oscillators: measures how closely two Receivers (hands) couple to one
Source (score), via live Kuramoto r(t), Hilbert phase on each hand's
onset-density, Welch PSD slope of IOI. The TypeScript modules behind
that live at `sgrounds/lib/piano/{hilbert,kuramoto,onsetPSD}.ts`; their
numpy twins live here under `packages/stats/py/`.

## 2. Why the three tracks belong together

- **Phase organization that resists stationary-phase cancellation** is
  the mechanism we track in Navier–Stokes.
- **Phase organization in a forced oscillator** (chant → breath, or
  one circadian oscillator entraining another) is the mechanism in
  sleep/respiratory physiology.
- **Phase organization between two hands at a keyboard** is the
  mechanism in the piano trainer — the pedagogical sandbox where the
  math is easiest to see.

Different domains; same question in each: *when does coordination
stabilise, and when does it drive the system past a threshold?* The
answer is likely different in each setting. What's shared is the
instrument.

## 3. Methodology — the claim ledger

Every result in this repo lives in exactly one of these tiers. Each
`<track>/CLAIMS.md` carries its own ledger. Nothing merges to `main`
without a tier assignment.

| Tier | Burden of proof | How we file it |
|---|---|---|
| **Proposed mechanism** | None yet beyond motivation | One paragraph; name what would make it testable |
| **Mathematical result** | Proof, stated assumptions, boundary cases | Written statement + reference proof (file or paper DOI) |
| **Exact computation** | Reproducible script, deterministic output, independent verification | Code in `<track>/exact/`, test under `tests/`, result committed |
| **Numerical evidence** | Reproducible with recorded seeds, split train/test, held-out metrics | Code + saved artifacts in `<track>/numerical/`, pre-registered hypothesis |
| **Clinical evidence** | Published study, dataset provenance, limits of generalization | Citation + per-paper summary in `physiology/references/` |
| **Contradicted / unresolved** | Preserved as negative result; not deleted | Moved into a `# Retired` section with the superseding commit SHA |

**Negative results are first-class.** A pre-registered test that fails
tells us as much as one that succeeds. We do not quietly re-tune until
the number improves.

**Agreement between AI collaborators is review, not independent
evidence.** If both AIs reached the same conclusion from the same
calculation, that's one data point, not two.

## 4. Repository layout

```
./
├── AGENTS.md               # Codex instructions; imports RESEARCH.md
├── CLAUDE.md               # Claude instructions; imports RESEARCH.md
├── RESEARCH.md             # this file
├── api/                    # FastAPI service (evidence search + Bayes scenarios)
├── ui/                     # Streamlit evidence browser
├── library/                # local PDFs for ingest (gitignored)
├── fluids/                 # Navier–Stokes research track
│   ├── README.md
│   ├── CLAIMS.md
│   ├── exact/              # reproducible exact-computation artifacts
│   └── numerical/          # pre-registered simulation studies
├── physiology/             # neonatal cardiopulmonary modelling
│   ├── README.md
│   ├── CLAIMS.md
│   └── references/         # per-paper summaries + equation notes
├── packages/
│   └── stats/              # shared math library
│       ├── README.md
│       ├── py/             # numpy canonical implementation
│       ├── ts/             # typescript twin, consumed by sgrounds/piano
│       └── vectors/        # shared JSON test vectors
├── hou-luo/                # inviscid 1D singularity-tracking (open PR #1)
└── pangram/                # unrelated prime-word research (kept as-is)
```

## 5. Writing voice (per sgrounds CLAUDE.md)

The sgrounds project treats the Norse mythological layer (Norns,
wyrd, Loki, Yggdrasil, the semicolon `;` as the shuttle of the loom)
as load-bearing conceptual infrastructure, not decoration. We preserve
that voice in prose where it fits — a session is a thread, the archive
is the tapestry, an unexpected result is a Loki-moment. We do *not*
let it leak into mathematical claims or clinical guidance. Equations
and physiology stay strict.

## 6. Clinical caveat

Nothing in this repo is validated for patient care. Scenario models
(PDA, BPD, periodic breathing) are research instruments and teaching
scaffolds. Any use near real patients requires separate clinical
validation, data-handling approval, and the clinician's judgment —
which is where it belongs anyway.

## 7. Deployment

See [`docs/deployment.md`](docs/deployment.md). Short version: Vercel
auto-deploys are **paused** (ignored build step) until the baseline
is green; Railway is the chosen host for the FastAPI + pgvector
backend when the UI needs it web-reachable; Supabase is the auth path
once NICU-Math needs sign-in, same account as sgrounds. The research
spine stays silent on hosting; `docs/deployment.md` is where hosting
decisions live and are revised.

## 8. Related work in-tree

- `hou-luo/` — adaptive-mesh 1D Hou-Luo singularity-tracking (open
  PR #1 by @rafaellemus92). Treat as the inviscid blow-up candidate
  companion to the viscous phase-organization work in `fluids/`.
- Open branches at merge time of this file: `claude/breath-rhythm-ns-jet`,
  `claude/neonatal-torus-app-RlFrZ`, `claude/new-session-sbrl43`,
  `claude/nicu-torus-setup-yD6CZ`. Each should be rebased onto the
  current `main` and re-filed into the appropriate track folder once
  this spine lands.

---

**S ; R → N.** Source ; Receiver → the New. The repo's name of what
we're doing.
