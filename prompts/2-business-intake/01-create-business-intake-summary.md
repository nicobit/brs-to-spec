# Prompt — Create Business Intake Summary

## Purpose

Create one PO-reviewable business intake output from the normalized BRS.

## Inputs

Use:
- `input/brs.md`
- `input/input-package.md`
- `input/initial-architecture.md` only for context, not technical design.

## Output file

```text
business-intake/business-intake-summary.md
```

## Output structure

```markdown
# Business Intake Summary

## 1. Executive Summary

## 2. Business Objectives

| Objective ID | Objective | Business value | Stakeholder | Notes |
|---|---|---|---|---|

## 3. Scope

### In Scope

### Out of Scope

## 4. High-Level Requirements

| Requirement ID | Requirement | Type | Priority if known | Source / evidence | Clarification needed |
|---|---|---|---|---|---|

## 5. Business Capabilities

| Capability ID | Capability | Description | Related requirements | Business value |
|---|---|---|---|---|

## 6. Gaps and Questions

| ID | Type | Question / gap | Owner | Blocks delivery? | Notes |
|---|---|---|---|---|---|

## 7. Risks and Assumptions

## 8. Initial Delivery Considerations

## 9. PO Review Checklist
```

## Rules

- Use business language.
- Do not create technical design.
- Do not create implementation tasks.
- Do not invent requirements.
- Mark missing information explicitly.
- Keep the output suitable for PO review.
