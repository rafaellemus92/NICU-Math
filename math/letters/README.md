# letters: a draft email and its companion notes

This folder holds correspondence, not an audit. It has a draft email to Steven Strogatz and a
plain-language essay that goes with it. Both were written with AI help in October 2026.

| File | What it is |
|---|---|
| [`strogatz-email.md`](strogatz-email.md) | The draft email, a "Before you send" checklist, and a source for every claim in it. **Not sent.** Words in square brackets, such as [role], [hospital] and [link], are placeholders; the checklist says what goes in each. [link] is the live Shared Air page, https://nicu-math.vercel.app/shared-air. |
| [`words.md`](words.md) | "The words that drew me in": shared vocabulary across the bedside, the mathematics and old texts (labelled as analogy), a table of physics ideas with a status for each, and short essays. For a later reply. |
| [`check_numbers.py`](check_numbers.py) | Recomputes the derived numbers quoted in `words.md`. Standard library only. |
| [`check_numbers.txt`](check_numbers.txt) | Its stored output. |
| [`ncbi_gene_counts.txt`](ncbi_gene_counts.txt) | Protein-coding genes per chromosome from NCBI Gene, queried 18 October 2026. `check_numbers.py` reads it. |

## How this folder relates to the rest of `math/`

- **Physics and biology.** The table in part 2 of `words.md` covers the same ideas as the audited
  fact-check, [`../reports/physics-biology-factcheck.md`](../reports/physics-biology-factcheck.md).
  The fact-check quotes each idea word for word and has the full evidence and the scripts; the table
  here defers to it and links each row to its section. Status words map as follows: True = "true /
  partly true", Analogy = "metaphor that maps onto real structure", Doesn't hold = "false as
  stated", Unsupported = "unsupported". "Open" has no single counterpart there.
- **Shared Air.** The email's model claims come from the Shared Air audit,
  [`../shared-air/AUDIT.md`](../shared-air/AUDIT.md). The page itself is published at
  https://nicu-math.vercel.app/shared-air from
  [`../../web/public/shared-air/index.html`](../../web/public/shared-air/index.html).
- **Lean.** Several claims point to theorems in [`../wyrd-mathlib/`](../wyrd-mathlib/):
  `same_synchrony_different_future` and `same_synchrony_different_future_24` (synchrony R alone
  does not fix its own future) and the `Bistability.lean` theorems (the second, co-arousal state).
  The repository guide, [`../README.md`](../README.md), lists them as proved in Lean. They were not
  rebuilt for this folder.
- **Navier-Stokes.** The September 2026 blow-up claim and Clay's response are summarised in
  `words.md`. The full source list is in section 8 of
  [`../ns-phase-audit/enstrophy-jet/RESULTS.md`](../ns-phase-audit/enstrophy-jet/RESULTS.md).
- **Fuller recomputations.** `check_numbers.py` is a short check. The archived scripts behind the
  fact-check are in [`../reports/physics-biology/`](../reports/physics-biology/): `glucose_weak.py`,
  `gravity_time.py` and `compute_bio.py`.

## Re-running the numbers

From this folder:

```
python3 check_numbers.py           # prints the numbers; last line: "matches stored check_numbers.txt"
python3 check_numbers.py --write   # rewrites check_numbers.txt
```

## Still open

- The email has not been sent. The On Point episode it thanks him for is likely but not confirmed
  (see the checklist).
- NCBI and Ensembl give different gene counts per chromosome, and both change between releases.
  The ranking used in `words.md` is the same under both.
- The essays in parts 4 and 5 of `words.md` are metaphors built on real physics. The bridges from
  the physics to a life are not physics claims.
