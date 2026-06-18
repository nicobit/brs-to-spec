# Data Contract

## Metadata

| **Field** | **Value** |
|---|---|
| **Status** | **In progress** |
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by event | {{event_id}} |

## Data Asset Catalog

| DA-NNN | Name | Owner | Classification | PII Fields | Encrypted at Rest | Encrypted in Transit | Retention |
|---|---|---|---|---|---|---|---|
| DA-001 | | {{service/module}} | Internal / Confidential / PII / Regulated | | Yes / No | Yes / No | {{period / trigger}} |

## Schema Definitions

### DA-001: {{Name}}

| Field | Type | Required | Constraints | PII? | PII Type | Encryption | BRS Source |
|---|---|---|---|---|---|---|---|
| | string/int/date/decimal | Yes / No | BR-NNN | Yes / No | name/email/address/financial/health | field-level / column | FR-NNN |

## PII Mapping

| DA-NNN | PII Field | PII Type | Encrypted | Retention Period | Deletion Trigger | Regulatory Basis |
|---|---|---|---|---|---|---|
| DA-001 | | | Yes / No | | user deletion / expiry / N/A | GDPR / internal |

## Data Flow

| DA-NNN | Producer | Consumers | Flow Type | Cross-boundary? |
|---|---|---|---|---|
| | | | Sync / Async | Yes / No |

## Migration Plan

| DA-NNN | Change Type | Migration Strategy | Backward Compatible | Rollback Plan |
|---|---|---|---|---|
| | Additive / Versioned / Breaking | | Yes / No | |

## Access Control

| DA-NNN | Read | Write | Delete | Auth mechanism | BR-NNN |
|---|---|---|---|---|---|

## Accepted Risks

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|

## Decision

**Decision:** Approved / Request Changes / Blocked  
**Rationale:** {{reason}}

---
*Status: In progress — set to Accepted by data/security gate owner. Never self-accept.*
