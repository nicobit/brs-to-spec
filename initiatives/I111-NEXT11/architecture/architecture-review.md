# Initial Architecture Review

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I111-NEXT11 |
| Author | Solutions Architect |
| Date | 2026-06-18 |
| Inputs | business-analysis/requirements.md, business-analysis/gaps-and-questions.md, business-intake/business-intake-summary.md |

## Initiative-Architecture Fit

This table maps high-level feature areas to proposed components and assesses fit.

| Feature Area | Proposed Component | Fit | Rationale | Owner |
|---|---|---|---|---|
| Application Intake | API Gateway + Application Backend | High | Stateless intake, validation and ARN assignment are standard web patterns | Product Engineering |
| AI Scoring | AI Scoring Service (isolated) | High | Requires explainability surface and model isolation for compliance | AI Platform |
| Credit/AML Integrations | Integrations Layer (connectors) | Medium | Dependent on provider contracts and SLA handling (GAP-002/003) | Integrations Team |
| Underwriter Workflow | Underwriter UI + Queue | High | Simple internal web UI with immutable action recording | Ops/Product |
| Disbursement | Disbursement Integration (Temenos T24) | Medium | Requires connector and reconciliations agreements (GAP-005) | Core Banking Team |

## Architecture Constraints

| Constraint | Rationale | Violation Consequence | Owner | Mitigation |
|---|---|---|---|---|
| UK data residency | Regulatory/GDPR requirement | Non-compliance, regulatory fines and remediation | Security | UK-only cloud regions; data residency checks in CI |
| Use Experian / DocuSign / Temenos | Contractual dependency (C-002) | Integration delays, scope reduction | Procurement | Fast-track API scoping and interface contracts |
| Explainability for AI | FCA requirement | Model redesign, compliance rejection | Head of AI | Define explanation schema and implement in scoring API |

## Brownfield Impact

Write `Greenfield - no brownfield impact` if not applicable.

| Component | Change Type | Consumers | Backward Compatible? | Migration Required | Rollback Possible |
|---|---|---|---|---|---|
| Temenos T24 disbursement | Modified (disbursement API integration) | Downstream reconciliation and reporting consumers (payments, ledger export) | No | Yes — reconciliation batch job required | Partial — manual reconciliation and ledgers require operator playbook |
| AI Scoring Service | New component (model scoring service) | Underwriter dashboard, offer generator, applicant-facing messages | Yes (service contract) | Yes — rollout via feature flags and staged model rollout | Yes — revert to prior model and reprocess in staging before full rollback |

**Regression surface:** disbursement confirmations and reconciliation paths which existing downstream consumers rely upon.

**Rollback sensitivity:** High — manual reconciliation required; potential customer financial impact.

## Quality Attribute Assessment

### Performance

| Attribute | Target | Assessment | Evidence |
|---|---|---|---|
| Performance | AI scoring ≤90s end-to-end (NFR-002) | Design for async scoring + caching; scale AI workers horizontally | Benchmark plan: schedule load tests and record baseline |

### Security

| Attribute | Target | Assessment | Evidence |
|---|---|---|---|
| Security | AES-256 at rest; TLS1.3 | Enforce PII encryption and RBAC for underwriter interfaces | Security design checklist attached; consult Security team for checklist items |

### Scalability

| Attribute | Target | Assessment | Evidence |
|---|---|---|---|
| Scalability | 500 concurrent submissions (NFR-003) | Use autoscaling application services and event-driven ingestion | Load test plan |

### Availability

| Attribute | Target | Assessment | Evidence |
|---|---|---|---|
| Availability | 99.9% business-hours uptime (NFR-006) | Multi-AZ deployment, circuit breakers on external deps | DR runbook |

## Open Decisions

| ID | Decision | Owner | Impact | Status | Rationale |
|---|---|---|---|---|---|
| OD-001 | Approve UK-only hosting (IaaS vs managed PaaS) | Head of Infrastructure | Affects deployment model and ops cost | Pending | Need cost and compliance trade-offs to be documented for decision |
| OD-002 | AI explainability data model shape | Head of AI | Affects DB schema and API contracts | Pending | Define required fields for customer and regulator reporting |

## Active Assumptions

| Assumption | If False, Then... | Owner |
|---|---|---|
| Experian integration SLA can meet 30s | If False, Then: route to underwriter by default and increase operational capacity for manual review | Integrations |
| Temenos T24 supports asynchronous disbursement callbacks | If False, Then: implement reconciliation polling and manual confirmation workflows | Core Banking |

## Known Unknowns

| ID | Unknown | Impact | Discovery Path |
|---|---|---|---|
| KU-001 | Exact Experian error codes and retry semantics | High | Request API contract from Experian; run connectivity tests |
| KU-002 | HMRC KYC availability and throttling | High | Engage Compliance and request API SLA details |

## Recommendations and Next Steps

1. Obtain API contracts for Experian, HMRC, DocuSign, and Temenos; update Integrations Layer design.
2. Define audit log tamper-evidence approach (append-only with signed snapshots) and retention policy with Security.
3. Produce a minimal deployment diagram and run a small spike to validate AI explainability APIs.
