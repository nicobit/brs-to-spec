# Prompt — Create Requirements Catalog

## Purpose

Create or update `business-analysis/requirements.md` based on:

- `business-intake/business-intake-summary.md`
- `input/brs.md` or `input/brs/*.md`

This prompt is based on the AI Unified Process `/requirements` prompt and adapted for initiative-local artifact production.

## Instructions

Create or update the requirements catalog at `business-analysis/requirements.md`.

The document must contain three separate Markdown tables:

- Functional requirements
- Non-functional requirements
- Constraints

## DO NOT

- Mix requirement types in a single table
- Skip the user-story format for functional requirements
- Use duplicate IDs across requirement types
- Leave the Status column empty
- Invent requirements not supported by `business-intake/business-intake-summary.md` or source BRS files
- Collapse multiple atomic requirements into one row

## Inputs

Required:

- `business-intake/business-intake-summary.md`
- `input/brs.md` or `input/brs/*.md`

Optional:

- `routing/routing-decision.md`
- architecture notes only when they are already present as upstream context, not as a source of new business requirements

## Requirement Types

### Functional Requirements (FR)

Define what the system should do.

Always use the user story format:

`As a [role], I want [goal] so that [benefit].`

Suggested table:

| ID | Title | User Story | Priority | Status | Source |
|---|---|---|---|---|---|
| FR-001 |  |  | High / Medium / Low | Open | |

### Non-Functional Requirements (NFR)

Define measurable quality attributes.

Suggested table:

| ID | Title | Requirement | Category | Priority | Status | Source |
|---|---|---|---|---|---|---|
| NFR-001 |  |  | Performance / Security / Availability / Scalability / Usability / Compliance | High / Medium / Low | Open | |

### Constraints (C)

Define limitations and boundaries imposed on the solution.

Suggested table:

| ID | Title | Constraint | Category | Priority | Status | Source |
|---|---|---|---|---|---|---|
| C-001 |  |  | Technical / Regulatory / Business / Schedule / Platform / Integration | High / Medium / Low | Open | |

## Quality checks

Every requirement must pass these checks before finalizing:

| Check | Rule |
|---|---|
| Measurable | NFRs must contain a number, threshold, or objectively testable condition |
| Singular | One requirement per row |
| Unambiguous | No subjective wording such as "user-friendly", "appropriate", or "fast" without a measure |
| Testable | A pass/fail test should be possible |
| Traceable | Every row must reference a source section or artifact |
| Unique IDs | No duplicate IDs across all tables |

## Workflow

1. Read `business-intake/business-intake-summary.md` fully.
2. Read the BRS source files fully.
3. Build a complete inventory of functional requirements, non-functional requirements, and constraints.
4. Normalize each atomic requirement into exactly one row.
5. Write the three requirement tables.
6. Validate that every row has Status and Source populated.
7. Verify that no requirement type has been merged into another table.

## Output expectations

The result should become the canonical business-analysis catalog for later use by:

- `entity-model.md`
- `use-cases.puml`
- `use-cases/UC-*.md`
- `business-rules.md`
- planning and traceability artifacts

## Error handling

- If the business-intake summary is missing, stop and report the blocker.
- If the BRS and intake summary conflict, preserve the conflict as a note and raise it for resolution rather than silently merging.
- If stakeholder roles are unclear, use the best-supported role wording from source material and note ambiguity.
