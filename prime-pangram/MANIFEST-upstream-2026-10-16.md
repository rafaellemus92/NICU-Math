# Prime pangram project — packaged sources

Packaged on 2026-10-16 from two Git repositories at their current branch tips.
The paths under each top-level folder are exactly the paths inside that
repository, so the directory structure is preserved.

| Folder | Repository | Branch | Commit | Contents |
|---|---|---|---|---|
| `NICU-Module/pangram/` | rafaellemus92/NICU-Module | `claude/pangram-prime-words-kgdssi` | `2323373` | Prime perfect pangrams in bijective base 26: Python + C search and counting code, onset/coda lists, dictionaries, results |
| `sgrounds/experiments/` | rafaellemus92/sgrounds | `claude/new-session-sbrl43` | `633f161` | Coupled base-26 five-pair pangram finder (Python), the `wyrd` Lean 4 proofs, the `wyrd-mathlib` bridge to Mathlib, and `checks/` (complete enumerations for both naming rules) |
| `sgrounds/.github/workflows/lean.yml` | rafaellemus92/sgrounds | `claude/new-session-sbrl43` | `633f161` | GitHub Action that builds both Lean projects and audits their axioms |

## Where to find each kind of file

- **Lean sources, core Lean only (no Mathlib):** `sgrounds/experiments/wyrd/`
  (`Wyrd.lean`, `Audit.lean`, `Wyrd/*.lean`). Proved there: the encoding is
  reversible, the 4296 certificate, the 1352 lower bound, distinctness, parity,
  **4296 is the smallest sum** (`smallest_pangram_sum` in `Wyrd/Smallest.lean`:
  a kernel-run search over the 1,472 remaining even sums, proved complete in
  `Wyrd/Minimal.lean`, over precomputed data in `Wyrd/MinimalData.lean` and
  `Wyrd/MinimalTable0.lean` … `MinimalTable3.lean`), Euclid's infinitude of
  primes (`Wyrd/Euclid.lean`), and √2 irrational in whole-number form
  (`Wyrd/Sqrt2.lean`). `scripts/gen_candidates.py` and `scripts/GenTables.lean`
  regenerate the precomputed data; the kernel re-checks it, so it is not trusted.
- **Lean sources with Mathlib:** `sgrounds/experiments/wyrd-mathlib/`
  (`WyrdMathlib/Bridge.lean`, `WyrdMathlib/Sqrt2.lean`): `IsPrime ↔ Nat.Prime`,
  the primes form an infinite set, the ten pangram primes are `Nat.Prime`,
  `Irrational √2`, and Bertrand's postulate borrowed from Mathlib.
- **Lake configuration:** `lakefile.toml`, `lake-manifest.json` and
  `lean-toolchain` in each Lean folder. Both pin `leanprover/lean4:v4.35.0`;
  `wyrd` has no dependencies, `wyrd-mathlib` requires Mathlib `v4.35.0` and `../wyrd`.
- **Python:** `NICU-Module/pangram/*.py`, `sgrounds/experiments/coupled_prime26_pangram.py`,
  `sgrounds/experiments/checks/enumerate_all.py`, `sgrounds/experiments/wyrd/scripts/gen_candidates.py`.
- **C helpers:** `NICU-Module/pangram/mr.c` (Miller–Rabin), `xcover.c` (exact
  cover), `freedp.c` (independent count); `sgrounds/experiments/checks/pangram_all.c`
  (complete enumeration of five-pair pangrams).
- **Exact onset/coda data:** `NICU-Module/pangram/clusters.py` (70 onsets and
  175 codas, each list including the empty cluster, with example words).
- **Dictionaries:** `NICU-Module/pangram/results/english_prime_words.txt` and
  `results/free_prime_masks.txt`. Both are generated; `run_a_english.py` and
  `run_d_free_count.py` rebuild them.
- **Tests:** `python3 core.py && python3 engine.py` runs the self-tests in
  `NICU-Module/pangram`. In each Lean folder, `lake build` checks every proof and
  `lake env lean Audit.lean` lists the axioms each theorem uses; the GitHub
  Action runs both and fails on `sorry` or `native_decide`.
- **Machine-readable results:** `NICU-Module/pangram/results/*.json`,
  `results/b_lattice/*.json`, `results/b_lattice/log_*.txt`,
  `results/b_single_cluster.json`, `results/b_single_k5.txt`;
  `sgrounds/experiments/checks/coupled_all.txt` (all 12 coupled-rule pangrams),
  `checks/plain_all.txt` (empty: none exist under plain naming) and the two run logs.
- **READMEs:** `NICU-Module/pangram/README.md`; `sgrounds/experiments/README.md`,
  `checks/README.md`, `wyrd/README.md`, `wyrd/ROADMAP.md`, `wyrd-mathlib/README.md`.

## Deliberately not included

