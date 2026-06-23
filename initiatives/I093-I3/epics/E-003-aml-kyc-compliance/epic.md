# E-003 — AML/KYC Compliance

## Metadata

| Field | Value |
|---|---|
| Epic ID | E-003 |
| Initiative ID | I093-I3 |
| Wave | D1 |
| Priority | Must |
| Increment | D1 |
| Created at | 2026-06-22 |
| Created by | delivery-lead |
| Status | Draft |

---

## Business Objective

Enable automated AML and KYC checks during application intake to reduce manual review workload, ensure regulatory compliance, and prevent high-risk customers from progressing to offer generation.

---

## Scope

**In scope:**
- Customer identity verification and document validation
- Sanctions and PEP screening during onboarding
- Risk scoring for AML decisioning and reviewer handoff

**Out of scope:**
- Full case management system for investigations (handled by a downstream epic)

---

## High-Level Acceptance Criteria

- AC-E-001: The system performs identity verification and flags unverifiable applicants.
- AC-E-002: Sanctions/PEP matches produce a high-risk flag and create a reviewer task.

---

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| BRS | §AML/KYC | AML and KYC compliance requirements |
| Requirement | FR-012, FR-013, FR-014 | See requirements/atomic-requirements.md |

---

## Impacted Systems

| System / Module | Change Type | Notes |
|---|---|---|
| Applicant portal | Integration | upload documents, present verification UI |
| Identity Verification Service | New | integrate third-party vendor API |
| AML Screening Service | New | sanctions/PEP screening and scoring |

---

## Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| E-001 Application Intake | Epic | Yes | Intake must be able to accept documents and forward to verification |

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Third-party verification vendor downtime | Medium | High | Add retry/backoff, degrade to manual review path |

---

## Foundation / Setup

No foundation setup required beyond ensuring the Applicant portal can accept document uploads and a vendor account for identity verification is provisioned.

---

## Open Questions

| ID | Question | Proposed / Notes |
|---|---|---|
| OQ-003 | What is the fallback for HMRC KYC API when unavailable — manual verification or auto-refer? | Proposed: manual verification (see input/brs.md) |
| OQ-004 | What AML database providers beyond HM Treasury are required (Dow Jones, others)? | Proposed: HM Treasury only (see input/brs.md) |

*Resolution*: OQ-003 and OQ-004 have been resolved and signed off. See `input/checklists/hmrc-kvc-fallback.md` and `input/decisions/aml-provider-decision.md` for evidence. Central OQ catalogue updated to Closed.


## Stories

| Story ID | Title | Layers | Priority | Increment | Readiness |
|---|---|---|---|---|---|
| S-003.1 | Identity verification and document capture | Frontend / Backend / Integration | Must | D1 | Ready |
| S-003.2 | AML screening and sanctions check | Backend / Integration | Must | D1 | Ready |
| S-003.3 | Customer risk assessment and reviewer handoff | Backend / Integration | Must | D1 | Ready |

---

## Advisory Reviews

*This section is populated automatically by the advisory review step when enabled.*

---

*Status: Draft — set to Accepted only after epic review gate. Never self-accept.*
