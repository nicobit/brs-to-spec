# Use Case Diagram

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I021-NEXT21 |
| Created at | 2026-06-17T17:40:00+00:00 |
| Created by | product-owner |
| Status | Draft |

## Use Case Diagram

```mermaid
graph LR
  ACT_APPLICANT([Applicant])
  ACT_UNDERWRITER([Underwriter])
  ACT_COMPLIANCE([Compliance Team])
  ACT_SYSTEM([System])

  UC_SUBMIT(UC-001 Submit Application)
  UC_VIEW_STATUS(UC-002 View Status)
  UC_PRE_SCREEN(UC-003 AI Pre-screening)
  UC_UNDERWRITE(UC-004 Underwrite Application)
  UC_DISBURSE(UC-005 Disburse Funds)
  UC_DOCS(UC-006 Manage Documents)
  UC_KYC(UC-007 Perform AML/KYC Checks)
  UC_GENERATE_OFFER(UC-008 Generate Offer)
  UC_ACCEPT_OFFER(UC-009 Accept Offer)
  UC_NOTIFY(UC-010 Send Notifications)

  ACT_APPLICANT --> UC_SUBMIT
  ACT_APPLICANT --> UC_VIEW_STATUS
  ACT_SYSTEM --> UC_PRE_SCREEN
  ACT_UNDERWRITER --> UC_UNDERWRITE
  ACT_SYSTEM --> UC_DISBURSE
  ACT_SYSTEM --> UC_DOCS
  ACT_SYSTEM --> UC_KYC
  ACT_SYSTEM --> UC_GENERATE_OFFER
  ACT_APPLICANT --> UC_ACCEPT_OFFER
  ACT_SYSTEM --> UC_NOTIFY
```

## UC Catalog

| UC-NNN | Title | Primary Actor(s) | FR Sources |
|---|---|---|---|
| UC-001 | Submit Application | Applicant | FR-001, FR-002, FR-003 |
| UC-002 | View Application Status | Applicant | FR-005 |
| UC-003 | AI Pre-screening | System | FR-006, FR-007, FR-008 |
| UC-004 | Underwrite Application | Underwriter | FR-015, FR-017 |
| UC-005 | Disburse Funds | System | FR-024, FR-025 |
| UC-006 | Manage Documents | Applicant / System | FR-021, FR-022 |
| UC-007 | Perform AML/KYC Checks | System / Compliance Team | FR-012, FR-013, FR-014 |
| UC-008 | Generate Offer | System | FR-019, FR-020 |
| UC-009 | Accept Offer | Applicant | FR-021, FR-022 |
| UC-010 | Send Notifications | System | FR-004, FR-027 |

## Coverage Notes

This use case set maps to the primary lifecycle: intake → pre-screen → underwriting → offer → disbursement. It traces FR clusters to specific UCs; none are intentionally excluded.

---

*Set Status: Accepted only by human approval when required by the workflow. Never self-accept.*
