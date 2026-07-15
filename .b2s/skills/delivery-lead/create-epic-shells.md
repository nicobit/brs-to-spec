# Skill - Create Epic Shells

## Identity

```text
skill_id:    delivery-lead.create-epic-shells
persona:     delivery-lead
action_id:   create-epic-shells
produces:    epics/
```

## When this skill is used

Run after the elaboration plan is approved. This skill generates the epic overview and implementation contract for one epic. Stories are produced by the next action (`create-epic-stories`).

## Role for this task

You are a senior delivery lead defining the business scope, traceability, and technical contract for one epic. The implementation contract you produce will be read by the story generation action as a concrete input — make it precise.

## Per-item execution

This action runs once per epic. The engine provides `{current_item}` (the epic ID) and `{item_folder}` (the resolved epic folder path if the folder already exists, e.g. `epics/E-002-ai-pre-screening-scoring/`, or empty if this is the first run).

- If `{item_folder}` is non-empty, use it as the folder path (the folder already exists from a previous run or retry)
- If `{item_folder}` is empty, create the folder as `epics/E-NNN-<slug>/` where `<slug>` is derived from the epic title
- Create ONLY the folder and files for that one epic
- Do not create folders for other epics
- The engine will call this action again for each remaining epic

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.

If a required input is missing, stop and report the blocker.

## Hard constraints

- Create one folder per epic: `epics/E-NNN-<slug>/`
- **The folder slug MUST be derived from the canonical epic title in `delivery-skeleton.md`.** Do not rename, rephrase, or expand the epic title when creating the folder name. If the skeleton says `E-003 — Compliance & KYC`, the folder must be `epics/E-003-compliance-kyc/`, not `epics/E-003-application-decisioning-underwriter-routing/`. When computed context includes `canonical_title`, use it as the authoritative source.
- The `epic.md` heading must contain the canonical title from the skeleton (e.g. `# E-003 — Compliance & KYC`)
- Each folder contains `epic.md` and `implementation-contract.md`
- Do NOT create story files - that is the next action's job
- Every requirement mapped to this epic in the delivery skeleton must appear in `epic.md` source traceability
- Do not leave placeholder text
- If `architecture/solution-decisions.md` exists: note every `create-new` decision targeting this epic in the contract - the story action will need them to generate technical enablement stories
- If `architecture/impacted-systems.md` or `architecture/solution-decisions.md` shows an external provider, dashboard surface, callback flow, shared platform concern, or cross-system workflow for this epic, make those surfaces explicit in the contract so the story action can generate dedicated implementation stories rather than burying them inside generic e2e work
- The `## UI Surface` section is a scoped extract from `architecture/ui-specification.md`, not a new source of initiative-level UI truth
- Do not invent new routes, fields, validation rules, states, or bindings that are absent from the UI spec unless they come from explicit clarification input
- If clarification input changes a UI fact, carry the resolved value and reference the corresponding `UIQ-*` or clarification answer source
- Do not redefine repository ownership, application ownership, or frontend technology choices here when they are already owned by `architecture/solution-decisions.md`
- If a UI page is `partial` or `blocked`, preserve that status honestly in the epic contract instead of normalizing it into build-ready detail

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
If `computed_inputs` is present, read every path listed there — these contain
engine-derived data scoped to the current epic. Use computed inputs as the
primary source for requirements and system mappings.
If computed clarification context is present and it shows an existing
`input/clarifications/{current_item}.yaml` file, treat those answers as
authoritative human clarifications for this epic.
Do not start writing until all inputs are read completely.

### Step 2 - Extract scope for the current epic

From `planning/delivery-skeleton.md` (or the computed epic context), extract:
- epic title and objective
- features (F-NNN) and their requirement mappings
- requirement IDs and titles mapped to this epic
- dependencies on other epics
- application layers
- target repositories (if present from solution decisions)
- whether the epic includes named external integrations, operator or admin UI, callback workflows, stateful handoffs, audit or observability obligations, or explicit fallback behavior

From `planning/elaboration-plan.md`, extract the wave assignment and ordering rationale.

### Step 3 - Extract solution decisions for this epic (when available)

If `architecture/solution-decisions.md` exists (or filtered solution decisions are in the computed epic context):

1. Find all decisions (SD-NNN) whose linked requirements belong to this epic.
2. Group them by category: service, API, UI, data, integration, infrastructure.
3. Note which decisions are `create-new` — the story action will need dedicated stories for these.
4. Carry decision details into the implementation contract sections.

