# S-NNN.N — {{Story Title}}

## Metadata

| Field | Value |
|---|---|
| Story ID | S-NNN.N |
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

Generate ALL scenarios needed to fully specify the behaviour. Do NOT stop at 2 scenarios.
Each criterion has: a numbered ID, descriptive title, test type annotation, criticality tag, automation recommendation, and a Gherkin scenario with concrete values.

**Required scenario types** — include every type that applies to this story:

| Type | When to include | Example |
|---|---|---|
| Happy path | Always | Successful submission returns ARN |
| Validation / negative | When the story accepts user or API input | Missing mandatory field returns 400 with field-level errors |
| Authorization | When the story has role/permission requirements | Unauthorized user receives 403 |
| Boundary | When the story involves thresholds, limits, or ranges | Loan amount at exactly £10,000 threshold |
| Integration failure | When the story calls external services | Experian timeout triggers fallback to REFER_TO_UNDERWRITER |
| State transition | When the story changes entity status | Application in DECLINED cannot be resubmitted |
| Concurrency / idempotency | When duplicate or parallel requests are possible | Duplicate submission within 1 second returns same ARN |
| Audit / compliance | When the story produces auditable events | State change emits audit event with actor and timestamp |

**Criticality tags** (risk-based):
- `[critical]` — must never fail in production; regression = incident. Always automate.
- `[important]` — significant business impact if broken. Automate where practical.
- `[standard]` — normal coverage. Automate if cost-effective.

**Automation tags:**
- `[automate]` — must be covered by automated tests (unit, integration, or e2e).
- `[manual]` — better suited for manual or exploratory testing (UX, accessibility, visual).
- `[automate-later]` — automate after initial delivery; acceptable as manual for MVP.

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

A story with 1 layer and 1 requirement should have at least 3-4 scenarios.
A story with 2+ layers or 2+ requirements should have at least 5-6 scenarios.
A story involving external integrations or state machines should have 6+ scenarios.

---

## Test Expectations

| Test Type | What to Test | Why | Automation |
|---|---|---|---|
| Unit | {{specific function/logic}} | {{business rule or validation}} | Must automate |
| Integration | {{external system interaction}} | {{adapter, API call, DB query}} | Must automate |
| API | {{endpoint contract}} | {{request/response schema, errors}} | Must automate |
| E2E | {{user flow}} | {{end-to-end business scenario}} | Automate / Manual |

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
