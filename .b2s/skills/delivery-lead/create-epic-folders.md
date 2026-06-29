# Skill - Create Epic Folders

## Identity

```text
skill_id:    delivery-lead.create-epic-folders
persona:     delivery-lead
action_id:   create-epic-folders
produces:    epics/
```

## When this skill is used

Run after the elaboration plan is approved. This skill generates one epic folder per epic containing the epic overview and individual lean story files.

## Role for this task

You are a senior delivery lead producing elaborated epic packages that are ready for planning review. This phase defines business scope, story slicing, traceability, story-level behavioral detail, and the implementation contract that defines the technical surface (data entities, API, events, business rules) for the epic.

## Per-item execution

This action runs once per epic. The engine provides `{current_item}` (the epic ID) and `{item_folder}` (the resolved epic folder path if the folder already exists, or empty if this is the first run).

When `{current_item}` is provided:
- If `{item_folder}` is non-empty, use it as the folder path
- If `{item_folder}` is empty, create the folder as `epics/E-NNN-<slug>/` where `<slug>` is derived from the epic title
- Create ONLY the folder and files for that one epic
- Do not create folders for other epics
- The engine will call this action again for each remaining epic

When `{current_item}` is NOT provided, create folders for ALL epics.

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.

If a required input is missing, stop and report the blocker.

## Hard constraints

- Create one folder per epic: `epics/E-NNN-<slug>/`
- Each folder contains `epic.md`, `implementation-contract.md`, and `stories/` with story files
- Every epic in the delivery skeleton must have a folder
- Every story must trace to at least one requirement
- Acceptance criteria MUST be in Given/When/Then Gherkin format with test type, criticality, and automation annotations
- Do NOT produce only 2 scenarios per story — that is the absolute minimum for trivial stories. Most stories need 4-8 scenarios covering: happy path, validation/negative, authorization, boundary, integration failure, state transition, concurrency, and audit
- Each Gherkin scenario must use concrete values (field names, HTTP codes, entity states, thresholds from BRS) — not vague outcomes like "the system handles it"
- Each AC must have a criticality tag (`[critical]`, `[important]`, `[standard]`) and automation tag (`[automate]`, `[manual]`, `[automate-later]`)
- Each story must declare which application layers it touches
- Each story must have `## Business Context`
- Each story must have `## Implementation Guidance` referencing epic context and future implementation prep artifacts when available
- Each story must have `## Test Expectations`
- Every requirement mapped to this epic in the delivery skeleton must be covered by at least one story
- **Each feature (F-NNN) from the delivery skeleton must produce at least one story.** Do NOT collapse an entire epic into a single story. If the delivery skeleton defines features F-001 and F-002 for this epic, you must produce at least 2 stories — one per feature. Features exist because they represent distinct, independently deliverable capabilities
- If a feature covers multiple requirements that span different application layers (frontend + backend + integration), consider splitting into layer-specific stories
- Unresolved questions and ambiguities from the linked requirements must be carried into the relevant story `## Open Questions` section
- Do not leave placeholder text
- If `architecture/solution-decisions.md` exists: every `create-new` decision targeting this epic must result in at least one dedicated story (e.g., infrastructure provisioning, API scaffolding, schema creation, CI/CD pipeline setup, or repository initialization). Do NOT generate only business-functional stories when technical enablement stories are needed to deliver them
- If `architecture/solution-decisions.md` exists: each story must include a `## Technical Scope` section that describes the concrete work per component. For each component the story touches, specify: the repository name (or "monorepo" if single-repo), the component type (api / ui / db / worker / integration / infrastructure), the technology (e.g., .NET 8, React, Azure SQL), and what must be done there (e.g., "create POST /applications endpoint", "add applications table with migration", "create notification settings page"). A single story can touch multiple components — list all of them
- If `architecture/solution-decisions.md` does NOT exist but `input/architecture.md` or `input/repository-context.md` exists, still produce the `## Technical Scope` section using what is known. If only a single repository is known, all work items target that repository
- If no repository information is available at all, omit `## Technical Scope`

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
Do not start writing until all inputs are read completely.

