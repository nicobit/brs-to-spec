# Prompt 6 — BDD Rules and Story-Level BDD Generation

## Context

You are working on the `.b2s` framework at the root of this repository.

Currently BDD scenarios are gated behind the `BDD` trigger in `quality_gates_triggered`. If the readiness check does not trigger BDD, no BDD is produced at all. The external review identified this as a problem: BDD should be a default output for business-facing stories, not an optional gate.

The `create-openspec-handoff` skill already requires at least two BDD scenarios per story inside `story.md`. But the standalone `create-bdd-scenarios` skill still only runs when gated. The two behaviors are inconsistent.

Your task is to make BDD generation consistent and quality-controlled across the framework.

## Step 1 — Update create-bdd-scenarios skill

Read `.b2s/skills/qa-analyst/create-bdd-scenarios.md`.

The current skill only runs when BDD is triggered by the readiness check. Update it as follows:

**Remove** the precondition that says "stop if the gate was not triggered".

**Replace** it with two modes:

**Mode A — Gate-triggered (existing behavior):**
When `BDD` is in `quality_gates_triggered`, generate a standalone BDD file per feature under `quality-gates/bdd/F-NNN.md`. These are comprehensive, fully traceable, multi-scenario files for regulated or governance-heavy initiatives.

**Mode B — Story-embedded (new behavior):**
When `BDD` is not triggered, still generate the minimum BDD required for each story and embed it in the story package. This mode produces no standalone `quality-gates/bdd/` files — the BDD lives inside `specs/F-XXX.X-<slug>/story.md` Section 5.

The skill is called by `create-openspec-handoff`. It does not need to be invoked as a separate workflow action for Mode B — the openspec handoff skill already handles Mode B internally. This note is to clarify that Mode B is not a gap; it is intentional.

**Update the preconditions** to:
- If BDD gate is triggered: proceed with Mode A (standalone files)
- If BDD gate is not triggered: document this clearly in the skill and instruct the agent that story-level BDD is handled by `create-openspec-handoff`

**Update the scenario quality rules** in the skill:

Add a section called "Scenario Quality Rules" with the following:

```
Each scenario MUST:
- be written in valid Given/When/Then Gherkin
- describe observable business behaviour, not implementation steps
- have a meaningful name that identifies the business situation
- link to the AC-NNN it validates
- link to the story ID (F-XXX.X) it belongs to

Each scenario MUST NOT:
- describe developer activity ("Given the developer writes code")
- have a vague Then clause ("Then the feature works", "Then it succeeds")
- duplicate the user story sentence verbatim as the scenario name

Required scenario types per story (include all that apply):
- happy path (always required)
- negative / validation (always required)
- authorization / permission (required when roles or access control exist)
- business rule enforcement (required when BR-NNN applies)
- state transition (required when workflow states exist)
- integration failure (required when external system call exists)
- audit / compliance (required when audit log or regulatory requirement exists)
- edge case (required when the BRS or architecture review calls one out)
```

Add a "Bad vs Good" example block at the end of the skill:

**Bad:**
```gherkin
Scenario: Submit application
  Given the user is logged in
  When they click submit
  Then the application is submitted
```

**Good:**
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

## Step 2 — Update the openspec-handoff skill BDD instruction

Read `.b2s/skills/engineering-lead/create-openspec-handoff.md`.

In the `story.md` Section 5 instruction, add the following rules:

```
BDD scenario quality rules (apply to every scenario written):
- valid Given/When/Then only
- observable business behaviour only — no implementation details
- meaningful scenario name — not a copy of the story title
- link each scenario to the AC-NNN it validates
- link each scenario to the story ID

Required scenario coverage per story:
- happy path: always
- validation/negative: always
- authorization: when the story involves roles or permissions
- business rule: when BR-NNN constrains the behaviour
- state transition: when a workflow state changes
- integration failure: when an external system is called
- audit/compliance: when an audit event must be recorded

Do not write generic scenarios. If the initiative has no relevant actor permissions,
state transition, or integration call for a given story, omit those types and note why.
```

## Step 3 — Update the bdd-scenarios artifact template

Read `.b2s/artifact-templates/bdd-scenarios.md`.

Add a "Scenario Quality Checklist" section at the end:

```markdown
## Scenario Quality Checklist

Before marking this file complete, verify each scenario:

- [ ] Written in valid Given/When/Then Gherkin
- [ ] Scenario name describes the business situation, not the implementation
- [ ] Then clause is observable and specific (not "it works" or "it succeeds")
- [ ] Linked to AC-NNN
- [ ] Linked to story ID (F-XXX.X)
- [ ] Happy path covered per story
- [ ] Negative/validation path covered per story
- [ ] Authorization scenario present where roles exist
- [ ] State transition scenario present where workflow states exist
- [ ] Integration failure scenario present where external calls exist
- [ ] Audit scenario present where compliance is required
```

## What not to change

- Do not change the `create-bdd-scenarios` action entry in `stage-actions.yaml`.
- Do not change the condition `BDD in quality_gates_triggered` — that controls the standalone gate-triggered mode and must remain.
- Do not add a new workflow action for story-level BDD.
- Do not modify any initiative workspace files.

## Done criteria

- [ ] `.b2s/skills/qa-analyst/create-bdd-scenarios.md` has Mode A / Mode B clarification
- [ ] `.b2s/skills/qa-analyst/create-bdd-scenarios.md` has the Scenario Quality Rules section
- [ ] `.b2s/skills/qa-analyst/create-bdd-scenarios.md` has the Bad vs Good example
- [ ] `.b2s/skills/engineering-lead/create-openspec-handoff.md` has the BDD quality rules block in Section 5
- [ ] `.b2s/artifact-templates/bdd-scenarios.md` has the Scenario Quality Checklist
- [ ] All existing tests still pass: `python -m pytest .b2s/tests/ -q`
