# Skill - Create OpenSpec Handoff

## Identity

```text
skill_id:    engineering-lead.create-openspec-handoff
persona:     engineering-lead
action_id:   create-openspec-handoff
produces:    specs/
```

## When this skill is used

Run only when delivery mode is `OpenSpec`, readiness is `Ready`, and all
triggered gates are accepted.

## Preconditions

Before starting, verify:
- `engineering-readiness/readiness-check.md` is `Ready`
- all triggered gates are accepted
- `planning/delivery-structure.md` has story IDs
- `engineering-readiness/initiative-context.md` exists
- `architecture/architecture-rules.md` exists
- `quality-gates/nfr-assessment.md` exists

## Step 1 - Read all inputs

Read these files in full before writing anything. Do not start writing until all
are read completely.

Required:
- `{workspace_root}/planning/delivery-structure.md` - story IDs, epics, features, FR coverage
- `{workspace_root}/engineering-readiness/initiative-context.md` - architecture summary, tech stack, integration map
- `{workspace_root}/architecture/architecture-rules.md` - constraints the coding agent must not violate
- `{workspace_root}/engineering-readiness/readiness-check.md` - readiness status, open decisions
- `{workspace_root}/quality-gates/nfr-assessment.md` - explicit NFRs, operational constraints, compliance and resiliency expectations

Read if present:
- `{workspace_root}/business-analysis/requirements.md` - FR and NFR references per story
- `{workspace_root}/business-analysis/business-rules.md` - BR references per story
- `{workspace_root}/business-analysis/use-cases/` - use case detail per feature
- `{workspace_root}/business-analysis/actors-and-personas.md` - actors for user story sentences
- `{workspace_root}/architecture/architecture-review.md` - brownfield impact, integration risks
- `{workspace_root}/planning/traceability-matrix.md` - FR to story to AC mapping
- `{workspace_root}/planning/epics/` - epic context: business objective, impacted systems, risks
- `{workspace_root}/planning/features/` - feature context: scope, business value, BDD expectations, implementation notes
- `{workspace_root}/quality-gates/bdd-scenarios.md` or per-feature BDD files - BDD scenarios to embed
- `{workspace_root}/quality-gates/api-contract.md` - API impact per story
- `{workspace_root}/quality-gates/data-contract.md` - data model impact per story
- `{workspace_root}/quality-gates/test-strategy.md` - testing expectations and quality levels
- `{resolved_optional_inputs}` - technical-specification artifacts when workflow type is `technical-spec-modular`

Read every policy file listed in `{resolved_policy_inputs}` in full before
creating story packages.

## Step 1b - Apply technical specifications when present

Check for these paths after reading the optional inputs above. When they exist,
treat them as authoritative. Do not regenerate equivalent detail from scratch;
read the spec and copy it into the story.

If `{workspace_root}/technical-specifications/api/exposed/` exists and contains files:
- Read each exposed API spec file.
- For each story, find the endpoint or endpoints that story implements.
- Populate Section 6 `API Impact` with the exact endpoint path, method, request
  fields, response fields, auth mechanism, and error codes from the spec.
- Populate Section 7 `Constraints` with auth mechanism and SLA values from the spec.

If `{workspace_root}/technical-specifications/api/consumed/` exists and contains files:
- Read each consumed API spec for external systems this story calls.
- Populate Section 6 `Impacted Components` with the external system endpoint
  path, auth mechanism, and timeout from the consumed spec.
- Populate Section 7 `Constraints` with PII minimization rules from the consumed spec.

If `{workspace_root}/technical-specifications/data/` exists and contains files:
- Read the data schema spec for the domain this story writes to.
- Populate Section 6 `Data Impact` with the exact entity name, field names,
  types, and constraints from the schema spec.
- Note any PII fields and their retention period.

If `{workspace_root}/technical-specifications/integrations/` exists and contains files:
- Read the integration spec for each external system this story calls.
- Populate Section 8 `Dependencies` with the integration timeout, retry policy,
  and fallback behavior from the integration spec.

When technical-spec artifacts are present, do not re-derive fields they already
define. Use the spec value verbatim.

