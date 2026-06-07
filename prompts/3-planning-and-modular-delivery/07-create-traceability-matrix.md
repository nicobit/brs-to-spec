# Prompt — Create Traceability Matrix

## Purpose

Create end-to-end traceability for enterprise delivery.

## Inputs

Use:
- `input/brs.md`
- `business-intake/business-intake-summary.md`
- `modules/software-modules.md` if available
- `planning/capability-module-map.md`
- `planning/delivery-increments.md`
- `architecture/global-architecture-rules.md`

## Output file

```text
planning/traceability-matrix.md
```

## Output structure

```markdown
# Traceability Matrix

| Requirement ID | Business Capability | Module(s) | Deliverable | OpenSpec Change | Validation |
|---|---|---|---|---|---|

## Unmapped Requirements

| Requirement ID | Requirement | Reason unmapped | Owner |
|---|---|---|---|

## Architecture Constraints Traceability

| Constraint ID | Constraint | Module(s) | Deliverable(s) | Validation |
|---|---|---|---|---|
```

## Rules

- Every high-priority requirement must be mapped.
- Every active deliverable must have validation.
- Architecture constraints must be traceable to modules/deliverables where applicable.
