# Architecture Review

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I011-MB |
| Created at | 2026-06-28 |
| Created by | architect |
| Status | Draft |

## Initiative-Architecture Fit

| Feature Area | Existing Components Touched | New Components / Boundaries | Contract Changes | Blast Radius |
|---|---|---|---|---|
| Application Intake | Applicant portal, email service, ARN generator | New intake API, validation service | None initially | Medium |
| AI Pre-screening & Scoring | ML model runtime, feature store | Scoring service, explainability store | Model contract with explainability | High |
| AML / KYC | HMRC API, sanctions lists | Compliance queue, PEP screening service | None | High |
| Underwriter Workflow | Underwriter UI, queueing system | Enhanced underwriter dashboard | None | Medium |
| Offer & Disbursement | DocuSign, Temenos T24 gateway | Offer generator, payment orchestration | T24 contract updates | High |

## Architecture Constraints

| ID | Constraint | Rationale | Violation Consequence | Source |
|---|---|---|---|---|
| ARCH-C-001 | All personal data must remain in UK datacentres | UK GDPR and data residency requirements | Regulatory breach; stop deployment | input/brs.md C-002 |
| ARCH-C-002 | Use Experian CreditExpert for credit reports | Enterprise contract requirement | Integration non-compliance; rework | input/brs.md C-003 |
| ARCH-C-003 | AI models must be explainable and auditable | FCA requirements for explainability | Disallowed model; require redesign | input/brs.md C-004 |

*Note: These constraints will be normalized into AR-NNN identifiers in the Architecture Rules artifact.*

## Brownfield Impact

| Component | Change Type | Consumers | Backward Compatible? | Migration Required | Rollback Possible |
|---|---|---|---|---|---|
| Temenos T24 gateway | Integration contract / new disbursement flow | Core banking, operations | Yes | Yes | Medium |
| Experian CreditExpert | New integration | Scoring pipeline | Yes | Yes | Medium |
| HMRC KYC API | New integration | Compliance workflow | Yes | Yes | Medium |

**Regression surface:** Underwriting decisions and disbursement flows are at risk if integration latencies or schema changes occur.

**Rollback sensitivity:** Medium - rolling back requires coordination with core banking and notification to operations.

## Quality Attribute Assessment

| Attribute | Requirement (from BRS) | Assessment | Risk |
|---|---|---|---|
| Performance | NFR-001, NFR-002 | Scoring pipeline target 90s; intake <2s – requires optimized prefetch and caching | High for scoring under load |
| Security | NFR-004, FR-012/FR-013 | PII encryption and AML/KYC gating required | High (regulatory) |
| Scalability | NFR-003 | Must support 500 concurrent submissions; design for horizontal scaling | Medium |
| Availability | NFR-006 | 99.9% during business hours | Medium-High |

## Open Decisions

| DEC-001 | Which AI model vendor and deployment pattern will be used (in-house vs third-party)? | Head of AI | Use Azure Foundry as initial vendor | Before model selection and training |
| DEC-002 | Final contract terms with Temenos T24 for disbursement API | IT Architecture | Assume internal payment gateway available | Before disbursement implementation |

## Active Assumptions

| Assumption | Source | If False, Then |
|---|---|---|
| Experian contract endpoints are available | input/brs.md C-003 | Route to underwriter for missing reports; increase manual work |
| HMRC KYC API has required matching capabilities | input/brs.md FR-013 | Implement manual verification fallback; increased ops load |

## Known Unknowns

| Unknown | Impact | Discovery Path |
|---|---|---|
| Exact SLAs and throttling limits for Experian and HMRC APIs | May affect scoring latency and routing | Confirm with integration teams and run load tests |

---
*Set Status: Draft — for architecture review and gate validation.*
