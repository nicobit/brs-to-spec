# Prompt — Create Delivery Structure

## Purpose

Create a delivery structure that preserves the business view and prepares for modular delivery when needed.

## Inputs

Use:
- `input/brs.md`
- `input/initial-architecture.md` if available
- `business-intake/business-intake-summary.md`

## Output file

```text
planning/delivery-structure.md
```

## Output structure

```markdown
# Delivery Structure

## 1. Delivery Mode Assumption

## 2. Business Capabilities

| Capability ID | Capability | Business value | Related requirements | Priority | Notes |
|---|---|---|---|---|---|

## 3. Candidate Software Modules

| Module ID | Module name | Responsibility | Module type | Related capabilities | Architecture source/constraint |
|---|---|---|---|---|---|

## 4. Capability-to-Module Map

## 5. Candidate Delivery Slices

## 6. Items Requiring Architecture Alignment

## 7. Recommendation
```

## Rules

- Do not jump directly from BRS to detailed user stories.
- Preserve the business capability view.
- Use software modules as a bridge to engineering execution.
- Do not contradict the initial architecture document.
- If a candidate module conflicts with the initial architecture, mark it as an architecture decision.