- **JavaScript:** neither project contains any. Every branch of both
  repositories was searched for JavaScript, TypeScript or HTML files that
  mention pangrams, and none exist.
- **Build outputs:** the compiled helpers `libmr.so`, `xcover`, `freedp` and
  `pangram_all`, Python `__pycache__/`, and Lean's `.lake/` directories
  (including the ~7 GB Mathlib cache that `wyrd-mathlib` downloads).
- **Large intermediates:** `results/reach_mod*.npz`, `results/_xcover_*.dat`
  and `results/*.log` were never committed; the scripts regenerate them.
- **Files from `/tmp` or a scratchpad:** the verification files written earlier
  in this session are now committed as `sgrounds/experiments/checks/`, so they
  come from the branch tip like everything else.
- **Secrets:** none were found in the packaged files.

## Rebuilding

Python and C. Requires Python 3 with NumPy (`pip install numpy`) and gcc. The
block below is the "Reproduce everything" recipe copied verbatim from
`NICU-Module/pangram/README.md` at the packaged commit. That README heads the
block "≈2 h on 4 cores, 8 GB RAM" and, in its notes, puts the total wall time for
everything at about 3 hours on 4 cores; per-script timings are listed there. The
witness search for R(3,0) and R(0,3) is skipped on purpose (see its notes). In
this archive the directory is `NICU-Module/pangram`, so begin with
`cd NICU-Module/pangram` instead of `cd pangram`:

```sh
cd pangram
gcc -O2 -shared -fPIC -o libmr.so mr.c && gcc -O2 -o xcover xcover.c && gcc -O2 -o freedp freedp.c
python3 core.py && python3 engine.py            # self-tests (closed-form check of the engine)
python3 run_a_english.py
python3 structure.py
python3 run_d_free_count.py && ./freedp results/free_prime_masks.txt
python3 run_c_english.py
python3 run_b_lattice.py B                         # free family, n+m <= 5
python3 run_b_lattice.py "R(0,0)" "R(1,0)" "R(0,1)" "R(1,1)" "R(2,0)" "R(0,2)" "R(2,1)" "R(1,2)" "R(2,2)"
python3 run_b_lattice.py "R(3,0)" "R(0,3)" --nowitness   # witness search skipped (see notes)
for i in 0 1 2; do python3 reach.py $i; done ; python3 run_b_single.py 5
python3 check_single.py jvq ; python3 check_onset3.py 3 ; python3 check_onset3.py 4 ; python3 check_coprime.py
python3 summarize.py                                # regenerates the lattice tables from results/b_lattice/*.json
```

The five-pair finder and the complete enumerations:

```sh
python3 sgrounds/experiments/coupled_prime26_pangram.py          # coupled digits: N = 4296, ~0.2 s
python3 sgrounds/experiments/coupled_prime26_pangram.py --plain  # plain base 26: no solution up to 18,250
cd sgrounds/experiments/checks && gcc -O2 -o pangram_all pangram_all.c
./pangram_all coupled 1352 457000   # all 12 solutions, ~2 min
./pangram_all plain   1352 457000   # none, ~2 min
```

Lean, core project (the toolchain downloads on first use; the build is about
10 minutes on 4 cores, mostly the minimality search):

```sh
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
cd sgrounds/experiments/wyrd
lake build
lake env lean Audit.lean
```

Lean with Mathlib (needs the prebuilt Mathlib files, about 7 GB):

```sh
cd sgrounds/experiments/wyrd-mathlib
lake exe cache get
lake build
lake env lean Audit.lean
```

`elan` fetches the pinned toolchain from `releases.lean-lang.org` (verified:
that is the host it downloaded v4.35.0 from). The Mathlib download was not run
in this session. For the pinned Mathlib revision, `lake exe cache get` fetches
the git dependencies from `github.com` and the prebuilt files from
`cache.mathlib.org`, following redirects, so the final storage host may differ;
`lakecache.blob.core.windows.net` is only used with
`MATHLIB_CACHE_DEBUG_USE_LEGACY=1`. In a Claude cloud session with limited
network access, add whichever host the download reports as refused.

## Changes since the previous archive

The previous archive was built from sgrounds `be739df` and NICU-Module
`4c12e62`. New since then:

- sgrounds: the Lean proof that 4296 is the smallest sum (`Smallest.lean`,
  `Minimal.lean`, `MinimalData.lean`, `MinimalTable0-3.lean`, `scripts/`),
  Euclid (`Euclid.lean`), √2 (`Sqrt2.lean`), the `wyrd-mathlib` project, the
  CI job for it, and `checks/` (with the fixes made after review: the Python
  enumerator's early-cover guard and the README's account of what is Lean-proved).
- NICU-Module: thirteen commits of pangram-analysis fixes and results
  (`run_b_lattice.py`, `summarize.py`, `xcover.c`, new `R(o,c)` lattice
  results, `b_single_cluster.json`, `b_single_k5.txt`, README wording).
