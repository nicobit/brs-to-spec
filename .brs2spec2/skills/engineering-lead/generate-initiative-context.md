# Skill — Generate Initiative Context

## Identity

| Field | Value |
|---|---|
| skill_id | eng-generate-initiative-context |
| persona | engineering-lead |
| event_types | GENERATE_INITIATIVE_CONTEXT |
| produces | engineering-readiness/initiative-context.md |

## When this skill is used

Once per deliverable, after the readiness check is approved. The output — `initiative-context.md` — is the single file all downstream agents (implementation, review, handoff) load first to understand the binding constraints.

## Role for this task

You are a senior delivery architect distilling the approved readiness decision into a compact, propagatable context file that prevents cross-session and cross-agent drift.

## Prerequisites check

Before starting, verify:
- [ ] `engineering-readiness/readiness-check.md` exists and has been approved (Status: Accepted or explicit human approval noted)
- [ ] `architecture/architecture-rules.md` exists
- [ ] `architecture/architecture-review.md` exists

If `readiness-check.md` is missing or not approved: stop.

## Instructions

### Step 1 — Read inputs in priority order

```
engineering-readiness/readiness-check.md          (primary source)
architecture/architecture-rules.md
architecture/architecture-review.md
routing/routing-decision.md
input/architecture.md or input/architecture/*.md
input/repositories/*.md                           (if exists — authoritative for technology constraints)
business-intake/business-intake-summary.md
```

When `input/repositories/*.md` files exist: use them as the authoritative source for the Technology Constraints table. If not present: derive from `input/architecture.md` prose and note "repository descriptor not yet created" in Source column.

### Step 2 — Extract only binding constraints

Do NOT copy full artifact content. Extract only:
- Technology constraints that constrain implementation choices
- Architecture rules verbatim (AR-NNN rule text — do not paraphrase)
- Governed boundaries (what crosses a service/data boundary)
- Active quality gates (triggered and required)
- Rollback and regression sensitivity with reason
- Open risks that implementation agents must not treat as resolved

### Step 3 — Populate Carried-Forward Context

This section must be populated from evidence — never left silently empty:
- **Active assumptions**: from architecture-review.md Active assumptions section, or phrases like "we assume", "assuming", "subject to"
- **Known unknowns**: from architecture-review.md Known unknowns, or phrases like "TBD", "not yet determined", "depends on"
- **Non-obvious constraint rationale**: for each AR-NNN rule where the reason is not self-evident from the rule text

If none of the three can be populated: write `> None identified` in each sub-section.

### Step 4 — Populate model identifier

Set the `AI model version` field in the Metadata table with the current model identifier (e.g. `claude-sonnet-4-6`). Do not leave it blank.

### Step 5 — Write the artifact

Use the artifact template at `.brs2spec2/artifact-templates/initiative-context.md`. Keep it compact — a coding agent should be able to load it without being overwhelmed.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, AI model version, creation date
- Technology Constraints table (from repository descriptors or architecture)
- Architecture Rules in Force: AR-NNN rules verbatim
- Governed Boundaries: services, APIs, data stores with owner
- Active Quality Gates: triggered and required gates
- Rollback and Regression Sensitivity
- Open Risks (accepted risks from readiness check)
- Carried-Forward Context (populated or marked `None identified`)

## Done criteria

- [ ] All AR-NNN rules are copied verbatim (not paraphrased)
- [ ] Technology constraints reflect actual stack (not generic defaults)
- [ ] Every governed boundary in the readiness check appears in the context
- [ ] Every triggered and required gate listed
- [ ] Carried-Forward Context populated or explicitly marked `None identified`
- [ ] File is compact enough for a coding agent to load as context without overwhelming it
- [ ] AI model version field populated
- [ ] Result file written with `status: pass` and `artifacts_written` listing `engineering-readiness/initiative-context.md`

## Stop conditions

- If readiness-check.md is missing or not approved: stop.
- Do not invent constraints not present in the source artifacts.
- Do not duplicate full sections from source artifacts — extract only binding facts.
