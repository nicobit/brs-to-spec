# Prompt — Map Capabilities to Modules

## Purpose

Create traceability from business capabilities and requirements to software modules.

## Output file

```text
planning/capability-module-map.md
```

## Output structure

```markdown
# Capability to Module Map

| Requirement ID | Capability | Primary module | Supporting modules | Notes |
|---|---|---|---|---|

## Cross-Module Concerns
| Concern | Modules impacted | Required rule / decision |
|---|---|---|

## Traceability Risks
| Risk | Impact | Mitigation |
|---|---|---|
```

## Rules

- Do not lose business traceability.
- Every module must map to business value, architecture need, or platform need.
- Every high-priority requirement must map to at least one module.
