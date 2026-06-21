# Skill - Create BDD Scenarios

## Identity

```text
skill_id:    qa-analyst.create-bdd-scenarios
persona:     qa-analyst
action_id:   create-bdd-scenarios
produces:    quality/bdd/F-NNN.md (agile-delivery-flow) or quality-gates/bdd/F-NNN.md (enterprise-modular)
```

## When this skill is used

Run after the story quality gate is approved. Creates one BDD file per feature with full Gherkin scenarios.

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.

If a required input is missing, stop and report the blocker.

## Mandatory generation rule

Generate BDD scenarios for ALL stories in ALL feature files, regardless of their quality review status. If the story quality review flagged stories as failing, generate BDD scenarios for them anyway — the human approved the gate, which means "proceed despite gaps." Do not skip stories, do not produce empty output, do not second-guess the gate decision.

## Instructions

### Step 1 - Read all inputs

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
Do not start writing until all inputs are read completely.

### Step 2 - Identify features and stories

Read the feature story files from `planning/stories/` (or `planning/delivery-structure.md` if story files are not present). Each feature file contains one or more stories. Generate one BDD output file per feature.

If the input paths reference `business-analysis/requirements.md` instead, group FR-NNN requirements into feature clusters and generate one file per cluster.

### Step 3 - Write scenarios

Assign globally sequential `SCN-NNN` IDs. Write one file per feature to the output directory specified by `{primary_output}` (typically `quality/bdd/F-NNN.md` or `quality-gates/bdd/F-NNN.md`).

For each FR in the cluster, apply the Required Scenario Coverage rules below.

Every scenario must include full Gherkin and reference:
- the `FR-NNN` it validates
- the `BR-NNN` business rule it enforces (if applicable)
- the actor from `actors-and-personas.md` who performs the action

## Scenario Quality Rules

Each scenario MUST:
- be written in valid Given/When/Then Gherkin
- describe observable business behaviour, not implementation steps
- have a meaningful name that identifies the business situation
- link to the FR-NNN it validates
- link to the BR-NNN business rule it enforces (if applicable)
- name the actor performing the action (from actors-and-personas.md)

Each scenario MUST NOT:
- describe developer activity (e.g. "Given the developer writes code")
- have a vague Then clause (e.g. "Then the feature works", "Then it succeeds")
- duplicate the FR title verbatim as the scenario name

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

- [ ] Every FR-NNN is covered by at least one scenario
- [ ] FR-NNN rows are grouped into F-NNN feature cluster files
- [ ] One `F-NNN.md` file exists per feature cluster under `quality-gates/bdd/`
- [ ] Every story has minimum scenario coverage (happy path + negative)
- [ ] `SCN-NNN` IDs are globally sequential across all files
- [ ] Every scenario has full Gherkin with a concrete Then clause
- [ ] Every scenario links to FR-NNN (and BR-NNN where applicable)
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
