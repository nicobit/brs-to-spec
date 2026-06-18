# Architecture Review

### Detailed Fit Analysis

- Application intake: The portal and API gateway must minimize synchronous work. Recommendation: push heavy validation into a server-side validation queue and use client-side checks for immediate UX feedback. Implement back-pressure signals to avoid overloading scoring pipelines.

- Scoring & decisioning: The scoring service must emit a deterministic, auditable explanation for every recommendation. Recommendation: adopt a hybrid pipeline where a small explainability adapter attaches feature-contribution data to each score and store both the score and explanation in the immutable audit store.

- Compliance screening: AML and KYC checks should be executed before any offer generation; failures must create a COMPLIANCE_HOLD state with human-review queues and operator notifications. Plan for throttling and retry semantics for HMRC/AML lookups.


## Metadata

| Field | Value |
|---|---|
| Initiative ID | I013-NEXT13 |
| Created at | 2026-06-16 |
| Created by | architect |
| Status | Draft |

## Initiative-Architecture Fit

| Feature Area | Existing Components Touched | New Components / Boundaries | Contract Changes | Blast Radius |
|---|---|---|---|---|
| Application intake & validation | Applicant portal, API gateway | Intake API, validation service | None external; ties to front-end and auth | Medium |
| AI scoring & decisioning | ML inference service (proposed) | Scoring service, explainability adapter | Experian / HMRC data inputs; model input contract | High |
| Compliance (AML / KYC) | AML/KYC providers, notification service | Compliance screening pipeline, compliance queue | Integration with HM Treasury / HMRC; must preserve PII handling | High |
| Underwriter workflow | Underwriter dashboard (existing UI) | Underwriter queue service, enriched audit view | Downstream underwriter UI contracts | Medium |
| Offer & disbursement | Offer generator, payment gateway connector | Offer document generator, disbursement orchestrator | Integration with internal payment gateway -> Temenos T24 | High |
| Observability & audit | Logging platform, metrics pipeline | Immutable audit store, structured events producer | Event schema for ARN, timestamps, actors | Medium |

## Architecture Constraints

### Analysis

- Application intake must remain lightweight; validation logic should be split between client and an API gateway to keep UX snappy and protect backend services.
- Scoring must tolerate occasional external-latency spikes by using a staging queue with time-bounded retries and explicit refer-to-underwriter paths to preserve user experience and regulatory safety.
- Disbursement orchestration must be designed for idempotency and explicit acknowledgment handling because mistakes at this boundary have high operational impact.


| ID | Constraint | Rationale | Violation Consequence | Source |
|---|---|---|---|---|
| ARCH-C-001 | UK-only data residency for PII and audit data | Regulatory and GDPR requirements for customer data | Non-compliance, regulatory fines, blocking of go-live | input/brs.md |
| ARCH-C-002 | Explainable AI only — no black-box-only models | FCA and explainability requirements | Model choice restricted; additional engineering for explanations | input/brs.md |
| ARCH-C-003 | Use enterprise Experian and DocuSign contracts | Procurement / enterprise policy | Integration rework or procurement delays | input/brs.md |
| ARCH-C-004 | Immutable, tamper-evident audit log | Regulatory auditability requirement | Fails compliance audits; legal risk | input/brs.md |
| ARCH-C-005 | Integration SLAs: Experian/HMRC/T24 within stated latencies | Meeting decision-time objectives | Increased referral rates or degraded user experience | input/brs.md |

## Brownfield Impact

Existing core systems (Temenos T24 and enterprise integrations) are in-scope and require adapters. Expect moderate brownfield impact where the internal payment gateway and T24 adapter need explicit API contracts.

### Analysis

- The Temenos T24 integration is the riskiest brownfield change: it will require a small, well-scoped adapter with contract tests and replayable integration tests to avoid operational errors.
- Where possible, introduce a staged adapter endpoint and run a shadow mode to validate payloads before enabling live disbursements.
- Backwards compatibility depends on the payment gateway supporting idempotent operations and schema versioning; if not available, plan a mitigation and longer rollout window.

