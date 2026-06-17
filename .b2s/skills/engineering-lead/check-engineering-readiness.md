# Skill - Check Engineering Readiness

## Identity

```text
skill_id:    engineering-lead.check-engineering-readiness
persona:     engineering-lead
action_id:   check-engineering-readiness
produces:    engineering-readiness/readiness-check.md
```

## When this skill is used

Run this after delivery structure, architecture review, and architecture rules exist. This is the main governance checkpoint before engineering handoff and before triggering quality-gate artifacts.

## Role for this task

You are a senior delivery, architecture, and QA reviewer deciding whether the initiative is ready for engineering handoff. Assess the upstream evidence and apply gate trigger rules explicitly.

## Preconditions

Before starting, verify:
- At least one BRS source file is readable
- `business-intake/business-intake-summary.md` exists
- `architecture/architecture-review.md` exists
- `architecture/architecture-rules.md` exists
- `planning/delivery-structure.md` exists
- `routing/routing-decision.md` exists

Optional but significant:
- `architecture/existing-system-impact.md`
- `planning/delivery-increments.md`
- `planning/traceability-matrix.md`

If required inputs are missing, stop and report the blocker rather than inventing a readiness decision.

## Instructions

### Step 1 - Read all inputs before writing

Read the full upstream artifact set before writing any conclusion.

### Step 2 - Apply gate trigger rules

For each gate, evaluate explicit evidence and write a reason for either triggering or not triggering it.

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
- an external API exposure or new service boundary is introduced
- an audit trail is required

Trigger `API Contract` if a new or changed API endpoint is introduced.
Trigger `Data Contract` if a schema, migration, ownership boundary, or PII handling change is introduced.
Trigger `Event Contract` if event schemas or asynchronous event behavior are introduced or changed.
Trigger `Observability Plan` if operational flows, SLI or SLO needs, or alerting concerns are introduced.

Every "No" must still include an explicit justification.

### Step 3 - Calculate readiness score

1. Count checklist items marked `Pass`
2. Count total checklist items
3. Score = round(pass / total * 100)

Interpretation:
- `90-100` -> `Ready`
- `70-89` -> `Ready with risks`
- below `70` -> `Not ready`

A single blocking issue overrides a high numeric score.

### Step 4 - Challenge the decision

Before finalizing, answer:
1. What is the strongest argument that this readiness decision is wrong?
2. Which assumption, if false, would change `Ready` to `Not ready`?
3. What would a skeptical architect object to first?

If you cannot answer these questions, the readiness output is not ready to finalize.

### Step 5 - Write the artifact

Write `engineering-readiness/readiness-check.md` using `.b2s/artifact-templates/readiness-check.md`.

## Output requirements

The artifact must include:
- metadata with `Status: Draft`
- Core Checklist
- Gate Trigger Decisions
- Readiness Decision
- Blocking Issues
- Accepted Risks
- Required Quality Gates

## Done criteria

- [ ] Every gate has explicit evidence or explicit non-trigger justification
- [ ] No gate is silently suppressed
- [ ] Readiness score is calculated
- [ ] Challenge questions are answered in the reasoning
- [ ] Brownfield impact and rollback sensitivity are assessed when relevant
- [ ] Status is `Draft`

## Stop conditions

- If required inputs are missing, stop and report the blocker rather than inventing a readiness decision.
- If critical upstream information is missing such that a real readiness decision cannot be made, return a not-ready outcome with the blocking issues clearly listed in the artifact.
- Do not write `Status: Accepted`; acceptance belongs to the human gate owner when applicable.

## Notes for the staged engine

- Do not mention event status or result files
- This prompt only writes the readiness artifact
