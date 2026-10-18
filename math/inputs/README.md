# inputs: the user's uploaded source materials

The files the user uploaded during the work, kept as uploaded. They are inputs
to the proofs and audits in the rest of [`math/`](../README.md), not results.

| File | What it is |
|---|---|
| [`Shared_Air_Model_v1.md`](Shared_Air_Model_v1.md) | The *Shared Air* model page as first uploaded: a cells-to-pair model of mother–infant attunement with three worlds (Perceived, Physical, Alike), bedside tests, equations and limits. Text only; the interactive simulator is not included. |
| [`Shared_Air_Model_v2_revised.md`](Shared_Air_Model_v2_revised.md) | The same page revised on 16 October after ChatGPT's audit, which had worked from v1. These are v2's own claims: Test 4's inverted U does not need the delay, the other-parent contrast needs a matched control, the locking condition holds to first order, and "ratios other than n:1" is added to the limits. [`../shared-air/AUDIT.md`](../shared-air/AUDIT.md#10-the-v2-revision-of-the-model-text) §10 gives the checked version of each edit. The delay is not needed for the runs that never recover, but on 200 fresh seeds per point the rise of Test 4's median recovery time does need it; "removing it changes almost nothing" holds only on the page's 14 stored runs ([§4](../shared-air/AUDIT.md#4-what-actually-makes-test-4s-u-shape)). Comparing the same mother awake and asleep is not a matched control for synchrony, though holding against not is ([§6](../shared-air/AUDIT.md#6-the-room-subtraction-caveat)). The live note's "the two adults are matched" holds only while mom is awake and in the room (§6). "Fourteen runs per point" describes the earlier page; the corrected page stores 200 (§4). |
| [`shared_air_proof_audit.zip`](shared_air_proof_audit.zip) | ChatGPT's independent proof audit of the Shared Air equations: `README.txt`, `proof_notes.md`, a standard-library checker `verify_shared_air.py` and its output `audit_results.json`. It worked from the v1 text without the simulator code; [`../shared-air/AUDIT.md`](../shared-air/AUDIT.md) checks its claims against the simulator. The Lean audit of the same equations is in [`../wyrd-mathlib/WyrdMathlib/SharedAir/`](../wyrd-mathlib/WyrdMathlib/SharedAir/). |
| [`periodic_ns_phase_audit.zip`](periodic_ns_phase_audit.zip) | ChatGPT's periodic Navier–Stokes proof exercise: `proof_notes.md`, an exact rational Fourier checker `verify_periodic_ns.py` and `results.txt`, showing that the fields ±u have the same spectrum but opposite initial enstrophy change (1/8 and −3/8 at ν = 1/28). Its quantities at t = 0 are proved in Lean in [`../wyrd-mathlib/WyrdMathlib/PeriodicNS/`](../wyrd-mathlib/WyrdMathlib/PeriodicNS/) (`Example.lean`, `Averages.lean`, `SignFlip.lean`); the enstrophy balance itself is not formalised. |
| [`periodic_ns_lab_v1.zip`](periodic_ns_lab_v1.zip) | ChatGPT's periodic Navier–Stokes phase lab v1, built from the exercise above: solver, 24 simulations, 19 tests and exact phase-family identities. Those identities are re-derived by [`../numerics/navier-stokes/nslab_v1_exact_identities.py`](../numerics/navier-stokes/nslab_v1_exact_identities.py). |
| [`periodic_ns_lab_v2_audit.zip`](periodic_ns_lab_v2_audit.zip) | ChatGPT's lab v2 package as uploaded for audit (folder `periodic_ns_lab_v2/`, with `CLAUDE_HANDOFF.md`, `RESULTS.md`, `proof_notes.md` and `MANIFEST_SHA256.txt`). It is the object audited in [`../ns-phase-audit/`](../ns-phase-audit/). |
| [`all-time-phase-response.zip`](all-time-phase-response.zip) | ChatGPT's (Codex) all-time small-b phase response delivery of 18 October: `DELIVERY.txt`, `SHA256SUMS.txt`, a patch against `efff6a5`, `math/all-time-phase-response/`, and unchanged copies of `audit_v2/dns/ns.py` and `audit_v2/exact/nsseries.py`. The in-repository copy, with the changes its README lists, is [`../all-time-phase-response/`](../all-time-phase-response/). |
| [`coupled_prime26_pangram_original.py`](coupled_prime26_pangram_original.py) | The original prime-pangram script. It is byte-for-byte identical to [`../coupled_prime26_pangram.py`](../coupled_prime26_pangram.py). |

Four screenshot images from the conversation were not included.

The ZIP files are other people's code. To run anything in them, extract each
into its own new folder and run Python with `python3 -I`. The audit scripts in
`../ns-phase-audit/` expect the v2 package extracted next to `audit_v2/`:

```sh
cd ../ns-phase-audit
unzip ../inputs/periodic_ns_lab_v2_audit.zip   # creates periodic_ns_lab_v2/
```
