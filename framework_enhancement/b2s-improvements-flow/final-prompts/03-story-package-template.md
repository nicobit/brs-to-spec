# Prompt 3 — Story Package Template

## Context

You are working on the `.b2s` framework at the root of this repository.

The artifact template `.b2s/artifact-templates/story-package.md` already exists and defines a 12-section content contract for a story package. It was created as the canonical atomic unit of implementation for AI-assisted delivery.

The skill `.b2s/skills/engineering-lead/create-openspec-handoff.md` already references this template and instructs the agent to populate all 12 sections with specific content derived from inputs.

Your task is to verify the template is complete and extend the `create-delivery-structure` skill so that the story entries it produces contain enough information to drive story package generation downstream.

## What to verify

### 1. Verify story-package.md is complete

Read `.b2s/artifact-templates/story-package.md`.

Confirm it contains all 12 sections:
1. User Story (actor, capability, outcome, business goal, scope in/out)
2. Source Traceability (BRS, FR-NNN, BR-NNN, AR-NNN)
3. Business Rules Applied
4. Acceptance Criteria (Given/When/Then, linked to FR-NNN and SCN-NNN)
5. BDD Scenarios (valid Gherkin, happy path + negative minimum)
6. Implementation Context (components, data, API, UI, integration)
7. Constraints (architecture rules, security, compliance)
8. Dependencies
9. Implementation Tasks (concrete, with area and validation)
10. Test Expectations
11. Definition of Done
12. Coding-Agent Prompt (self-contained)

If any section is missing or contains only placeholder labels with no guidance, add the missing content. Do not remove or restructure existing sections.

### 2. Extend the delivery-structure skill

Read `.b2s/skills/delivery-lead/create-delivery-structure.md`.

The current skill produces story rows in a table inside `delivery-structure.md`. The rows contain: story ID, user story sentence, AC reference, priority, increment.

Add a new step after Step 5 in the skill instructions:

**Step 5b — Enrich story entries for downstream generation**

For each story row, after the main table, add a collapsible or inline block that records:
- linked FR-NNN references (from `requirements.md`)
- linked BR-NNN references (from `business-rules.md` if present)
- the actor name (from `actors-and-personas.md` if present)
- the primary impacted component (derived from architecture review)
- one sentence of scope — what is explicitly out of scope for this story

This enrichment is used by `create-openspec-handoff` to generate deep story packages without having to re-derive the links from scratch.

Also update the done criteria to include:
- [ ] Every story row has FR-NNN links
- [ ] Every story row has an explicit out-of-scope statement

### 3. Update the artifact template for delivery-structure

Read `.b2s/artifact-templates/delivery-structure.md`.

After the story table inside each feature section, add a story detail block:

```markdown
#### F-XXX.X — Story Detail

| Field | Value |
|---|---|
| Actor | {{actor name}} |
| Linked requirements | FR-NNN, FR-NNN |
| Linked business rules | BR-NNN, BR-NNN |
| Primary component | {{component name}} |
| Out of scope | {{one sentence}} |
```

This block is optional in Compact mode, required in Standard and Full Governance mode.

## What not to change

- Do not change the stage-actions.yaml entries for `create-delivery-structure` or `create-openspec-handoff`.
- Do not change the folder structure of `specs/`.
- Do not add new workflow actions.
- Do not touch any initiative workspace files.

## Done criteria

- [ ] `.b2s/artifact-templates/story-package.md` has all 12 sections with concrete guidance
- [ ] `.b2s/skills/delivery-lead/create-delivery-structure.md` has Step 5b
- [ ] `.b2s/artifact-templates/delivery-structure.md` has the story detail block
- [ ] No existing content was removed or structurally changed
