# Prompt — Create Use Case Specification

## Purpose

Create or update one or more use case specification documents for specified `UC-NNN` IDs in:

- `business-analysis/use-cases/`

This prompt is based on the AI Unified Process `/use-case-spec` prompt and adapted for initiative-local artifact production.

## Instructions

Create or update use case specification documents for the requested use case IDs in `business-analysis/use-cases/`.

Each use case must be written as a separate document.

## DO NOT

- Write vague or incomplete scenarios
- Skip numbering steps in the Main Success Scenario
- Omit alternative flows for error conditions
- Leave postconditions undefined
- Mix multiple use cases in one document
- Use technical implementation details in the flow steps

## Inputs

Required:

- `business-analysis/requirements.md`
- `business-analysis/use-cases.puml`

Optional:

- `business-analysis/business-rules.md`
- `business-analysis/actors-and-personas.md`
- architecture feedback already captured as accepted upstream context

## Template

Each file should follow this structure:

```markdown
# Use Case: <name>

## Overview
**Use Case ID:** UC-001
**Use Case Name:** ...
**Primary Actor:** ...
**Goal:** ...
**Status:** Draft

## Preconditions

## Main Success Scenario
1. ...

## Alternative Flows
### A1: ...

## Postconditions
### Success Postconditions
### Failure Postconditions

## Business Rules
### BR-001: ...
```

## Workflow

1. Read `business-analysis/requirements.md`.
2. Read `business-analysis/use-cases.puml`.
3. Identify the specified use case.
4. Write the overview section with actor and goal.
5. Define preconditions.
6. Write the main success scenario as numbered steps.
7. Add alternative flows for error conditions, optional paths, and exceptional situations.
8. Define success and failure postconditions.
9. Reference applicable business rules when available.

## Quality rules

- One file per use case only.
- Main flow steps must be in business language.
- Each use case must represent a complete actor goal.
- Alternative flows should branch from real decision points, not arbitrary invented scenarios.
- Postconditions must describe observable business state, not implementation internals.

## Output expectations

These files are canonical behavioral specifications.

They should later support:

- delivery structure creation
- BDD scenario generation
- test strategy
- handoff story/design/tasks

## Error handling

- If the requested `UC-NNN` does not exist in `use-cases.puml`, stop and report it.
- If business rules are missing, continue and note the missing cross-reference rather than inventing rules.
- If actor names are not yet stabilized, use the best-supported role wording and flag later alignment.
