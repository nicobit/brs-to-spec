# Architecture Review

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I093-I3 |
| Created at | 2026-06-22 |
| Created by | architect |
| Status | Draft |

## Initiative-Architecture Fit

| Feature Area | Existing Components Touched | New Components / Boundaries | Contract Changes | Blast Radius |
|---|---|---|---|---|
| Application Intake | Applicant portal, email ingestion, legacy intake service | New web intake service, public API gateway | Minor: validation API contract | Medium |
| AI Pre-screening & Scoring | No existing model pipeline | Scoring pipeline, explainability service, model registry | New scoring API and explainability contract | High |
| Integrations (Experian, HMRC, DocuSign, T24) | Experian connector (existing), core banking (T24) | Integration adapters with circuit-breakers | Explicit API contracts required for Experian and T24 | High |
| Underwriter Workflow | Email/manual queues, case management | Underwriter queue service, audit log store | Audit log write contract (immutability) | Medium |
| Observability & Audit | Central logging (partial) | Immutable audit store, event bus (structured events) | Event schema changes for ARN and state transitions | High |

## Architecture Constraints

| ID | Constraint | Rationale | Violation Consequence | Source |
|---|---|---|---|---|
| ARCH-C-001 | All PII must remain in UK regions and be encrypted at rest and in transit | Regulatory and GDPR data residency requirement | Non-compliance; legal and regulatory risk | BRS / Governance |
| ARCH-C-002 | Use Experian CreditExpert API for credit reports; fall back to manual routing if unavailable | Contractual integration requirement and performance SLAs | Increased manual workload; slower decisioning | BRS FR-009 |
| ARCH-C-003 | Temenos T24 integration via existing internal payment gateway API | Existing core banking integration constraint | Disbursement failures; operations impact | BRS Constraints |
| ARCH-C-004 | AI model decisions must be explainable (no opaque black-boxes) | FCA requirement for explainability and human oversight | Regulatory rejection; inability to operate in automated mode | BRS Constraints |

*Note: These constraints will be normalized into `AR-NNN` identifiers in the Architecture Rules artifact.*

## Brownfield Impact

Write `Greenfield - no brownfield impact` if not applicable.

| Component | Change Type | Consumers | Backward Compatible? | Migration Required | Rollback Possible |
|---|---|---|---|---|---|
| Temenos T24 connector | Modified | Payments, Disbursement process | Yes | Yes | Yes |
| Legacy intake service | Replaced by new intake API | Applicant portal, email ingestion | No (replace) | Yes | Yes |
| Experian integration | Adapter update | Scoring pipeline | Yes | Yes | Yes |

**Regression surface:** Existing disbursement flows and reconciliation processes are at risk if T24 message formats or sequencing change.  
**Rollback sensitivity:** Medium - requires coordination with payments and reconciliation teams; rolling back to legacy intake is feasible but audit reconciliation may be manual.

## Quality Attribute Assessment

| Attribute | Requirement (from BRS) | Assessment | Risk |
|---|---|---|---|
| Performance | NFR-001, NFR-002 (form load ≤2s, scoring ≤90s) | Draft architecture supports async scoring and caching; front-end optimisations required | Medium - scoring latency under peak load needs testing |
| Security | NFR-004 (PII encryption), AML/KYC requirements (FR-012/FR-013) | Encryption and network controls planned; identity proofing via HMRC | High - compliance blockers if not implemented correctly |
| Scalability | NFR-003 (500 concurrent submissions) | Scalable queue-based processing and autoscaling planned | Medium - needs capacity tests and autoscaling policies |
| Availability | NFR-006 (99.9% business hours) | Multi-AZ for services; circuit-breakers on external APIs | Medium - external API SLAs are the dominant risk |

## Open Decisions

| DEC-NNN | Question | Owner | Default Assumption | Required Before |
|---|---|---|---|---|
| DEC-001 | Which AI model vendor/approach will be used (in-house vs third-party)? | Head of AI | Use Azure Foundry prototype for PoC | Model selection before automated approval thresholds |
| DEC-002 | Cooling-off waiver legal flow required? | Legal | Assume not required for Phase 1 | Legal sign-off before launch |
| DEC-003 | HMRC fallback behaviour when KYC API unavailable | Compliance | Manual verification by ops | KYC fallback before automated offer generation |
| DEC-004 | Exact AML data providers beyond HM Treasury | Compliance | HM Treasury only | Integration testing with AML provider |
| DEC-005 | T24 payment gateway contract readiness | IT Architecture | API contract will be defined internally | T24 contract before disbursement automation |

## Active Assumptions

| Assumption | Source | If False, Then |
|---|---|---|
| Experian API meets 30s latency under expected load | BRS FR-009 | Route to underwriter; increase manual processing capacity |
| HMRC identity verification available and accurate | BRS FR-013 | Increased compliance holds; manual verification required |
| Central audit store can be made write-once/tamper-evident | FR-028 / NFR-005 | Use append-only storage + signed event envelopes; additional ADR required |

## Known Unknowns

| Unknown | Impact | Discovery Path |
|---|---|---|
| AI model explainability tooling and compatibility with vendor | Affects ability to auto-approve; regulatory acceptance | Prototype with Azure Foundry; model explainability evaluation |
| Temenos T24 message schema and error semantics | Affects rollback and reconciliation | Contract negotiation and integration tests with T24 sandbox |
| Experian integration rate limits under peak volume | Affects STP rate; may increase underwriter load | Load tests with Experian sandbox |

---
*Set Status: Accepted only by workflow or human approval when applicable. Never self-accept.*
