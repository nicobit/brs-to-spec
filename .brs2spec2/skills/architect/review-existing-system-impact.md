# Skill — Review Existing System Impact

## Identity

| Field | Value |
|---|---|
| skill_id | arch-review-existing-system-impact |
| persona | architect |
| event_types | REVIEW_EXISTING_SYSTEM_IMPACT |
| produces | architecture/existing-system-impact.md |

## When this skill is used

Only when the initiative changes an existing system (brownfield). Triggered by the architecture review when it identifies material brownfield impact. Runs after `REVIEW_INITIAL_ARCHITECTURE` and before `CHECK_ENGINEERING_READINESS`.

Skip if the initiative is purely greenfield with no changes to existing components.

## Role for this task

You are a senior architect performing a targeted brownfield impact assessment: identifying every existing component, contract, consumer, and data asset affected by the initiative — and the risk and mitigation approach for each.

## Prerequisites check

Before starting, verify:
- [ ] `input/brs.md` (or `input/brs/*.md`) is readable
- [ ] `input/architecture.md` (or `input/architecture/*.md`) is readable
- [ ] `architecture/architecture-review.md` exists and identifies brownfield impact
- [ ] `business-intake/business-intake-summary.md` exists

If the architecture review explicitly states "greenfield — no brownfield impact": stop and write a one-line artifact confirming this. Do not run this full assessment.

## Instructions

### Step 1 — Identify all affected components

For each change described in the BRS:
- Which existing service, module, or component is modified?
- What existing data tables, schemas, or migrations are affected?
- What existing API endpoints are changed (signature, behaviour, or removal)?
- What existing events or message contracts change?

### Step 2 — Map consumers and dependencies

For each affected component:
- Who are the current consumers? (List systems, services, and clients known from architecture.md)
- What contracts do they depend on?
- What changes in behaviour will they experience?
- What notification or migration window is required?

### Step 3 — Assess compatibility and rollback

For each change:
- **Backward compatibility**: is the change compatible with existing consumers, or does it break them?
- **Migration approach**: what migration strategy is required? (additive, versioned, breaking-with-migration-window)
- **Feature flag**: can this change be gated? What is the rollout strategy?
- **Rollback sensitivity**: can this change be reversed if it fails in production? What is the rollback procedure?

### Step 4 — Assess regression surface

- Which existing test suites cover the changed components?
- What regression risk exists? (Low / Medium / High with justification)
- What additional regression testing is recommended?

### Step 5 — Write the artifact

Use the artifact template at `.brs2spec2/artifact-templates/existing-system-impact.md` if it exists; otherwise produce the structured output described below. Set `Status: Draft`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- Affected components table: Component, Type (service/schema/API/event), Change, Consumers, Backward Compatible?
- Migration and rollback assessment per major change
- Regression surface assessment
- Recommended guards: feature flags, parallel run, migration window requirements

## Done criteria

- [ ] All affected components from the BRS have been identified
- [ ] Consumer mapping is complete for each affected component
- [ ] Backward compatibility is explicitly assessed (not skipped)
- [ ] Rollback sensitivity is stated with a rollback approach or "cannot rollback" with justification
- [ ] Regression surface is assessed with a risk level
- [ ] No invented impacts — every assessment traces to BRS or architecture inputs
- [ ] `Status: Draft` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `architecture/existing-system-impact.md`

## Stop conditions

- If the initiative is confirmed greenfield: do not run this skill. Write a one-line confirmation artifact.
- If `input/architecture.md` is missing: proceed with BRS-only assessment and flag the gap.
- Do not invent consumers or dependencies not present in the architecture inputs.
