# Prompt — Define Delivery Increments

## Purpose

Group capabilities and module work into vertical, testable delivery increments.

Each increment should represent a coherent deliverable that can be validated and demonstrated.

This prompt creates a roadmap of deliverables such as D1, D2, D3.

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

#### Scope
##### In Scope
##### Out of Scope

#### Acceptance Criteria
Use Given/When/Then where possible.

#### Automated Validation Criteria
List the automated tests, checks, or validations expected for this deliverable.

#### Dependencies
#### Risks / Open Questions

#### OpenSpec Change Recommendation
```text
openspec/changes/D1-<deliverable-name>/
  proposal.md
  design.md
  tasks.md
```
```

## Rules

- Create vertical deliverables, not theoretical product epics.
- Each deliverable should be testable and demonstrable.
- Each deliverable should ideally fit into 2-3 weeks of engineering work, but this is a guideline, not a hard mathematical rule.
- Do not generate implementation tasks for all deliverables.
- Only the active deliverable should be converted into an OpenSpec change.
- Include automated validation criteria for every deliverable.
- Preserve traceability to requirements, capabilities, and modules.
