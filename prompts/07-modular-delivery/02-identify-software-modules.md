# Prompt — Identify Software Modules

## Purpose

Decompose a large BRS-driven initiative into isolated software modules.

This is not a replacement for business capabilities. It maps business capabilities to technical delivery boundaries.

## Output file

```text
modules/software-modules.md
```

## Output structure

```markdown
# Software Modules

## 1. Module Overview
| Module ID | Module Name | Type | Responsibility | Owner | Related capabilities |
|---|---|---|---|---|---|

## 2. Module Details

### MOD-001 — <Module Name>
#### Responsibility
#### In Scope
#### Out of Scope
#### Owned Data
#### Exposed APIs / Interfaces
#### Consumed APIs / Interfaces
#### Events Produced
#### Events Consumed
#### Dependencies
#### Risks / Open Questions

## 3. Module Dependency Map
## 4. Module Isolation Risks
```

## Rules

- Create modules with clear boundaries.
- Avoid generic layers unless they represent a meaningful delivery boundary.
- Do not call every module a bounded context.
- Keep modules small enough for downstream AI coding agents.
- Avoid creating too many tiny modules.
