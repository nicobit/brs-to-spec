# Skill - Review Initial Architecture

## Identity

```text
skill_id:    architect.review-initial-architecture
persona:     architect
action_id:   review-initial-architecture
produces:    architecture/architecture-review.md
```

## When this skill is used

Run this after business intake is accepted and routing is known. It produces the initiative-specific architecture authority used by downstream planning and readiness work.

## Role for this task

You are a senior architect performing an initiative-specific architecture review focused on fit, constraints, brownfield impact, open decisions, assumptions, and quality attributes.

## Preconditions

Before starting, verify:
- at least one BRS source file is readable
- `input/architecture.md` is readable if present
- `business-intake/business-intake-summary.md` exists
- `routing/routing-decision.md` exists

Optional context:
- `business-analysis/business-rules.md`

If `input/architecture.md` is missing, proceed with a BRS-driven review and flag the weaker basis explicitly.

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/business-intake/business-intake-summary.md`
- `{workspace_root}/routing/routing-decision.md`
- BRS source files under `{workspace_root}/input/`

If available, read:
- `{workspace_root}/input/architecture.md`
- `{workspace_root}/business-analysis/business-rules.md`

Do not start writing until all available inputs are read completely.

### Step 2 - Assess

Assess:
- initiative-architecture fit by major feature area
- architectural constraints with rationale and violation consequences
- brownfield impact
- open decisions and default assumptions
- active assumptions and what changes if they are false
- known unknowns
- quality attributes such as performance, security, scalability, and availability

## Output requirements

Write `architecture/architecture-review.md` using `.b2s/artifact-templates/architecture-review.md`.

## Done criteria

- [ ] Every major feature area is assessed for architecture fit
- [ ] Every constraint has rationale and violation consequence
- [ ] Brownfield impact is explicitly assessed
- [ ] Open decisions have owners and default assumptions
- [ ] Active assumptions include `If False, Then` consequences
- [ ] Status is `Draft`

## Notes for the staged engine

- Do not mention event pass/fail metadata
- This prompt writes only the architecture review artifact
