# Architecture Review

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I0092-I1 |
| Created at | 2026-06-22 |
| Created by | architect |
| Status | Draft |

## Initiative-Architecture Fit

| Feature Area | Existing Components Touched | New Components / Boundaries | Contract Changes | Blast Radius |
|---|---|---|---|---|
| Application intake & scoring | Applicant Portal, Loan Origination API, AI Scoring Service, Experian integration | AI Scoring Service, Notification Service, Audit Log Store | Experian API contract; DocuSign, T24 adapters | Medium |
| Underwriter workflow | Underwriter Dashboard, Loan Origination API, Audit Log Store | Underwriter queue and escalation integration | Audit schema contract | Low |
| Offer & disbursement | Loan Origination API, Payment Gateway Adapter, T24 | Payment Gateway Adapter integration to T24 | Internal payment gateway contract | High |

## Architecture Constraints

| ID | Constraint | Rationale | Violation Consequence | Source |
|---|---|---|---|---|
| ARCH-C-001 | All PII and audit data must reside in Azure UK South or UK West | GDPR and bank data residency policy | Block deployment; legal non-compliance | input/architecture.md, BRS Constraints |
| ARCH-C-002 | AI scoring must provide explainability artifacts for every decision | FCA requirements for explainability | Cannot use black-box models; audit findings | input/brs.md (constraint: explainable models) |
| ARCH-C-003 | Audit log must be append-only and tamper-evident (Cosmos DB) | Regulatory auditability and OBJ-003 | Regulatory non-compliance; block go-live | input/architecture.md, FR-028 |
| ARCH-C-004 | External integrations must implement circuit breakers with fallbacks | NFR-007, operational safety | Increased failure and involuntary automation; route to manual review | input/architecture.md, NFR-007 |

## Brownfield Impact

Write `Greenfield - no brownfield impact` if not applicable.

| Component | Change Type | Consumers | Backward Compatible? | Migration Required | Rollback Possible |
|---|---|---|---|---|---|
| Loan Origination API | New / Expanded orchestration | Underwriter Dashboard, Notification Service, Payment Gateway | Yes | Minimal data migration for ARN mapping | Yes |

**Regression surface:** Underwriter workflows and audit logging are high-sensitivity areas; changes must avoid altering audit schema.

**Rollback sensitivity:** Medium — must ensure no data-loss for in-flight applications.

## Quality Attribute Assessment

| Attribute | Requirement (from BRS) | Assessment | Risk |
|---|---|---|---|
| Performance | NFR-002, FR-009 latency budgets | Architecture supports async scoring and Service Bus; must size AI service and Experian calls | Medium (depends on Experian SLA)
| Security | NFR-004, FR-012..FR-014 | PII encryption, Azure AD for staff, managed identities for services | High (regulatory impact)
| Scalability | NFR-003 | Design uses Azure App Services + Container Apps + Service Bus for decoupling | Medium (requires capacity planning)
| Availability | NFR-006 | Multi-region (UK South primary, UK West DR) planned; graceful degradation routes to manual review | Medium |

## Open Decisions

| DEC-NNN | Question | Owner | Default Assumption | Required Before |
|---|---|---|---|---|
| DEC-001 | AI model vendor / in-house vs third-party | Head of AI | Use Azure Foundry-based in-house model (per OQ-001) | Model selection and explainability approach |
| DEC-002 | HMRC KYC fallback behaviour (manual vs auto-refer) | Compliance | Manual verification queue | Implementation of Compliance Service flows |
| DEC-003 | T24 payment gateway contract details | IT Architecture | Internal payment gateway adapter available | Disbursement integration workstream |

## Active Assumptions

| Assumption | Source | If False, Then |
|---|---|---|
| Experian enterprise contract exists and meets latency SLAs | input/brs.md | Route more work to underwriters; higher manual load |
| DocuSign contract available | input/brs.md | Replace with alternative e-sign provider or postpone e-sign integration |
| Audit log implemented in append-only Cosmos DB | input/architecture.md | Require new storage solution or redesign audit retention |

## Known Unknowns

| Unknown | Impact | Discovery Path |
|---|---|---|
| Exact T24 API contract and error semantics | Affects disbursement reliability and retry semantics | Confirm with IT Architecture and run integration tests |

---
*Set Status: Draft — this architecture review requires human architect acceptance before proceeding to create architecture rules.*
