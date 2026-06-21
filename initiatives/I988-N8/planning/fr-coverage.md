# Requirement Coverage Report

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I988-N8 |
| Created at | 2026-06-21 |
| Created by | delivery-lead |
| Status | Draft |

---

## Coverage Summary

| Metric | Value |
|---|---|
| Total requirements (from atomic-requirements) | 18 |
| Covered by at least one story | 18 |
| Not covered | 0 |
| Coverage percentage | 100% |

---

## Full Coverage Matrix

| REQ / FR | Requirement Title | Capability | Epic | Feature | Story | Status |
|---|---|---|---|---|---|---|
| REQ-001 | Applicant can submit personal loan application online | Intake | E-001 | F-001 | F-001.1 | Covered |
| REQ-002 | Assign unique Application Reference Number (ARN) | Intake | E-001 | F-001 | F-001.1 | Covered |
| REQ-003 | Email confirmation on submission | Notifications | E-001 | F-002 | F-002.1 | Covered |
| REQ-004 | AI pre-screening and risk scoring | Scoring | E-002 | F-003 | F-003.1 | Covered |
| REQ-005 | Experian integration | Integration | E-002 | F-004 | F-004.1 | Covered |
| REQ-006 | AML / KYC screening | Compliance | E-003 | F-005 | F-005.1 | Covered |
| REQ-007 | Offer generation and acceptance | Offer | E-004 | F-008 | F-008.1 | Covered |
| REQ-008 | Auto-decline notification and cooling-off policy | Notifications | E-001 | F-002 | F-002.2 | Covered |
| REQ-009 | Underwriter queue presentation | Underwriter | E-003 | F-006 | F-006.1 | Covered |
| REQ-010 | Underwriter action logging | Audit | E-003 | F-006 | F-006.2 | Covered |
| REQ-011 | Underwriter escalation for unactioned items | Escalation | E-003 | F-006 | F-006.3 | Covered |
| REQ-012 | Disbursement instruction to core banking | Payments | E-004 | F-009 | F-009.1 | Covered |
| REQ-013 | Observability events emission | Observability | E-003 | F-007 | F-007.1 | Covered |
| REQ-014 | Performance and concurrency targets | NFR | E-005 | F-010 | F-010.1 | Covered |
| REQ-015 | Data residency and encryption | Security | E-005 | F-010 | F-010.1 | Covered |
| REQ-016 | Applicant status retrieval | Status | E-001 | F-002 | F-002.1 | Covered |
| REQ-017 | AI recommendation thresholds | Scoring | E-002 | F-003 | F-003.1 | Covered |
| REQ-018 | Credit data ephemeral handling | Data | E-002 | F-003 | F-003.1 | Covered |
| REQ-019 | DocuSign integration and offer template rules | Integration | E-004 | F-008 | F-008.1 | Covered |
| REQ-020 | Offer template versioning and storage | Offers | E-004 | F-008 | F-008.1 | Covered |
| REQ-021 | Disbursement confirmation and audit | Payments | E-004 | F-009 | F-009.1 | Covered |
| REQ-022 | Audit event schema and store | Observability | E-003 | F-007 | F-007.1 | Covered |
| REQ-023 | Admin metrics and dashboards | Reporting | E-005 | F-011 | F-011.1 | Covered |
| REQ-024 | Metrics retention and export requirements | Reporting | E-005 | F-010 | F-010.1 | Covered |

| NFR-002 | Scoring pipeline performance (<=90s) | NFR | E-002 | F-003 | F-003.1 | Covered |
| NFR-003 | API latency and concurrency targets | NFR | E-005 | F-010 | F-010.1 | Covered |
| NFR-004 | Data residency and encryption policy | NFR | E-005 | F-010 | F-010.1 | Covered |

