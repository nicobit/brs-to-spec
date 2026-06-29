# Implementation Contract — E-NNN {{Epic Title}}

Include ONLY the sections that are relevant to this epic. Do not include empty sections.

---

## Data Entities

*Include only if this epic creates, updates, reads, or persists business data.*

### ER Diagram

```mermaid
erDiagram
    {{ENTITY_A}} {
        uuid id PK
        string field_1
        string field_2
        timestamp created_at
    }
    {{ENTITY_B}} {
        uuid id PK
        uuid entity_a_id FK
        string field_1
    }
    {{ENTITY_A}} ||--o{ {{ENTITY_B}} : "has many"
```

### {{Entity Name}}

| Field | Type | Required | Constraints | Source |
|---|---|---|---|---|
| {{field}} | string / int / date / decimal / boolean / uuid | Yes / No | {{specific: "0-1000", "UK NI format", "ISO 8601"}} | FR-NNN |

**State Machine** (if entity has lifecycle states):

```mermaid
stateDiagram-v2
    [*] --> {{state_1}}
    {{state_1}} --> {{state_2}}: {{trigger}}
    {{state_2}} --> {{state_3}}: {{trigger}}
```

| Transition | Trigger | Actor | Side Effects |
|---|---|---|---|
| {{from}} → {{to}} | {{what causes it}} | {{who triggers it}} | {{events, notifications, audit}} |

---

## API Surface

*Include only if this epic exposes or consumes APIs.*

```yaml
openapi: "3.0.3"
info:
  title: "{{Epic Title}} API"
  version: "1.0.0"
paths:
  /api/v1/{{resource}}:
    post:
      summary: "{{purpose}}"
      operationId: "{{operationId}}"
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - {{field_1}}
              properties:
                {{field_1}}:
                  type: string
                  description: "{{description}}"
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
        "422":
          description: "Business rule violation"
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### Consumed APIs (External)

| API | Provider | Timeout | Fallback | Circuit Breaker |
|---|---|---|---|---|
| {{api}} | {{provider}} | {{ms}} | {{fallback behaviour}} | {{threshold}} |

---

## Events

*Include only if this epic publishes, consumes, or reacts to events.*

| Event | Type | Producer | Consumers | Trigger |
|---|---|---|---|---|
| {{event.name}} | domain / audit | {{service}} | {{consumers}} | {{trigger}} |

### {{event.name}}

**Payload:**

| Field | Type | Required | Description |
|---|---|---|---|
| {{field}} | string / uuid / timestamp | Yes / No | {{description}} |

**Delivery:** at-least-once / at-most-once
**Idempotency key:** {{field}}

---

## Business Rules

*Include only rules that affect implementation for this epic.*

| Rule | Condition | Effect | Source |
|---|---|---|---|
| {{rule}} | {{when this applies}} | {{what happens}} | FR-NNN / BR-NNN |

---

## UI Surface

*Include only if this epic delivers user-facing pages. Derive from `architecture/ui-specification.md`, scoped to pages owned by this epic.*

This section is a scoped extract from `architecture/ui-specification.md`.

Rules:
- Do not originate new initiative-level UI truth here.
- Preserve `Specification Status`, `Blocking Dependencies`, and `Contract Mode` from the source UI specification unless explicit clarification resolves them.
- If epic-local clarification changes a UI fact, reference the originating `UIQ-*` or clarification answer in `## Open Design Questions`.

### Pages Owned by This Epic

| Page | Route | Application | Specification Status | Blocking Dependencies | Linked FRs |
|---|---|---|---|---|---|
| {{page name}} | {{/route}} | {{app name}} | {{confirmed/inferred/partial/blocked}} | {{UIQ-NNN, GAP-NNN or "none"}} | {{FR-NNN}} |

*Pages with status `partial` or `blocked` have unresolved dependencies. These must be resolved before the page enters active story generation. Carry blocking open questions into the `## Open Design Questions` section below.*

### Page: {{Page Name}}

**Layout:** {{component arrangement}}
**Specification status:** {{confirmed/inferred/partial/blocked}}
**Blocking dependencies:** {{UIQ-NNN, GAP-NNN or "none"}}

**Form fields** (if applicable):

| Field | Type | Required | Validation | Source |
|---|---|---|---|---|
| {{field}} | {{text/select/date/currency}} | {{Yes/No}} | {{concrete rule}} | {{FR-NNN}} |

**Data binding:**

| Component | Endpoint | Method | Contract Mode | Notes |
|---|---|---|---|---|
| {{form/table}} | {{/api/v1/...}} | {{POST/GET}} | {{confirmed/partial/mock/unknown}} | {{what is sent/shown}} |

**States:** loading → {{behavior}} | error → {{behavior}} | success → {{behavior}}

**User flow:** {{step-by-step: user action → system response → navigation}}

---

## Non-Functional Constraints

*Include only constraints that affect implementation for this epic.*

| Constraint | Target | Source |
|---|---|---|
| {{e.g. response time < 2s}} | {{component}} | NFR-NNN / AR-NNN |

---

## Open Design Questions

| Question | Impact | Must Resolve Before |
|---|---|---|
| {{question}} | {{what's blocked}} | {{story ID or "implementation start"}} |

---
*Include only relevant sections. A UI-only epic may have no Events section. A backend pipeline may have no API surface. Do not generate empty sections.*
