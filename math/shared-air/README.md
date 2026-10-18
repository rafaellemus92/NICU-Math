# Shared Air audit tools

An audit and reproduction harness for the existing
[Shared Air HTML](../../web/public/shared-air/index.html). This is an
**unvalidated synthetic teaching model**, not patient evidence. The audit's
historical reviews and saved outputs are not fresh verification or clinical validation.

Source: `rafaellemus92/NICU-Math`, `claude/breath-rhythm-ns-jet`, exact commit
`77916bb51ea88ea6e1b2cddd2cd6e9309993383f`, folder `shared-air/`.
Source HTML and the integration-base page both have Git blob
`d283a8ebaaf13fe2a262d212f0eca4afc2c17c00`. No HTML was duplicated or edited.
The source README's pending-publication wording is superseded here by the
verified repository integration; external artifact/hosting publication is not checked.

## Included and excluded

- [AUDIT.md](AUDIT.md): historical claims, mechanisms, corrections and unresolved issues.
- `tools/`: standalone Node checks. `load.js` defaults to the integrated HTML,
  relative to this folder, independent of the working directory.
- `results/`: historical synthetic outputs and review records; original provenance
  retained. Redacted `<session scratchpad>` placeholders are archival descriptions,
  not usable machine-specific paths.
- HTML, package manifest, `regen_def.js` (can write the app), `render.js`
  (machine-specific browser setup), render log and HTML corrections diff are excluded.
  See the [pinned source](https://github.com/rafaellemus92/NICU-Math/blob/77916bb51ea88ea6e1b2cddd2cd6e9309993383f/shared-air) for those artifacts.

## Reproduce without changing the page

From repository root, Node 18+:

```sh
node math/shared-air/tools/quick_check.js
node math/shared-air/tools/lock_proto.js
node math/shared-air/tools/theory_check.js
# Optional ensemble studies, not part of the focused import validation:
node math/shared-air/tools/room_check.js 60 1000
node math/shared-air/tools/adjudicate.js 1.5 0 20 300000
node math/shared-air/tools/time_sweep.js
```

`quick_check` compares all 16 stored DEF.pulse fields and fails on disagreement.
Locking/theory scripts print numerical diagnostics; a zero exit alone is not a
proof of their mathematical claims. Full 200-seed adjudication, stored sweep
regeneration and browser checks were not rerun in this import.
Current outcomes and runtimes: [import record](../navier-stokes-jet/IMPORT.md).

## Unresolved limitations

Phase noise is not scaled with timestep; changing dt is not a demonstrated
convergence study. Reported infant heart rate differs from beat count under
strong pulse forcing (historical audit: 150.48 vs 143.84 bpm at strength 16,
about 0.9 bpm discrepancy at default 6). Recovery uses the first 15-second hold
and can miss relapse. The delay has a minimum one-step value; zero-delay
mathematics does not exactly describe the running simulator. These issues are
preserved, not repaired by importing the audit tools.
