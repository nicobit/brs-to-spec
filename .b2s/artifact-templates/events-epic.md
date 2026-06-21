# Events — E-NNN {{Epic Title}}

## Event Catalog

| Event | Type | Producer | Consumers | Trigger | Delivery | Story |
|---|---|---|---|---|---|---|
| {{event.name}} | domain / integration / audit | {{service}} | {{service(s)}} | {{what causes emission}} | at-least-once / at-most-once | F-NNN.N |

---

## Event Definitions

### {{event.name}}

| Field | Value |
|---|---|
| Purpose | {{why this event exists}} |
| Producer | {{service or component}} |
| Consumers | {{service(s) that subscribe}} |
| Trigger | {{state change or action that causes emission}} |
| Delivery Guarantee | at-least-once / at-most-once |
| Ordering | unordered / ordered per {{partition key}} |
| Idempotency Key | {{field used for deduplication}} |

**Payload Schema:**

| Field | Type | Required | Description |
|---|---|---|---|
| {{field}} | string / int / date / uuid | Yes / No | {{description}} |

**Envelope:**

| Field | Purpose |
|---|---|
| correlation_id | Trace across services |
| timestamp | Event creation time (UTC) |
| event_version | Schema version for evolution |
| source | Producer service identifier |

---

## Audit Events

| Event | Trigger | Required Fields | Retention | Source |
|---|---|---|---|---|
| {{event}} | {{state transition}} | {{fields that must be captured}} | {{retention policy}} | AR-NNN / FR-NNN |

---
*Only create this file if the epic emits or subscribes to domain events. Derive from requirements and architecture rules.*
