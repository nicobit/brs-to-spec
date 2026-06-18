# Actors and Personas

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I013-NEXT13 |
| Created at | 2026-06-16 |
| Created by | product-owner |
| Status | Draft |

## Actor Catalog

| ACT-NNN / SYS-NNN | Name | Type | Primary Goal | Source |
|---|---|---|---|---|
| ACT-001 | Applicant | Human | Submit application, receive decision/status | use-cases.puml / input/brs.md |
| ACT-002 | Underwriter | Human | Review referred applications, decide or request info | use-cases.puml / business-analysis/requirements.md |
| ACT-003 | Compliance | Human / Team | Review AML/KYC holds and approve exceptions | use-cases.puml / input/brs.md |
| ACT-004 | Admin | Human | Operational monitoring and disbursement oversight | use-cases.puml / input/architecture.md |
| SYS-001 | AI Scoring Service | System | Produce risk score and recommendation from inputs | use-cases.puml / input/brs.md |
| SYS-002 | Experian CreditExpert | External System | Provide credit bureau data for scoring | use-cases.puml / input/brs.md |
| SYS-003 | HMRC Identity Verification | External System | Provide KYC identity verification | input/brs.md / input/architecture.md |
| SYS-004 | DocuSign | External System | E-signature for offer acceptance | input/brs.md |
| SYS-005 | Temenos T24 (via Payment Gateway) | External System | Receive disbursement instructions | input/brs.md / input/architecture.md |

## Interaction Patterns

- `ACT-001 (Applicant)` initiates `UC-001 Submit Application` → system validates fields (`BR-001`) → receives ARN (`BR-002`) and confirmation email (`BR-003`).
- `SYS-001 (AI Scoring Service)` subscribes to submission events, produces `Score` (FR-006/FR-007) and may trigger `SYS-002` (Experian) lookups.
- `SYS-002 (Experian)` responses influence recommendation; failures route to `ACT-002 (Underwriter)` per `BR-005`.
- `ACT-002 (Underwriter)` reviews queued items (FR-015) and performs actions recorded as `UnderwriterAction` (FR-018).
- `ACT-003 (Compliance)` handles COMPLIANCE_HOLD cases and prevents offer generation (FR-014).
- `SYS-004 (DocuSign)` is invoked for offer acceptance and returns evidence logged in `AuditEvent` (FR-022).
- `SYS-005 (Temenos T24)` receives disbursement payload from `PaymentInstruction` after acceptance and cooling-off (FR-024).

## Permissions & Restrictions

- Applicants cannot access other applicants' data; status lookup requires ARN + DOB (FR-005).
- Underwriters have Azure AD authenticated access with RBAC; actions are recorded immutably (FR-018).
- Compliance team can view full PII under elevated RBAC but write actions must be auditable.

## Interaction Matrix (high level)

| Actor/System | UC-001 | UC-002 | UC-005 | UC-006 | UC-007 | UC-008 | UC-009 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ACT-001 Applicant | I |   |   |   |   |   |   |
| SYS-001 AI Scoring |   | A | I | I |   |   |   |
| SYS-002 Experian |   | R |   |   |   |   |   |
| ACT-002 Underwriter |   |   |   |   | R |   |   |
| ACT-003 Compliance |   |   |   | R |   |   |   |
| SYS-005 T24 |   |   |   |   |   |   | C |

Key: I=Initiates, A=Acts/Assesses, R=Responds, C=Consumes/Receives

---

*Set Status: Draft — review with architecture and security for permissions specifics.*
