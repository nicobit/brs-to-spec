# Data Entities — E-NNN {{Epic Title}}

## Entity Catalog

| Entity | Type | Owned by This Epic? | Related Epics | Notes |
|---|---|---|---|---|
| {{entity name}} | New / Modified | Yes / No (shared) | E-NNN | {{brief purpose}} |

---

## ER Diagram

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

Include ALL entities owned or modified by this epic. Show primary keys (PK), foreign keys (FK), field types, and relationships. Do NOT abbreviate — every field from the Entity Definitions tables below must appear in the diagram.

---

## Entity Definitions

### {{Entity Name}}

| Field | Type | Required | Constraints | Source |
|---|---|---|---|---|
| {{field_name}} | string / int / date / decimal / boolean / uuid | Yes / No | {{validation, format, range — be specific: "0-1000", "UK NI format", "ISO 8601"}} | FR-NNN |

Do NOT use generic types without constraints. Every field must have specific validation rules derived from the BRS.

**State Machine** (if applicable):

```mermaid
stateDiagram-v2
    [*] --> {{state_1}}
    {{state_1}} --> {{state_2}}: {{trigger}}
    {{state_2}} --> {{state_3}}: {{trigger}}
    {{state_2}} --> {{state_4}}: {{trigger}}
```

| Transition | Trigger | Actor | Side Effects |
|---|---|---|---|
| {{from}} → {{to}} | {{what causes this transition}} | {{who/what triggers it}} | {{events emitted, notifications, audit}} |

**Relationships:**

| Related Entity | Relationship | Cardinality | Join Key | Notes |
|---|---|---|---|---|
| {{entity}} | belongs_to / has_many / references | 1:1 / 1:N / N:M | {{foreign key field}} | {{cascade rules}} |

---

## Cross-Epic References

| Entity | This Epic Uses | Other Epics That Use It | Shared Fields |
|---|---|---|---|
| {{entity}} | {{fields this epic reads/writes}} | E-NNN | {{which fields are shared}} |

---

## Data Constraints

| Constraint | Source | Impact |
|---|---|---|
| {{e.g. PII must be encrypted at rest with AES-256}} | AR-NNN | {{which entities/fields are affected}} |

---
*Every field must have specific type, constraints, and source. Use Mermaid erDiagram for relationships and stateDiagram for state machines. Do NOT abbreviate field definitions.*