### Step 2 - Extract scope for the current epic

From `planning/delivery-skeleton.md`, extract the epic to elaborate:
- epic title and objective
- features
- requirement IDs and titles mapped to this epic
- dependencies
- application layers
- target repositories (if present — added when solution decisions exist)

From `planning/elaboration-plan.md`, extract the wave assignment and ordering rationale.

### Step 2b - Extract solution decisions for this epic (when available)

If `architecture/solution-decisions.md` exists in `{resolved_optional_inputs}`:

1. Find all decisions (SD-NNN) whose linked requirements belong to this epic.
2. Group them by category: service, API, UI, data, integration, infrastructure.
3. For each `create-new` decision, plan a dedicated story:
   - **New service** → infrastructure provisioning story (create repo, CI/CD, deployment target)
   - **New API endpoint** → API scaffolding story (endpoint skeleton, request/response schemas, error handling)
   - **New data schema** → data setup story (create table/collection, migration script, seed data)
   - **New UI page/module** → UI scaffolding story (routing, component structure, design tokens)
   - **New integration** → integration setup story (adapter, circuit breaker, contract test, mock)
   - **New pipeline** → DevOps story (CI config, environment variables, deployment)
4. For every decision (including `modify-existing` and `extend-existing`), determine the concrete work items per component. Example: a "trigger scoring on submission" story might produce:
   - `loan-origination-api` (api, .NET 8) → emit `scoring.requested` event after application persistence
   - `ai-scoring-service` (worker, Python/FastAPI) → consume `scoring.requested`, run model, persist score
   - `notification-service` (worker, .NET 8) → consume `scoring.completed`, send notification
5. If there is only one repository (monorepo), all work items target that single repo — group by component type instead (api layer, UI layer, DB migration, etc.).
6. Carry this information into Steps 4 and 5 — it becomes the `## Technical Scope` section of each story.

If `architecture/solution-decisions.md` does NOT exist, skip this step.

### Step 3 - Create `epic.md`

Create `epics/E-NNN-<slug>/epic.md` using `.b2s/artifact-templates/epic-folder.md`.

Populate every section with specific initiative content:
- business objective
- explicit in-scope and out-of-scope boundaries
- high-level acceptance criteria
- source traceability using canonical requirement titles
- impacted systems
- dependencies and risks
- foundation/setup needs
- stories table

### Step 4 - Create implementation contract

Create `epics/E-NNN-<slug>/implementation-contract.md` using `.b2s/artifact-templates/implementation-contract.md`.

This contract defines the technical surface for the epic. Include only relevant sections:
- **Data Entities**: ER diagram, field tables, state machines for entities with lifecycle states
- **API Surface**: OpenAPI schemas for endpoints this epic exposes or consumes
- **Events**: domain and audit events with payload schemas
- **Business Rules**: conditions and effects that affect implementation
- **Non-Functional Constraints**: performance, security, or availability targets

Derive content from the BRS, architecture review, architecture rules, and the requirements mapped to this epic. The stories will reference this contract for technical detail.

### Step 5 - Create story files

**Story count rule:** create at least one story per feature (F-NNN) from the delivery skeleton. If the delivery skeleton defines 3 features for this epic, produce at least 3 stories. A story may cover one feature or a subset of a feature — but never multiple features in one story.

For each story in this epic, create `epics/E-NNN-<slug>/stories/S-NNN.N-<slug>.md` using `.b2s/artifact-templates/lean-story.md`.

Each story must include:
1. Specific actor and business outcome
2. `## Business Context` explaining why the behavior matters
3. `## Linked Requirements` with canonical requirement IDs and titles
4. `## Implementation Guidance` referencing `implementation-contract.md` for entities, API endpoints, events, and business rules
5. `## Acceptance Criteria` — comprehensive Gherkin scenarios (see below)
6. `## Test Expectations` with automation column
7. `## Out of Scope`
8. `## Dependencies`
9. `## Open Questions` carrying forward unresolved requirement ambiguities

