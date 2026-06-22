# Architecture Review

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I111-N11 |
| Created at | 2026-06-22 |
| Created by | architect |
| Status | Draft |

## Initiative-Architecture Fit

| Feature Area | Existing Components Touched | New Components / Boundaries | Contract Changes | Blast Radius |
|---|---|---|---|---|
| Application Intake & Scoring | Applicant Portal, Loan Origination API, AI Scoring Service, Service Bus | AI Scoring Service (container), Compliance Service | Experian, HMRC, DocuSign, T24 contracts | Medium |
| Offer & Disbursement | Loan Origination API, Payment Gateway Adapter, T24 | Payment Gateway contract surface | T24 contract required (OQ-005) | High |
| Underwriter & Admin UIs | Underwriter Dashboard, Admin Dashboard | None | None | Low |

## Architecture Constraints

| ID | Constraint | Rationale | Violation Consequence | Source |
|---|---|---|---|---|
| ARCH-001 | All data and services must remain in UK regions (UK South/West) | GDPR data residency requirement | Non-compliance / regulatory risk | input/architecture.md; BRS Constraints |
| ARCH-002 | AI decisions must be explainable and auditable | FCA and audit trail requirement | Block releases until explainability is provided | input/brs.md (constraints) |
| ARCH-003 | Integration calls must use circuit-breakers and defined fallbacks | Maintain availability and predictable failure modes | Increased incidents and incorrect auto-decisions | input/brs.md NFR-007 |

## Brownfield Impact

Write `Greenfield - no brownfield impact` if not applicable.

| Component | Change Type | Consumers | Backward Compatible? | Migration Required | Rollback Possible |
|---|---|---|---|---|---|
| Temenos T24 payment gateway | Integration / adapter | Core banking, Disbursement workflows | Yes (adapter) | Yes — contract and testing | Yes (retry/compensating) |

**Regression surface:** Disbursement integration risks affecting settlement and reporting if contract differences exist.

**Rollback sensitivity:** High — financial ledger implications; requires manual reconciliation.

## Quality Attribute Assessment

| Attribute | Requirement (from BRS) | Assessment | Risk |
|---|---|---|---|
| Performance | NFR-002 — scoring <= 90s | Achievable with autoscaling + async patterns; depends on Experian and model latency | Medium (external API dependency) |
| Security | NFR-004 — encryption, managed identities | Strong: Azure-managed keys, API Management, RBAC recommended | Low (requires strict config) |
| Scalability | NFR-003 — 500 concurrent submissions | Use Service Bus buffering, autoscale, containerized scoring | Medium (requires load testing) |
| Availability | NFR-006 — 99.9% business hours | Multi-region deployment + DR plan recommended | Medium (operational complexity) |

## Open Decisions

| DEC-NNN | Question | Owner | Default Assumption | Required Before |
|---|---|---|---|---|
| DEC-001 | Model vendor / approach (in-house vs third-party) | Head of AI | Use Azure Foundry prototype; finalize vendor during design | AI design and explainability artefacts |
| DEC-002 | T24 contract readiness and API surface | IT Architecture | Payment gateway adapter contract required | Disbursement implementation (REQ-016) |

## Active Assumptions

| Assumption | Source | If False, Then |
|---|---|---|
| Experian API is available within latency budget | input/brs.md FR-009 | Route to REFER_TO_UNDERWRITER; increase manual queue capacity |
| DocuSign contract and callbacks reliable | input/brs.md FR-022 | Fallback to email-based acceptance and manual processing |

## Known Unknowns

| Unknown | Impact | Discovery Path |
|---|---|---|
| Exact model explainability output format required by FCA | Affects scoring service design and event contract | Prototype model and consult compliance |

---
*Set Status: Accepted only by workflow or human approval when applicable. Never self-accept.*
