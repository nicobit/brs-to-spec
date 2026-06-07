# Prompt — Create Global Architecture Rules

## Purpose

Create global architecture rules that every module and deliverable must respect.

## Inputs

Use:
- `input/initial-architecture.md`
- `architecture/initial-architecture-review.md`
- `business-intake/business-intake-summary.md`
- `planning/delivery-structure.md`

## Output file

```text
architecture/global-architecture-rules.md
```

## Output structure

```markdown
# Global Architecture Rules

## 1. System Context
## 2. Architectural Principles
## 3. Technology Stack
## 4. Module Boundary Rules
## 5. API Rules
## 6. Data Ownership Rules
## 7. Authentication and Authorization Rules
## 8. Audit and Compliance Rules
## 9. Error Handling Rules
## 10. Observability Rules
## 11. Security Rules
## 12. Performance and Resilience Rules
## 13. Deployment and Environment Rules
## 14. Decisions and Open Questions
```

## Rules

- Derive rules from the initial architecture review when available.
- Do not invent architecture that conflicts with `input/initial-architecture.md`.
- Keep this document stable.
- Mark unresolved decisions clearly.
