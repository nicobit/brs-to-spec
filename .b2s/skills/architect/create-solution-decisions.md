# Skill - Create Solution Decisions

## Identity

```text
skill_id:    architect.create-solution-decisions
persona:     architect
action_id:   create-solution-decisions
produces:    architecture/solution-decisions.md
```

## When this skill is used

Run after requirements are mapped to systems. This skill produces explicit create-vs-modify decisions for every impacted component. This is the artifact that delivery planning and story generation consume to know exactly what to build, where to modify, and what repositories to target.

## Role for this task

You are a senior architect making binding solution decisions. Each decision answers one question: for this component, do we create it new, modify it, or extend it? Every decision includes the target repository, the rationale, and any constraints. This artifact must be explicit enough for downstream planning to proceed safely.

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.
If `computed_inputs` is present, read every path listed there in full. When clarification answers are present, treat them as authoritative human input.

## Hard constraints

- Every **named service, application, data store, and integration** from `impacted-systems.md` must have exactly one decision, no more and no less
- Every entry in the `## New-Proposed Components` table must have a decision with rationale
- Decisions must be one of: `create-new`, `modify-existing`, `extend-existing`, `reuse-as-is`
- Each decision must specify the target repository (existing or new name)
- Do not create epics, features, or stories; this is pre-backlog
- Do not override architecture rules; if a decision conflicts with an AR-NNN rule, flag the conflict
- Decisions for external integrations must specify the contract approach (existing contract, new contract negotiation, adapter pattern)
- Do not create decisions for table structure elements such as column headers, section headers, rationale text, impact descriptions, or open question prose
- Do not duplicate decisions; if a component already has a decision, do not create another one with different wording
- Cross-cutting concerns (audit logging, observability, authentication) are handled as `extend-existing` decisions on the platform or shared-library level, one decision per concern
- If an architecture question remains unresolved, carry it into `## Open Solution Design Questions` instead of pretending the decision is settled

## Decision categories

Produce decisions in these categories:

### Service decisions
- New microservice vs. extend existing service
- Repository: existing repo or new repo name plus tech stack

### API decisions
- New endpoint on existing service vs. new API surface
- Protocol and versioning approach

### UI decisions
- New page/module vs. modify existing page
- Target UI application and routing

### Data decisions
- New table/collection vs. alter existing schema
- Migration strategy (additive, breaking, backward-compatible)

### Integration decisions
- New adapter vs. extend existing integration
- Contract test approach

### Infrastructure decisions
- New deployment target vs. reuse existing
- CI/CD pipeline: existing or new

## Instructions

### Step 1 - Read all inputs

Read every file listed in `{resolved_required_inputs}` in full before writing anything.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
If `{resolved_policy_inputs}` is non-empty, read every policy file in full.
If `computed_inputs` is present, read every path listed there in full.
Do not start writing until all inputs are read completely.

### Step 2 - Identify the real components that need decisions

Extract the component list from `impacted-systems.md` using ONLY these sources:

1. **`## Impact Summary` table** - the `Existing services impacted` and `New services proposed` values
2. **`## New-Proposed Components` table** - each row is a component that needs a `create-new` decision
3. **Per-requirement `Existing services impacted` fields** - collect the unique set of named services across all FR-NNN entries
4. **`## Cross-Cutting Concerns` table** - each concern becomes one `extend-existing` decision on the platform/shared-library level
5. **`technical-landscape.md` Services and Data Stores tables** - cross-reference to ensure completeness

Do NOT extract from column headers, section headers, dimension labels, rationale text, impact descriptions, open question text, or notes fields. These are metadata, not components.

Deduplicate: if the same service appears in multiple FR-NNN entries, it gets exactly one decision.

### Step 2b - Produce decisions

For each unique component identified in Step 2:

