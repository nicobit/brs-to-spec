# Prompt — Identify Software Modules

## Purpose

Decompose a large initiative into isolated software modules.

## Inputs

Use:
- `business-intake/business-intake-summary.md`
- `planning/delivery-structure.md`
- `architecture/initial-architecture-review.md`
- `architecture/global-architecture-rules.md`

## Output file

```text
modules/software-modules.md
```

## Output structure

```markdown
# Software Modules

## 1. Module Overview

| Module ID | Module Name | Type | Responsibility | Owner | Related capabilities | Architecture constraint |
|---|---|---|---|---|---|---|

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
#### Architecture Constraints Applied
#### Risks / Open Questions

## 3. Module Dependency Map

## 4. Module Isolation Risks
```

## Rules

- Respect the initial architecture review.
- Respect global architecture rules.
- Avoid generic layers unless they represent meaningful delivery boundaries.
- Do not call every module a bounded context.
- If a needed module conflicts with architecture, mark it as an open architecture decision.