**Acceptance criteria depth rules:**

For each story, generate scenarios for EVERY applicable type:
- **Happy path** (always) — use concrete field names, HTTP codes, entity states from the BRS and implementation contract
- **Validation / negative** (when story accepts input) — specific field, specific error
- **Authorization** (when story has role/permission) — who can and cannot access
- **Boundary** (when thresholds exist) — exact values from BRS (e.g., £10,000, 60 seconds, 500 concurrent)
- **Integration failure** (when story calls external service) — timeout, error, fallback behavior
- **State transition** (when story changes entity status) — valid and invalid transitions
- **Concurrency / idempotency** (when duplicates are possible) — duplicate requests, race conditions
- **Audit / compliance** (when story produces auditable events) — event emitted with required fields

Each AC must include:
- `[test-type]`: `[unit]`, `[integration]`, `[api]`, or `[e2e]`
- `[criticality]`: `[critical]`, `[important]`, or `[standard]`
- `[automation]`: `[automate]`, `[manual]`, or `[automate-later]`

Minimum scenario counts:
- 1 layer, 1 requirement: at least 3-4 scenarios
- 2+ layers or 2+ requirements: at least 5-6 scenarios
- External integrations or state machines: at least 6+ scenarios

### Step 6 - Verify traceability

Before finishing, cross-check:
- every requirement mapped to this epic is referenced by at least one story
- every linked requirement title matches the canonical title in `requirements/atomic-requirements.md`
- each story's business behavior still matches the linked requirement meaning
- blocking open questions and ambiguities are present in the relevant story

### Step 7 - Self-verify before writing

**Before writing any file**, verify EACH story against this checklist. If any item fails,
fix the story content before writing — do not write and hope validation catches it.

For EACH story, confirm:
- [ ] Has metadata table with `| Layers | ... |` row
- [ ] Has `## Business Context` section with at least 2 sentences
- [ ] Has `## Linked Requirements` with canonical IDs
- [ ] Has `## Implementation Guidance` referencing the implementation contract
- [ ] Has `## Acceptance Criteria` with `\```gherkin` block
- [ ] Gherkin block has at least 3 `Scenario:` entries (4+ for integration/state stories)
- [ ] Each scenario has `[test-type]`, `[criticality]`, `[automation]` tags
- [ ] Has `## Test Expectations` section
- [ ] Has `## Open Questions` if linked requirements have ambiguities

Also confirm `implementation-contract.md` exists with populated sections.

**If you cannot produce a story at this quality level, do NOT write a skeletal stub.**
It is better to produce fewer stories at full quality than many stubs that fail validation.

## Output requirements

Write to `epics/E-NNN-<slug>/` containing:
- `epic.md`
- `implementation-contract.md`
- `stories/S-NNN.N-<slug>.md`

## Done criteria

- [ ] Epic folder exists with `epic.md`, `implementation-contract.md`, and `stories/`
- [ ] Implementation contract has relevant sections populated (data entities, API, events, rules)
- [ ] Stories reference the implementation contract in their Implementation Guidance
- [ ] Every story has canonical requirement traceability
- [ ] Every story has Gherkin acceptance criteria with test type annotations
- [ ] Open questions are propagated to the right stories
- [ ] Story count is at least equal to the number of features (F-NNN) in the delivery skeleton for this epic
- [ ] Stories collectively cover all requirements for the epic
- [ ] If solution decisions exist, every `create-new` decision for this epic has a corresponding story
- [ ] If solution decisions or repo context exist, each story has `## Technical Scope` with concrete work per component
- [ ] No placeholder text remains

## Stop conditions

- If `planning/delivery-skeleton.md` is missing, stop and report the blocker
- If `requirements/atomic-requirements.md` is missing, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes one epic folder per invocation when per-item mode is active
- Validation and state updates are handled by the `.b2s` engine
