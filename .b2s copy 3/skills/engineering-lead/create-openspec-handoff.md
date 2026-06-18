# Skill — Create OpenSpec Handoff

## Identity

```text
skill_id:    engineering-lead.create-openspec-handoff
persona:     engineering-lead
action_id:   create-openspec-handoff
produces:    specs/
```

## When this skill is used

Run only when delivery mode is `OpenSpec`, readiness is `Ready`, and all triggered gates are accepted.

## Preconditions

Before starting, verify:
- `engineering-readiness/readiness-check.md` is `Ready`
- all triggered gates are accepted
- `planning/delivery-structure.md` has story IDs
- `engineering-readiness/initiative-context.md` exists
- `architecture/architecture-rules.md` exists

## Step 1 — Read all inputs

Read these files in full before writing anything. Do not start writing until all are read completely.

**Required:**
- `{workspace_root}/planning/delivery-structure.md` — story IDs, epics, features, FR coverage
- `{workspace_root}/engineering-readiness/initiative-context.md` — architecture summary, tech stack, integration map
- `{workspace_root}/architecture/architecture-rules.md` — constraints the coding agent must not violate
- `{workspace_root}/engineering-readiness/readiness-check.md` — readiness status, open decisions

**Read if present:**
- `{workspace_root}/business-analysis/requirements.md` — FR/NFR references per story
- `{workspace_root}/business-analysis/business-rules.md` — BR references per story
- `{workspace_root}/business-analysis/use-cases/` — use case detail per feature
- `{workspace_root}/business-analysis/actors-and-personas.md` — actors for user story sentences
- `{workspace_root}/architecture/architecture-review.md` — brownfield impact, integration risks
- `{workspace_root}/planning/traceability-matrix.md` — FR → story → AC mapping
- `{workspace_root}/planning/epics/` — epic context: business objective, impacted systems, risks
- `{workspace_root}/planning/features/` — feature context: scope, business value, BDD expectations, implementation notes
- `{workspace_root}/quality-gates/bdd-scenarios.md` or per-feature BDD files — BDD scenarios to embed
- `{workspace_root}/quality-gates/api-contract.md` — API impact per story
- `{workspace_root}/quality-gates/data-contract.md` — data model impact per story

## Step 2 — Enumerate stories

From `delivery-structure.md`, extract the full list of story IDs in order: `F-001.1`, `F-001.2`, etc.

Count them. The number of story folders you create must equal this count exactly.

## Step 3 — Create dependency graph

Create `specs/dependency-graph.md`.

For each story, list:
- story ID and title
- stories it depends on (from delivery-structure.md or business logic)
- external system dependencies
- recommended implementation order (which stories must be built first)

## Step 4 — Create one story folder per story

For each story `F-XXX.X`, create the folder `specs/F-XXX.X-<slug>/` and generate the following files.

### story.md

Follow the structure in `.b2s/artifact-templates/story-package.md` exactly.

Populate every section with specific content derived from the inputs. Do not leave placeholder text. Specifically:

**Section 1 — User Story:** Write the full As a / I want / so that sentence using the actor from `actors-and-personas.md`. State the business goal in 2–5 sentences. List in-scope and out-of-scope items explicitly. Populate the Feature and Epic metadata fields from the feature-package and epic-package files when available — use the feature goal and epic business objective to inform the business goal paragraph.

**Section 2 — Source Traceability:** Link to the BRS section, FR-NNN from `requirements.md`, BR-NNN from `business-rules.md`, and AR-NNN from `architecture-rules.md` that apply to this story.

**Section 3 — Business Rules Applied:** Extract every BR that constrains the behaviour of this story. State its impact concretely.

**Section 4 — Acceptance Criteria:** Write testable Given/When/Then criteria. Each must link to FR-NNN, BR-NNN, and SCN-NNN. At minimum: one happy path criterion, one validation/negative criterion.

**Section 5 — BDD Scenarios:** Write valid Gherkin. If BDD scenarios exist in `quality-gates/bdd-scenarios.md` or `quality-gates/bdd/` for this story, use them here rather than generating new ones.

BDD scenario quality rules (apply to every scenario written):
- valid Given/When/Then only — no narrative prose inside scenario steps
- observable business behaviour only — no implementation details, no UI click descriptions
- meaningful scenario name — not a copy of the story title, not "Test feature"
- link each scenario to the AC-NNN it validates (add a comment line `# AC-NNN` before the scenario)
- link each scenario to the story ID (add `# F-XXX.X` before the scenario)

Required scenario coverage per story:
- happy path: always
- validation/negative: always
- authorization: when the story involves roles or permissions
- business rule: when BR-NNN constrains the behaviour
- state transition: when a workflow state changes
- integration failure: when an external system is called
- audit/compliance: when an audit event must be recorded

Do not write generic scenarios. If the initiative has no relevant actor permissions, state transition, or integration call for a given story, omit those types and note why in a comment above the scenario block.

**Section 6 — Implementation Context:** List every component touched (API endpoint, service, database table, event, UI screen). Describe data impact (field names, types, constraints), API impact (endpoint, request/response schema, error codes), UI impact, and integration impact from `architecture-review.md` and `api-contract.md`.

**Section 7 — Constraints:** Copy every architecture rule from `architecture-rules.md` that applies to this story. Include security, data residency, SLA, and compliance constraints explicitly.

**Section 8 — Dependencies:** List story-level and external dependencies. Mark whether each is blocking.

**Section 9 — Implementation Tasks:** Write 3–8 concrete tasks per story. Bad: "implement backend". Good: "Add `POST /applications` endpoint that validates payload against schema V1, returns 422 with field-level errors on validation failure, and emits `ApplicationCreated` event". Each task must have a target area and a validation expectation.

**Section 10 — Test Expectations:** Specify what unit, integration, API, UI, negative, permission, and regression tests are needed. Be specific about what each test must cover.

**Section 11 — Definition of Done:** Confirm all checkboxes are relevant to this story.

**Section 12 — Coding-Agent Prompt:** Write a complete, self-contained prompt that a coding agent can execute without reading any other file. Include: goal, files/components impacted, constraints, step-by-step implementation guide, tests to add, what not to change, and a validation checklist.

### design.md

Document:
- all components touched (layer, responsibility, interface)
- sequence diagram or narrative flow for the main scenario
- data model changes (new fields, new tables, new events)
- API surface (endpoints, request/response, error handling)
- integration touchpoints (system, protocol, failure handling)
- observability (logs, metrics, traces, audit events)
- brownfield impact from `architecture-review.md`

### tasks.md

List all implementation tasks in execution order. Group by area: API, Service, Database, UI, Tests, Docs. For each task include: what to build, acceptance expectation, and which story file or test validates it.

### coding-prompt.md

Copy the coding-agent prompt from `story.md` Section 12 and expand it with:
- the full component list from `design.md`
- the full task list from `tasks.md`
- explicit "do not touch" rules based on `architecture-rules.md`

This file is the single entrypoint for the coding agent. It must be self-contained.

## Done criteria

- [ ] story count equals folder count (no missing, no extra)
- [ ] `specs/dependency-graph.md` exists and lists implementation order
- [ ] every story folder has: `story.md`, `design.md`, `tasks.md`, `coding-prompt.md`
- [ ] every `story.md` has all 12 sections populated with specific content (no placeholders, no generic text)
- [ ] every story links to at least one FR-NNN, one BR-NNN (if business rules exist), and one AC
- [ ] every story has at least two BDD scenarios in valid Gherkin
- [ ] every `coding-prompt.md` is self-contained and includes constraints and test instructions
- [ ] no story folder covers more than one story
