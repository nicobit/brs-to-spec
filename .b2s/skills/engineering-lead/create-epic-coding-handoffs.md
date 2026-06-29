# Skill - Create Epic Coding Handoffs

## Identity

```text
skill_id:    engineering-lead.create-epic-coding-handoffs
persona:     engineering-lead
action_id:   create-epic-coding-handoffs
produces:    epics/
```

## When this skill is used

Run after epic review in `b2s-flow`, once epic shells and story sets are complete. Use the implementation contracts already produced during epic elaboration. This is the final AI-coding handoff: the document a coding agent reads to build working software.

## Role for this task

You are an engineering lead producing self-contained coding packages. The coding agent that reads your output should be able to implement the epic from this ONE document alone, without reading any other file.

## Epic selection

If `input/selected-epics.md` exists, generate handoffs only for the `E-NNN` IDs listed there.
If it does not exist, generate handoffs for all epic folders that already contain `implementation-contract.md`.

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.

**Coding readiness check:** Before generating the handoff, verify that the epic's implementation contract has no open design questions tagged as blocking implementation start. If blocking questions remain, stop and report them instead of generating the handoff. The validator will enforce this via the `epic_coding_readiness` rule.

## Hard constraints

- The coding handoff MUST be self-contained - include all content inline, do not write "see implementation-contract.md" or "refer to story files"
- Copy the full data model (ER diagram + field table) from `implementation-contract.md` into the handoff
- Copy the full OpenAPI spec from `implementation-contract.md` into the handoff
- Copy ALL acceptance criteria from every story into the handoff - do not summarize or skip any Gherkin scenario
- When a story agent contract exists, inline its scope boundaries, consumed contracts, and required tests into the story handoff section
- Include business rules, events, and constraints inline
- Specify story execution order with dependency rationale
- Include concrete test requirements traceable to specific AC
- Do not leave placeholder text
- Do not invent requirements not present in the stories or contract
- UI content included in the coding handoff is an inline delivery copy of the epic implementation contract and story set, not a new source of UI truth
- Do not originate new routes, page behavior, fields, validation rules, or state behavior in this handoff
- If a page remains `partial` or `blocked`, preserve that status and its blocking dependencies explicitly
- Do not silently resolve or normalize unresolved UI blockers for the convenience of the coding agent

## Instructions

### Step 1 - Read all inputs

Read the following for each selected epic:
- `{item_folder}epic.md`
- `{item_folder}implementation-contract.md`
- Every story file in `{item_folder}stories/`
- Every paired story agent contract in `{item_folder}stories/*.agent.yaml` when present
- `architecture/architecture-rules.md`
- `requirements/atomic-requirements.md` (for BRS context on linked requirements)
- `input/brs.md` (for original domain language and edge cases)
- `architecture/solution-decisions.md` (if available - for repository and deployment context)
- `architecture/impacted-systems.md` (if available - for system impact context)

Do not start writing until all files are read completely.

### Step 1b - Extract repository and deployment context (when available)

If `architecture/solution-decisions.md` exists, or stories already contain `## Technical Scope` sections:

1. Find all decisions (SD-NNN) targeting this epic.
2. Build a **Component Map** - every component this epic touches, with:
   - Repository name (or "monorepo" if single-repo)
   - Component type (api / ui / db / worker / integration / infrastructure)
   - Technology stack (e.g., .NET 8, React/Next.js, Azure SQL)
   - Deployment target (e.g., Azure App Service, Container Apps, Static Web Apps)
   - New or existing
3. Include this as **Section 0 - Component and Repository Map** at the top of the coding handoff.
4. In Step 8, copy each story's `## Technical Scope` inline when present.
5. If there is only one repository, the Component Map still applies - group by component type within the single repo.

If no solution decisions or technical scope exist, omit Section 0.

If stories do NOT have `## Technical Scope` but `input/architecture.md` is available, derive the component map from the architecture document.

### Step 2 - Write Implementation Objective

Summarize what this epic delivers and why. Reference the business value from `epic.md` and the original BRS.

### Step 3 - Write Scope

