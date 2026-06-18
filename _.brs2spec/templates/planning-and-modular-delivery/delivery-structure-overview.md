# Delivery Structure — Overview

> Initiative: {{initiative ID}} — {{initiative name}}
> Delivery mode: {{delivery mode}}
> Execution mode: {{execution mode}}
> This file is the entry point for the delivery structure. Each epic has its own subfolder.

## Business capabilities

List capabilities only at the level needed to shape epics, features, and slices.

| Capability | Epics | Source requirements |
|---|---|---|
| {{capability}} | {{E-NNN}} | {{FR-NNN}} |

## Epic index

| Epic ID | Epic title | Folder | Source FRs |
|---|---|---|---|
| E-NNN | {{title}} | `E-NNN-<slug>/` | FR-NNN..FR-NNN |

## Governed boundaries

List only real service, data, or event boundaries that affect contracts or control points.

| Boundary ID | Boundary type | Producer / Owner | Consumer(s) | Created / Changed? | Why governed? | Likely contract gate |
|---|---|---|---|---|---|---|

## Candidate delivery slices

Keep this section summary-level until active deliverables are selected.

| Slice | Included features | Rationale | Dependencies |
|---|---|---|---|
| Slice 1 | F-NNN.N, F-NNN.N | {{rationale}} | {{dependencies}} |

## Story traceability rules

- Every story references its source `FR-NNN` in the feature file.
- Confirmed stories use `ACT-NNN` IDs from `business-analysis/actors-and-personas.md` — no free-text role names.
- Confirmed stories reference `BR-NNN` rules from `business-intake/business-rules.md` or include an explicit "Business rules: none apply — [reason]" note.
- Acceptance criteria reference `AC-NNN` rows in `input/brs.md` — text is copied verbatim, not paraphrased.
