# NICU Torus — Neonatal Knowledge Architecture

An Obsidian vault designed for neonatal-perinatal board preparation and NICU clinical reasoning. Topics are decomposed into recurring concept layers rather than isolated facts, forming a "torus" of interconnected knowledge.

## Quick Start

1. Open the `NICU_Torus/` folder as an Obsidian vault
2. Start at `00_Hubs/NICU Torus Hub.md`
3. Open `Canvas/NICU Torus Map.canvas` for the visual map
4. Browse domains via `01_Domains/` or topics via `02_Topics/`

## Architecture

### Folder Structure

```
NICU_Torus/
  00_Hubs/          → Master hub linking all domains
  01_Domains/       → 14 domain hub notes (organ-system level)
  02_Topics/        → Topic notes organized by domain subfolder
  03_Cases/         → Case-based learning (future)
  04_Pathways/      → Clinical decision pathways (future)
  05_Pearls/        → Standalone board pearls (future)
  06_Templates/     → Reusable note templates
  Attachments/      → Images, diagrams
  Canvas/           → Obsidian Canvas visual maps
```

### Domains (14)

| Domain | Status |
|--------|--------|
| Respiratory | Seeded (12 topics) |
| Cardiovascular | Seeded (10 topics) |
| Maternal-Fetal | Scaffold |
| Asphyxia-Resuscitation | Scaffold |
| Genetics-Dysmorphism | Scaffold |
| Nutrition-GI | Scaffold |
| Water-Salt-Renal | Scaffold |
| Endocrine-Metabolic-Thermal | Scaffold |
| Immunology-Infectious Disease | Scaffold |
| Hematology-Bilirubin | Scaffold |
| Neurology-Neurodevelopment | Scaffold |
| ENT-Eyes-Skin | Scaffold |
| Pharmacology | Scaffold |
| Ethics-Quality-Research | Scaffold |

### Conceptual Schema

Every topic note is decomposed into **13 concept families** plus an edge pearl:

1. **Identity** — What is it?
2. **Taxonomy / Developmental Placement** — Where does it fit?
3. **Structure** — Anatomy, histology, cell types
4. **Function** — Normal physiology, biochemistry
5. **Dysfunction / Pathophysiology** — What goes wrong?
6. **Clinical Phenotype** — Signs, symptoms, patterns
7. **Differential / Distinctions** — What it is vs. what it is not
8. **Diagnosis** — Labs, imaging, monitoring, pitfalls
9. **Management** — Stabilization → definitive → escalation
10. **Therapeutics** — Drugs, devices, mechanisms
11. **Complications / Outcomes** — Acute, chronic, prognosis
12. **Associations** — Genetics, syndromes, maternal-fetal links
13. **Context / Board Framing** — GA relevance, ethics, QI
14. **Edge Pearl** — High-yield board distinction

### Oyster Rings

Each topic also maps to a reasoning depth layer:

| Ring | Name | Purpose |
|------|------|---------|
| 1 | Identity | What is it? Core definition |
| 2 | Taxonomy | Where does it fit? Classification |
| 3 | Associations | What connects to it? |
| 4 | Distinctions | What is it NOT? Differentials |
| 5 | Edge | The rare pearl, the exception |

### Neonatal Meta-Axes

Topics can be filtered/tagged along these cross-cutting axes:

- Gestational age (preterm / term / post-term)
- Phase (fetal / transitional / postnatal)
- Structure vs function
- Acute stabilization vs chronic management
- Common vs rare
- Core fact vs edge pearl
- Maternal / placental / fetal / neonatal origin
- Bedside pattern vs mechanistic explanation

## YAML Frontmatter

Every note includes structured metadata:

```yaml
---
title: Topic Name
domain: Respiratory
topic_type: Core Topic
ring_focus: Identity        # Which Oyster Ring is primary
gestational_axis: preterm   # preterm, term, fetal, etc.
phase_axis:                 # fetal, transitional, postnatal
  - transitional
  - postnatal
tags:
  - nicu
  - boards
  - respiratory
related_notes:
  - Other Topic
  - Another Topic
---
```

## Canvas

The `Canvas/NICU Torus Map.canvas` file provides a radial visual map:

- **Center**: NICU Torus hub
- **Orbit 1**: 14 domain nodes
- **Orbit 2**: Individual topic nodes clustered by domain
- **Orbit 3**: Concept-layer spokes for selected topics

Cross-domain links (e.g., between Respiratory and Cardiovascular transitional physiology) are shown as connecting edges.

### Regenerating the Canvas

```bash
cd NICU_Torus
python generate_canvas.py
```

The script reads YAML frontmatter from all topic notes and generates a fresh canvas with radial layout.

## Templates

- `06_Templates/Topic Template.md` — Standard 14-section topic note
- `06_Templates/Domain Hub Template.md` — Domain overview with concept map table

To use in Obsidian: Settings → Core Plugins → Templates → set template folder to `06_Templates`.

## Design Principles

- **Markdown is the source of truth** — no databases, no proprietary formats
- **Human-readable and hand-editable** — works without plugins
- **Wiki-links everywhere** — `[[Note Name]]` for Obsidian graph navigation
- **Scalable** — add new domains/topics by copying templates
- **Board-oriented** — every note ends with an edge pearl

## Adding a New Topic

1. Copy `06_Templates/Topic Template.md` to `02_Topics/{Domain}/New Topic.md`
2. Fill in the YAML frontmatter
3. Work through each of the 14 sections
4. Add `[[wiki-links]]` to related notes
5. Update the domain hub note in `01_Domains/`
6. Run `python generate_canvas.py` to update the visual map

## License

Personal educational use. Medical content is for board preparation reference only and should not replace clinical judgment.
