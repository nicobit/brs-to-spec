# Architecture Review

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I988-N8 |
| Created at | 2026-06-21 |
| Created by | architect |
| Status | Draft |

## Initiative-Architecture Fit

| Feature Area | Existing Components Touched | New Components / Boundaries | Contract Changes | Blast Radius |
|---|---|---|---|---|
| Intake & Submission | Web UI, Application DB, Notification Service | Input validation service, ARN generator | Addition of ARN contract; email templates | Low |
| AI Scoring Pipeline | Scoring infra, Experian adapter | AI Scoring Service (explainability exporter), Explainability store | Scoring output contract (score, rationale, provenance) | Medium |
| Compliance (AML/KYC) | HMRC/KYC adapter, Compliance service | Compliance orchestration workflows | KYC result contract and hold semantics | Medium |
| Underwriter Workflow | Underwriter dashboard, Audit log store | Underwriter queue service | Underwriter action contract and immutable audit entries | Medium |
| Offer & E-signature | DocuSign integration, Offer templates | Offer generator, acceptance recorder | DocuSign envelope contract; acceptance audit fields | Medium |
| Disbursement & Core Banking | Payment gateway, T24 adapter | Disbursement adapter with reconciliation | Payment instruction contract and confirmation flow | High |

## Architecture Constraints

| ID | Constraint | Rationale | Violation Consequence | Source |
|---|---|---|---|---|
| ARCH-C-001 | All PII and audit data must reside in UK datacenters | Regulatory and data residency requirements (GDPR/FCA) | Non-compliance/legal/regulatory block | delivery-constitution.md / REQ-015 |
| ARCH-C-002 | AI scoring must emit explainability and provenance for every decision | FCA explainability and auditability needs | Model outputs unusable for audit; gate to production | delivery-constitution.md / REQ-004 |
| ARCH-C-003 | Use managed identities for all service-to-service auth | Prevent secret leakage and ensure least privilege | Security breach; secret sprawl | delivery-constitution.md |
| ARCH-C-004 | Experian credit data must not be persisted beyond scoring pipeline | Protect PII; minimize retention scope | Data residency/retention non-conformance | delivery-constitution.md / REQ-018 |

*Note: These constraints will be normalized into `AR-NNN` identifiers in the Architecture Rules artifact.*

## Brownfield Impact

Write `Greenfield - no brownfield impact` if not applicable.

| Component | Change Type | Consumers | Backward Compatible? | Migration Required | Rollback Possible |
|---|---|---|---|---|---|
| Temenos T24 adapter | Integration boundary (new adapter) | Payments, Reconciliation | No | Yes | Partial |
| Experian adapter | Operational change (transient handling) | Scoring pipeline | Yes | Minor | Yes |
| DocuSign integration | Contract alignment (envelope fields) | Offer generation | Yes | Minor | Yes |

**Regression surface:** Reconciliation and settlement flows touching T24 and payment rails are high risk; data mapping errors could cause settlement failures.
**Rollback sensitivity:** High - T24 integration changes require careful rollback and reconciliation procedures.

## Quality Attribute Assessment

| Attribute | Requirement (from BRS) | Assessment | Risk |
|---|---|---|---|
| Performance | Scoring pipeline ≤90s; email within 2 minutes | Achievable with autoscaling; Experian latency is primary risk | Medium |
| Security | AES-256 at rest, TLS1.3 in transit, managed identities | Meets requirements if Key Vault and RBAC enforced | Low-Medium |
| Scalability | Support 500 concurrent submissions | Requires autoscaling and stateless scoring services | Medium |
| Availability | Critical flows must tolerate Experian/HMRC outages via failover to human review | Design requires queueing and durable messaging | Medium-High |

## Open Decisions

| DEC-NNN | Question | Owner | Default Assumption | Required Before |
|---|---|---|---|---|
| DEC-001 | Which AI model vendor and explainability format will be used? | Head of AI | Use vendor X with SHAP-like explainability | Before production model training |
| DEC-002 | HMRC KYC fallback behaviour (manual verify vs auto-refer)? | Compliance | Manual verification for failures | Before go-live of automated checks |
| DEC-003 | ARN format and retention policy | Product Owner | Short alphanumeric + timestamp; retain for 7 years | Before audit reports enabled |
| DEC-004 | Disbursement reconciliation approach with T24 | Finance/Payments | Use eventual-confirmation + reconciliation job | Before first production disbursement |

## Active Assumptions

| Assumption | Source | If False, Then |
|---|---|---|
| Experian contract supports required queries within 30s | BRS / procurement | Route more cases to underwriter; increase latency SLA |
| DocuSign contract available for acceptance workflows | BRS | Offer acceptance via hosted PDF + manual signature fallback |
| T24 adapter or equivalent core banking connector will be available | Architecture input | Delay disbursements and require manual intervention |

## Known Unknowns

| Unknown | Impact | Discovery Path |
|---|---|---|
| Backup/replication policies for UK datacenters | Could affect DR/restore SLAs | Infrastructure design and infra team interviews |
| Detailed load profile and peak concurrency patterns | Affects autoscaling and cost estimates | Performance testing and telemetry in pilot |

---
*Set Status: Accepted only by workflow or human approval when applicable. Never self-accept.*
