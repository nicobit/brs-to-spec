# {{Story ID}} — {{Story Title}}

## Metadata

| Field | Value |
|---|---|
| Story ID | {{story_id}} |
| Feature | {{feature_id}} — {{feature_name}} |
| Epic | {{epic_id}} — {{epic_name}} |
| Priority | Must / Should / Could |
| Increment | D1 / D2 / D3 |
| Created at | {{date}} |
| Status | Draft |

---

## 1. User Story

As a **{{actor}}**,
I want to **{{capability}}**,
so that **{{business outcome}}**.

### Business Goal

{{2–5 sentences explaining the business purpose. Why does this story exist? What problem does it solve? What is the business risk if it is not implemented?}}

### Scope

**In scope:**
- {{specific capability or behaviour included}}

**Out of scope:**
- {{explicit exclusion to prevent scope creep}}

---

## 2. Source Traceability

| Source Type | Reference | Description |
|---|---|---|
| BRS | BRS-§N | {{section or clause from the original BRS}} |
| Requirement | FR-NNN | {{requirement description}} |
| Business Rule | BR-NNN | {{rule description}} |
| Architecture Rule | AR-NNN | {{constraint description}} |
| NFR | NFR-NNN | {{non-functional requirement}} |

---

## 3. Business Rules Applied

| Rule ID | Rule | Impact on This Story |
|---|---|---|
| BR-NNN | {{rule statement}} | {{how the rule constrains or shapes implementation}} |

---

## 4. Acceptance Criteria

Each criterion must be specific, testable, and linked to a requirement or business rule.

### AC-NNN — {{Criterion Name}}

**Given** {{precondition}}
**When** {{action}}
**Then** {{observable outcome}}

Traceability:
- Requirement: FR-NNN
- Business Rule: BR-NNN
- BDD Scenario: SCN-NNN

---

## 5. BDD Scenarios

Mandatory scenarios (include all that apply):
- happy path
- negative / validation path
- authorization / permission
- business rule enforcement
- state transition
- integration failure
- audit / compliance

```gherkin
Scenario: {{Scenario name — describe the observable behaviour, not the implementation}}
  Given {{system state before the action}}
  When {{one specific user or system action}}
  Then {{observable outcome}}
  And {{additional observable outcome}}
```

---

## 6. Implementation Context

### Impacted Components

| Component | Type | Expected Change |
|---|---|---|
| {{component name}} | API / UI / Service / Database / Event / Integration | {{what changes and why}} |

### Data Impact

{{New or changed fields, entities, status values, audit events, retention implications. Be specific — field names, data types, constraints.}}

### API Impact

{{Endpoint, method, request schema, response schema, error codes, idempotency, backward compatibility.}}

### UI Impact

{{Changed screens, user actions, validation messages, error states, accessibility expectations.}}

### Integration Impact

{{Upstream/downstream systems, failure modes, retry semantics, timeouts, fallbacks, circuit breakers.}}

---

## 7. Constraints

The coding agent must respect these constraints without exception:

- {{architecture constraint from AR-NNN}}
- {{security constraint}}
- {{data residency / compliance constraint}}
- {{performance / SLA constraint}}

---

## 8. Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| {{story or external dependency}} | Story / Technical / Architecture / Data / External | Yes / No | {{why and when it is needed}} |

---

## 9. Implementation Tasks

Tasks must be concrete and executable. No generic tasks.

| Task ID | Task | Area | Depends On | Validation |
|---|---|---|---|---|
| T-001 | {{specific task}} | API / UI / DB / Test / Docs | {{T-NNN or none}} | {{how to verify it is done}} |

---

## 10. Test Expectations

Required tests for this story:
- [ ] Unit tests — {{what to cover}}
- [ ] Integration tests — {{what to cover}}
- [ ] API / contract tests — {{what to cover}}
- [ ] UI tests — {{what to cover, if applicable}}
- [ ] Negative tests — {{failure modes to test}}
- [ ] Permission tests — {{role-based access to verify}}
- [ ] Audit / compliance tests — {{what to verify in audit log}}
- [ ] Regression scope — {{what existing behaviour must not break}}

---

## 11. Definition of Done

This story is complete only when:
- [ ] all acceptance criteria are implemented and verifiable
- [ ] all BDD scenarios are covered by automated or documented manual tests
- [ ] traceability matrix is updated
- [ ] all architecture constraints are respected
- [ ] no blocking open questions remain
- [ ] regression risks are addressed
- [ ] coding prompt has been executed and reviewed

---

## 12. Coding-Agent Prompt

Write this section so it can be given directly to GitHub Copilot Agent, Claude Code, Codex, Cursor, Devin, or another coding agent without additional context.

```
Story: {{story_id}} — {{story_title}}

Goal:
{{one paragraph describing what the coding agent must implement and why}}

Files / components likely impacted:
- {{file or component}}

Constraints (must not be violated):
- {{constraint}}

Expected implementation steps:
1. {{step}}

Tests to add or update:
- {{test}}

What NOT to change:
- {{explicit exclusion}}

Validation checklist before marking complete:
- [ ] {{check}}
```

---
*Status: Draft — set to Accepted only after human review.*
