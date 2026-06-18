# Process Flows

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I012-NEXT12 |
| Created at | 2026-06-16 |
| Created by | product-owner |
| Status | Draft |

## Overview

This document captures high-level process flows for the primary business scenarios, mapping to use cases and requirements.

## 1. Application Intake Flow (UC-001)

Steps:
- Applicant completes online form and submits (FR-001)
- System validates inputs (FR-002) and assigns ARN (FR-003)
- Confirmation email is sent (FR-004)

Notes: Client-side and server-side validation applied; correlation id assigned for tracing.

## 2. AI Pre-Screening and Decisioning Flow (UC-006, UC-007, UC-002)

Steps:
- On submission, system invokes AI scoring service (FR-006..FR-009)
- Score and recommendation persisted; if AUTO_APPROVE and amount ≤ £10,000, proceed to offer generation (FR-010)
- If REFER or requires human review, place in underwriter queue (FR-015)

Notes: Include model_version and inputs in audit snapshot; ensure fallback to refer when credit report unavailable.

## 3. AML/KYC Screening Flow (UC-003)

Steps:
- System invokes AML/KYC providers and aggregates results (FR-012..FR-014)
- If checks fail, set `COMPLIANCE_HOLD` and route to Compliance Team (BR-006)

Notes: Maintain evidence artifacts and PII handling in accordance with data residency constraints.

## 4. Underwriter Review and Escalation Flow (UC-002, UC-008)

Steps:
- Underwriter retrieves assigned case with AI score and credit summary (FR-016)
- Underwriter approves/declines/requests info; reasons mandatory for declines (BR-008)
- If no action within 4 business hours, escalate per BR-007 (FR-019)

Notes: Decisions are immutably recorded in `UnderwriterAction` and `AuditLog`.

## 5. Offer Generation, Acceptance, and Disbursement Flow (UC-004, UC-005)

Steps:
- Generate offer document and send to applicant via DocuSign (FR-020..FR-023)
- On acceptance, record timestamp and IP, then trigger disbursement to Temenos T24 (FR-022, FR-024)
- On disbursement confirmation, update status and notify applicant (FR-026, FR-027)

Notes: Retry policy for disbursement per BR-010; retain offer snapshot in `AuditLog`.

## 6. Observability and Audit Flow (UC-009, UC-010)

Steps:
- Emit structured events at submission, scoring, decision, offer, acceptance, and disbursement (FR-030)
- Persist immutable audit entries for state transitions and snapshots (FR-028, BR-011)

Notes: Events must include correlation id, timestamps, and relevant entity references.

## Flow Mappings and Coverage

| Flow | Primary UC | FR Coverage | Key BRs |
|---|---|---|---|
| Application Intake | UC-001 | FR-001..FR-005 | BR-001, BR-002 |
| AI Decisioning | UC-006 / UC-007 | FR-006..FR-011 | BR-004, BR-005 |
| AML/KYC Screening | UC-003 | FR-012..FR-014 | BR-006 |
| Underwriter Review | UC-002 / UC-008 | FR-015..FR-019 | BR-007, BR-008 |
| Offer & Disbursement | UC-004 / UC-005 | FR-020..FR-027 | BR-009, BR-010 |
| Observability | UC-009 / UC-010 | FR-028..FR-030 | BR-011, BR-012 |

---

*Set Status: Accepted only by workflow or human approval when applicable.*
