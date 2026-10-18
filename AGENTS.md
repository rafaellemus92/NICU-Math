# Shared project guidance: Codex and Claude Code

## Scope and evidence
- Keep the Python stack: FastAPI API (`main.py`), Streamlit UI (`app.py`), NumPy toy scenarios (`bayes.py`). No UI rewrite or new infrastructure without a scoped request.
- Initial clinical scope is **synthetic research and education** for respiratory mechanics and neonatal hemodynamics. Existing NEC/acidosis/extubation models are unvalidated demonstrations, not calibrated physiology or patient-specific treatment tools. Do not add patient-data uploads.
- Never commit patient data, secrets, or licensed PDF full texts. Do not inspect or print credential values. Use synthetic fixtures; `.env`, PDFs and `library/` are ignored, but review the staged diff too.
- Label claims as hypothesis, mathematical proof, exact calculation, numerical evidence, or unvalidated physiological model. State assumptions, definitions, units, domain and limitations. Numerical agreement is not proof; code checks are not clinical validation.
- Clinical observations may motivate phase-sensitive hypotheses. Clinical finite-time transitions are **not PDE singularities**. Inspirations are motivations, not established mathematical links. Do not claim to solve Navier–Stokes regularity.
- Preserve the separate `pangram/` research, results and existing patches. Do not infer clinical links from its terminology or numerical coincidences.

## Workflow
- Inspect Git status, instructions and relevant `.agents/skills` before editing. Preserve existing user work; use an isolated development branch.
- One implementation owner per task. Record owner, base commit, scope and validation in `docs/HANDOFF.md`. A second AI reviews the exact commit/diff and test outcomes independently before a human decides integration.
- No automatic merge or deployment. Do not push, change visibility, grant access, use paid APIs/services or contact another AI without explicit user authorization. Local commits are permitted for reviewable handoffs.
- Default to offline mode (`NICU_OFFLINE=1`, also the default when unset). Do not load environment secrets to run tests. External evidence services are legacy, opt-in, and require a separate reviewed task.
- Keep dependencies minimal. No long pangram enumeration or paid runs for routine smoke checks.

## Verification and handoff
Run from repository root:
```
python -m venv .venv
.venv/bin/python -m pip install -r requirements-test.txt
NICU_OFFLINE=1 .venv/bin/python -m unittest discover -s tests -v
NICU_OFFLINE=1 .venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000
# Separate terminal: .venv/bin/python -m streamlit run app.py
# Optional local containers: docker compose config --quiet; docker compose up --build
```
Package installation needs network on first setup; application smoke tests must not.
Record passed, failed and not-run checks separately, with exact commands and limitations. A seeded toy simulation demonstrates reproducibility only. Update the research index when adding a claim or experiment. Hand off a concrete branch/commit and review prompt; publishing a local branch is a separate user decision.