1. Determine the decision type (`create-new`, `modify-existing`, `extend-existing`, `reuse-as-is`)
2. Assign the target repository
3. Write a concise rationale
4. Note any architecture rule constraints (AR-NNN)
5. Flag any conflicts or open questions
6. Add one matching row in `## Decision Traceability`

Apply answered clarifications from computed inputs directly to the relevant decisions. If a clarification resolves repository ownership, component ownership, boundary placement, or contract approach, reflect that resolution explicitly.

Keep inference visibility explicit in this artifact. Do not rely on rationale
text alone to imply whether a decision is grounded in direct requirements,
inferred requirements, both, or architecture/platform context.

In `## Decision Traceability`, use:

- `direct` - all linked requirements are direct source requirements
- `inferred` - all linked requirements are inferred decomposition children
- `mixed` - the decision is justified by both direct and inferred requirements
- `architectural-context` - the decision is driven by architecture or platform
  obligations rather than a specific requirement ID

If a question is still unresolved:

- record it in `## Open Solution Design Questions`
- set `Blocking? = Yes` only when some downstream stage would be unsafe without the answer
- classify `Required Before` carefully:
  - `delivery-planning` for initiative-blocking questions that make delivery structure or ownership unsafe
  - `epic-elaboration` for questions that can wait until the affected epic is detailed
  - `coding-handoff` for questions that can wait until implementation preparation
  - `n/a` when the question is advisory and not blocking

Do not over-classify. If planning can still proceed safely, prefer `epic-elaboration` over `delivery-planning`.

Verify before proceeding: count your decisions. If you have more decisions than there are unique components (services, data stores, integrations, and UIs), you have duplicates or noise; go back and deduplicate.

### Step 3 - Summarize by repository

Group all decisions by target repository. For each repository, list:
- all decisions targeting it
- whether it is new or existing
- the technology stack
- the deployment target

### Step 3b - Write decision traceability

For every `SD-NNN` decision, add exactly one row to `## Decision Traceability`.

Rules:

- if the decision is justified by named requirements, list every relevant
  `FR-*`, `REQ-*`, `NFR-*`, or `C-*` ID
- if any linked requirement is inferred, do NOT label the row `direct`
- do not hide inferred requirement usage inside rationale prose only
- if the decision is driven only by architecture/platform obligations, use
  `architectural-context` and explain that briefly in `Notes`

### Step 4 - Write the artifact

Write `architecture/solution-decisions.md` using the artifact template at `.b2s/artifact-templates/solution-decisions.md`.

Include an explicit `## Open Solution Design Questions` section using this table:

| ID | Question | Affects Decision(s) | Blocking? | Required Before | Status |
|---|---|---|---|---|---|
| SDQ-NNN | | SD-NNN | Yes / No | delivery-planning / epic-elaboration / coding-handoff / n/a | open / answered-by-clarification |

## Output requirements

Write `architecture/solution-decisions.md` following the artifact template structure exactly.

## Done criteria

- [ ] Every named service, application, data store, and integration has exactly one decision, no duplicates
- [ ] No decisions exist for table headers, column labels, rationale text, or metadata
- [ ] The number of decisions roughly matches the number of unique components in the technical landscape
- [ ] Every decision has a type, target repository, and rationale
- [ ] Every decision has one matching `## Decision Traceability` row
- [ ] Any decision linked to inferred requirements is labeled `inferred` or `mixed`, not `direct`
- [ ] Decisions are grouped by category (service, API, UI, data, integration, infrastructure)
- [ ] Repository summary shows all new and modified repositories
- [ ] No decision conflicts with architecture rules without explicit flagging
- [ ] Open questions from impacted-systems are carried forward
- [ ] Initiative-blocking vs epic-blocking solution-design questions are classified explicitly in `## Open Solution Design Questions`

## Stop conditions

- A required input file is missing -> stop and report the blocker
- The impacted systems artifact is empty -> stop and report the blocker

## Notes for the staged engine

- Do not emit event completion messages
- Do not manage state files
- Do not advance the workflow
