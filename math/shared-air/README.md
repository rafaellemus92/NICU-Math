# Shared Air

The page and its simulator audit. The Lean proofs are in
[`../wyrd-mathlib/WyrdMathlib/SharedAir/`](../wyrd-mathlib/WyrdMathlib/SharedAir/) and
[`../wyrd-mathlib/WyrdMathlib/Limits/`](../wyrd-mathlib/WyrdMathlib/Limits/), and the Python delay
and bistability checks in [`../numerics/shared-air/`](../numerics/shared-air/) and
[`../numerics/shared-air-limits/`](../numerics/shared-air-limits/).

Shared Air is a single-page interactive model of a mother and her infant in the NICU. It asks a
bedside question. When a mother holds her baby and their heart rates rise and fall together, what
carries it?

The page builds three answers from the same simulated cells:

- **Perceived.** Mom notices the infant's state and responds, with a delay.
- **Physical.** Skin contact acts on the infant's cells directly, through warmth and mom's heartbeat.
- **Alike.** Nothing passes between them. They just share a room, its alarms and its rhythms.

Six tests then ask which bedside measurements could tell the three apart. The model has three
levels:

- **Cells.** Pacemaker and breathing cells are phase oscillators, not ion-channel models.
- **Person.** One arousal variable per person drives heart rate and breathing.
- **Pair.** Mom and infant are coupled by contagion, mirroring and soothing.

Every parameter is illustrative and chosen to give realistic resting rates. None is fitted to
patients. The page says so in its Limits section.

`AUDIT.md` explains what an outside "proof audit" of the model got right and what it overstated. It
also explains what actually drives the results, lists the corrections made to the page, compares
the page with the v2 revision of the model text, and lists the Lean proofs behind each claim.

## Where the page is

The corrected page lives in the website, at
[`../../web/public/shared-air/index.html`](../../web/public/shared-air/index.html). It is live at
https://nicu-math.vercel.app/shared-air. That file is the only copy; this folder holds no page of its
own. It also opens directly from disk in any current browser; nothing needs installing. The page
loads Google Fonts when online and falls back to system fonts offline. Stored results show at once.
"Run with my settings" reruns a test in the browser. Test 4 is the slowest: about 30–45 s on a
desktop, more on a phone.

## What is in this folder

| Path | What it is |
|---|---|
| `AUDIT.md` | The audit summary: claims, verdicts, mechanisms, corrections, review, the v2 text, Lean cross-links. |
| `tools/load.js` | Loads the model code out of the page for node. By default it finds the page at `../../web/public/shared-air/index.html` from this folder, wherever you run it from. |
| `tools/quick_check.js` | Reruns Test 5b and compares it with the stored result; prints the locking numbers. |
| `tools/lock_proto.js` | Exact 2:1 locking range for one forced phase, at adjustable resolution. Needs no HTML. |
| `tools/theory_check.js` | Linear facts (g*, g_c, the delay-induced oscillation), the stuck second state, and a deterministic recovery comparison. |
| `tools/adjudicate.js` | Test 4 on fresh seeds with the soothing cap on or off (the 200-seed table in AUDIT.md). |
| `tools/kick_check.js` | With arousal noise off: whether the heel stick alone reaches the stuck state, and the smallest kick that does. |
| `tools/room_check.js` | The room-subtraction caveat: the alike-world contrast with mom awake, asleep or away. |
| `tools/within_mom_check.js` | The same mother awake against asleep, and holding against not, in the alike world. |
| `tools/regen_def.js` | Recomputes the stored Test 4 and Test 5b results. Checks by default; `--write` stores them in the page. |
| `tools/time_sweep.js` | Times Test 4 at a few run counts. |
| `tools/render.js` | Optional browser check (Playwright) of the page file: page errors, overflow, rendered finding text. |
| `results/adjudication/` | The four 200-seed Test 4 runs (seeds 300000+i). |
| `results/checks/` | Saved output of every check below, with timings. Outputs saved before this folder moved into `math/` name the page `shared_air.html`, its file name then. |
| `results/verifier_findings.json` | The independent verifiers' and challengers' record (claims, verdicts, evidence). Two entries (R14, K18) carry an 18 October note. |
| `results/review_findings.json` | The independent review of the corrections. |
| `results/corrections.diff` | Original page to corrected page, with the stored-results line left out. |
| `package.json` | Script shortcuts only. There are no dependencies. |

## Reproducing the checks

Every check needs only node (18 or later; tested on 22.22.0). Run the commands from this folder,
for example `cd math/shared-air`. The scripts find the page from their own location, so they also
work from elsewhere. The timings were measured on a 4-core Linux container.

