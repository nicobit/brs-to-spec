# Requirement Coverage Report

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I010-GB |
| Created at | 2026-06-28T13:12:22.828235Z |
| Created by | delivery-lead |
| Status | Draft |

---

## Planned Coverage Summary

| Metric | Value |
|---|---|
| Total requirements (from atomic-requirements) | 41 |
| Assigned to an epic in delivery skeleton | 41 |
| Unassigned | 0 |
| Planned coverage | 100% |

---

## Generated Coverage Summary

| Metric | Value |
|---|---|
| Total requirements (computed) | 40 |
| In-scope requirements (elaborated epics) | 40 |
| Covered by at least one story | 40 |
| Not covered | 0 |
| Generated coverage (in-scope) | 100% |
| Deferred to later waves | 1 |

---

## Full Coverage Matrix

| REQ / FR | Requirement Title | Epic | Feature | Story | Open Questions Propagated | Elaboration Status | Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| FR-001 | Loan application submission | E-001 | F-001 | S-001.0 | No | elaborated | epics/E-001-intake-submission/stories/S-001.0-intake-e2e.md, epics/E-001-intake-submission/stories/S-001.2-intake-api-submit.md, epics/E-001-intake-submission/stories/S-001.3-frontend-infra-spike.md | Covered |
| FR-002 | Inline validation before submission | E-001 | F-001 | S-001.2 | No | elaborated | epics/E-001-intake-submission/stories/S-001.2-intake-api-submit.md | Covered |
| FR-003 | Assign Application Reference Number (ARN) | E-001 | F-001 | S-001.2 | No | elaborated | epics/E-001-intake-submission/stories/S-001.2-intake-api-submit.md | Covered |
| FR-004 | Email confirmation within 2 minutes | E-001 | F-001 | S-001.1 | No | elaborated | epics/E-001-intake-submission/stories/S-001.1-intake-email-poc.md | Covered |
| FR-005 | Retrieve status by ARN and DOB | E-001 | F-001 | S-001.4 | No | elaborated | epics/E-001-intake-submission/stories/S-001.4-status-lookup.md | Covered |
| FR-006 | Trigger AI pre-screening within 60s | E-002 | F-002 | S-002.0 | No | elaborated | epics/E-002-decisioning-scoring/stories/S-002.0-scoring-e2e.md | Covered |
| FR-007 | Produce risk score and recommendation | E-002 | F-002 | S-002.0 | No | elaborated | epics/E-002-decisioning-scoring/stories/S-002.0-scoring-e2e.md | Covered |
| FR-008 | Model inputs for scoring | E-002 | F-002 | S-002.0 | Yes | elaborated | epics/E-002-decisioning-scoring/stories/S-002.0-scoring-e2e.md | Covered |
| FR-009 | Experian integration | — | — | — | N/A | unassigned | — | **Not Covered** |
| FR-010 | AUTO_APPROVE flow for ≤£10,000 | E-002 | F-002 | S-002.0 | No | elaborated | epics/E-002-decisioning-scoring/stories/S-002.0-scoring-e2e.md, epics/E-002-decisioning-scoring/stories/S-002.1-scoring-ingestion.md | Covered |
| FR-011 | AUTO_DECLINE notification and cooling-off | E-002 | F-002 | S-002.0 | No | elaborated | epics/E-002-decisioning-scoring/stories/S-002.0-scoring-e2e.md, epics/E-002-decisioning-scoring/stories/S-002.1-scoring-ingestion.md | Covered |
| FR-012 | AML screening before offer generation | E-003 | F-003 | S-003.0 | Yes | elaborated | epics/E-003-compliance-underwriting/stories/S-003.0-compliance-e2e.md, epics/E-003-compliance-underwriting/stories/S-003.1-aml-orchestration.md | Covered |
| FR-013 | KYC identity verification | E-003 | F-003 | S-003.0 | Yes | elaborated | epics/E-003-compliance-underwriting/stories/S-003.0-compliance-e2e.md, epics/E-003-compliance-underwriting/stories/S-003.1-aml-orchestration.md | Covered |
| FR-014 | COMPLIANCE_HOLD routing | E-003 | F-003 | S-003.0 | No | elaborated | epics/E-003-compliance-underwriting/stories/S-003.0-compliance-e2e.md | Covered |
| FR-015 | Underwriter queue rules | E-003 | F-003 | S-003.0 | No | elaborated | epics/E-003-compliance-underwriting/stories/S-003.0-compliance-e2e.md | Covered |
| FR-016 | Underwriter dashboard contents | E-003 | F-003 | S-003.0 | No | elaborated | epics/E-003-compliance-underwriting/stories/S-003.0-compliance-e2e.md | Covered |
| FR-017 | Underwriter actions | E-003 | F-003 | S-003.0 | No | elaborated | epics/E-003-compliance-underwriting/stories/S-003.0-compliance-e2e.md | Covered |
| FR-018 | Immutable underwriter action record | E-003 | F-003 | S-003.0 | No | elaborated | epics/E-003-compliance-underwriting/stories/S-003.0-compliance-e2e.md, epics/E-003-compliance-underwriting/stories/S-003.2-underwriter-case-api.md, epics/E-005-platform-observability/stories/S-005.0-platform-e2e.md | Covered |
| FR-019 | Escalation after 4 business hours | E-003 | F-003 | S-003.2 | No | elaborated | epics/E-003-compliance-underwriting/stories/S-003.2-underwriter-case-api.md | Covered |
| FR-020 | Loan offer content | E-004 | F-004 | S-004.0 | No | elaborated | epics/E-004-offer-acceptance-disbursement/stories/S-004.0-offer-generation-e2e.md | Covered |
| FR-021 | Present offer via portal and email | E-004 | F-004 | S-004.0 | No | elaborated | epics/E-004-offer-acceptance-disbursement/stories/S-004.0-offer-generation-e2e.md | Covered |
| FR-022 | Digital acceptance via DocuSign | E-004 | F-004 | S-004.1 | No | elaborated | epics/E-004-offer-acceptance-disbursement/stories/S-004.1-digital-acceptance.md, epics/E-004-offer-acceptance-disbursement/stories/S-004.2-cooling-off.md | Covered |
| FR-023 | 14-day cooling-off enforcement | E-004 | F-004 | S-004.1 | Yes | elaborated | epics/E-004-offer-acceptance-disbursement/stories/S-004.1-digital-acceptance.md, epics/E-004-offer-acceptance-disbursement/stories/S-004.2-cooling-off.md | Covered |
| FR-024 | Trigger disbursement to T24 | E-004 | F-004 | S-004.3 | No | elaborated | epics/E-004-offer-acceptance-disbursement/stories/S-004.3-disbursement-orchestration.md | Covered |
| FR-025 | Disbursement instruction fields | E-004 | F-004 | S-004.3 | No | elaborated | epics/E-004-offer-acceptance-disbursement/stories/S-004.3-disbursement-orchestration.md | Covered |
| FR-026 | Disbursement confirmation handling and retries | E-004 | F-004 | S-004.3 | No | elaborated | epics/E-004-offer-acceptance-disbursement/stories/S-004.3-disbursement-orchestration.md | Covered |
| FR-027 | Applicant notification on disbursement | E-001 | F-001 | S-001.1 | No | elaborated | epics/E-001-intake-submission/stories/S-001.1-intake-email-poc.md | Covered |
| FR-028 | Immutable audit log of state transitions | E-005 | F-005 | S-005.1 | No | elaborated | epics/E-005-platform-observability/stories/S-005.1-platform-audit-append.md | Covered |
| FR-029 | Admin dashboard metrics and refresh | E-005 | F-005 | S-005.1 | No | elaborated | epics/E-005-platform-observability/stories/S-005.1-platform-audit-append.md | Covered |
| FR-030 | Emit structured observability events | E-005 | F-005 | S-005.1 | No | elaborated | epics/E-005-platform-observability/stories/S-005.1-platform-audit-append.md | Covered |
| NFR-001 | Intake form load time | E-001 | F-001 | S-001.0 | No | elaborated | epics/E-001-intake-submission/stories/S-001.0-intake-e2e.md | Covered |
| NFR-002 | AI scoring pipeline latency | E-002 | F-002 | S-002.0 | No | elaborated | epics/E-002-decisioning-scoring/stories/S-002.0-scoring-e2e.md | Covered |
| NFR-003 | Concurrency support | E-002 | F-002 | S-002.0 | No | elaborated | epics/E-002-decisioning-scoring/stories/S-002.0-scoring-e2e.md, epics/E-002-decisioning-scoring/stories/S-002.2-explainability-store.md | Covered |
| NFR-004 | PII encryption | E-001 | F-001 | S-001.0 | No | elaborated | epics/E-001-intake-submission/stories/S-001.0-intake-e2e.md, epics/E-001-intake-submission/stories/S-001.1-intake-email-poc.md, epics/E-001-intake-submission/stories/S-001.2-intake-api-submit.md, epics/E-001-intake-submission/stories/S-001.3-frontend-infra-spike.md, epics/E-001-intake-submission/stories/S-001.4-status-lookup.md | Covered |
| NFR-005 | Audit log durability | E-005 | F-005 | S-005.1 | No | elaborated | epics/E-005-platform-observability/stories/S-005.1-platform-audit-append.md | Covered |
| NFR-006 | Uptime | E-005 | F-005 | S-005.0 | No | elaborated | epics/E-005-platform-observability/stories/S-005.0-platform-e2e.md | Covered |
| NFR-007 | Integration resilience | E-002 | F-002 | S-002.0 | No | elaborated | epics/E-002-decisioning-scoring/stories/S-002.0-scoring-e2e.md, epics/E-002-decisioning-scoring/stories/S-002.2-explainability-store.md | Covered |
| C-001 | FCA Consumer Duty compliance | E-004 | F-004 | S-004.3 | No | elaborated | epics/E-004-offer-acceptance-disbursement/stories/S-004.3-disbursement-orchestration.md | Covered |
| C-002 | UK GDPR and data residency | E-004 | F-004 | S-004.3 | No | elaborated | epics/E-004-offer-acceptance-disbursement/stories/S-004.3-disbursement-orchestration.md | Covered |
| C-003 | Temenos T24 integration | E-004 | F-004 | S-004.3 | Yes | elaborated | epics/E-004-offer-acceptance-disbursement/stories/S-004.3-disbursement-orchestration.md | Covered |
| C-004 | Experian and DocuSign mandated integrations | E-004 | F-004 | S-004.3 | No | elaborated | epics/E-004-offer-acceptance-disbursement/stories/S-004.3-disbursement-orchestration.md | Covered |

---

## Not Covered Requirements

| REQ / FR | Requirement Title | Reason | Recommended Action |
|---|---|---|---|
| FR-009 | Experian integration | Not covered by current stories | Add story in relevant epic or re-scope |

---

## Gaps and Risks

- FR-008: What is the approved AI model vendor / approach for risk scoring?
- FR-023: Does the cooling-off waiver require legal sign-off?
- FR-013: Fallback for HMRC KYC when unavailable?
- FR-012: Exact AML database providers required
- C-003: Is the T24 payment gateway API contract defined?
