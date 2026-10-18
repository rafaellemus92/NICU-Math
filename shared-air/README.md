# Shared Air

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
also explains what actually drives the results, and lists the corrections made to this page.

## Opening it

Open `shared_air.html` in any current browser; double-clicking it works. Nothing needs installing.
The page loads Google Fonts when online and falls back to system fonts offline. Stored results show
at once. "Run with my settings" reruns a test in the browser. Test 4 is the slowest: about 30–45 s
on a desktop, more on a phone.

## What is in this folder

| Path | What it is |
|---|---|
| `shared_air.html` | The corrected page (sha256 `b5249de8…e295`). Its model code also runs in node. |
| `AUDIT.md` | The audit summary: claims, verdicts, mechanisms, corrections, review. |
| `tools/load.js` | Loads the model code out of the HTML for node. HTML paths are relative to this folder. |
| `tools/quick_check.js` | Reruns Test 5b and compares it with the stored result; prints the locking numbers. |
| `tools/lock_proto.js` | Exact 2:1 locking range for one forced phase, at adjustable resolution. Needs no HTML. |
| `tools/theory_check.js` | Linear facts (g*, g_c, the delay-induced oscillation), the stuck second state, and a deterministic recovery comparison. |
| `tools/adjudicate.js` | Test 4 on fresh seeds with the soothing cap on or off (the 200-seed table in AUDIT.md). |
| `tools/room_check.js` | The room-subtraction caveat: the alike-world contrast with mom awake, asleep or away. |
| `tools/regen_def.js` | Recomputes the stored Test 4 and Test 5b results. Checks by default; `--write` stores them. |
| `tools/time_sweep.js` | Times Test 4 at a few run counts. |
| `tools/render.js` | Optional browser check (Playwright): page errors, overflow, rendered finding text. |
| `results/adjudication/` | The four 200-seed Test 4 runs (seeds 300000+i). |
| `results/checks/` | Saved output of every check below, with timings. |
| `results/verifier_findings.json` | The independent verifiers' and challengers' record (claims, verdicts, evidence). |
| `results/review_findings.json` | The independent review of the corrections. |
| `results/corrections.diff` | Original page to corrected page, with the stored-results line left out. |
| `package.json` | Script shortcuts only. There are no dependencies. |

## Reproducing the checks

Every check needs only node (18 or later; tested on 22.22.0). Run the commands from this folder,
for example `cd shared-air`. The timings were measured on a 4-core Linux container.

| Check | Command | Time | What you should see |
|---|---|---|---|
| Model loads; Test 5b matches the stored result | `node tools/quick_check.js` | 4 s | `all 16 DEF.pulse fields match`; exact onset 4, closes 19.709, +10 bpm 8.376, −10 bpm never |
| Exact 2:1 locking | `node tools/lock_proto.js` | 2 s | onset 4.00023 at three resolutions; first-order 3.3135 |
| Theory | `node tools/theory_check.js` | 12 s | g* 0.0803558863, g_c 3.8580006724, oscillation at g 1.6117 for τ = 3, saddle-node at 2.0689 |
| Room subtraction | `node tools/room_check.js 60 1000` | 13 s | awake −0.037, asleep −0.123, away −0.206 |
| Same, other seeds | `node tools/room_check.js 100 20000` | 22 s | −0.020, −0.116, −0.225 |
| Test 4 adjudication, small | `node tools/adjudicate.js 1.5 0 20 300000` | 6 s | one JSON line (20 seeds; too few to read much into) |
| Test 4 adjudication, full | `node tools/adjudicate.js 1.5 0 200 300000 \| cmp - results/adjudication/t15_cap.json` | 50 s (62 s with four in parallel) | no output from `cmp` (identical) |
| Stored Test 4 and 5b results | `node tools/regen_def.js` | 2 min 18 s | `DEF.pulse reproduced exactly`, `DEF.sweep reproduced exactly` |
| Same, quick | `node tools/regen_def.js --R 14 --only sweep` | 10 s | the original page's 14-run curve (no comparison: R differs) |
| Browser (optional) | `NODE_PATH=/opt/node22/lib/node_modules node tools/render.js` | 4 s | no errors, no horizontal scroll at 1100 and 390 px |

The full adjudication arguments are `<tau> <capOff 0|1> <R> <seed0> [out.json]`. The four stored runs
are `0.02 0`, `0.02 1`, `1.5 0` and `1.5 1`, each with `200 300000`. Run all four in parallel and
they take about 62 s on 4 cores. Their medians use the page's `median`. The quartiles are simple
order statistics (`sorted[floor(p·R)]`), not interpolated.

`regen_def.js` never changes the page unless you pass `--write`. A write test on a scratch copy gave
a byte-identical file (`results/checks/regen_def_write_test.txt`).

`render.js` needs Playwright with Chromium already installed. Playwright is not bundled. Point
`NODE_PATH` at an existing install; the path above is this container's. Pass a directory as the
first argument to save screenshots.

## Publish status

The published artifact at https://claude.ai/artifact/Daui6a5m1K1N4up84DPvcR still shows the
**original, uncorrected** page. Publishing this corrected version is waiting on the owner's
permission. Until then, `shared_air.html` in this folder is the corrected version. The original
page's sha256 is `a34629b9…b451`; that file is not included, but `results/corrections.diff` shows
every change.

## Provenance

The page, the helper scripts and the checks were written by AI agents. They worked in several
rounds: build, independent verification, refutation, adjudication, correction and review. The node
scripts here are cleaned-up versions of the helpers from those rounds, made to run from this folder.
The verifiers' own scripts (Python with sympy and mpmath, plus node) are not included. Their findings
are recorded in `results/verifier_findings.json`. ChatGPT's audit package is described in `AUDIT.md`,
not copied.
