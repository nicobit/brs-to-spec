# Skill — Create Compact Handoff

## Identity

| Field | Value |
|---|---|
| skill_id | eng-create-compact-handoff |
| persona | engineering-lead |
| event_types | CREATE_COMPACT_HANDOFF |
| produces | handoff/compact-handoff-summary.md |

## When this skill is used

Optional summary helper. Run after the real handoff package already exists (`specs/` or `standalone-delivery/`). Creates a compact summary for engineering review, stakeholder briefings, or downstream coordination.

Does NOT replace the real handoff artifacts.

## Role for this task

You are an engineering lead creating a lightweight summary of an already-prepared handoff package — for stakeholders who need a one-page overview without reading the full specs.

## Prerequisites check

Before starting, verify:
- [ ] The real handoff exists: `specs/` with story folders OR `standalone-delivery/D1-*/` with all 5 files
- [ ] `engineering-readiness/readiness-check.md` exists

If the real handoff does not exist: stop — create the real handoff first.

## Instructions

### Read inputs

```
engineering-readiness/readiness-check.md
engineering-readiness/initiative-context.md
quality-gates/*.md (accepted gates only)
specs/<active-deliverable>/* or standalone-delivery/<active-deliverable>/*
routing/routing-decision.md
```

### Write compact summary

Include:
- Initiative ID, deliverable name, delivery mode, execution mode
- Architecture constraints: AR-NNN rules that constrain implementation (verbatim)
- Triggered quality gates and their status
- Story count and summary (N Must, N Should, N Could)
- Key risks and accepted risks from readiness check
- Where to find implementation artifacts (spec paths)

Rules:
- Do not create a second source of truth
- Do not invent missing tasks, requirements, or decisions
- Treat as a summary-only projection of approved source artifacts

## Output requirements

Single file: `handoff/compact-handoff-summary.md`

Must contain:
- Metadata section (initiative, mode, date)
- Architecture constraints summary (AR-NNN verbatim)
- Quality gates table (gate name, status, file path)
- Story summary table (story count by priority and increment)
- Risk summary
- Artifact index (paths to implementation files)

## Done criteria

- [ ] File exists at `handoff/compact-handoff-summary.md`
- [ ] Real handoff artifacts are referenced (not duplicated)
- [ ] No content invented beyond what source artifacts provide
- [ ] Result file written with `status: pass` and `artifacts_written` listing `handoff/compact-handoff-summary.md`

## Stop conditions

- If real handoff does not exist: stop and run the real handoff skill first.
- Do not create implementation guidance that conflicts with or duplicates the real handoff.
