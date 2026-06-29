# E-003 — Compliance & KYC

## Metadata

| Field | Value |
|---|---|
| Epic ID | E-003 |
| Initiative ID | I011-MB |
| Wave | Wave 2 |
| Priority | Must |
| Increment | D1 |
| Created at | 2026-06-28 |
| Created by | delivery-lead |
| Status | Draft |

---

## Business Objective

Provide AML and KYC checks integrated into the submission and scoring workflow to ensure regulatory compliance and safe decisioning. Failure to deliver prevents compliant offer generation.

---

## Scope

**In scope:**
- KYC verification using HMRC API and NI matching
- AML screening against sanction lists
- Compliance hold routing and audit entries

**Out of scope:**
- Manual remediation workflows beyond routing to compliance team

---

## High-Level Acceptance Criteria

- AC-E-001: KYC verification completes within 60 seconds when required (FR-013).
- AC-E-002: AML screening performed and compliance hold applied when checks fail (FR-012, FR-014).

---

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| FR-012 | AML screening | FR-012 |
| FR-013 | KYC verification | FR-013 |
| FR-014 | Compliance hold routing | FR-014 |
| FR-030 | Observability events | FR-030 |

---

## Impacted Systems

| System / Module | Change Type | Notes |
|---|---|---|
| KYC Adapter | Integration | HMRC API integration |
| Compliance Worker | Backend API | Routing and holds |
| AuditStore | Change | Ensure audit entries for holds and decisions |

---

## Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| E-002 Scoring | Epic | Yes | KYC may be triggered post-scoring |

---

## Stories

| Story ID | Title | Layers | Priority | Increment | Readiness |
|---|---|---|---|---|---|
| S-003.1 | Implement KYC HMRC adapter | Integrations | Must | D1 | Not Ready |
| S-003.2 | AML screening worker & rules | Backend API | Must | D1 | Not Ready |
| S-003.3 | Compliance hold routing & audit | Backend API / Infrastructure | Must | D1 | Not Ready |
| S-003.4 | Provision Compliance infra | Infrastructure | Must | D1 | Not Ready |
| S-003.5 | UI: Compliance flags in underwriter panel | Frontend | Must | D2 | Not Ready |

---

*Status: Draft.*
