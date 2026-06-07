# Prompt — Map Capabilities to Modules

## Purpose

Create traceability from requirements and business capabilities to software modules.

## Inputs

Use:
- `business-intake/business-intake-summary.md`
- `planning/delivery-structure.md`
- `modules/software-modules.md`
- `architecture/global-architecture-rules.md`

## Output file

```text
planning/capability-module-map.md
```

## Output structure

```markdown
# Capability to Module Map

| Requirement ID | Capability | Primary module | Supporting modules | Architecture constraints | Notes |
|---|---|---|---|---|---|

## Cross-Module Concerns

## Traceability Risks
```

## Rules

- Do not lose business traceability.
- Every high-priority requirement must map to at least one module.
- Every module must map to business value, architecture need, or platform need.
