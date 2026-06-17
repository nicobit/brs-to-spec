# Prompt 13 - Engineering Readiness Review Gate

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/engineering-readiness/readiness-check.md`
- `initiatives/<id>-<slug>/planning/delivery-structure.md`
- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `initiatives/<id>-<slug>/architecture/architecture-rules.md`

Optional:

- `initiatives/<id>-<slug>/planning/traceability-matrix.md`
- `initiatives/<id>-<slug>/architecture/existing-system-impact.md`

## Output file to create

- no framework artifact is created in this step

## Prompt for Office 365 Copilot

You are supporting the `.b2s` engineering readiness review gate.

Review the existing `readiness-check.md`. Do not rewrite the readiness artifact
unless a concrete issue is found.

Produce a review note with:

- Overall gate recommendation: `Approve` or `Needs changes`
- Gaps in core checklist evidence
- Incorrect or missing gate triggers
- Missing justification for any `No` gate decision
- Weak or missing blocking issues
- Risks accepted too casually
- Confidence level

Approve only if the readiness artifact is specific enough to govern downstream
quality-gate and handoff work. If changes are needed, list the minimum concrete
fixes before progression.
