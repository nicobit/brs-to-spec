# Prompt — Create Business Intake Summary

## Purpose

Create a single PO-reviewable business intake output from a raw BRS.

This prompt simplifies the first layer of the framework. Use it when the Product Owner should review one consolidated artifact instead of many intermediate files.

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
| ID | Type | Description | Impact | Owner |
|---|---|---|---|---|

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