| Check | Command | Time | What you should see |
|---|---|---|---|
| Model loads; Test 5b matches the stored result | `node tools/quick_check.js` | 4 s | `all 16 DEF.pulse fields match`; exact onset 4, closes 19.709, +10 bpm 8.376, −10 bpm never |
| Exact 2:1 locking | `node tools/lock_proto.js` | 2 s | onset 4.00023 at three resolutions; first-order 3.3135 |
| Theory | `node tools/theory_check.js` | 12 s | g* 0.0803558863, g_c 3.8580006724, oscillation at g 1.6117 for τ = 3, saddle-node at 2.0689 |
| Entering the stuck state | `node tools/kick_check.js` | 9 s | heel stick stuck at none; at g = 3 smallest kick 1.334 (τ 0.02) and 1.407 (τ 1.5), long run |
| Room subtraction | `node tools/room_check.js 60 1000` | 13 s | awake −0.037, asleep −0.123, away −0.206 |
| Same, other seeds | `node tools/room_check.js 100 20000` | 22 s | −0.020, −0.116, −0.225 |
| Same mother | `node tools/within_mom_check.js 60 1000` | 16 s | awake minus asleep +0.086 ± 0.013; holding minus not 0 |
| Same, other seeds | `node tools/within_mom_check.js 100 20000` | 22 s | +0.096 ± 0.009; holding minus not 0 |
| Test 4 adjudication, small | `node tools/adjudicate.js 1.5 0 20 300000` | 6 s | one JSON line (20 seeds; too few to read much into) |
| Test 4 on the page's own 14 seeds | `node tools/adjudicate.js 0.02 0 14 5000` and `node tools/adjudicate.js 1.5 0 14 5000` | 8 s | K = 3 median 140.25 at both delays |
| Test 4 adjudication, full | `node tools/adjudicate.js 1.5 0 200 300000 \| cmp - results/adjudication/t15_cap.json` | 50 s (62 s with four in parallel) | no output from `cmp` (identical) |
| Stored Test 4 and 5b results | `node tools/regen_def.js` | 2 min 18 s | `DEF.pulse reproduced exactly`, `DEF.sweep reproduced exactly` |
| Same, quick | `node tools/regen_def.js --R 14 --only sweep` | 10 s | the original page's 14-run curve (no comparison: R differs) |
| Browser (optional) | `NODE_PATH=/opt/node22/lib/node_modules node tools/render.js` | 4 s | no errors, no horizontal scroll at 1100 and 390 px |

The full adjudication arguments are `<tau> <capOff 0|1> <R> <seed0> [out.json]`. The four stored runs
are `0.02 0`, `0.02 1`, `1.5 0` and `1.5 1`, each with `200 300000`. Run all four in parallel and
they take about 62 s on 4 cores. Their medians use the page's `median`. The quartiles are simple
order statistics (`sorted[floor(p·R)]`), not interpolated.

`regen_def.js` never changes the page unless you pass `--write`, and then it writes to the live
page's file in `web/public/shared-air/`. A write test on a scratch copy gave a byte-identical file
(`results/checks/regen_def_write_test.txt`).

`render.js` needs Playwright with Chromium already installed. Playwright is not bundled. Point
`NODE_PATH` at an existing install; the path above is this container's. Pass a directory as the
first argument to save screenshots.

The page's sha256 is `e9017600…cd04` (printed by `quick_check.js`). It changed from `b5249de8…e295`
on 18 October with text edits only (AUDIT.md section 7); no model code changed, and the stored
results reproduce as before.

## Publish status

The corrected page is published on the site at https://nicu-math.vercel.app/shared-air, from
`web/public/shared-air/index.html`. An earlier claude.ai artifact,
https://claude.ai/artifact/Daui6a5m1K1N4up84DPvcR, still showed the **original, uncorrected** page
when this folder was written. The original page's sha256 is `a34629b9…b451`; that file is not
included, but its text is [`../inputs/Shared_Air_Model_v1.md`](../inputs/Shared_Air_Model_v1.md) and
`results/corrections.diff` shows every change to it.

## Provenance

The page, the helper scripts and the checks were written by AI agents. They worked in several
rounds: build, independent verification, refutation, adjudication, correction and review. The node
scripts here are cleaned-up versions of the helpers from those rounds, made to run from this folder.
The verifiers' own scripts (Python with sympy and mpmath, plus node) are not included. Their findings
are recorded in `results/verifier_findings.json`.

ChatGPT's audit package is kept as uploaded in
[`../inputs/shared_air_proof_audit.zip`](../inputs/shared_air_proof_audit.zip). The text of the
original page, which ChatGPT audited, is [`../inputs/Shared_Air_Model_v1.md`](../inputs/Shared_Air_Model_v1.md).
The v2 revision of that text, [`../inputs/Shared_Air_Model_v2_revised.md`](../inputs/Shared_Air_Model_v2_revised.md),
was made separately; AUDIT.md section 10 compares it with the corrected page.
