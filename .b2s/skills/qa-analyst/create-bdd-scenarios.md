# Skill - Create BDD Scenarios

## Identity

```text
skill_id:    qa-analyst.create-bdd-scenarios
persona:     qa-analyst
action_id:   create-bdd-scenarios
produces:    quality-gates/bdd/F-NNN.md
```

## When this skill is used

This skill runs only when the readiness check explicitly triggers the BDD gate (`BDD` in `quality_gates_triggered`). It creates feature-level BDD files with full Gherkin under `quality-gates/bdd/`.

**This is Mode A — gate-triggered standalone BDD.**

Mode B (story-embedded BDD) is handled internally by `create-openspec-handoff`. When BDD is not gate-triggered, story-level BDD scenarios are still produced inside each `specs/F-XXX.X-<slug>/story.md` Section 5. No separate workflow action is needed for Mode B — it is intentional.

## Modes

### Mode A — Gate-triggered (this skill)

Condition: `BDD` is in `quality_gates_triggered`.

Produces: one file per feature under `quality-gates/bdd/F-NNN.md`.

These are comprehensive, fully traceable, multi-scenario files for regulated or governance-heavy initiatives. They exist as standalone gate artifacts and feed into the review package.

### Mode B — Story-embedded (handled by create-openspec-handoff)

Condition: `BDD` is NOT in `quality_gates_triggered`.

Produces: BDD scenarios inside `specs/F-XXX.X-<slug>/story.md` Section 5 only.

No standalone `quality-gates/bdd/` files are created. This is not a gap — it is the intended behavior for non-gated initiatives.

## Preconditions

Before starting, verify:
- `engineering-readiness/readiness-check.md` marks `BDD` as triggered (Mode A gate condition)
- `planning/delivery-structure.md` exists with story IDs
- BRS source files are readable
- `business-analysis/business-rules.md` exists
- `business-analysis/actors-and-personas.md` exists

If the BDD gate was not triggered, stop and report:
> BDD gate was not triggered for this initiative. Story-level BDD is handled by `create-openspec-handoff` (Mode B). No standalone BDD files are required.

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/planning/delivery-structure.md`
- `{workspace_root}/business-analysis/business-rules.md`
- `{workspace_root}/business-analysis/actors-and-personas.md`
- `{workspace_root}/engineering-readiness/readiness-check.md`
- BRS source files under `{workspace_root}/input/`

Do not start writing until all available inputs are read completely.

### Step 2 - Write scenarios

Assign globally sequential `SCN-NNN` IDs and create one file per feature under `{workspace_root}/quality-gates/bdd/`.

For each story, apply the Required Scenario Coverage rules below.

Every scenario must include full Gherkin and reference the specific `AC-NNN` it validates and the story ID (`F-XXX.X`) it belongs to.

## Scenario Quality Rules

Each scenario MUST:
- be written in valid Given/When/Then Gherkin
- describe observable business behaviour, not implementation steps
- have a meaningful name that identifies the business situation
- link to the AC-NNN it validates
- link to the story ID (F-XXX.X) it belongs to

Each scenario MUST NOT:
- describe developer activity (e.g. "Given the developer writes code")
- have a vague Then clause (e.g. "Then the feature works", "Then it succeeds")
- duplicate the user story sentence verbatim as the scenario name

Required scenario coverage per story (include all that apply):
- happy path (always required)
- negative / validation (always required)
- authorization / permission (required when roles or access control exist)
- business rule enforcement (required when BR-NNN applies)
- state transition (required when workflow states exist)
- integration failure (required when external system call exists)
- audit / compliance (required when audit log or regulatory requirement exists)
- edge case (required when the BRS or architecture review calls one out)

If a scenario type does not apply to a story, note why it was omitted rather than silently skipping it.

## Output requirements

Use `.b2s/artifact-templates/bdd-scenarios.md` as the shape contract for each feature file.

## Done criteria

- [ ] Every feature has a BDD file
- [ ] Every story has minimum scenario coverage (happy path + negative)
- [ ] `SCN-NNN` IDs are globally sequential
- [ ] Every scenario has full Gherkin
- [ ] Every scenario links to AC-NNN and story ID
- [ ] Omitted scenario types are documented with reason
- [ ] Status is `In progress`

## Bad vs Good Scenario Examples

### Bad — do not write scenarios like this

```gherkin
Scenario: Submit application
  Given the user is logged in
  When they click submit
  Then the application is submitted
```

Problems: actor is "user" (generic), action is UI interaction not business behaviour, Then clause is vague, no observable business outcome, no link to AC-NNN.

### Good — write scenarios like this

```gherkin
Scenario: Reject submission for ineligible customer
  Given an operations user has completed an application for customer C-001
  And customer C-001 is marked as ineligible in the AML screening system
  When the user submits the application
  Then the submission is rejected with status 422
  And the application remains in "Draft" state
  And the user sees the message "Customer is not eligible for this product"
  And no approval workflow is initiated
  And an audit event "APPLICATION_REJECTED_INELIGIBLE" is recorded
```

Why this is good: named actor (operations user), specific precondition (AML flag), observable business outcomes (status, state, message, audit event), no implementation details.