When decisions show a provider adapter, dashboard page, callback endpoint, metrics surface, or shared platform extension, preserve that distinction explicitly in the contract. Do not flatten them into generic "backend changes".

If no solution decisions exist, skip this step.

### Step 3b - Apply epic clarifications when present

If computed clarification context indicates answers exist for the current epic:

1. Read every resolved answer carefully.
2. Apply those answers to the implementation contract sections they affect.
3. Remove or narrow matching open design questions when they are fully resolved.
4. Keep unresolved blockers explicit.

Do not invent extra resolution beyond what the clarification input says.

### Step 4 - Create `epic.md`

Create `epics/E-NNN-<slug>/epic.md` using `.b2s/artifact-templates/epic-folder.md`.

Populate every section with specific initiative content:
- business objective
- explicit in-scope and out-of-scope boundaries
- high-level acceptance criteria
- source traceability using canonical requirement titles
- impacted systems
- dependencies and risks
- foundation/setup needs
- features table (from delivery skeleton)

In `## Source Traceability`, keep requirement derivation visible:

- `source-text` for BRS section references
- `direct` for direct source requirements
- `inferred` for inferred decomposition children

Do not flatten inferred `REQ-*` requirements into generic requirement rows
without that basis signal.

### Step 5 - Create implementation contract

Create `epics/E-NNN-<slug>/implementation-contract.md` using `.b2s/artifact-templates/implementation-contract.md`.

This contract defines the technical surface for the epic. Include only relevant sections:
- **Data Entities**: ER diagram, field tables, state machines for entities with lifecycle states
- **API Surface**: OpenAPI schemas for endpoints this epic exposes or consumes
- **UI Surface**: If `architecture/ui-specification.md` exists AND this epic delivers frontend
  pages, populate the `## UI Surface` section. Extract only the pages owned by this epic from
  the initiative-level UI spec. Include fields, validation, data binding (with Contract Mode), states, and user flows.
  For each page, carry forward `Specification Status`, `Blocking dependencies`, and `Contract Mode` from the UI spec.
  If a page has status `partial` or `blocked`, carry its blocking open questions (UIQ-NNN) into the epic's `## Open Design Questions` section - these must be resolved before story generation for that page.
  If epic clarifications resolve one of those questions, update the affected page details and remove that blocker from the open questions list.
  Do not treat this section as a place to redefine initiative-level page truth - it is a scoped delivery extract.
  If this epic has no frontend pages, omit the section entirely.
- **Events**: domain and audit events with payload schemas
- **Business Rules**: conditions and effects that affect implementation
- **Non-Functional Constraints**: performance, security, or availability targets

For integration-heavy or workflow-heavy epics, be concrete enough that downstream story generation can split real implementation stories without guessing. When relevant, make these details explicit:
- provider or partner API contract shape
- callback endpoints and validation rules
- timeout, retry, and fallback behavior
- idempotency keys or duplicate-protection rules
- state transitions and confirmation handling
- audit and observability payload expectations
- applicant, operator, or underwriter notification triggers

If a dashboard, portal, admin page, or underwriter workbench is part of this epic, the contract must expose that UI surface explicitly so story generation can produce dedicated frontend stories instead of treating the entire feature as backend-only.

Derive content from the BRS, architecture review, architecture rules, and the requirements mapped to this epic. The stories (next action) will reference this contract for technical detail.

### Step 6 - Verify traceability

Before finishing, cross-check:
- every requirement mapped to this epic appears in `epic.md` source traceability
- the implementation contract covers the technical surface for all mapped requirements
- external integrations, UI surfaces, callback flows, and cross-cutting platform concerns are explicit when they are part of the epic scope
- no placeholder text remains

## Output requirements

Write to `epics/E-NNN-<slug>/` containing:
- `epic.md`
- `implementation-contract.md`

Do NOT create a `stories/` directory or any story files.

## Done criteria

- [ ] Epic folder exists with `epic.md` and `implementation-contract.md`
- [ ] `epic.md` has populated business objective, scope, traceability, and features
- [ ] Implementation contract has relevant sections populated (data entities, API, events, rules)
- [ ] Every requirement mapped to this epic in the skeleton is present in source traceability
- [ ] If solution decisions exist, `create-new` decisions are noted in the contract
- [ ] No placeholder text remains

## Stop conditions

- If `planning/delivery-skeleton.md` is missing, stop and report the blocker
- If `requirements/atomic-requirements.md` is missing, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes one epic shell per invocation when per-item mode is active
- Validation and state updates are handled by the `.b2s` engine
