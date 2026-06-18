# Architecture Rules

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I021-NEXT21 |
| Created at | 2026-06-17T18:15:00+00:00 |
| Created by | architect |
| Status | Draft |

## Rules Catalog

| AR-NNN | Rule | Rationale | Owner |
|---|---|---|---|
| AR-001 | All PII must be encrypted at rest and in transit | Compliance and security | architect |
| AR-002 | Disbursement operations must be idempotent | Prevent duplicate payments | architect / ops |
| AR-003 | External integrations must implement circuit breakers and fallbacks | Resilience for external vendors | architect |

---

*Set Status: Accepted only by workflow or human approval when applicable. Never self-accept.*

## Forbidden Patterns

- Storing unencrypted PII in logs or plaintext storage
- Hard-coding secrets in repository

## Coverage

These rules cover data protection, disbursement idempotency, and integration resilience; they map to AR-001..AR-003 and the architecture review requirements. Further rules will be added during detailed design.
