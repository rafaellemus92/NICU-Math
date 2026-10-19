# Addendum: reconstruction of ff29c90e and the newly accessible T = 1/2 dependencies

Auditor: Claude, session "Navier Stokes-Speech", 19 October 2026. This extends VERDICT.md in this folder.
Constraints: no edits to audited sources, no merges, no recursive reviewers (so no subagents, although ultracode
is on), no simulations, no array generation, no validator runs and no network fetches of the arrays.

Revision of 19 October 2026 (preserved version): sensitivity figures are stated as one-at-a-time hypotheticals, and
paths refer to this folder. The reconstruction itself is not committed here: the package, the restored repository
and the materialized sources stayed in the audit session's scratch space. This branch carries only reports,
scripts and outputs.

## 1. Reconstruction

- The four parts and the README arrived. The supplied `reassemble-nicu-audit.py.txt` was **not executed**: the
  sandbox blocks running downloaded code. I read it and reproduced its checks with my own
  `checker/reassemble_own.py`. All four part and chunk sizes and SHA-256 values match the README.
- Restored ZIP: 26,968,926 bytes, SHA-256 687256807635a173aa3b7d9d42d562417fd842d25bf78ef01f98db186a3c8f37. CRCs
  pass; 459 members; no absolute paths, `..` components or symlinks.
- My own check confirms all 458 MANIFEST.json members by size and hash, with no unlisted files, and both bundle
  hashes: published-base e6411b5f8f9def63…, unpublished-audit b8bbe74bb41be556….
- `verify_package.py` and `reconstruct.sh` were read, not executed. I ran the same git commands myself in a fresh
  repository, with global and system config disabled and LFS smudging off:
  - `published-base.bundle` holds complete history at 313f17fc;
  - `unpublished-audit.bundle` verifies against that base;
  - **HEAD = ff29c90e139ab34241d09070aa9316106f5247a1**, `git fsck --full` clean, clean checkout, no alternates;
  - the 12 commits are 8f96f0d … ff29c90.
- The published base is identical to GitHub `codex/endpoint-documentary-reconciliation` (313f17fc, tree 149db226).
- All 60 files of the first single-ZIP bundle are byte-identical to the same paths at ff29c90. So the first audit
  applies to the commit unchanged, and the checker on the reconstructed tree gives an identical log and JSON apart
  from wall time (`results/independent_t050_on_ff29c90.*`).

## 2. Dependencies now accessible (previously listed as omitted)

| dependency | where at ff29c90 | status |
|---|---|---|
| T=1/2 validator d849ec96, producer ad8e4fb8, chain 309b8699, per-cell chain 9d338c69 | `extension-t050/initial-source-diff.patch` over 8f96f0d sources | materialized by me with `patch`; all six hashes match |
| source hull 33e69640, z2-endpoint 160789cf | `resource-amendment/generated-sources/` (with hull/endpoint diff patches) | present; inspected |
| verify_percell 29f750b9, tr_remainder b193c13b, route-b bounds a5aadad5, time_refinement c2586f5d | `generated-sources/` | present; not needed (reproduced or bypassed in VERDICT.md) |
| extension READMEs, PREREGISTRATION, REVIEW_A/B/C, AMENDMENT, process records | `extension-t050/`, `resource-amendment/` | read (reviews skimmed for findings) |
| inherited-chain audit (T=1/4 full replay) | `inherited-chain-audit/` | AUDIT.md read |
| file-hash ↔ array-bytes-hash link for W/Q | `extension-t050/results/trajectory-manifest.json` | present (a recorded claim) |
| W_nodes.npy, Q_nodes.npy (546 MB) | excluded by design | still absent |

## 3. New checks

1. **Horizon transformations only.**
   - Validator: `NSTEP` 12500 → 25000 plus two docstring lines.
   - Producer: `T` 0.25 → 0.5.
   - Chain scripts: `T` and the scope assertion, a fixed-β assertion, and labels. `checker/make_t050_variant.py` had
     already reproduced every output of these.
   - Source hull and endpoint scripts: horizon constants, input pins, the cell count 250 → 500 and a timeout.
2. **The validator has no hidden t ≤ 1/4 assumption.**
   - e^{−νt_j} is enclosed at every node.
   - The residual is the exact residual of the finite-mode path: products are supported through k_x ≤ 11,
     k_y ≤ 31, and W through |n| ≤ 22, with no discarded tail.
   - The frozen-shear correction is per cell, and grids and weights do not depend on the horizon.
   - Review A additionally checks that the base-error rate stays nonnegative on [0, 1/2]
     (√8·e^{−νt} − ν > 0, since e^{−νt} ≥ 55/56).
