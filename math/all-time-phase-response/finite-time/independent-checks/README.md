# Independent checkers: Route A, Route B and the time-resolved endpoint remainder

Owner: Claude, session "Navier Stokes-Speech", 19 October 2026. Branch `claude/endpoint-sign-audit`,
based on `cedb77cc8eb45d9f465ff5e61383689e0fa001d8` (claude/endpoint-sign-research). Nothing outside this
folder is changed. These are AI audit artifacts: code that recomputes another author's results by an
independent route, with its outputs. They are evidence for or against those results, not proofs, not
human refereeing, and not formal verification. No trajectory was read, no LFS object was fetched, and no
DNS, validator, adjoint or q₂ solve was run.

## What each subfolder checks

| folder | audited commit and claim | method | outcome |
|---|---|---|---|
| `route-a-cd9c9f0/` | Route A corollary: the parent chain of ../NOTE.md with β₁ replaced by 3/1000 gives C_Z(1/4) ≤ 1.2102·10¹⁴ | a three-line hook on the parent's `constants.py` (`beta_hook.patch`), run once without and once with the hook | unhooked run reproduces ../results/constants.log at T = 1/4; hooked run gives C_Z ≤ 1.2102·10¹⁴ |
| `route-b-375e399/` | route-b-dissipation formulas (1), (3), (5), (7), (8): C_B ≤ 87807, \|R_Z\| ≤ 7.1123·10⁻⁶ at \|b\| = 0.003 | own transcription of the note's formulas, 90-digit decimal, nearest rounding | every value lies inside the committed interval of `bounds.json` |
| `endpoint-sign-cedb77cc/` | PLAN.md A–F and scripts/tr_remainder.py: C_one,TR ≤ 1201.92, rule (D), b* | own implementation of A–F and of DERIVATION.md variant B, on the parent's directed-rounding decimal intervals (not mpmath); exact-rational and tight-case tests; rerun of the per-cell chain | all committed numbers reproduced; see below |

## The endpoint-sign checks (cedb77cc)

Run from `endpoint-sign-cedb77cc/`, with `<FT>` this repository's `math/all-time-phase-response/finite-time`
and a fresh output directory (the series file is created exclusively):

    python3 -B independent_tr.py <FT> <fresh dir>          > independent_tr.log      # about 9 s
    python3 -I -B synthetic_checks.py <fresh dir>/tr_series_lambda1e6.json            # about 11 s
    python3 -I -B tight_weights.py                                                   # about 3 s

and, for the per-cell inputs, from `<FT>/endpoint-sign/scripts/`: `python3 -I -B make_chain_percell.py`
then `python3 -I -B chain_percell.py --json <fresh path>` (under 1 s). Total for the logs in `results/`:
24.6 s.

**Reproduced numerically** (logs in `results/`):

- The per-cell chain: the regenerated `chain_percell.py` is byte-identical to the committed script, and
  its fresh output is byte-identical to `endpoint-sign/results/chain_percell.json`
  (SHA-256 795e3a7b…, all 250 rows; `chain_percell_rerun.log`).
- Formulas A–F at all five λ: the time-resolved N_r(T), E_r(T), N̄ and C_one agree with
  `endpoint-sign/results/tr_remainder.json` to every printed digit; D_w,TR(T) ≤ 26061.109227257; the
  global collapse reproduces route-b-tightening's N_r, E_r, N̄ exactly (`independent_tr.log`).
- The final comparison and the smaller-amplitude conclusion, every endpoint rounded in its safe direction:

| quantity | committed | recomputed here |
|---|---|---|
| C_one,TR (λ = 10⁶) | 1201.9175374897… | ≤ 1201.9175374898 |
| lower end of J2 | 0.0082007206804663… | ≥ 0.0082007206804663 |
| β² C_one,TR | 0.0108172578374079… | ≤ 0.010817257837408 |
| H_b/b² at \|b\| = 0.003 | ≥ −0.0026165371569416… | ≥ −0.0026165371569417 |
| b*, lower end | 0.0026120932319102… | ≥ 0.0026120932319102 (< β) |

  Rule (D) is the target comparison of the sign of H_b(T) over the whole range; it fails as a comparison
  (0.0082007 is not above 0.0108173). That is not a defective formula. The positive sign of H_b(T) holds,
  conditionally on the assumptions below, for every 0 < |b| < 0.00261209 (strict); |b| = 0.003 remains
  unresolved.

