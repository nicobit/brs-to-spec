# {{Domain Name}} — Data Schema Specification

## Metadata

| **Field** | **Value** |
|---|---|
| **Status** | **In progress** |
| Schema ID | {{schema_id, e.g. DS-001}} |
| Initiative ID | {{initiative_id}} |
| Data domain | {{Applications / Decisions / Audit / Users / ...}} |
| Storage type | {{relational / document / key-value / time-series / mixed}} |
| Owner | {{team or role}} |
| Shared across teams | {{Yes / No — if Yes, list teams}} |
| Created at | {{date}} |
| Created by | engineering-lead |

## Purpose

{{What domain this schema covers, which stories produce or consume it, and why it exists as a distinct schema unit.}}

## Traceability

| Source | Reference | Description |
|---|---|---|
| BRS | FR-NNN | {{requirement that drives this data structure}} |
| Architecture | ARCH-C-NNN | {{data residency, PII, or storage constraint}} |
| Business rule | BR-NNN | {{rule that translates to a schema constraint}} |

## Entities

### {{EntityName}}

{{One line: what this entity represents.}}

| Field | Type | Required | Default | Constraints | PII? | Description |
|---|---|---|---|---|---|---|
| id | uuid | Yes | generated | PK | No | Primary key |
| created_at | timestamp | Yes | now() | — | No | Creation timestamp |
| updated_at | timestamp | Yes | now() | — | No | Last update timestamp |
| {{field}} | {{string / int / date / decimal / boolean / uuid}} | {{Yes / No}} | {{default or —}} | {{UK / FK / CHECK / NOT NULL}} | {{Yes / No}} | {{description}} |

**Indexes:**

| Name | Fields | Type | Rationale |
|---|---|---|---|
| {{idx_name}} | {{fields}} | {{btree / hash / gin}} | {{why — query pattern or uniqueness}} |

**Relationships:**

| Field | References | On delete | Notes |
|---|---|---|---|
| {{field}} | {{Entity.field}} | {{CASCADE / RESTRICT / SET NULL}} | {{cross-boundary? shared?}} |

## Enumerations

| Enum name | Values | Used in | Source |
|---|---|---|---|
| {{enum_name}} | {{value1, value2, value3}} | {{Entity.field}} | {{BR-NNN or BRS §N}} |

## PII Inventory

| Field | Entity | PII type | Masking in non-prod | Retention | Deletion trigger | Regulatory basis |
|---|---|---|---|---|---|---|
| {{field}} | {{Entity}} | {{name / DOB / financial / identity / contact}} | {{masked / pseudonymised / clear}} | {{period}} | {{event or policy}} | {{GDPR / internal}} |

## Data Flow

| Entity | Producer | Consumers | Flow type | Cross-boundary? |
|---|---|---|---|---|
| {{Entity}} | {{service}} | {{service(s)}} | {{sync / async / batch}} | {{Yes / No}} |

## Migration Strategy

| Field | Value |
|---|---|
| Approach | {{additive only / blue-green / feature flag}} |
| Rollback plan | {{describe}} |
| Staging verification | {{how migrations are verified before prod}} |
| Shared schema coordination | {{if shared: who approves schema changes}} |

## Open Questions

| # | Question | Owner | Needed before | Status |
|---|---|---|---|---|
| 1 | {{question}} | {{owner}} | {{milestone}} | Open |

---
*Status: In progress — set to Accepted only after data architecture review. Never self-accept.*