## Step 1c - Apply handoff policies

Apply the policy context from `{resolved_policy_inputs}`:
- make test expectations explicit enough for downstream execution
- keep coding-agent instructions self-contained and constraint-aware
- do not imply permission to change unrelated systems or architecture boundaries
- call out likely impacted files, modules, services, interfaces, and data stores explicitly

## Step 2 - Enumerate stories

From `delivery-structure.md`, extract the full list of story IDs in order:
`F-001.1`, `F-001.2`, and so on.

Count them. The number of story folders you create must equal this count exactly.

## Step 3 - Create dependency graph

Create `specs/dependency-graph.md`.

For each story, list:
- story ID and title
- stories it depends on
- external system dependencies
- major impacted areas
- recommended implementation order

## Step 4 - Create one story folder per story

For each story `F-XXX.X`, create the folder `specs/F-XXX.X-<slug>/` and
generate the following files:
- `story.md`
- `design.md`
- `tasks.md`
- `coding-prompt.md`

### story.md

Follow the structure in `.b2s/artifact-templates/story-package.md` exactly.

Populate every section with specific content derived from the inputs. Do not
leave placeholder text.

Section expectations:
- Section 1 `User Story`: write the full story sentence and explain the business
  goal in 2 to 5 sentences. State explicit in-scope and out-of-scope items.
- Section 2 `Source Traceability`: link BRS, FR, BR, AR, and every relevant
  `NFR-NNN` from `quality-gates/nfr-assessment.md`.
- Section 3 `Business Rules Applied`: extract every BR that constrains the story.
- Section 4 `Acceptance Criteria`: write testable Given/When/Then criteria and
  link each to FR, BR where relevant, and BDD scenario IDs.
- Section 5 `BDD Scenarios`: use existing BDD where present; otherwise write
  valid Gherkin with happy path and negative coverage at minimum.
- Section 6 `Implementation Context`: list impacted components, data impact, API
  impact, UI impact, and integration impact.
- Section 7 `Constraints`: copy applicable architecture rules and use
  `quality-gates/nfr-assessment.md` as the primary source for non-functional,
  operational, security, resilience, and compliance constraints.
- Section 8 `Dependencies`: include story and external dependencies and mark blockers.
- Section 9 `Implementation Tasks`: write 3 to 8 concrete tasks with target area
  and validation expectation.
- Section 10 `Test Expectations`: specify unit, integration, API, UI, negative,
  permission, regression, and NFR-verification tests as applicable.
- Section 11 `Definition of Done`: keep all checks relevant to the story.
- Section 12 `Coding-Agent Prompt`: make it fully self-contained. Include
  business context, technical context, acceptance criteria, impacted files or
  areas, constraints, implementation steps, tests to add, what not to change,
  and a validation checklist.

### design.md

Document:
- all components touched with layer, responsibility, and interface
- sequence flow for the main scenario
- data model changes
- API surface
- integration touchpoints and failure handling
- observability and audit expectations
- brownfield impact

### tasks.md

List all implementation tasks in execution order. Group by area: API, Service,
Database, UI, Tests, Docs. For each task include what to build, acceptance
expectation, and which story file or test validates it.

### coding-prompt.md

Copy the coding-agent prompt from `story.md` Section 12 and expand it with:
- the full component list from `design.md`
- the full task list from `tasks.md`
- explicit do-not-touch rules from `architecture-rules.md`
- explicit NFR constraints from `quality-gates/nfr-assessment.md`

This file is the single entrypoint for the coding agent. It must be
self-contained.

## Done criteria

- [ ] story count equals folder count
- [ ] `specs/dependency-graph.md` exists and lists implementation order
- [ ] every story folder has `story.md`, `design.md`, `tasks.md`, and `coding-prompt.md`
- [ ] every `story.md` has all 12 sections populated with specific content
- [ ] every story links to at least one FR-NNN and every relevant NFR-NNN
- [ ] every story has at least two BDD scenarios in valid Gherkin
- [ ] every `coding-prompt.md` is self-contained and includes business context, technical context, impacted areas, constraints, and test instructions
- [ ] no story folder covers more than one story