**In Scope:** list every concrete deliverable from the stories.
**Out of Scope:** list everything that is NOT in the stories but a developer might assume is included. Be specific.
**Constraints:** extract architecture rules, NFR targets, and security constraints that apply to this epic.

### Step 4 - Inline the Data Model

Copy the ER diagram and field definitions from `implementation-contract.md` into Section 3. Include:
- Every entity with all fields, types, required flag, and validation rules
- State machines if the entity has lifecycle states
- Field constraints from the BRS

Do NOT summarize - include the full model.

### Step 5 - Inline the API Specification

Copy the OpenAPI spec from `implementation-contract.md` into Section 4. Include:
- Every endpoint with full request/response schemas
- All error responses (400, 403, 404, 422, 500)
- Required vs optional fields

Do NOT summarize - include the full spec.

### Step 5b - Inline UI Specification (when applicable)

If `implementation-contract.md` has a `## UI Surface` section, copy it into Section 5 of the handoff. Include:
- Every page with route, layout, and component arrangement
- Specification status and blocking dependencies for each page
- Form fields with types, validation rules, and defaults
- Data binding to API endpoints with Contract Mode
- States: loading, error, success behaviors
- User flows: step-by-step navigation

Pages with specification status `partial` or `blocked` must be clearly marked in the handoff. The coding agent must not treat these pages as ready to implement - they require resolution of their blocking dependencies first. Include the blocking open questions so the coding agent knows what is unresolved.
Do not originate new UI facts here - this section must remain an inline delivery copy of scoped upstream truth.

If the epic has no frontend pages, omit Section 5 entirely.

### Step 6 - Inline Events and Business Rules

Copy events table and business rules table from `implementation-contract.md`. Include event payload schemas.

### Step 7 - Determine Story Execution Order

Read all stories and their dependencies. Produce an execution order:
- foundation stories first
- then stories that depend on the foundation
- integration stories after core logic
- UI stories that consume the API last

### Step 8 - Inline ALL Acceptance Criteria

For EACH story, in execution order:
- Write the story type
- Write implemented requirements and referenced requirements
- Write the user story statement
- Write in-scope and out-of-scope summary
- Write implementation guidance (entity, API, events, rules - referencing the sections above)
- Inline dependency contracts from the paired `.agent.yaml` when present
- Copy EVERY acceptance criterion with its full Gherkin scenario
- Include test type, criticality, and automation tags
- Do NOT skip any scenario - the coding agent will implement exactly what is specified

### Step 9 - Write Test Requirements

For each test type (unit, integration, API contract, E2E):
- List specific tests to write
- Trace each test to a specific AC
- Include criticality level
- When a story agent contract exists, copy its required tests into a story-specific test obligations table

### Step 10 - Document Risks and Open Questions

Copy unresolved risks and open questions from stories and the implementation contract. For each, state what breaks if unresolved.

### Step 11 - Write Definition of Done

Include the standard checklist from the template. Add epic-specific items if needed.

## Output requirements

Write `{item_folder}coding-handoff.md` using `.b2s/artifact-templates/epic-coding-handoff.md`.

The output must be a complete, standalone coding package. A coding agent reading only this file should know:
- what to build
- how it should behave
- what NOT to build
- what order to build it
- how to verify it works
- what constraints apply

## Done criteria

- [ ] Every selected epic has `coding-handoff.md`
- [ ] Data model is inline with full field definitions
- [ ] API spec is inline with full OpenAPI
- [ ] ALL acceptance criteria from ALL stories are present
- [ ] Story execution order is specified with rationale
- [ ] Test requirements are traceable to specific AC
- [ ] Risks and open questions are explicit
- [ ] No placeholder text remains
- [ ] No references to external files - everything is inline
- [ ] If solution decisions or technical scope exist, Section 0 (Component and Repository Map) is present
- [ ] If stories have Technical Scope, each story section in the handoff includes the concrete work per component
- [ ] If story agent contracts exist, each story section includes their scope boundaries and dependency contracts

## Stop conditions

- If `implementation-contract.md` does not exist for a selected epic, skip that epic and report it
- If no story files exist for a selected epic, skip that epic and report it

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- Validation and state updates are handled by the `.b2s` engine
