# Prompt — Create OpenSpec Change for Active Deliverable

## Role

You are an engineering lead preparing one delivery increment for implementation using OpenSpec.
The output of this prompt is a self-contained folder that an engineer (or AI coding agent via `/opsx:apply`) can pick up and implement without opening any other artifact.

## When to use

Only when `execution_mode` is `OpenSpec` and all of the following are true:
- `engineering-readiness/readiness-check.md` exists and decision is `Ready`
- All triggered quality gates have `Status: Accepted` in their Metadata
- The active deliverable is identified in `planning/delivery-structure.md`

## Inputs — read in this order

1. `planning/workflow-state.json` — identify current stage and active deliverable
2. `planning/delivery-structure.md` — epics, features, user stories, and increment definition
3. `engineering-readiness/initiative-context.md` — scope, integrations, constraints
4. `architecture/architecture-rules.md` — binding rules that engineers must follow
5. `input/architecture.md` — deployment topology, integration decisions
6. `quality-gates/security-review.md` — security checklist and accepted risks
7. `quality-gates/api-contract.md` — API surface, auth, error codes, contracts
8. `quality-gates/data-contract.md` — schema, PII mapping, retention, residency
9. `quality-gates/observability-plan.md` — telemetry catalog, alert rules, runbooks

## Output — one folder per active deliverable

```
openspec/changes/{{deliverable-id}}-{{slug}}/
  proposal.md        ← why, scope, constraints, reference table
  design.md          ← self-contained technical context for the increment
  tasks.md           ← ordered implementation checklist
  specs/
    api.md           ← distilled API surface for this increment
    data.md          ← distilled data model changes for this increment
    observability.md ← distilled telemetry signals and alerts for this increment
```

**One folder per increment — generate all increments defined in `planning/delivery-structure.md` in sequence.** Each increment gets its own folder (`D1-<slug>/`, `D2-<slug>/`, `D3-<slug>/`) with its own scoped `proposal.md`, `design.md`, `tasks.md`, and `specs/`. After completing one folder, immediately continue to the next increment without stopping. Stop only when all increments in the delivery structure have a folder, or when a genuine stop condition is reached (missing input, unresolved dependency between increments).

## Output rules

### proposal.md
- State the business driver in one paragraph (why this, why now)
- List concrete system changes as bullet points — no implementation detail
- Include a scope table: features and user stories in scope, with requirement traceability
- List explicit out-of-scope items — deferred features, integrations, increments
- List success criteria with measurable targets sourced from BRS / NFRs
- Include a reference table pointing to the full gate artifacts by path — do not inline the full gate content here

### design.md
- Must be self-contained: an engineer should be able to implement from `design.md` + `tasks.md` + `specs/` without opening any other artifact
- API surface table: method, path, purpose, auth, request, response, contract artifact → `specs/api.md`
- Data model table: table, change, key columns, PII flag, encryption, contract artifact → `specs/data.md`
- Integration points table: integration, protocol, auth, async?, idempotency, contract artifact
- Architecture constraints table: only rules from `architecture-rules.md` that apply to this increment
- Security decisions table: derived from `quality-gates/security-review.md` — decisions relevant to this increment
- Observability requirements table: signals engineers must emit — derived from `quality-gates/observability-plan.md`
- Optional Mermaid sequence diagram: only if async flow or integration boundary is genuinely hard to follow from text. Do not add if a diagram already exists in `input/architecture.md`.
- Open questions: unresolved items that must be answered before or during implementation

### tasks.md
- Tasks are ordered — earlier tasks may be dependencies for later ones
- One task per independently reviewable unit of work (one PR boundary)
- Each task must include: user story, requirement, acceptance source, architecture constraint, data tables touched, API endpoints touched, telemetry events to emit, evidence expected
- Validation tasks: one per acceptance criterion requiring an explicit test
- Handoff checklist: standard items + increment-specific items from quality gates

### specs/ folder
- `specs/api.md`: endpoints and webhooks for this increment only. Include request/response schemas, error codes, auth, idempotency. Reference the contract artifact for sandbox credentials and full SLA — do not paste credentials.
- `specs/data.md`: tables created or modified in this increment only. Include columns, PII classification, encryption approach, migration notes. Reference the gate artifact for full DDL and Legal sign-off.
- `specs/observability.md`: telemetry signals, tracing approach, and alerts for components built in this increment only. Mark signals as mandatory. Reference runbooks by path — do not duplicate them.

## Quality bar

A good output:
- Can be handed to an engineer or `/opsx:apply` with no additional context
- Has every task traceable to a requirement, user story, and acceptance source
- Makes telemetry emission mandatory in each task that touches an instrumented component
- Distills gate content into `specs/` without losing the detail an engineer needs
- Does not inline full gate artifact content into `proposal.md` or `design.md`
- Does not create tasks for the whole BRS or multiple increments
- Does not produce vague tasks (`implement backend`, `add API`, `handle errors`)

## Anti-patterns

- Stopping after the first increment — continue until all increments in `delivery-structure.md` have a folder
- Mixing features from different increments into one folder — each folder is scoped to exactly one increment
- Inlining the full data contract table into `design.md` — put it in `specs/data.md` and reference it
- Creating tasks without telemetry emission requirements
- Generating `gitlab-issues.md` or any planning-tool export — that is downstream of this prompt
- Copying user stories directly as tasks — derive engineering tasks from stories + architecture + gate constraints
- Ignoring architecture rules in task definitions
- Generating code

## Stop conditions

If any required input is missing or a quality gate is not Accepted: list what is missing, state the impact, stop. Do not generate partial output.

## Self-review checklist

Before finalising, verify:
- [ ] One increment only
- [ ] `design.md` is self-contained — an engineer can implement from it without opening gate artifacts
- [ ] Every task has: user story, requirement, acceptance, constraint, data, API, events to emit, evidence
- [ ] `specs/api.md` covers all endpoints and webhooks for this increment
- [ ] `specs/data.md` covers all table changes with PII and encryption noted
- [ ] `specs/observability.md` marks all signals as mandatory and references runbooks by path
- [ ] No gate artifact content duplicated — referenced by path instead
- [ ] No tasks for out-of-scope features
- [ ] No generated code
