# Hou–Luo blowup lab

A one-dimensional model of swirling flow at the wall of a pipe, with a
viscosity knob, for watching concentration fight diffusion.

## Run it
```bash
pip install numpy matplotlib
python hou_luo.py            # ~2 minutes: inviscid run + viscosity sweep + figure
python hou_luo.py --check    # adds a grid-convergence check (slower)
python hou_luo.py --help     # all options
```
Outputs: `hou_luo_results.png` (figure) and `hou_luo_results.json` (numbers).

## Open it in Claude Code
On a computer, either open this folder from the **Code** tab of the Claude
desktop app, or in a terminal:
```bash
cd hou-luo
claude
```
Claude Code reads `CLAUDE.md` automatically. That file holds the project
brief, ground rules, baseline results, and roadmap.

### Starter prompt (paste this in)
> Read CLAUDE.md. First run `python hou_luo.py --check` and confirm you
> reproduce the baseline results. Then start Step 1: get the inviscid run past
> max|ω| = 1,000 with a converged result. Make a plan before writing code,
> check it against the ground rules, and show me the reciprocal plot when
> you're done.

Next prompts, one at a time:
- "Do Step 2 of CLAUDE.md. Explain dynamic rescaling to me before you code it."
- "Do Step 3. Tell me plainly whether the data support the hypothesis."
- "Use subagents: one implements, one independently checks convergence and
  citations, and neither one sees the other's conclusions first."
