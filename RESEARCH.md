# NICU-Math research spine

Read this alongside [AGENTS.md](AGENTS.md), the shared operational guidance,
and [docs/RESEARCH_INDEX.md](docs/RESEARCH_INDEX.md), the evidence map.
This reconciles the research scaffolding proposed in PR #5 with the existing
`math/` consolidation and the synthetic-only application scope.

## 1. Working thesis and tracks

**Working hypothesis:** selected summary statistics may omit phase or spatial
organization needed to predict a system's dynamics. This is a motivation to test
specific statements, not a universal theorem or an established bridge between
fluid dynamics, neonatal physiology, music and topology.

| Track | Location | Status |
| --- | --- | --- |
| Existing proofs, audits and experiments | `math/` | Preserved from main; see `math/README.md` for individual claims and assumptions. |
| Fluid-dynamics proposals | `fluids/` | Claim-ledger scaffold; PR #6 implementation is separate and not integrated here. |
| Respiratory mechanics and neonatal hemodynamics | `physiology/` | Two-compartment closed-form teaching model plus proposals; no clinically validated implementation here. |
| Shared numerical instruments | `packages/stats/` | Proposed Python/TypeScript tools and shared JSON vectors, not an installed library. |
| Application demonstrations | `api/app/`, `ui/` | Offline toy scenarios; not calibrated physiological models. |

The sibling sgrounds music project motivated interest in phase, coupling and
summary statistics. Its code and cross-language equivalence have not been verified
in this reconciliation. Norse imagery (wyrd, Norns, Loki, the semicolon as a
connection) can be retained as the author's prose motivation, never as evidence
or terminology in theorem statements, units, test assertions or clinical claims.

## 2. Questions, not established links

- Do triad-phase features explain or predict stretching beyond explicitly named
  summary statistics? State the equations, solution class and comparison first.
- How do distributed resistance/compliance and delays affect a synthetic reduced
  respiratory or hemodynamic model? State units, boundary conditions and parameter
  assumptions before simulating.
- Can common numerical diagnostics be defined by explicit shared test vectors?
  A similar statistic in two domains does not establish a shared mechanism.

Clinical observations may motivate phase-sensitive hypotheses, but clinical
finite-time transitions are not PDE singularities. No claim is made to solve
Navier–Stokes regularity. Results for an inviscid 1D model do not establish 3D
viscous regularity or blow-up.

## 3. Claim ledger and evidence requirements

| Category | Required evidence |
| --- | --- |
| Hypothesis / proposed mechanism | Precise testable statement, motivation and falsification criteria. |
| Mathematical proof | Definitions, assumptions, domain, boundary cases and an inspectable proof. |
| Exact calculation | Exact arithmetic/symbolic derivation, bounds, reproducible command and independent verification. Deterministic floating-point output alone is not exact. |
| Numerical evidence | Seeds, tolerances, convergence/error checks, pre-registered hypothesis and held-out comparisons where appropriate. |
| Unvalidated physiological model | Equations, units, parameter provenance and explicit absence of clinical calibration/validation. |
| Clinical evidence | Verified primary citation, population, methods, limitations and relevance; no patient data here. |
| Contradicted / unresolved | Preserve the original claim, negative result and superseding commit/source. |

Pre-register experiments before running; preserve null results rather than retune
until a preferred outcome appears. Record exact code/commit and command with every
result. AI agreement is review, not a second independent observation. Track
ledgers must distinguish proposed artifacts from files that actually exist.

## 4. Workflow and scope

One implementation owner per task; independent review of exact diff and tests;
a human decides integration. Follow AGENTS.md for branch, publishing and test
rules. Claims and limitations travel with code in PR descriptions and handoffs.

Initial clinical scope is synthetic research and education for respiratory
mechanics and neonatal hemodynamics. No patient-specific recommendations, patient
data, patient-data upload UI or licensed PDF full texts. Future clinical studies,
external datasets and hosted services require separate scope and authorization.

## 5. Navigation

- [Existing math archive](math/README.md), including the consolidated
  `math/pangram-prime-words/` and `math/prime-pangram/search/` and `math/hou-luo-1d/hou-luo/` work.
- [Fluid proposals](fluids/CLAIMS.md) and [physiology proposals](physiology/CLAIMS.md).
- [Shared instruments plan](packages/stats/README.md).
- [Reconciliation decisions and validation](docs/HANDOFF.md).
