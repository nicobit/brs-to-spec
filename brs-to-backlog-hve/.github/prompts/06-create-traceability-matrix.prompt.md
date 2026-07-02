# 06 — Create Traceability Matrix

You are a requirements traceability analyst.

## Input

Read:

- `/input/brs.md`
- `/output/01-extracted-capabilities.md`
- `/output/02-candidate-epics.md`
- `/output/03-candidate-stories.md`
- `/output/04-backlog-review.md`
- `.github/skills/traceability-matrix/SKILL.md`
- `.github/instructions/brs-traceability.instructions.md`

## Goal

Create a traceability matrix that links BRS requirements to capabilities, epics, stories, and acceptance criteria.

## Output

Create:

```text
/output/06-traceability-matrix.md
```

Use this structure:

# Traceability Matrix

## 1. Matrix Summary

| BRS Reference | BRS Requirement / Need | Capability ID | Epic ID | Story ID | Acceptance Criteria | Status | Gap |
|---|---|---|---|---|---|---|---|

Status values:

- Covered
- Partially covered
- Not covered
- Needs clarification

## 2. Uncovered BRS Items

List BRS requirements not covered by capabilities, epics, or stories.

## 3. Partially Covered Items

List requirements that need additional stories or acceptance criteria.

## 4. Assumptions and Low-Confidence Mappings

List any weak mappings.

## 5. Recommended Fixes

Suggest backlog changes to close traceability gaps.
