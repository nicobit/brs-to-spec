# Gaps and Questions

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I012-NEXT12 |
| Created at | 2026-06-16 |
| Created by | product-owner |
| Status | Draft |

## Gap Catalog

| GAP-NNN | Category | Description | Impact | Severity | Suggested Resolution | Owner | BRS Source |
|---|---|---|---|---|---|---|---|
| GAP-001 | Integration | Experian integration contract details (rate-limits, fields) are not specified; fallback behaviour needs concrete mapping. | Integration risk affecting scoring | High | Confirm Experian field mapping and fallback rules with vendor | product-owner / architect | FR-009 |
| GAP-002 | Security / Privacy | Data residency and PII handling for Experian and DocuSign workflows need confirmation (cross-border constraints). | Compliance risk | High | Confirm data flows and storage locations with security/arch team | product-owner / security |
| GAP-003 | Non-Functional | SLA for AI scoring under peak load not specified with clear load profile. | Performance risk | Medium | Define expected concurrent submissions and test profile | product-owner / ops | FR-006, NFR-002 |
| GAP-004 | Process | Underwriter SLAs and on-call escalation workflow details (business hours, contacts) are incomplete. | Operational risk | Medium | Define escalation SLA and contact list | ops / delivery |
| GAP-005 | Edge Case | Disbursement retry policy beyond one retry is unspecified for persistent failures. | Financial risk | Medium | Define manual exception workflow and retry/backoff policy | product-owner / ops | FR-026 |

## Critical Path

### Blocking Gaps

| GAP-NNN | Description | Impact | Owner |
|---|---|---|---|
| GAP-001 | Experian contract and field mapping | High | product-owner / architect |
| GAP-002 | Data residency constraints for third-party services | High | product-owner / security |

### High-Severity Gaps

| GAP-NNN | Description | Default Assumption (if proceeding) | Owner |
|---|---|---|---|
| GAP-003 | AI scoring SLA | Assume normal load <= 500 concurrent submissions; validate during performance testing | product-owner / ops |

### Low-Severity Gaps

| GAP-NNN | Description | Assumption | Risk if assumption is wrong |
|---|---|---|---|
| GAP-005 | Disbursement retry beyond one attempt | Assume manual exception for persistent failures | ops | Operational delays and manual intervention |

## Coverage Summary

| Category | Count |
|---|---|
| Blocking gaps | 2 |
| High-severity gaps | 1 |
| Low-severity gaps | 1 |
| Total gaps | 4 |

---

*Blocking gaps must be resolved or explicitly accepted with assumptions before downstream planning can proceed.*
