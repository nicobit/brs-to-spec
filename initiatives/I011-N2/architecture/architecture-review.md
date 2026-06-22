# Architecture Review

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I011-N2 |
| Created at | 2026-06-21 |
| Created by | architect |
| Status | Draft |

## Initiative-Architecture Fit

| Feature Area | Existing Components Touched | New Components / Boundaries | Contract Changes | Blast Radius |
|---|---|---|---|---|
| Applicant intake & portal | Applicant Portal (React/Static Web App), Notification Service | None | None | Low |
| AI Scoring & Pre-screening | AI Scoring Service (new) | New inference service boundary; explanation metadata contract required | New scoring contract; Experian integration | Medium |
| AML/KYC compliance | Compliance Service (new) | Integration to HM Treasury / HMRC | Sanctions/KYC contract | High |
| Underwriter workflow | Underwriter Dashboard (Static Web App), Loan Origination API | Queue semantics and audit contract | Internal API changes; audit store usage | Medium |
| Offer & Disbursement | Notification Service, Payment Gateway Adapter | DocuSign integration; T24 adapter | DocuSign and T24 API contracts | High |

## Architecture Constraints

| ID | Constraint | Rationale | Violation Consequence | Source |
|---|---|---|---|---|
| ARCH-C-001 | All data in UK regions only | GDPR / data residency requirement | Non-compliance risk; stop delivery | BRS: Constraints; architecture draft |
| ARCH-C-002 | AI models must be explainable and provide decision metadata | FCA explainability requirement | Model deployment blocked; regulatory risk | BRS: constraints |
| ARCH-C-003 | External integrations must implement circuit breakers and fallbacks | Availability and compliance | Increased failure surface; route to manual review | NFR-007; architecture draft |

*Note: These constraints will be normalized into architecture rules for downstream artifacts.*

## Brownfield Impact

| Component | Change Type | Consumers | Backward Compatible? | Migration Required | Rollback Possible |
|---|---|---|---|---|---|
| Temenos T24 integration (Payment Gateway Adapter) | New adapter | Core banking, Disbursement pipeline | Yes (adapter pattern) | Yes | Yes |
| Applicant Portal | Modified (new fields, flow) | Applicants | Yes | Yes | Yes |
| Audit Log Store (Cosmos DB) | New append-only usage | All services writing audit entries | Yes | Yes | No |

**Regression surface:** Payment/disbursement and audit pathways are highest risk due to financial impact and regulatory visibility. Integration contract and error handling must be validated.

**Rollback sensitivity:** High for disbursement and audit flows — any rollback complexity requires manual reconciliation.

## Quality Attribute Assessment

| Attribute | Requirement (from BRS) | Assessment | Risk |
|---|---|---|---|
| Performance | NFR-002: scoring completes within 90s | Achievable with dedicated inference service and caching; monitor under load | Medium (depends on model & Experian latency) |
| Security | NFR-004: AES-256 at rest, TLS 1.3 | Platform supports required encryption; must enforce key management and RBAC | High if misconfigured |
| Scalability | NFR-003: 500 concurrent submissions | Requires autoscaling for API and scoring services; queue backpressure | Medium |
| Availability | NFR-006: 99.9% during business hours | Design for multi-region (UK South/UK West) and circuit breakers | Medium-High (external deps affect availability) |

## Open Decisions

| DEC-NNN | Question | Owner | Default Assumption | Required Before |
|---|---|---|---|---|
| DEC-001 | AI model vendor / approach (in-house vs Experian PowerCurve) | Head of AI | Azure Foundry (per OQ-001) | Model selection and explainability design |
| DEC-002 | HMRC KYC fallback behaviour (manual verification vs auto-refer) | Compliance | Manual verification | Compliance workflow implementation |
| DEC-003 | T24 payment gateway contract status | IT Architecture | Adapter can be defined internally | Disbursement integration workstream |

## Active Assumptions

| Assumption | Source | If False, Then |
|---|---|---|
| Experian contract and API availability | BRS / constraints | Route to underwriter; increase manual work |
| DocuSign e-sign contract in place | BRS | Use alternate e-sign provider or manual acceptance flow |
| Azure-managed keys and UK region tenancy available | Architecture draft | Revisit key management and hosting choices |

## Known Unknowns

| Unknown | Impact | Discovery Path |
|---|---|---|
| Exact Experian API latency under peak | Affects scoring SLA and routing | Performance testing with partner data |
| T24 payment gateway contract details | Affects disbursement contract and rollback | Procurement and API review |

---
*Set Status: Draft — requires architecture review and human approval for constraints and high-risk integrations.*