| FR-001 | Online application form submission | Intake | E-001 | F-001 | F-001.1 | Covered |
| FR-002 | ARN assignment on submit | Intake | E-001 | F-001 | F-001.1 | Covered |
| FR-003 | Submission validation rules | Intake | E-001 | F-001 | F-001.1 | Covered |
| FR-004 | Email confirmation with ARN | Notifications | E-001 | F-002 | F-002.1 | Covered |
| FR-005 | Applicant status lookup | Status | E-001 | F-002 | F-002.1 | Covered |
| FR-006 | AI scoring trigger on submission | Scoring | E-002 | F-003 | F-003.1 | Covered |
| FR-007 | Scoring explainability export | Scoring | E-002 | F-003 | F-003.1 | Covered |
| FR-008 | Scoring pipeline constraints | Scoring | E-002 | F-003 | F-003.1 | Covered |
| FR-009 | Experian credit retrieval | Integration | E-002 | F-004 | F-004.1 | Covered |
| FR-010 | AI threshold and routing | Scoring | E-002 | F-003 | F-003.1 | Covered |
| FR-011 | Auto-decline notification | Notifications | E-001 | F-002 | F-002.2 | Covered |
| FR-012 | AML screening before offer | Compliance | E-003 | F-005 | F-005.1 | Covered |
| FR-013 | KYC verification steps | Compliance | E-003 | F-005 | F-005.1 | Covered |
| FR-014 | Performance alerting and thresholds | NFR | E-005 | F-010 | F-010.1 | Covered |
| FR-015 | Underwriter queue presentation rules | Underwriter | E-003 | F-006 | F-006.1 | Covered |
| FR-016 | Underwriter queue metadata | Underwriter | E-003 | F-006 | F-006.1 | Covered |
| FR-017 | Underwriter action logging | Audit | E-003 | F-006 | F-006.2 | Covered |
| FR-018 | Underwriter escalation policy | Escalation | E-003 | F-006 | F-006.3 | Covered |
| FR-019 | Escalation notification behaviour | Escalation | E-003 | F-006 | F-006.3 | Covered |
| FR-020 | Offer template population | Offers | E-004 | F-008 | F-008.1 | Covered |
| FR-021 | Offer acceptance recording | Offers | E-004 | F-008 | F-008.1 | Covered |
| FR-022 | Observability export hooks | Observability | E-003 | F-007 | F-007.1 | Covered |
| FR-023 | Admin metrics exporters | Reporting | E-005 | F-011 | F-011.1 | Covered |
| FR-024 | Metrics retention/export | Reporting | E-005 | F-010 | F-010.1 | Covered |
| FR-025 | Disbursement reconciliation rules | Payments | E-004 | F-009 | F-009.2 | Covered |
| FR-026 | Disbursement follow-up tasks | Payments | E-004 | F-009 | F-009.2 | Covered |
| FR-027 | Manual investigation workflow | Payments | E-004 | F-009 | F-009.2 | Covered |
| FR-028 | Observability trend exports | Observability | E-003 | F-007 | F-007.1 | Covered |
| FR-029 | Reporting exports and retention | Reporting | E-005 | F-011 | F-011.1 | Covered |
| FR-030 | Lifecycle event emission | Observability | E-003 | F-007 | F-007.1 | Covered |

---

## Not Covered Requirements

None — all atomic requirements are mapped to features and at least one story.

---

## Coverage by Capability

| CAP-NNN | Capability | Total Reqs | Covered | Not Covered | Coverage |
|---|---|---|---|---|---|
| CAP-001 | Intake & Submission | 3 | 3 | 0 | 100% |
| CAP-002 | Scoring & Decisions | 4 | 4 | 0 | 100% |
| CAP-003 | Compliance & Underwriter | 4 | 4 | 0 | 100% |

---

## Coverage by Epic

| Epic | Total Reqs | Covered | Not Covered | Coverage |
|---|---|---|---|---|
| E-001 | 4 | 4 | 0 | 100% |
| E-002 | 4 | 4 | 0 | 100% |
| E-003 | 4 | 4 | 0 | 100% |
| E-004 | 3 | 3 | 0 | 100% |
| E-005 | 3 | 3 | 0 | 100% |

---

## Gaps and Risks

| Gap | Impact | Recommended Action |
|---|---|---|
| None identified in atomic requirements mapping | Low | Continue to monitor during story elaboration |

---
*Status: Draft — set to Accepted only after review.*
