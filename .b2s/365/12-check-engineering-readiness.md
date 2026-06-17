# Prompt 12 - Check Engineering Readiness

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/business-intake/business-intake-summary.md`
- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `initiatives/<id>-<slug>/architecture/architecture-rules.md`
- `initiatives/<id>-<slug>/planning/delivery-structure.md`
- `initiatives/<id>-<slug>/routing/routing-decision.md`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder
- `.b2s/artifact-templates/readiness-check.md`

Optional but important:

- `initiatives/<id>-<slug>/architecture/existing-system-impact.md`
- `initiatives/<id>-<slug>/planning/delivery-increments.md`
- `initiatives/<id>-<slug>/planning/traceability-matrix.md`
- `initiatives/<id>-<slug>/business-analysis/gaps-and-questions.md`

## Output file to create

- `initiatives/<id>-<slug>/engineering-readiness/readiness-check.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `check-engineering-readiness`.

Read the full upstream artifact set before writing any conclusion. Do not invent
readiness evidence when required inputs are missing.

Evaluate the core checklist and explicitly apply gate trigger rules.

Trigger `BDD Scenarios` if any of these apply:

- role-based authorization
- multi-step workflows or state transitions
- async execution paths
- dry-run, preview, or confirmation flows before destructive actions
- exception, retry, or recovery paths
- complex validation rules from business rules

Trigger `Test Strategy` if any of these apply:

- multiple test levels are needed
- regression risk exists in an existing system
- audit or compliance validation is required

Trigger `Security Review` if any of these apply:

- authentication or authorization is involved
- sensitive or PII data is handled
- external API exposure or a new service boundary is introduced
- an audit trail is required

Trigger these when applicable:

- `API Contract` for new or changed API endpoints
- `Data Contract` for schema, migration, ownership boundary, or PII handling changes
- `Event Contract` for event schema or async behavior changes
- `Observability Plan` for operational flows, SLI/SLO needs, or alerting concerns

Every `No` decision must include explicit written justification.

Calculate readiness score:

- score = round(pass / total * 100)
- `90-100` -> `Ready`
- `70-89` -> `Ready with risks`
- below `70` -> `Not ready`

A single blocking issue overrides a high numeric score.

Before finalizing, answer:

1. What is the strongest argument that this readiness decision is wrong?
2. Which assumption, if false, would change `Ready` to `Not ready`?
3. What would a skeptical architect object to first?

Write `engineering-readiness/readiness-check.md` using the provided template.

The artifact must include:

- Core Checklist
- Gate Trigger Decisions
- Readiness Decision
- Blocking Issues
- Accepted Risks
- Required Quality Gates

Status must be `Draft`. Do not self-accept.
