# Prompt — Define Delivery Increments

## Purpose

Group capabilities and module work into vertical, testable delivery increments.

## Inputs

Use:
- `business-intake/business-intake-summary.md`
- `architecture/initial-architecture-review.md`
- `architecture/global-architecture-rules.md`
- `modules/software-modules.md`
- `planning/capability-module-map.md`

## Output file

```text
planning/delivery-increments.md
```

## Output structure

```markdown
# Delivery Increments

## 1. Increment Overview

| Deliverable ID | Name | Goal | Business value | Estimated size | Modules involved | Status |
|---|---|---|---|---|---|---|

## 2. Deliverables

### D1 — <Deliverable Name>

#### Goal
#### Business Value
#### Included Capabilities
#### Included Requirements
#### Modules Involved

| Module | Work needed in this deliverable |
|---|---|

#### Architecture Constraints Applied

| Constraint | Source | Impact |
|---|---|---|

#### Scope

##### In Scope
##### Out of Scope

#### Acceptance Criteria

Use Given/When/Then where possible.

#### Automated Validation Criteria

#### Dependencies

#### Risks / Open Questions

#### OpenSpec Change Recommendation
```

## Rules

- Create vertical deliverables, not theoretical epics.
- Each deliverable should be testable and demonstrable.
- Include architecture constraints applied to each deliverable.
- Do not generate implementation tasks for all deliverables.
- Only the active deliverable should be converted into an OpenSpec change.
