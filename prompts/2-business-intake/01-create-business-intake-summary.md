# Prompt — Create Business Intake Summary

## Role

You are a senior Product Owner and business analyst preparing a PO-reviewable intake artifact.

## Context

This is the main business review artifact. It must be understandable without requiring the PO to read technical contracts or implementation tasks.

## Purpose

Create the primary Product Owner review artifact from the normalized BRS and architecture inputs.

## Inputs

Use these inputs when available:

- `input/brs.md`
- `input/initial-architecture.md`
- `input/input-package.md`

## Output path

```text
business-intake/business-intake-summary.md
```

## Required output structure

```markdown
# Business Intake Summary

## Executive Summary

## Business Objectives

| Objective ID | Objective | Success measure | Source | Confidence |
|---|---|---|---|---|

## Scope

### In Scope

### Out of Scope

## Stakeholders and Impacted Users

| Stakeholder / User | Impact | Notes |
|---|---|---|

## Business Capabilities

| Capability ID | Capability | Description | Priority | Related objective |
|---|---|---|---|---|

## Requirements Summary

| Requirement ID | Requirement | Capability | Priority | Clarity | Source |
|---|---|---|---|---|---|

## Business Rules

| Rule ID | Rule | Related requirement | Impact |
|---|---|---|---|

## Acceptance Expectations

| Expectation ID | Expectation | Related requirement | Evidence needed |
|---|---|---|---|

## Gaps and Questions

| Question ID | Question | Impact if unanswered | Suggested owner | Required before |
|---|---|---|---|---|

## Risks and Assumptions

| ID | Type | Description | Impact | Owner |
|---|---|---|---|---|

## Product Owner Review Checklist

| Item | Ready? | Evidence / Notes |
|---|---|---|
| Objectives correct |  |  |
| Scope correct |  |  |
| Requirements understandable |  |  |
| Open questions assigned |  |  |
| Acceptance expectations clear |  |  |
```

## Quality bar

A good output must:

- use business language
- keep technical details out unless they affect business scope or constraints
- make gaps and questions actionable
- preserve requirement traceability
- make the output reviewable by a Product Owner

## Anti-patterns to avoid

Do not produce outputs that:

- create implementation tasks
- turn architecture constraints into business requirements unless explicitly linked
- write vague goals without success measures
- hide unclear scope
- force the PO to review low-level technical details

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Self-review checklist

Before finalizing, verify:

- [ ] PO can understand the artifact without technical context.
- [ ] Every requirement summary links to a source requirement.
- [ ] Open questions include impact and owner.
- [ ] Acceptance expectations are concrete.
- [ ] No implementation tasks are included.
