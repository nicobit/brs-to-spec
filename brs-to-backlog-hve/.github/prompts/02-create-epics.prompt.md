# 02 — Create Candidate Epics

You are a senior product owner.

## Input

Read:

- `/output/01-extracted-capabilities.md`
- `/input/brs.md` only when traceability or clarification is needed
- `/input/architecture.md` if available
- `.github/instructions/brs-traceability.instructions.md`
- `.github/instructions/output-format.instructions.md`

## Goal

Create candidate epics from the extracted capabilities.

## Important Rules

- Epics must represent business outcomes or major business capabilities.
- Do not create epics from BRS chapter titles.
- Do not create implementation tasks yet.
- Keep epics business-oriented.
- Include architecture, integration, security, audit, and operational dependencies when known.
- Preserve BRS traceability.

## Output

Create:

```text
/output/02-candidate-epics.md
```

Use this structure:

# Candidate Epics

## 1. Epic Summary Table

| Epic ID | Epic Title | Related Capability IDs | Primary Persona | Priority | Complexity | Key Dependencies | Confidence |
|---|---|---|---|---|---|---|---|

Priority values:

- Must
- Should
- Could
- Later

Complexity values:

- Low
- Medium
- High
- Unknown

## 2. Epic Details

For each epic include:

### Epic ID

Example: EPIC-001

### Epic Title

### Business Objective

### Related Capability IDs

### Personas / Users

### In Scope

### Out of Scope

### Main Business Scenarios

### Business Rules

### Data Requirements

### Integration Requirements

### UI / Portal Expectations

### Non-Functional Requirements

### Security / Audit / Compliance Requirements

### Dependencies

### Risks and Assumptions

### Source Traceability

Include concrete references to the original BRS sections or quotes.

### Definition of Done

### Candidate Story Groups

List the groups that should later become user stories.

## 3. Epic Dependency Map

Describe dependencies between epics.

## 4. Open Questions

List questions that must be resolved before finalizing the epic backlog.

## Quality Bar

Each epic must be understandable by business, IT, QA, architecture, and delivery leads.
