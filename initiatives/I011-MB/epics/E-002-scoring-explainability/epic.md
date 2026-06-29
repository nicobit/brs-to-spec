# E-002 — Scoring & Explainability

## Metadata

| Field | Value |
|---|---|
| Epic ID | E-002 |
| Initiative ID | I011-MB |
| Wave | Wave 2 |
| Priority | Must |
| Increment | D1 |
| Created at | 2026-06-28 |
| Created by | delivery-lead |
| Status | Draft |

---

## Business Objective

Validate and deliver an auditable AI scoring pipeline that produces risk scores and explainability traces usable by underwriters and for regulatory audit. Failure to deliver this epic prevents automated decisioning and regulatory compliance for AI-driven scores.

---

## Scope

**In scope:**
- Scoring service that consumes `application.submitted` events and computes risk scores and recommendations
- ExplainabilityStore schema and persistence for traceability
- `/scores/{id}` API to return score + explainability payload
- Experian integration for credit data used by scoring

**Out of scope:**
- Underwriter UI implementation (covered in E-004)
- Offer generation and e-sign (E-005)

---

## High-Level Acceptance Criteria

- AC-E-001: Scoring pipeline produces a risk score and a recommendation in {AUTO_APPROVE, REFER_TO_UNDERWRITER, AUTO_DECLINE} for each submission (FR-007).
- AC-E-002: Scoring end-to-end completes within 90 seconds under normal load (NFR-002).
- AC-E-003: Explainability payload for each scored application is persisted and retrievable via `/scores/{id}` (AP-002 / SD-002 / D-002).

---

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| Requirement | FR-007 | Risk score and recommendation |
| Requirement | FR-008 | Scoring inputs |
| Requirement | FR-009 | Experian integration |
| Requirement | FR-030 | Observability events |
| NFR | NFR-002 | Scoring pipeline latency |
| Constraint | C-004 | Explainability required |

---

## Impacted Systems

| System / Module | Change Type | Notes |
|---|---|---|
| Scoring Service | New / Changed | Containerised ML runtime, scoring and explainability export |
| ExplainabilityStore | New | Persist explainability traces and query API |
| Experian Adapter | Integration | Credit bureau data for scoring inputs |
| /scores API | New | Expose score + explainability to UI and audit consumers |

---

## Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| E-001 Intake & Submission | Epic | Yes | Scoring consumes submission events and ARN mapping |
| Experian integration | External | Yes | Credit data required for scoring; circuit breaker per NFR-007 |

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Model explainability incomplete for regulatory needs | Medium | High | Use Azure Foundry explainability features; persist traces in ExplainabilityStore (D-002) |
| External API latency (Experian) delaying scoring | High | High | Circuit breakers, retries, fallback to manual referral, early integration testing |

---

## Foundation / Setup

Provision AKS cluster or container host for ML runtime, configure GPU-enabled nodes if required, and create ExplainabilityStore (nb-repo). Ensure audit-compliant retention and UK-only data residency.

---

## Stories

| Story ID | Title | Layers | Priority | Increment | Readiness |
|---|---|---|---|---|---|
| S-002.1 | Implement Scoring Service processor | Backend API / Backend | Must | D1 | Not Ready |
| S-002.2 | ExplainabilityStore schema and persistence | Backend API / Infrastructure | Must | D1 | Not Ready |
| S-002.3 | Experian adapter and resilience | Integrations | Must | D1 | Not Ready |
| S-002.4 | Provision ML runtime infra (AKS) | Infrastructure | Must | D1 | Not Ready |
| S-002.5 | Implement GET /scores/{id} API | Backend API | Must | D1 | Not Ready |

---

## Advisory Reviews

*This section will be populated by advisory review personas if enabled.*

---
*Status: Draft — set to Accepted only after epic review gate.*