3. **Source hull (the input with least slack for J2) is sound as written.**
   - Each coefficient's disc hull of the 51 nodes contains the whole piecewise-affine path, by convexity.
   - The exact Leray projection on (k_x, k_y, 1) is evaluated on discs.
   - The mean tensor is (Q⊗Q̄ + Q̄⊗Q)/4 = the z-average of q⊗q. Only x and y rows are differentiated (the z-average
     kills ∂_z), and the zero mode is set to zero, which is correct for an exact derivative.
   - The norm is √Σ|F_k|², without the ½ factor, which is correct for a real k_z = 0 field. This bounds the z-average
     of B(q_N, q_N) over each whole coarse cell.
4. **Endpoint script matches my independent derivation.**
   - It uses the final node (t = T).
   - ‖∇q_N‖² = ½Σ(|k|²|Q|² − |k·Q|²) and ‖Δw_N‖² = ½Σ(1+n²)²|W_n|².
   - E = ½(‖∇q_N‖ ∓ ε₁)², with ε₁ = chain.json's rounded-up 4.8005E-4.
   - G = √(e^{−2νT}/2 + ‖Δw_N‖²) + √(2/27)·ε_W, with the identity 4(x+2)³ − 27(x+1)² = (x−1)²(4x+5) ≥ 0 checked.
   - The reconciliation in VERDICT.md B2 reproduces its stored E and G to 40 digits from the stored exact fractions.
5. **Freeze integrity.** certify.py and its PLAN, bounds.py and its PLAN, and evaluate.py and its PLAN are each
   byte-identical from their freeze commit to their result commit and at HEAD. Between base and head the only
   modified files are `docs/HANDOFF.md` (+80/−0) and `docs/RESEARCH_INDEX.md` (+57/−0); every inherited source
   and result is untouched.
6. **Inherited-chain audit (Codex, T = 1/4).**
   - It ran the full 12,500-cell residual validator once on cached arrays and matched every enclosure. Source-hull
     and endpoint replays also matched, and its Group A reviewer independently derived Lemma M and the every-cell
     bounds.
   - Its independent directed R250 computation certifies C_A ≤ 4.06707921079 < 4.06707921080.
   - It found one substantive defect: the per-cell verifier's predicate does not prove upper direction (exact
     counterexample retained). At T = 1/2 this is moot, because the rerun of the reviewed recursion reproduces all
     500 rows directly.
7. **Extension reviews A/B/C.** No blocking defects. The one pre-run defect (stale T = 0.25 output label) is fixed
   in the patch above.

## 4. Scalar reproduction versus full residual rerun

- **Reproduced (array-free):**
  - the analytic adjoint lemma and the 274 bound;
  - the 500-row chain and the closure, from `validated.json`, by reviewed code;
  - Ahat, D_w, I_∞, N_r, E_r, D_r and the nonself bound;
  - J2 and the final comparison, H/b² ≥ 0.0032893405898; reconciled to the committed 0.0032893405206 in VERDICT.md B2;
  - E and G from the stored exact fractions.
- **Not rerun at T = 1/2 (needs the excluded arrays):**
  - the 25,000-cell residual validation that produced `validated.json`;
  - the 500-cell source-hull replay;
  - recomputation of the two endpoint fractions and of ‖Δq_N(T)‖.
- The code for all of these is now inspected and is horizon-generic. The same code's T = 1/4 run was fully replayed
  by the inherited-chain audit.
- **What stays inherited:**
  - that these programs were run on the recorded arrays and produced the stored numbers;
  - the correctness of the hand-written binary64 disc arithmetic and the platform assumptions (round-to-nearest,
    gradual underflow, no FMA);
  - standard PDE foundations.
- The rigorous claim requires every one of these enclosures to be a valid bound. The one-at-a-time sensitivity
  figures (U_i 2.45 %, G 2.34 %, E 0.00329) only show where the conclusion has least slack. They are not error
  allowances.

## 5. Updated gap status (references to VERDICT.md section E)

- **E1 (array-derived enclosures not recomputable from the bundle):** narrowed.
  - The producing scripts, their reviews and the hash link are now included and inspected.
  - What remains is recomputing U_i, E, G and ‖Δq_N(T)‖ from the excluded arrays.
  - Repair still recommended: ship Q_nodes[25000] and W_nodes[25000] (about 21 KB) so E, G and ‖Δq_N(T)‖ can be
    recomputed exactly without the 546 MB arrays.
- **E2 (validated-only ‖Δq_N‖ fallback, margin 0.000351):** stands as a recommendation.
- **E3 (per-cell coverage citation):** supported by the inherited-chain audit's Group A derivation; cite it from
  PROOF.md §5.
- **E4 (inactive cap), E5 (uneven slack) and E6 (full-precision envelopes, +6.9·10⁻¹¹):** unchanged.

## 6. Verdict

Unchanged: **not disproved.** For every 0 < |b| ≤ 0.003, H_b(1/2) ≥ 0.00328934052060975·b². The claim is
conditional on the excluded-array computations being valid enclosures (inspected, not replayed at T = 1/2) and on
the stated arithmetic and PDE assumptions. The package resolves the earlier "omitted dependency" findings except for
the arrays themselves.