**Tested on synthetic data** (`synthetic_checks.log`, `tight_weights.log`):

- Summation by parts against cumulative upper bounds: the implemented form (nonincreasing majorant,
  terminal term φ_j B_j, coefficients φ_i − φ_{i+1} on B_i, B₋₁ = 0) is valid in 4000/4000 exact-rational
  trials; dropping the majorant, dropping the terminal term, or shifting B by one index fails in 1645,
  1381 and 436 trials.
- Propagation weights: on x′ = (m − ν)x + f with m, f constant on each cell (exact solution), the
  inclusive weight exp(Σ_{k=i..j}(m_k − ν)Δ) dominates (worst ratio 0.94); excluding the source cell fails
  (ratio 3.19). With cellwise sup inputs the excluded variant shows no violation (0.58), so a test needs
  the tight case.
- The cumulative envelopes D_w,j and K_j are nondecreasing in j (a sanity check; summation by parts
  does not need it).
- A deliberately wrong time-resolved variant (source cell excluded from the weight) passes both the
  collapse check and the "time-resolved ≤ global" check (`independent_tr.log`, last line): those checks are
  consistency checks of the implementation, not evidence that the time-resolved inequalities hold.

**Inspected, not reproduced:** the paper derivation of each of A–F (zero initial data for w, r, the mean
of r and the Lemma B cap; cumulative use of δ_j, D_w,j, I∞,j with sup factors and largest weights;
Cauchy–Schwarz and Minkowski steps; the observable inequality); Lemma M's coverage of every per-cell row
(it states monotonicity of K(t; b), N_w(t; b), and the rows are exact upper endpoints); the mpmath
rounding inside tr_remainder.py and sign_enclosure.py, which were not run (mpmath is not installed here).

**Audit findings sent to the owner (none blocking):** pin `source-only-hull/results/full.json`
(SHA-256 0d2ab266fd226091a9116b83c54621ad480f2b8306f16e9dd830a705629cfa82) in both scripts; add exact
toy-equation tests that reject the wrong weight and summation-by-parts variants (the two scripts here are
such tests); verify all 250 per-cell rows (done here by the rerun); state Lemma M's per-cell coverage and
the completed review status.

**Inherited, not re-verified here:** the absorption certificate at 763c275 (validated enclosures, Lemma M,
closure; IEEE binary64 round-to-nearest with gradual underflow and no fused multiply-add); the parent at
cd9c9f0 (C_A ≤ 4.06707921080, base-flow bounds, (I1)–(I6), mean-zero Agmon); route-b-dissipation (audited
by this session at 375e399) and route-b-tightening Lemmas A and B; the z2-endpoint enclosure (G ≤ 1.8534,
½‖∇q₁(T)‖²); the source-only hull bounds; correct Python `decimal` and mpmath.

## Route B (375e399)

`python3 -I -B independent_eval.py <FT> > results/independent_eval.log` (under 1 s). Its inputs
(route-b-dissipation/results/bounds.json, absorption-b003 chain.json and validated.json) are unchanged
between 375e399 and cedb77cc. Nearest-rounded 90-digit arithmetic: a check of the formulas, not a
certificate; the committed intervals are the certificate.

## Route A (cd9c9f0)

`results/base_T025.log` and `results/beta003_T025.log` are the outputs as produced on 19 October 2026 in a
scratch copy; they are preserved, not rerun. To reproduce (about 20 s each): copy ../constants.py and
../results/lattice_sums.log into a scratch folder (`results/lattice_sums.log` beside the script), apply
`patch constants.py < beta_hook.patch`, then run `python3 -B constants.py --T 0.25` and
`python3 -B constants.py --T 0.25 --beta 3/1000`.

`SHA256SUMS` lists every file in this folder.
