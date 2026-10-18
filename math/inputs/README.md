# inputs: the user's uploaded source materials

The files the user uploaded during the work, kept as uploaded. They are inputs
to the proofs and audits in the rest of [`math/`](../README.md), not results.

| File | What it is |
|---|---|
| [`Shared_Air_Model_v1.md`](Shared_Air_Model_v1.md) | The *Shared Air* model page as first uploaded: a cells-to-pair model of mother–infant attunement with three worlds (Perceived, Physical, Alike), bedside tests, equations and limits. Text only; the interactive simulator is not included. |
| [`Shared_Air_Model_v2_revised.md`](Shared_Air_Model_v2_revised.md) | The same page revised on 16 October after ChatGPT's audit: Test 4's inverted U does not need the delay, the other-parent contrast needs a matched control, the locking condition holds to first order, and "ratios other than n:1" is added to the limits. |
| [`shared_air_proof_audit.zip`](shared_air_proof_audit.zip) | ChatGPT's independent proof audit of the Shared Air equations: `proof_notes.md`, a standard-library checker `verify_shared_air.py` and its output `audit_results.json`. The Lean audit of the same equations is in [`../wyrd-mathlib/WyrdMathlib/SharedAir/`](../wyrd-mathlib/WyrdMathlib/SharedAir/). |
| [`periodic_ns_phase_audit.zip`](periodic_ns_phase_audit.zip) | ChatGPT's periodic Navier–Stokes proof exercise: `proof_notes.md`, an exact rational Fourier checker `verify_periodic_ns.py` and `results.txt`, showing that the fields ±u have the same spectrum but opposite initial enstrophy change (1/8 and −3/8 at ν = 1/28). Its quantities at t = 0 are proved in Lean in [`../wyrd-mathlib/WyrdMathlib/PeriodicNS/`](../wyrd-mathlib/WyrdMathlib/PeriodicNS/) (`Example.lean`, `Averages.lean`, `SignFlip.lean`); the enstrophy balance itself is not formalised. |
| [`periodic_ns_lab_v1.zip`](periodic_ns_lab_v1.zip) | ChatGPT's periodic Navier–Stokes phase lab v1, built from the exercise above: solver, 24 simulations, 19 tests and exact phase-family identities. Those identities are re-derived by [`../numerics/navier-stokes/nslab_v1_exact_identities.py`](../numerics/navier-stokes/nslab_v1_exact_identities.py). |
| [`periodic_ns_lab_v2_audit.zip`](periodic_ns_lab_v2_audit.zip) | ChatGPT's lab v2 package as uploaded for audit (folder `periodic_ns_lab_v2/`, with `CLAUDE_HANDOFF.md`, `RESULTS.md`, `proof_notes.md` and `MANIFEST_SHA256.txt`). It is the object audited in [`../ns-phase-audit/`](../ns-phase-audit/). |
| [`coupled_prime26_pangram_original.py`](coupled_prime26_pangram_original.py) | The original prime-pangram script. It is byte-for-byte identical to [`../coupled_prime26_pangram.py`](../coupled_prime26_pangram.py). |

Four screenshot images from the conversation were not included.

The ZIP files are other people's code. To run anything in them, extract each
into its own new folder and run Python with `python3 -I`. The audit scripts in
`../ns-phase-audit/` expect the v2 package extracted next to `audit_v2/`:

```sh
cd ../ns-phase-audit
unzip ../inputs/periodic_ns_lab_v2_audit.zip   # creates periodic_ns_lab_v2/
```
