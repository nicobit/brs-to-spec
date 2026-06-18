# Prompt — Generate Delivery Overview

## Role

You are a delivery documentation assistant producing a readable delivery map for an active initiative.

## When to use

Run this prompt **ad hoc** when you want a human-readable view of the full delivery structure — epics, features, user stories, and their current status. It is not part of the delivery workflow — run it manually when needed.

It is useful for:
- Sprint planning preparation
- Stakeholder progress reviews
- Dependency visualisation
- Onboarding developers to the scope

## What to read

Read the following from the active initiative workspace. Skip gracefully if a file does not exist.

- `planning/delivery-structure.md` — epics, features, user stories
- `planning/delivery-increments.md` — increment structure (Enterprise / Modular mode only)
- `planning/traceability-matrix.md` — requirement-to-story traceability (if present)
- `specs/dependency-graph.md` — wave-ordered execution plan (if handoff exists)
- `state/workflow-state.json` — current stage and next action
- `engineering-readiness/readiness-check.md` — readiness decision

## Output

Save the output to `docs/initiatives/<initiative-slug>/delivery-overview.md`.

Tell the user the exact path before writing.

## Template

```markdown
# Delivery Overview — [Initiative Name]

> Generated from initiative workspace. Last updated: [date].
> Source of truth is `planning/delivery-structure.md` — this document is a readable snapshot.

## Summary

| Field | Value |
|---|---|
| Total epics | |
| Total features | |
| Total user stories | |
| Must-have stories | |
| Delivery mode | |
| Readiness | Ready / Not ready / Not assessed |

---

## Delivery structure

### Epic: [E-NNN] [Epic Name]

**Outcome:** [What changes for the business when this epic is done]
**Priority:** Must have / Should have / Nice to have

#### Feature: [F-NNN.N] [Feature Name]

**Capability:** [What the system will be able to do]
**Priority:** Must have / Should have / Nice to have

| Story ID | Story | Acceptance criteria ref | Requirement ref | Status |
|---|---|---|---|---|
| F-NNN.N-NNN | | | REQ-NNN | Pending / In progress / Done |

[Repeat for each feature and epic]

---

## Delivery increments

> Only present if delivery-increments.md exists.

| Increment | Stories included | Dependencies | Target |
|---|---|---|---|
| Inc-1 | | | |

---

## Dependency wave order

> Only present if specs/dependency-graph.md exists.

| Wave | Stories | Parallel? | Blocked by |
|---|---|---|---|
| Wave 1 | | Yes / No | — |

---

## Traceability summary

> Only present if traceability-matrix.md exists.

| Requirement | Stories that deliver it |
|---|---|
| REQ-NNN | F-NNN.N-NNN, F-NNN.N-NNN |
```

## Quality bar

A good delivery overview:
- Reflects the actual delivery-structure.md content — does not invent stories or features
- Marks stories as Pending / In progress / Done based on what exists in the handoff folders
- Shows the dependency wave order only if the handoff has been generated
- Uses business language for epic outcomes and feature capabilities
- Notes clearly if the delivery structure is still draft (stories are stubs)

## After producing the overview

Tell the user:
1. The file has been saved to `docs/initiatives/<slug>/delivery-overview.md`
2. Re-run after each major stage (delivery structure confirmed, handoff generated) to keep it current
3. This file is documentation only — editing it does not affect `planning/delivery-structure.md`
4. If this is a new initiative, add its nav block to `mkdocs.yml` under `Initiative Samples:` — see `generate-initiative-summary.md` for the exact block to add.
