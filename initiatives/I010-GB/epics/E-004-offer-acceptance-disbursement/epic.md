# E-004 — Offer, Acceptance & Disbursement

## Metadata

| Field | Value |
|---|---|
| Epic ID | E-004 |
| Initiative ID | I010-GB |
| Wave | 1 |
| Priority | Must |
| Increment | D1 |
| Created at | 2026-06-28 |
| Created by | delivery-lead |
| Status | Draft |

---

## Business Objective

Generate loan offers, capture applicant acceptance (digital signature), and orchestrate disbursement to the core banking system (Temenos T24). Deliver a reliable, auditable flow that preserves regulatory evidence and supports customer-facing acceptance tracking.

---

## Scope

**In scope:**
- Offer generation, presentation via portal and email, digital acceptance capture (DocuSign), cooling-off enforcement, and disbursement orchestration to T24.

**Out of scope:**
- Downstream accounting reconciliation and settlement reporting beyond disbursement confirmation handling.

---

## High-Level Acceptance Criteria

- AC-E-001: System can generate and present an offer with all required fields (amount, APR, terms) and persist an auditable offer document.
- AC-E-002: Applicant acceptance recorded via DocuSign with timestamp and IP, and triggers cooling-off logic.
- AC-E-003: Disbursement instruction sent to T24 with required fields and idempotent retries; confirmation handled and stored.

---

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| BRS | §5 Offer & Disbursement | Offer lifecycle and acceptance requirements |
| Requirement | FR-020..FR-026 | See implementation contract for per-requirement mapping |

---

## Impacted Systems

| System / Module | Change Type | Notes |
|---|---|---|
| Offer generation service / Intake API | New / Integration | New offer document schema and callbacks to DocuSign |
| DocuSign adapter | New / Integration | Callback handling and acceptance recording |
| Disbursement orchestration | New | T24 integration and idempotency logic |

---

## Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| E-002, E-003 | Epic | Yes | Scoring and compliance outcomes required before offer generation |

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| DocuSign contract or callback delays | Medium | High | Implement retry/backoff, offline acceptance queue, alerting |

---

## Foundation / Setup

No foundation setup required beyond provisioning the proposed `repo-intake-api` and DocuSign credentials; CI/CD infra will reuse existing pipelines.

---

## Stories

| Story ID | Title | Layers | Priority |
|---|---|---|---|
| S-004.0 | Offer generation end-to-end | frontend / backend / infrastructure / integration | Must |
| S-004.1 | Digital acceptance via DocuSign | frontend / backend / integration | Must |
| S-004.2 | Cooling-off notifications and enforcement | backend / integration | Must |
| S-004.3 | Disbursement orchestration to T24 | backend / integration / infrastructure | Must |

---

## Layer Coverage

| Layer | Covered by |
|---|---|
| frontend | S-004.0, S-004.1 |
| backend | S-004.0, S-004.1, S-004.2, S-004.3 |
| infrastructure | S-004.0, S-004.3 |
| integration | S-004.0, S-004.1, S-004.2, S-004.3 |


## Advisory Reviews

*Status: Draft — advisory reviews will be appended when enabled.*

---
*Status: Draft — set to Accepted only after epic review gate.*
