# Skill - Create Epic Folders

## Identity

```text
skill_id:    delivery-lead.create-epic-folders
persona:     delivery-lead
action_id:   create-epic-folders
produces:    epics/
```

## When this skill is used

Run after the elaboration plan is approved. This skill generates one epic folder per epic containing the epic overview, an implementation contract, and individual story files.

## Role for this task

You are a senior delivery lead producing implementation-ready epic packages. Each epic folder must be self-contained — a developer or AI coding agent takes one epic folder and has everything needed to implement the stories within it.

## Per-item execution

This action runs once per epic. The engine provides `{current_item}` — the epic ID to elaborate in this invocation (e.g., "E-001").

When `{current_item}` is provided:
- Create ONLY the folder and files for that one epic
- Do not create folders for other epics
- The engine will call this action again for each remaining epic

When `{current_item}` is NOT provided, create folders for ALL epics.

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.

If a required input is missing, stop and report the blocker.

## INVEST principles for stories

Every user story MUST follow the INVEST principles:

- **Independent** — each story can be delivered without requiring another story in the same epic to be done first (unless explicitly listed as a dependency)
- **Negotiable** — the story describes WHAT and WHY, not HOW
- **Valuable** — each story delivers observable business value to an actor. "Set up database tables" is NOT a valid story.
- **Estimable** — the scope is clear enough for effort estimation
- **Small** — implementable in a focused session. If a story covers more than 3 requirements, split it.
- **Testable** — concrete acceptance criteria in Given/When/Then format

## Story completeness rule

The stories within each epic MUST collectively cover ALL requirements mapped to that epic in the delivery skeleton. If the skeleton maps 5 requirements to E-001, then E-001's stories must reference all 5.

## Hard constraints

- Create one folder per epic: `epics/E-NNN-<slug>/`
- Each folder contains: `epic.md`, `implementation-contract.md`, and `stories/` with story files
- Every epic in the delivery skeleton must have a folder
- Every story in the delivery skeleton must have a story file
- Acceptance criteria MUST be in Given/When/Then Gherkin format with test type annotations
- Generate as many AC as needed — do NOT limit to a fixed count
- Each story must trace to at least one requirement (FR/REQ)
- Each story must declare which application layers it touches (Frontend, Backend, Infrastructure, Integration)
- Each story must have a `## Business Context` section explaining WHY it matters
- Each story must have `## Implementation Guidance` referencing the contract
- Each story must have `## Test Expectations` with test types and what to verify
- Do not leave placeholder text — every field must be populated
- Actors must be specific role names, not "user" or "person"

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
Do not start writing until all inputs are read completely.

### Step 2 - Extract hierarchy from skeleton

From `planning/delivery-skeleton.md`, extract the epic to elaborate (matching `{current_item}` if provided):
- Epic title and features
- Requirements mapped to this epic
- Application layers declared in the skeleton

### Step 3 - Read elaboration plan for wave ordering

From `planning/elaboration-plan.md`, extract the wave assignment for this epic.

### Step 4 - Create epic.md

Create `epics/E-NNN-<slug>/epic.md` using `.b2s/artifact-templates/epic-folder.md`.

Populate every section:
- **Business Objective**: derive from BRS and requirements, not generic
- **Scope**: explicit in/out, name things a developer might wrongly assume
- **High-Level Acceptance Criteria**: epic-level outcomes, testable
- **Foundation / Setup**: project scaffolding, CI/CD, deployment needs — or "No foundation setup required"
- **Stories table**: list all stories with layers, priority, increment, readiness

### Step 5a - Extract technical elements from sources (DO THIS BEFORE WRITING)

Before writing the implementation contract, systematically extract technical elements from the inputs. Go through each source one at a time and build lists. Do not skip this step.

**From the BRS** (`input/brs.md`) — for each requirement linked to this epic:
- Read the requirement text word by word
- List every data field mentioned (e.g., "full name" → field: full_name, type: string)
- List every status or state value mentioned (e.g., "AUTO_APPROVE, REFER_TO_UNDERWRITER, AUTO_DECLINE")
- List every API action implied (e.g., "allow an applicant to submit" → POST endpoint; "retrieve status" → GET endpoint)
- List every event implied (e.g., "send email confirmation" → event: confirmation.requested; "emit structured observability event" → event)
- List every business rule (e.g., "within 2 minutes", "loan amount £1,000–£50,000", "30-day cooling-off")
- List every external system mentioned (e.g., "Experian CreditExpert API", "DocuSign", "Temenos T24")

**From the architecture review** (`architecture/architecture-review.md`):
- List components and their responsibilities relevant to this epic
- List data stores and which entities they hold
- List integration patterns (circuit breakers, fallbacks, timeouts)

**From architecture rules** (`architecture/architecture-rules.md`):
- List AR-NNN rules that apply to this epic's components

**From architecture input** (`input/architecture.md`, if present):
- List existing schemas, tech stack details, deployment constraints

Write down the complete extraction as a mental checklist. Every item in your lists MUST appear in the implementation contract.

