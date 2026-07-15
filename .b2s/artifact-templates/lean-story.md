# S-NNN.N — {{Story Title}}

## Metadata

| Field | Value |
|---|---|
| Story ID | S-NNN.N |
| Story Type | {{frontend-form / frontend-page / backend-endpoint / event-consumer / schema-migration / generic}} |
| Epic | E-NNN — {{Epic Title}} |
| Actor | {{specific role name — NOT "user", "person", or "someone"}} |
| Layers | {{one or more of: frontend, backend, infrastructure, integration}} |
| Priority | Must / Should / Could |
| Increment | D1 / D2 |
| Status | Draft |

## User Story

As a {{named actor}}, I want {{capability}}, so that {{business outcome}}.

## Business Context

{{Minimum 2 full sentences explaining WHY this story matters and what business value it delivers. One sentence will fail validation.}}

## Linked Requirements

| ID | Requirement | Basis |
|---|---|---|
| FR-NNN | {{canonical requirement title from atomic-requirements.md}} | direct / inferred |

## Requirements Implemented

- {{requirement IDs this story directly implements}}

## Requirements Referenced

- {{requirement IDs this story mentions or depends on but does not own}}

## In Scope

- {{concrete behavior this story must implement}}

## Implementation Guidance

- **Entity:** {{entity name from ../implementation-contract.md}}
- **API:** {{endpoint from ../implementation-contract.md}}
- **Status:** {{initial status on creation, if applicable}}
- **Events:** {{events emitted by this story, if any}}
- **Rules:** {{business rules that apply, if any}}

## Dependency Contracts

| Dependency | Type | Contract Consumed | Why It Matters |
|---|---|---|---|
| {{S-NNN.N or external system}} | Story / External / Epic | {{201 response / event schema / table contract / UI contract}} | {{what this story needs from it}} |

## UI Behaviour

*Include ONLY when Layers includes "frontend" AND the implementation contract has a `## UI Surface` section. Omit this section entirely otherwise.*

- **Page:** {{page name and route}}
- **Components affected:** {{form / table / card / modal}}
- **Fields:** {{form fields with validation rules}}
- **States:** loading → {{display}} | error → {{display}} | success → {{display}}
- **Flow:** {{user action → system response → navigation}}

## Acceptance Criteria

### AC-001 — {{criterion title}} `[unit]` `[critical]` `[automate]`

```gherkin
Scenario: {{meaningful scenario name}}
  Given {{precondition with concrete values}}
  When {{action with specific input}}
  Then {{observable outcome with specific expected value}}
```

### AC-002 — {{criterion title}} `[integration]` `[important]` `[automate]`

```gherkin
Scenario: {{meaningful scenario name}}
  Given {{precondition}}
  When {{action}}
  Then {{observable outcome}}
```

### AC-003 — {{criterion title}} `[api]` `[critical]` `[automate]`

```gherkin
Scenario: {{meaningful scenario name}}
  Given {{precondition}}
  When {{action}}
  Then {{observable outcome}}
```

### AC-004 — {{criterion title}} `[e2e]` `[standard]` `[automate-later]`

```gherkin
Scenario: {{meaningful scenario name}}
  Given {{precondition}}
  When {{action}}
  Then {{observable outcome}}
```

## Test Expectations

| Test Type | What to Test | Why | Automation |
|---|---|---|---|
| Unit | {{specific function/logic}} | {{business rule or validation}} | Must automate |
| Integration | {{external system interaction}} | {{adapter, API call, DB query}} | Must automate |
| API | {{endpoint contract}} | {{request/response schema, errors}} | Must automate |
| E2E | {{user flow}} | {{end-to-end business scenario}} | Automate / Manual |

## Required Tests

- Unit: {{specific validator, helper, or domain rule}}
- Integration / API: {{specific contract or side effect}}
- E2E: {{specific user or system flow}}
- Accessibility: {{specific behavior when relevant, otherwise "Not applicable"}}

## Out of Scope

- {{what a developer might assume is included but is not}}

## Dependencies

| Dependency | Type | Blocking? |
|---|---|---|
| {{dependency}} | Story / External / Epic | Yes / No |

## Open Questions

| ID | Question | Impact |
|---|---|---|
| OQ-NNN | {{question}} | {{what's blocked until resolved}} |
