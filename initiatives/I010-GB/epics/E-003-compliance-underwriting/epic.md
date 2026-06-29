# E-003 — Compliance & Underwriting

## Metadata

| Field | Value |
|---|---|
| Epic ID | E-003 |
| Initiative ID | I010-GB |
| Title | Compliance & Underwriting |
| Priority | Must |
| Risk | High |
| Dependencies | E-002 |
| Created at | 2026-06-28 |
| Created by | delivery-lead |
| Status | Draft |

---

## Business Objective

Provide compliance orchestration and underwriter tools to detect AML/KYC issues, route cases to compliance, and support manual underwriting decisions with explainability artifacts.

---

## Scope

In scope:
- AML/KYC orchestration and HMRC identity verification (FR-012, FR-013).
- Underwriter queue and case detail UI and APIs (FR-015..FR-018).
- Compliance hold routing and audit trails (FR-014, FR-018).

Out of scope:
- Scoring model implementation (E-002).

---

## Acceptance Criteria

- AC-E-003-1: AML screening completes within SLA and flags `COMPLIANCE_HOLD` on failure.
- AC-E-003-2: Underwriter dashboard shows required fields and explainability artifacts for reviewed cases.
- AC-E-003-3: Compliance holds are auditable and immutable.

---

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| Functional | FR-012 | AML screening before offer generation |
| Functional | FR-013 | KYC identity verification |
| Functional | FR-014 | COMPLIANCE_HOLD routing |
| Functional | FR-015 | Underwriter queue rules |
| Functional | FR-016 | Underwriter dashboard contents |
| Functional | FR-017 | Underwriter actions |
| Functional | FR-018 | Audit and retention for compliance |

---

## Impacted Systems

| System | Change Type | Notes |
|---|---|---|
| AML/KYC orchestrator | New | Integrate HMRC and third-party verifiers |
| Underwriter dashboard | New | UI and APIs to support casework |
| Audit store | Change | Ensure hold reasons are recorded immutably |

---

## Stories

| Story ID | Title | Layers | Priority |
|---|---|---|---|
| S-003.0 | Compliance e2e POC | frontend / backend / infrastructure / integration | Must |
| S-003.1 | AML orchestration connector | backend / integration | Must |
| S-003.2 | Underwriter case API | backend / frontend | Must |

---

## Advisory Reviews

*Status: Draft — proceed to review after technical validation.*
