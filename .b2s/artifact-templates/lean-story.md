# F-NNN.N — {{Story Title}}

## Metadata

| Field | Value |
|---|---|
| Story ID | F-NNN.N |
| Epic | E-NNN — {{Epic Title}} |
| Actor | {{specific role name, not "user"}} |
| Layers | Frontend / Backend / Infrastructure / Integration |
| Priority | Must / Should / Could |
| Increment | D1 / D2 |
| Status | Draft |

---

## User Story

As a {{actor}}, I want {{capability}}, so that {{outcome}}.

---

## Business Context

{{2-3 sentences on why this story matters and what business value it delivers.}}

---

## Linked Requirements

| ID | Requirement |
|---|---|
| FR-NNN | {{requirement title}} |

---

## Implementation Guidance

Reference epic context first, and the epic's implementation contract when it exists:

- **Entity:** {{entity name from epic context or ../implementation-contract.md}}
- **API:** {{endpoint from epic context or ../implementation-contract.md}}
- **Status:** {{initial status on creation, if applicable}}
- **Events:** {{events emitted by this story, if any}}
- **Rules:** {{business rules that apply, if any}}

---

## Acceptance Criteria

Generate as many acceptance criteria as needed to fully describe the behaviour. Each criterion includes a test type annotation and a Gherkin scenario. Cover all applicable types: happy path, negative/validation, authorization, state transition, integration failure, audit/compliance.

### AC-001 — {{criterion title}} `[unit]`

```gherkin
Scenario: {{meaningful scenario name}}
  Given {{precondition}}
  When {{action}}
  Then {{observable business outcome}}
```

### AC-002 — {{criterion title}} `[integration]`

```gherkin
Scenario: {{meaningful scenario name}}
  Given {{precondition}}
  When {{action}}
  Then {{observable business outcome}}
```

Test type annotations: `[unit]` for service logic, `[integration]` for external calls/adapters, `[api]` for HTTP endpoint contracts, `[e2e]` for user flows.

---

## Test Expectations

| Test Type | What to Test | Why |
|---|---|---|
| Unit | {{specific function/logic}} | {{business rule or validation}} |
| Integration | {{external system interaction}} | {{adapter, API call, DB query}} |
| API | {{endpoint contract}} | {{request/response schema, errors}} |
| E2E | {{user flow}} | {{end-to-end business scenario}} |

---

## Out of Scope

- {{what a developer might assume is included but is not}}

---

## Dependencies

| Dependency | Type | Blocking? |
|---|---|---|
| {{dependency}} | Story / External / Epic | Yes / No |

---

## Open Questions

| ID | Question | Impact |
|---|---|---|
| OQ-NNN | {{question}} | {{what's blocked until resolved}} |

---
*Status: Draft — set to Accepted only after epic review gate. Never self-accept.*
