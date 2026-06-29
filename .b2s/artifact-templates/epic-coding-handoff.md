# Coding Handoff - E-NNN {{Epic Title}}

This document is a self-contained coding package. A coding agent should be able to implement this epic by reading ONLY this file. Do not reference external files - include all content inline.

---

## 1. Implementation Objective

{{What to build, why it matters, and what business outcome it enables. 2-3 sentences.}}

---

## 2. Scope

### In Scope
- {{Concrete deliverable 1}}
- {{Concrete deliverable 2}}

### Out of Scope - Do NOT Implement
- {{Explicitly excluded functionality 1}}
- {{Explicitly excluded functionality 2}}

### Constraints
- {{Architecture rule or NFR that limits implementation choices}}
- {{Technology constraint}}
- {{Security constraint}}

---

## 3. Data Model

### Entity Diagram

```mermaid
erDiagram
    {{ENTITY}} {
        uuid id PK
        string field_1
    }
```

### Field Definitions

| Entity | Field | Type | Required | Constraints | Validation Rules |
|---|---|---|---|---|---|
| {{Entity}} | {{field}} | string / int / date / decimal / uuid | Yes / No | {{max length, format, FK}} | {{regex, range, enum values}} |

### State Machine (if applicable)

```mermaid
stateDiagram-v2
    [*] --> {{state_1}}
    {{state_1}} --> {{state_2}}: {{trigger}}
```

| Transition | Trigger | Actor | Side Effects |
|---|---|---|---|
| {{from}} -> {{to}} | {{event or action}} | {{who}} | {{events emitted, notifications}} |

---

## 4. API Specification

### {{METHOD}} {{/api/v1/resource}}

**Purpose:** {{what this endpoint does}}

```yaml
openapi: "3.0.3"
paths:
  /api/v1/{{resource}}:
    {{method}}:
      summary: "{{purpose}}"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - {{field_1}}
                - {{field_2}}
              properties:
                {{field_1}}:
                  type: string
                  description: "{{description}}"
                {{field_2}}:
                  type: string
      responses:
        "201":
          description: "Created"
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
                    format: uuid
        "400":
          description: "Validation error"
        "403":
          description: "Unauthorized"
        "404":
          description: "Not found"
```

Repeat for each endpoint in this epic.

---

## 5. UI Specification

*Include only if this epic delivers frontend pages. Copy from the implementation contract's `## UI Surface` section.*

### Page: {{Page Name}}

**Route:** {{/path}} | **Application:** {{app name}}

**Layout:** {{component arrangement}}

**Form fields:**

| Field | Type | Required | Validation | Default |
|---|---|---|---|---|
| {{field}} | {{type}} | {{Yes/No}} | {{concrete rule}} | {{default or -}} |

**Data binding:** {{which API endpoints from Section 4 this page calls}}

**States:**
- Loading: {{what to show}}
- Validation error: {{inline errors / summary}}
- Server error: {{banner / toast / redirect}}
- Success: {{confirmation / redirect / modal}}

**User flow:** {{step-by-step from user action to system response to next page}}

*Repeat for each page owned by this epic.*

---

## 6. Events

| Event | Type | Trigger | Payload Fields | Delivery |
|---|---|---|---|---|
| {{event.name}} | domain / audit | {{when emitted}} | {{field1, field2, timestamp}} | at-least-once / at-most-once |

### Event Payload Schema

```json
{
  "event_type": "{{event.name}}",
  "{{field_1}}": "{{type}}",
  "{{field_2}}": "{{type}}",
  "timestamp": "ISO-8601"
}
```

---

## 7. Business Rules

| Rule ID | Condition | Effect | Source |
|---|---|---|---|
| BR-NNN | {{when this applies}} | {{what happens}} | {{FR/REQ reference}} |

---

## 8. Story Execution Order

Implement stories in this order. Each story includes its full acceptance criteria below.

| Order | Story ID | Title | Layers | Why this order |
|---|---|---|---|---|
| 1 | S-NNN.N | {{title}} | {{layers}} | {{dependency or foundation reason}} |
| 2 | S-NNN.N | {{title}} | {{layers}} | {{reason}} |

---

## 9. Acceptance Criteria by Story

### S-NNN.N - {{Story Title}}

**Story Type:** {{frontend-form / frontend-page / backend-endpoint / event-consumer / schema-migration / generic}}

**Requirements Implemented:** {{FR-NNN, FR-NNN}}

**Requirements Referenced:** {{FR-NNN, NFR-NNN, or None}}

**User Story:** As a {{actor}}, I want {{capability}}, so that {{outcome}}.

**In Scope:**
- {{concrete behavior to implement}}

**Out of Scope:**
- {{explicit exclusion}}

**Implementation Guidance:**
- Entity: {{entity from data model above}}
- API: {{endpoint from API spec above}}
- Events: {{events to emit}}
- Rules: {{business rules that apply}}

**Dependency Contracts:**
- {{dependency and exact contract this story consumes}}

#### AC-001 - {{criterion title}} `[test-type]` `[criticality]` `[automation]`

```gherkin
Scenario: {{meaningful scenario name}}
  Given {{precondition with concrete values}}
  When {{action with specific input}}
  Then {{observable outcome with specific expected value}}
```

#### AC-002 - {{criterion title}} `[test-type]` `[criticality]` `[automation]`

```gherkin
Scenario: {{scenario name}}
  Given {{precondition}}
  When {{action}}
  Then {{outcome}}
```

*(Repeat all AC from the story - do not summarize or skip any)*

---

*(Repeat Section 9 for every story in the execution order)*

---

## 10. Test Requirements

### Unit Tests

| Test | What to verify | Source AC | Criticality |
|---|---|---|---|
| {{test name}} | {{specific assertion}} | AC-NNN | Critical / Important / Standard |

### Integration Tests

| Test | What to verify | Source AC | Criticality |
|---|---|---|---|
| {{test name}} | {{specific assertion}} | AC-NNN | Critical / Important / Standard |

### API Contract Tests

| Test | Endpoint | Expected behavior | Source AC |
|---|---|---|---|
| {{test name}} | {{METHOD /path}} | {{request -> response}} | AC-NNN |

### E2E Tests

| Test | Flow | Source AC | Automation |
|---|---|---|---|
| {{test name}} | {{user journey}} | AC-NNN | Automate / Manual |

### Story-Specific Required Tests

| Story | Required test obligation | Source |
|---|---|---|
| S-NNN.N | {{explicit required test from story agent contract}} | story `.agent.yaml` |

---

## 11. Risks and Open Questions

| Item | Type | Impact | What must happen |
|---|---|---|---|
| {{risk or question}} | Risk / Open Question | {{what breaks if unresolved}} | {{decision or mitigation needed}} |

---

## 12. Definition of Done

- [ ] All stories implemented per execution order
- [ ] All `[critical]` and `[important]` AC covered by automated tests
- [ ] API contract matches the OpenAPI spec in Section 4
- [ ] Events emitted match the schema in Section 6
- [ ] Business rules from Section 7 are enforced
- [ ] No functionality implemented that is listed in Out of Scope
- [ ] Existing tests still pass
- [ ] No unrelated refactoring

---
*This handoff is self-contained. Implement from this document alone. Do not invent features not specified here.*