| Component | Change Type | Consumers | Backward Compatible? | Migration Required | Rollback Possible |
|---|---|---|---|---|---|
| Temenos T24 adapter / payment gateway | New integration / adapter | Disbursement service, reconciliations | No (contract-driven) | Yes | Yes (if gateway supports staged endpoints) |
| Experian connector | Integration update | Scoring pipeline | Yes | Yes | Yes |

**Regression surface:** Disbursement and reconciliation flows are highest risk due to core banking dependency and missing contract detail (see GAP-001).  
**Rollback sensitivity:** High — mistakes in payment payloads can cause incorrect disbursements.

## Quality Attribute Assessment

| Attribute | Requirement (from BRS) | Assessment | Risk |
|---|---|---|---|
| Performance | Form load <= 2s; scoring <= 90s | Architecture supports lightweight front-end + async pipelines; scoring requires low-latency integrations and async retries | Medium-High (external SLAs) |
| Security | Encrypt PII at rest AES-256; TLS 1.3 in transit | Centralized secrets, key management, and encryption-at-rest must be enforced; identity via Azure AD | High (non-compliance risk) |
| Scalability | Support 500 concurrent submissions | Design with autoscaling front-end and stateless APIs; queuing for scoring and underwriter workflows | Medium (requires capacity testing) |
| Availability | 99.9% SLA during business hours | Use multi-zone deployment in Azure UK regions, redundancy for critical services | Medium-High (integration availability risk) |

### Assessment Notes

- Performance: To meet the 90s scoring target, segregate synchronous applicant-facing flows (validation, ARN issuance) from longer-running scoring pipelines. Use optimistic UI patterns for scoring that surface progress while preserving auditability.
- Security: Enforce tenant-scoped key management and ensure audit write paths are protected with separate roles to avoid accidental tampering.
- Scalability: Partition scoring by tenant or hashed ARN namespace to avoid hot partitions in downstream data stores.


## Open Decisions

| DEC-NNN | Question | Owner | Default Assumption | Required Before |
|---|---|---|---|---|
| DEC-001 | Payment gateway / T24 API contract shape and error semantics | IT Architecture | Contract will provide REST schema and idempotency guidance | Implementation of disbursement orchestrator |
| DEC-002 | Explainability approach for scoring (rule-based explanations vs model introspection) | Head of AI / Architect | Use hybrid explainability adapter delivering feature contributions | Choice of scoring model and SCA requirements |
| DEC-003 | Immutable audit storage technology (append-only DB vs WORM storage) | Architect / Platform | Use append-only store with tamper-evident checksums in UK region | Compliance sign-off and retention policy |

## Active Assumptions

| Assumption | Source | If False, Then |
|---|---|---|
| HMRC KYC fallback is manual verification | input/architecture.md | If false, automation gap increases; need additional vendor or extended timeline |
| Internal payment gateway will support required payload fields | GAP-001 / input/brs.md | If false, rework payment orchestration and delay disbursement slice |

## Known Unknowns

| Unknown | Impact | Discovery Path |
|---|---|---|
| Exact Temenos T24 adapter contract and error semantics | High — affects disbursement correctness and rollback | Engage IT Architecture and request API schema; run adapter spike |
| AI model explainability implementation cost and latency | Medium-High — may increase scoring latency or engineering effort | Evaluate candidate explainability libraries and run performance tests |

### Recommendation

- Proceed to architect review focusing on the T24/payment-gateway contract (GAP-001) and the explainability approach (DEC-002).  
- Create a small integration spike for the payment gateway with contract tests and a shadow-dispatch mode.  
- Define measurable acceptance criteria for explainability latency and confidence before locking the scoring model choice.


---
*Set Status: Draft — submit for architect review (`gate-architecture-review`).*
