# Prompt — Find Gaps and Questions

## Purpose

Create or update `business-analysis/gaps-and-questions.md`.

This prompt is adapted from `.brs2spec2/skills/product-owner/find-gaps-and-questions.md`, extended so it can absorb findings not only from raw requirements but also from entity, use-case, rule, and architecture analysis.

## Instructions

Create or update `business-analysis/gaps-and-questions.md`.

Identify every ambiguity, missing specification, conflicting requirement, unresolved dependency, and unanswered question that could block architecture, planning, readiness, or handoff.

## DO NOT

- Invent gaps just to populate the document
- Collapse multiple issues into one generic item
- Hide blocking issues inside vague notes

## Inputs

Required:

- `business-intake/business-intake-summary.md`
- `business-analysis/requirements.md`

Optional:

- `business-analysis/entity-model.md`
- `business-analysis/use-cases/UC-*.md`
- `business-analysis/business-rules.md`
- architecture findings already written into architecture artifacts

## Gap categories

Review for at least:

- Ambiguity gaps
- Missing specification gaps
- Conflict gaps
- Scope boundary gaps
- Acceptance-criteria gaps
- Integration or external-system gaps
- Data ownership or lifecycle gaps

## Workflow

1. Review the requirements catalog.
2. Cross-check with entity model, use cases, business rules, and architecture findings when available.
3. Record one `GAP-NNN` per issue.
4. Assign severity and ownership.
5. Identify which gaps block architecture, which block planning, and which can proceed with assumptions.

## Required structure

Suggested catalog:

| ID | Category | Description | Impact | Severity | Suggested Resolution | Owner | Source |
|---|---|---|---|---|---|---|---|
| GAP-001 |  |  |  | Blocking / High / Low |  |  |  |

Also include:

- Blocking gaps
- High-severity gaps
- Low-severity gaps
- Assumptions that permit progress

## Output expectations

This artifact should later support:

- open decisions
- architecture review
- planning confidence
- readiness blocking logic
- handoff risk notes

## Error handling

- If no meaningful gaps are found, produce the artifact with an explicit note that the analysis was performed and no material gaps were identified.
- If a gap arises from conflicting source artifacts, preserve the conflict rather than resolving it silently.
