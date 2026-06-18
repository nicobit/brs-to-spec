# Event Contract

## Metadata

| **Field** | **Value** |
|---|---|
| **Status** | **In progress** |
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by | engineering-lead |

## Event Catalog

| EVT-SCHEMA-NNN | Type | Producer | Consumers | Trigger | Delivery Guarantee |
|---|---|---|---|---|---|
| EVT-SCHEMA-001 | domain.event.name | Service A | Service B | State change | at-least-once |

## Event Definitions

### EVT-SCHEMA-001: domain.event.name

| Field | Value |
|---|---|
| Purpose | |
| Producer | |
| Consumers | |
| Trigger | |
| Delivery guarantee | at-least-once / at-most-once / exactly-once |
| Ordering guarantee | unordered / ordered per partition key |
| Idempotency | |
| Schema evolution | additive only / versioned / breaking-with-migration |
| Dead letter handling | |

**Schema:**

| Field | Type | Required | Constraints |
|---|---|---|---|
| | string / int / date / decimal | Yes / No | |

**Envelope:**

| Field | Purpose |
|---|---|
| correlation_id | |
| timestamp | |
| event_version | |
| source | |

## Schema Evolution Rules

| Event Type | Compatibility Rule | Consumer Impact |
|---|---|---|
| domain.event.name | additive only | |

## Accepted Risks

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|

---
*Status: In progress - set to Accepted by the engineering gate owner. Never self-accept.*
