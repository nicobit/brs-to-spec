# Architecture Review

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I010-GB |
| Created at | 2026-06-28 |
| Created by | architect |
| Status | Draft |

## Initiative-Architecture Fit

| Feature Area | Existing Components Touched | New Components / Boundaries | Contract Changes | Blast Radius |
|---|---|---|---|---|
| Application Intake | Web frontend, email subsystem | Intake API, ARN service | None initially | Medium |
| AI Pre-Screening & Scoring | Model hosting, feature store | Scoring pipeline, explainability service | Integration with model telemetry | High |
| Experian Integration | Integration platform / API gateway | Credit adapter with circuit-breaker | Experian API contract | Medium |
| AML / KYC | Compliance queue, casework tools | AML/KYC orchestration service | HMRC/HM Treasury connectors | High |
| Underwriter Workflow | Case management queue | Underwriter dashboard service | None (UI integration) | Medium |
| Disbursement | Internal payment gateway, Temenos T24 | Disbursement orchestration | T24 payment contract | High |
| Observability & Audit | Logging platform, event bus | Immutable audit store, structured events | Storage and retention contracts | High |

## Architecture Constraints

| ID | Constraint | Rationale | Violation Consequence | Source |
|---|---|---|---|---|
| ARCH-C-001 | All production personal data must reside in UK datacenters | UK GDPR / data residency requirement | Legal non-compliance, regulatory fines | input/brs.md - Constraints |
| ARCH-C-002 | Use Experian CreditExpert for credit reports | Enterprise supplier contract | Supplier mismatch and contractual breach | input/brs.md - FR-009 |
| ARCH-C-003 | Use DocuSign for e-signatures | Enterprise supplier contract | Rework of acceptance flow | input/brs.md - FR-022 |
| ARCH-C-004 | Integrate with Temenos T24 for disbursement | Core banking requirement | Disbursement failure, operational risk | input/brs.md - C-003 |
| ARCH-C-005 | AI models must be explainable and produce rationale | FCA explainability requirement | Regulatory non-acceptance of automated decisions | input/brs.md - Constraints |

*Note: These constraints will be normalized into `AR-NNN` identifiers in the Architecture Rules artifact.*

## Brownfield Impact

Greenfield and brownfield mix: moderate brownfield impact where Experian, T24, and existing logging/identity systems are touched.

| Component | Change Type | Consumers | Backward Compatible? | Migration Required | Rollback Possible |
|---|---|---|---|---|---|
| Temenos T24 (payment gateway) | New boundary / Adapter | Core banking, operations | Yes | Yes | Yes |
| Experian Credit adapter | New adapter | Scoring pipeline, compliance | Yes | Yes | Yes |
| Audit store (immutable) | New component | All services emitting events | Yes | Yes | Partial |

**Regression surface:** Integrations with T24 and Experian are high-risk: payment and credit flows can break onboarding and disbursement.

**Rollback sensitivity:** High - disbursement and compliance regressions carry legal and financial risk.

## Quality Attribute Assessment

| Attribute | Requirement (from BRS) | Assessment | Risk |
|---|---|---|---|
| Performance | Intake form load ≤2s; scoring ≤90s | Needs focused performance testing for scoring pipeline under load; caching at intake recommended | Medium-High |
| Security | PII encryption, audit trails | Strong requirements; ensure key management and access controls planned | High |
| Scalability | 500 concurrent submissions | Architecture must support autoscaling for intake and scoring components | Medium |
| Availability | 99.9% business-hours uptime | Design for multi-AZ hosting, resilient integrations with circuit breakers | High |

## Open Decisions

| DEC-NNN | Question | Owner | Default Assumption | Required Before |
|---|---|---|---|---|
| DEC-001 | Which AI model vendor and hosting approach will be used (in-house vs third-party)? | Head of AI | Use Azure Foundry (architecture input) | Model selection and explainability approach |
| DEC-002 | Exact AML provider list beyond HM Treasury? | Compliance | HM Treasury only | AML design and data feeds |
| DEC-003 | T24 payment gateway contract completeness | IT Architecture | Contract to be defined by team | Final disbursement adapter implementation |

## Active Assumptions

| Assumption | Source | If False, Then |
|---|---|---|
| Experian and DocuSign contracts are available | input/brs.md | Implementation will require procurement and timeline delay |
| Test environments for T24 and Experian will be provided | Operational planning | Integration testing will be delayed; increase manual verification efforts |

## Known Unknowns

| Unknown | Impact | Discovery Path |
|---|---|---|
| Exact API SLAs for Experian and HMRC | Affects timeout and retry strategies | vendor contracts / test calls |
| Model explainability output format needed by regulators | Affects model selection and telemetry | regulator guidance and pilot model outputs |

---
*Set Status: Accepted only by workflow or human approval when applicable. Never self-accept.*
