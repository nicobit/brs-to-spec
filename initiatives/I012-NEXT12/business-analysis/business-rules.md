# Business Rules

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I012-NEXT12 |
| Created at | 2026-06-16 |
| Created by | product-owner |
| Status | Draft |

## Business Rules Catalog

| BR-NNN | Category | Rule Statement | BRS Source | Affected Requirements | Affected Actors | Notes |
|---|---|---|---|---|---|---|
| BR-001 | Validation | All required application fields (as defined in FR-001) must be present and pass format validation before accepting submission. | FR-001 | FR-001, FR-002 | Applicant, System | Client and server-side validation required |
| BR-002 | Identification | Assign a unique ARN to every submitted application at time of acceptance; ARN must be globally unique and immutable. | FR-003 | FR-003 | System | ARN format ARN-YYYYNNN |
| BR-003 | Notification | Send confirmation email containing ARN within 2 minutes of submission. | FR-004 | FR-004 | System | Retry 2 times on transient email failure |
| BR-004 | Scoring | Trigger AI pre-screening within 60 seconds of submission; store `score_value`, `model_version`, and `recommendation`. | FR-006 | FR-006, FR-007 | System, AI Service | Include model version in audit trail |
| BR-005 | Decisioning | If `score_recommendation` == AUTO_APPROVE and amount ≤ £10,000 then generate offer automatically pending AML/KYC pass. | FR-010 | FR-010 | System | AML/KYC must be satisfied before disbursement |
| BR-006 | AML/KYC Hold | If AML or KYC checks fail, set application status to `COMPLIANCE_HOLD` and route to Compliance Team for manual review. | FR-012, FR-014 | FR-012..FR-014 | Compliance Team | Record reasons and evidence in `ComplianceCheck` entity |
| BR-007 | Escalation | Escalate underwriter queue items after 4 business hours of no action. | FR-019 | FR-019 | System, Ops | Notify escalation channel and on-call persona |
| BR-008 | Underwriter Actions | Underwriter decisions must include action (`approve`, `decline`, `request_info`) and a mandatory reason for declines. | FR-017 | FR-017, FR-018 | Underwriter | Persist action metadata immutably in `UnderwriterAction` |
| BR-009 | Offer Acceptance | Digital acceptance must record timestamp, actor identity, and IP address; acceptance opens disbursement pipeline. | FR-022, FR-024 | FR-022, FR-024 | System | Log acceptance snapshot in `AuditLog` |
| BR-010 | Disbursement Retry | If disbursement confirmation not received within 2 minutes, retry once then surface a manual exception for investigation. | FR-026 | FR-026 | System, Ops | Record retry attempts and outcome |
| BR-011 | Audit Logging | Record immutable audit entries for every state transition with a snapshot of relevant data. | FR-018, FR-028 | FR-018, FR-028 | System | Use write-once storage where available |
| BR-012 | Observability | Emit structured observability events for key lifecycle events (submission, scoring, underwriter decision, offer generation, disbursement). | FR-030 | FR-030 | System, Admin | Events include correlation id and timestamps |

## Coverage Note

| FR-NNN | Business rule(s) | Status |
|---|---|---|
| FR-001 | BR-001 | Covered |
| FR-003 | BR-002 | Covered |
| FR-004 | BR-003 | Covered |
| FR-006..FR-010 | BR-004, BR-005 | Covered |
| FR-012..FR-014 | BR-006 | Covered |
| FR-015..FR-019 | BR-007, BR-008 | Covered |
| FR-022..FR-026 | BR-009, BR-010 | Covered |
| FR-018, FR-028 | BR-011 | Covered |
| FR-029..FR-030 | BR-012 | Covered |

---

*Set Status: Accepted only by workflow or human approval when applicable.*
