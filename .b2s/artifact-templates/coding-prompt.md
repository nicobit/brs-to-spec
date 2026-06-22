# Coding Prompt — S-NNN.N {{Story Title}}

## Goal

{{One paragraph: what to build, why it matters, and the business outcome. The coding agent must understand the purpose without reading any other file.}}

---

## Acceptance Criteria

| AC | Criterion | Test Type | Scenario |
|---|---|---|---|
| AC-001 | {{criterion}} | unit / integration / api / e2e | {{Gherkin scenario name}} |

### AC-001 — {{criterion title}}

```gherkin
Scenario: {{scenario name}}
  Given {{precondition}}
  When {{action}}
  Then {{observable outcome}}
```

**Test type:** {{unit / integration / api / e2e}}
**What to verify:** {{specific assertion the test must make}}

---

## Architecture Constraints

| AR-NNN | Constraint | Impact on This Story |
|---|---|---|
| {{id}} | {{rule statement}} | {{how it constrains implementation}} |

---

## API Contract

{{Include only if this story implements or calls an API. Copy the relevant OpenAPI YAML fragment from the epic's api-surface.md — the full path definition with request schema, response schema, and error responses. Do NOT summarise as one-liners.}}

```yaml
# Paste the relevant OpenAPI path definition here
```

---

## Data Contract

{{Include only if this story creates or modifies data entities. Copy the full entity field table from the epic's data-entities.md — every field with type, required, constraints. Do NOT summarise as one-liners.}}

**Entity:** {{name}}

| Field | Type | Required | Constraints |
|---|---|---|---|
| {{field}} | {{type}} | Yes / No | {{specific validation}} |

**State transitions:** {{from → to, with triggers — copy from data-entities.md if applicable}}

---

## Event Contract

{{Include only if this story emits or subscribes to events. Copy relevant event details from the epic's events.md.}}

**Event:** {{event.name}}
**Trigger:** {{what causes emission}}
**Payload:** {{key fields}}

---

## Test Expectations

| Test Type | What to Test | Why |
|---|---|---|
| Unit | {{specific function/logic}} | {{business rule or validation}} |
| Integration | {{external system interaction}} | {{adapter, API call, DB query}} |
| API | {{endpoint contract}} | {{request/response schema, errors}} |
| E2E | {{user flow}} | {{end-to-end business scenario}} |

---

## Boundaries

**Out of scope — do NOT implement:**
- {{what this story explicitly excludes}}

**Do NOT change:**
- {{modules, services, or files that must not be modified by this story}}

---
*This prompt is self-contained. A coding agent reads ONLY this file to implement the story. All constraints, schemas, and test expectations are inline.*
