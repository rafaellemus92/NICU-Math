# Pinned source matrix

| Branch | Full head | Delta vs main |
|---|---|---|
| `main` | `efff6a5b43d699c22eb6bef8c0ce666837d3d785` | base |
| `codex/startup-collaboration` | `6131438df9c8c4bbae265efe1d2f4d79ca3b1b45` | 79 files changed, 1539 insertions(+), 7191 deletions(-) |
| `codex/integrate-research-workspace` | `ab448aaa429bf3bc3c4c5bc2a41b5be6778e1f28` | 62 files changed, 2697 insertions(+), 392 deletions(-) |
| `codex/import-flow-research` | `a9aaf1f49ec68c9e90ab65fa7f81158d954bdc87` | 113 files changed, 9561 insertions(+), 392 deletions(-) |
| `codex/correct-fluid-claims` | `14fe98a43ca49784540de8fcb03a9f931754975e` | 78 files changed, 3488 insertions(+), 1952 deletions(-) |
| `codex/fix-synthetic-breath-analysis` | `43160952f2c851e2c9e340a66b48651a6a285046` | 79 files changed, 4006 insertions(+), 2073 deletions(-) |
| `claude/breath-rhythm-ns-jet` | `6f874a2697842a10a3e799f05ab0d65e575e7373` | 109 files changed, 9497 insertions(+), 266 deletions(-) |
| `claude/all-time-phase-response` | `1245d0c430c90bdbf1ba6cc735a2068bb2c28776` | 125 files changed, 12413 insertions(+), 90 deletions(-) |
| `claude/peaceful-wozniak-oaprql` | `43d41e916957b02359a5b0959057019fb8cf6950` | 155 files changed, 11434 insertions(+), 2352 deletions(-) |
| `codex/all-time-phase-response` | `12ea61f7c7973348cc4f17e5f838a25509fc02bb` | 13 files changed, 2118 insertions(+) |
| `claude/phase-family-b2` | `a6c0739104272a3074aa1e4b5c90402c2c8a25ea` | 49 files changed, 9726 insertions(+), 1860 deletions(-) |
| `claude/phase-locking-9k2m` | `0c3fe5d167059856ed78ec343ed99bf31114e7a1` | 16 files changed, 2370 insertions(+), 1860 deletions(-) |
| `codex/physiology-two-compartment` | `49c5f82889b0535ab7272aaaafa03842cbda574e` | 776 files changed, 1090 insertions(+), 206496 deletions(-) |
| `claude/new-session-sbrl43` | `a5e20d3c51fb4da586b3a7ceaf22b806b77ff942` | Two commits on PR17; homepage, smoke tests and handoff only |

## Older PR15 source recovered during correction review

`SOURCE_FILES.json` records 46 mappings to commit
`77916bb51ea88ea6e1b2cddd2cd6e9309993383f`. That commit was not reachable
from the 14 originally pinned branch refs; the original delivery bundle did
**not** contain it or the five blobs listed below. The imported/adapted copies
do not substitute for byte-identical source preservation.

An exact-SHA fetch from origin recovered the full commit. All 46 source paths
were verified against the map's Git blob IDs. With the user's additional
authorization it will be protected by the non-release archival tag
`archive/research-source-77916bb-20261018` (no force update). Publication status
and tag-object ID are reported in the correction handoff, not assumed here.

| Original path | Blob missing from original bundle |
|---|---|
| `navier-stokes-jet/README.md` | `54d4e0279f311b6b4db0ed12cbe4819aa22623bc` |
| `navier-stokes-jet/RESULTS.md` | `13a4b19803726d3b21380b19ba4a5eccc069dad4` |
| `shared-air/AUDIT.md` | `1be316b8ac396272acc747723a656ebd641ce8bb` |
| `shared-air/README.md` | `83d6c77b97832ccac9acff916efee27b8ce54cc0` |
| `shared-air/tools/load.js` | `df358a8bab9358fdf5536c0e25e59477d5efd04f` |

The original bundle is retained unchanged for audit. A supplemental verified
source bundle accompanies the correction handoff. No source manifest hashes
were rewritten.
