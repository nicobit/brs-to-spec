# Actors and Personas

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I012-NEXT12 |
| Created at | 2026-06-16 |
| Created by | product-owner |
| Status | Draft |

## Human Actors (ACT-NNN)

| ACT-NNN | Name | Description | Primary Goal | Permissions | Restrictions | BRS Source |
|---|---|---|---|---|---|---|
| ACT-001 | Applicant | Person applying for a loan via the online portal | Submit application and receive ARN; accept offers | Create application, view status | Cannot approve offers | FR-001..FR-005 |
| ACT-002 | Underwriter | Human reviewer handling REFER cases and >£10k decisions | Assess referred applications and approve/decline | Read application data, change status, add notes | Cannot directly disburse funds | FR-015..FR-019 |
| ACT-003 | Compliance Team | Compliance reviewers for AML/KYC holds | Review compliance holds and clear or escalate | View flagged cases, add remediation notes | Cannot approve offers | FR-012..FR-014 |
| ACT-004 | Admin / Ops | Platform administrators and operations staff | Monitor system health and investigate exceptions | Access dashboards and audit logs | Restricted from viewing raw PII unless authorized | FR-029..FR-030 |

## Systems (SYS-NNN)

| SYS-NNN | Name | Type | Description | Integration | BRS Source |
|---|---|---|---|---|---|
| SYS-001 | AI Scoring Service | External / Internal Automated | Produces `AI_Score` and recommendation | API / event | FR-006..FR-009 |
| SYS-002 | Experian Credit Service | External | Provides credit report payloads | API | FR-009 |
| SYS-003 | DocuSign | External | E-signature provider for offers | API / webhook | FR-020..FR-023 |
| SYS-004 | Temenos T24 | External | Core banking system for disbursements | API / gateway | FR-024..FR-027 |
| SYS-005 | Audit & Observability | Internal | Captures events, metrics, and traces | Event stream | FR-028..FR-030 |

## Interaction Matrix

| Actor | Initiates | Reads | Modifies | Approves / Rejects | Receives |
|---|---|---|---|---|---|
| Applicant | UC-001, UC-004 | Application status | Submission | Acceptance via e-sign | Email notifications |
| Underwriter | UC-002 | Application details, score, credit report | Decision status, notes | Approve / Decline | Underwriter notifications |
| Compliance Team | UC-003 | AML/KYC evidence | Hold status, remediation notes | Clear / Escalate | Compliance notifications |
| Admin / Ops | UC-009, UC-010 | Dashboards, audit logs | System configurations | N/A | System alerts |

---

*Set Status: Accepted only by workflow or human approval when applicable.*
