# {{Feature ID}} — {{Feature Title}}

## Metadata

| Field | Value |
|---|---|
| Feature ID | {{feature_id}} |
| Parent Epic | {{epic_id}} — {{epic_name}} |
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by | delivery-lead |
| Status | Draft |

## Feature Goal

{{2–3 sentences: what coherent business capability does this feature deliver? How does it relate to its parent epic?}}

## Business Value

{{Why does this feature matter to the business? What is the cost of not having it? Who benefits and how?}}

## Scope

**In scope:**
- {{item explicitly included}}

**Out of scope:**
- {{item explicitly excluded to prevent scope creep}}

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| BRS | BRS-§N | {{section or clause}} |
| Requirement | FR-NNN | {{requirement description}} |
| Business Rule | BR-NNN | {{rule description}} |

## Business Rules

| Rule ID | Rule | Impact on Feature |
|---|---|---|
| BR-NNN | {{rule statement}} | {{how the rule constrains or shapes this feature}} |

## Impacted Components

| Component | Type | Expected Change |
|---|---|---|
| {{component name from architecture review}} | API / UI / Service / Database / Event / Integration | {{what changes and why}} |

## Stories

| Story ID | Story Title | Priority | Increment | Status |
|---|---|---|---|---|
| F-NNN.N | {{story title}} | Must / Should / Could | D1 / D2 | Draft |

## Acceptance Criteria Summary

{{High-level statement of what "done" looks like for this feature as a whole. What must be true for the feature to be considered complete?}}

## BDD Coverage Expectations

{{Which scenario types are expected per story. Example:
- F-NNN.1: happy path, negative/validation, authorization
- F-NNN.2: happy path, state transition, integration failure, audit}}

## Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| {{dependency}} | Feature / Story / External | Yes / No | {{when and why}} |

## Implementation Notes

{{Key technical or architectural decisions the implementing team must know before starting. Reference specific architecture rules (AR-NNN) or constraints that apply.}}

## Test Strategy Summary

{{What test types are required (unit, integration, API, UI, BDD, performance), what the coverage target is, and who owns sign-off.}}

---
*Status: Draft — set to Accepted only after human review.*