### Step 5b - Write implementation-contract.md

Create `epics/E-NNN-<slug>/implementation-contract.md` using `.b2s/artifact-templates/implementation-contract.md`.

**Include ONLY the sections relevant to this epic.** Do not generate empty sections.

**Data Entities** — include if this epic creates, updates, or persists business data:
- Mermaid `erDiagram` with ALL fields from your extraction in Step 5a — not a subset
- Field tables with specific types and constraints derived from the BRS (e.g., "loan_amount: decimal, range £1,000–£50,000" not just "amount: number")
- State machine with Mermaid `stateDiagram-v2` if you found status values in Step 5a
- Every field you extracted MUST appear. If you extracted 8 fields, the ER diagram has 8 fields.

**API Surface** — include if this epic exposes or consumes APIs:
- Complete OpenAPI 3.0 YAML — every field from Step 5a extraction with type, format, constraints
- Request schema: include ALL fields that an API consumer must provide (from BRS field list)
- Response schema: include the response fields (identifiers, status, timestamps)
- Error responses: 400 (validation), 404 (not found), 422 (business rule violation) with specific conditions
- For consumed external APIs: endpoint, auth, timeout, circuit breaker, fallback behaviour
- The OpenAPI spec must be usable by a coding agent to generate server stubs — do NOT write a skeleton

**Events** — include if this epic publishes, consumes, or reacts to events:
- One definition per event with payload schema (field table, not a one-liner)
- Delivery guarantee (at-least-once / at-most-once)
- Idempotency key
- Consumers list

**Business Rules** — every rule from Step 5a extraction with condition, effect, and source FR
**Non-Functional Constraints** — SLAs, performance targets, security constraints from BRS/AR-NNN
**Open Design Questions** — questions that must be resolved before coding

### Step 6 - Create story files

For each story under this epic, create `epics/E-NNN-<slug>/stories/F-NNN.N-<slug>.md` using `.b2s/artifact-templates/lean-story.md`.

For each story:
1. **User Story** — specific actor, concrete capability, business outcome
2. **Business Context** — 2-3 sentences on WHY this story matters
3. **Layers** — which application layers this story touches
4. **Linked Requirements** — FR-NNN from atomic-requirements
5. **Implementation Guidance** — reference the contract: which entity, API, events, rules apply
6. **Acceptance Criteria** — ALL applicable scenarios with test type annotations:
   - `[unit]` for service logic and business rules
   - `[integration]` for external system calls, adapters, DB operations
   - `[api]` for HTTP endpoint request/response contracts
   - `[e2e]` for end-to-end user flows
   - Required: happy path + negative/validation (always)
   - Conditional: authorization, state transition, integration failure, audit/compliance
7. **Test Expectations** — table of test types, what to test, and why
8. **Out of Scope** — what a developer might wrongly assume is included
9. **Dependencies** — story-level or external
10. **Open Questions** — with impact statement

### Step 7 - Verify completeness

Before finishing, perform these cross-checks:

**Field coverage cross-check:** For each BRS requirement linked to this epic, re-read the requirement text. List every field, attribute, and data element mentioned. Verify that EACH one appears in the implementation contract's entity definitions or ER diagram. If a requirement says "full name, date of birth, NI number" and your entity only has "applicant_name" — you are missing fields. Fix before finishing.

**API coverage cross-check:** For each requirement that describes an API behaviour ("the system shall allow...", "retrieve...", "submit..."), verify the endpoint exists in the OpenAPI spec with complete request/response schemas.

**Checklist:**
- [ ] epic.md has all sections populated
- [ ] implementation-contract.md has only relevant sections (no empty sections)
- [ ] If data entities exist: ER diagram includes ALL fields from BRS requirements, not just a subset
- [ ] If APIs exist: OpenAPI YAML has every endpoint implied by requirements, with full schemas
- [ ] Every story has Business Context, User Story, Layers, Implementation Guidance, Test Expectations
- [ ] Every story has at least 2 Gherkin AC with test type annotations
- [ ] Stories collectively cover all requirements mapped to this epic
- [ ] All declared application layers are touched by at least one story
- [ ] No placeholder text remains

## Output requirements

Write to `epics/E-NNN-<slug>/` containing:
- `epic.md` (always)
- `implementation-contract.md` (always — with only relevant sections)
- `stories/F-NNN.N-<slug>.md` (one per story)

## Done criteria

- [ ] Epic folder exists with correct structure
- [ ] Implementation contract has relevant sections only
- [ ] Every story follows INVEST principles
- [ ] Every story has specific actor, business context, layers, implementation guidance
- [ ] Every story has Gherkin AC with test type annotations
- [ ] Every story has test expectations table
- [ ] Stories cover all requirements for this epic
- [ ] No placeholder text remains

## Stop conditions

- If `planning/delivery-skeleton.md` is missing, stop and report the blocker
- If `requirements/atomic-requirements.md` is missing, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes one epic folder per invocation when per-item mode is active
- Validation and state updates are handled by the `.b2s` engine
