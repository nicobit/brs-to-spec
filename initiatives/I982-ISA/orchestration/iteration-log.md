# Iteration Log — I982-ISA

## Goal State

*Derived from input/brs.md and input/architecture.md on iteration 1. Referenced on all subsequent iterations.*

**Initiative:** AI-Powered Loan Origination Platform (I982-ISA)

**Final objective:** An AI coding assistant can implement every capability in this initiative without asking a single clarifying question.

### Capabilities to implement (in order)

| # | Capability | Source requirements | Status |
|---|---|---|---|
| 1 | Application domain model and state machine | FR-001 to FR-030, NFR-004, NFR-005 | done |
| 2 | Experian CreditExpert API integration contract | FR-009, NFR-007 | pending |
| 3 | HMRC KYC API integration contract | FR-013, NFR-007 | pending |
| 4 | HM Treasury AML sanctions API integration contract | FR-012, OQ-004 | pending |
| 5 | AI Scoring Service — risk scoring model and recommendation engine (Azure Foundry, OQ-001) | FR-006, FR-007, FR-008, FCA constraint | pending |
| 6 | Loan Origination API — application intake and state machine (Epics 1–4) | FR-001 to FR-019 | pending |
| 7 | DocuSign e-signature integration contract (webhook callback) | FR-022, NFR-007 | pending |
| 8 | Temenos T24 payment gateway adapter | FR-024, FR-025, FR-026, OQ-005 | pending |
| 9 | Loan offer generation | FR-020, FR-021 | pending |
| 10 | Cooling-off period enforcement (30-day reapplication ban + 14-day post-acceptance) | FR-011, FR-023 | pending |
| 11 | Notification Service (email + portal triggers) | FR-004, FR-011, FR-014, FR-021, FR-023, FR-027, FR-030 | pending |
| 12 | Audit log (immutable Cosmos DB append-only store) | FR-028, FR-030, NFR-005 | pending |
| 13 | Admin dashboard metrics API | FR-029, FR-030 | pending |
| 14 | Applicant self-service portal (intake form, status, offer acceptance) | FR-001, FR-005, FR-022 | pending |
| 15 | Underwriter and admin dashboard UIs | FR-016, FR-017, FR-029 | pending |
| 16 | CI pipeline and quality gates | NFR-001 to NFR-007 | pending |

### Technology and architecture constraints

- **Cloud:** Azure UK South (primary) + Azure UK West (DR) — all data must remain in UK data centres (GDPR data residency)
- **Backend:** .NET 8 / ASP.NET Core (Loan Origination API, Compliance Service, Payment Gateway Adapter); Python / FastAPI (AI Scoring Service); .NET 8 Azure Functions (Notification Service)
- **Frontend:** React / Next.js on Azure Static Web Apps (Applicant Portal, Underwriter Dashboard, Admin Dashboard)
- **Databases:** Azure SQL Hyperscale (mutable application state), Azure Cosmos DB (audit log — append-only)
- **Async transport:** Azure Service Bus (AMQP) between Loan Origination API, AI Scoring Service, Compliance Service, Notification Service
- **Authentication:** Applicants via email + OTP; underwriters/admins via Azure AD RBAC; service-to-service via managed identities (no stored secrets)
- **Ingress:** Azure API Management (rate limiting, WAF, TLS 1.3 termination)
- **Enterprise contracts:** Experian CreditExpert API (existing), DocuSign (existing), Temenos T24 (we define the contract — OQ-005)
- **AI model vendor:** Azure Foundry (OQ-001 resolved)
- **Encryption:** AES-256 at rest, TLS 1.3 in transit (NFR-004)

### Best practices mandatory for this initiative type

This is a **regulated fintech** initiative. The following are non-negotiable and enforced automatically:

- **Idempotency keys** on every state transition and external API call (retrY safety for payment and e-signature events)
- **Immutable audit log** — append-only Cosmos DB container; write-once at SQL level for `UnderwriterDecisionRecord`
- **Explainable AI** — FCA requirement; no black-box models; `ai_explanation_ref` required on every scoring response; `null` is a scoring error
- **Circuit breakers on all external calls** — Experian, HMRC, DocuSign, T24 (NFR-007); each has defined fallback (REFER_TO_UNDERWRITER for Experian; manual verification for HMRC; ops alert for T24)
- **GDPR right-to-erasure compatible model** — credit bureau data not persisted (architecture.md); PII fields encrypted at column level; PII not included in audit event data_snapshots
- **PII minimisation in logs** — PII fields masked in application logs; full PII only via Audit Log Store with elevated RBAC
- **Cooling-off enforcement at state machine level** — 30-day reapplication ban (FR-011), 14-day post-acceptance (FR-023) enforced as state guards, not application-layer checks
- **At-least-once delivery** on Service Bus with idempotent consumers — state machine rejects duplicate transitions for same idempotency key
- **AML/KYC clear before any offer** — state machine structurally prevents OFFER_GENERATION transition without compliance check completed

### Open questions blocking implementation

All BRS open questions are answered (OQ-001 to OQ-005). No blocking open questions remain at domain model level.

Remaining open facts (will surface in integration contract iterations):
- Experian CreditExpert API: exact endpoint URL, OAuth 2.0 client credentials details, credit report response schema, rate-limiting error structure (HTTP 429)
- HMRC KYC API: exact endpoint, authentication, response schema for NI/name/DOB cross-reference
- T24 disbursement API: request/response schema, authentication (we define the contract per OQ-005)
- DocuSign webhook: exact payload schema for `envelope_status = COMPLETED` events, signature of webhook authentication header

---

## Iteration 1

| Field | Value |
|---|---|
| Date | 2026-07-02 |
| Gap closed | No entity definitions or state machine existed — a developer could not write the Application entity, any state-machine guard, any audit log event schema, or any routing logic for the Loan Origination API or Compliance Service without guessing field names, types, and state names |
| Artifact produced | `architecture/domain-model.md` |
| Confidence delta | Implementability: 0% → ~30%. A developer can now write the Application entity, LoanOffer, UnderwriterDecisionRecord, AuditEvent, and Underwriter entities with precise field types, constraints, and indexes. All 17 application states, 23 transitions, and 17 business rules are specified with concrete guards, actors, and enforcement points. |
| Next gap | Experian CreditExpert API integration contract (FR-009): a developer cannot implement the AI scoring pipeline without knowing the exact credit report request schema, the response field mapping to FR-008 scoring inputs (debt-to-income ratio, credit history length, active debt count), the HTTP 429 rate-limiting response structure, and the circuit breaker threshold and fallback trigger point. |
| Continue | yes |

### Reasoning

The domain model is the highest-value artifact for iteration 1 because it unblocks every downstream capability. Every service — Loan Origination API, AI Scoring Service, Compliance Service, Audit Log, Notification Service — references the Application entity and its state machine. Without concrete field types, the state machine transition table, and business rule enforcement points, a developer would have to guess dozens of implementation details: how is the reapplication ban enforced, what happens when Experian is unavailable, where does the 4-hour escalation timer start, what fields go into each audit event snapshot. This artifact closes all of those gaps in one iteration.

---

## Iteration 2

| Field | Value |
|---|---|
| Date | 2026-07-02 |
| Gap closed | No Experian CreditExpert API integration contract existed — a developer could not implement the AI scoring pipeline (FR-009) without knowing the credit report request schema, response field mapping to FR-008 scoring inputs, HTTP error catalogue with fallback behaviours per status code, circuit breaker configuration, timeout values, or Service Bus event contracts for the credit-check result |
| Artifact produced | `architecture/experian-integration.md` |
| Confidence delta | AI scoring pipeline implementability: 0% → ~70%. A developer can now implement the complete Experian call: OAuth 2.0 token management, request construction from Application entity fields, response field mapping to DTI/LTI computation and credit history inputs, circuit breaker with `fail_max=3 / timeout=60s`, all 11 error cases with fallback routing, Service Bus event schemas for both success and failure paths, and observability signals with alert thresholds |
| Next gap | AI Scoring Service internal contract (FR-006, FR-007, FR-008, FCA explainability constraint): a developer cannot implement the AI Scoring Service without knowing how it is triggered (Service Bus subscription), how it calls Azure Foundry for inference, what feature vector is sent to the model, how the model response is mapped to AUTO_APPROVE/REFER_TO_UNDERWRITER/AUTO_DECLINE recommendation, and how the FCA-required explainability artefact is generated and stored |
| Continue | yes |

### Reasoning

The Experian integration contract closes the largest single unknown in the AI scoring pipeline. Every field mapping, timeout value, error code, and fallback routing decision was underspecified — a developer would have had to guess all of them. The contract now gives concrete values (25s timeout, fail_max=3, 60s reset, response field names, DTI/LTI formula, NIN-based identity matching) that can be implemented directly. The four open questions (IQ-001 to IQ-004) are flagged as blocking for production readiness but not for skeleton implementation.

---

## Iteration 3

| Field | Value |
|---|---|
| Date | 2026-07-02 |
| Gap closed | No AI Scoring Service implementation contract existed — a developer could not implement FR-006, FR-007, FR-008, or the FCA explainability requirement without knowing the Service Bus trigger schema, how PII is decrypted and used for the Experian call, how the 14-feature vector is built, how Azure Foundry is called, how repayment_probability maps to ai_risk_score and recommendation thresholds, how the SHAP explainability artefact is structured and stored, or how failure in any dependency routes to REFER_TO_UNDERWRITER |
| Artifact produced | `coding-packages/CP-001-ai-scoring-service/coding-package.md` |
| Confidence delta | AI Scoring Service implementability: 0% → ~85%. A developer can now implement the complete service: Service Bus consumer with idempotency, PII decryption from Key Vault, Experian call (from INT-001), 14-feature vector construction with encoding table and edge cases, Azure Foundry endpoint contract (request/response schemas), recommendation thresholds (700/400 pending business confirmation), SHAP explainability JSON with all 14 feature contributions and decline reason categories, blob storage write with failure escalation path, all 7 acceptance criteria as Gherkin scenarios, and full test plan with CI gate requirements |
| Next gap | Compliance Service contract (FR-012 to FR-014): a developer cannot implement the Compliance Service without knowing the HMRC KYC API request/response schema and MANUAL_REQUIRED fallback (OQ-003), the HM Treasury sanctions API format (OQ-004: HM Treasury only), the COMPLIANCE_HOLD vs UNDERWRITER_QUEUE routing decision rules, and the Service Bus event contracts for the AML and KYC check results |
| Continue | yes |

### Reasoning

The AI Scoring Service coding package closes the single most complex gap in the AI pipeline. Without concrete thresholds, feature vector schema, SHAP artefact format, and Service Bus event contracts, every developer decision would have been a guess. The FCA explainability requirement was particularly high-risk — without specifying that `ai_explanation_ref = null` is a scoring failure (not an acceptable output), a developer would have likely let it pass silently. The four open questions (AIQ-001 to AIQ-004) are flagged; AIQ-003 (NIN matching) is critical and may require extending FR-001.

---

*(Repeat ## Iteration N block for each loop cycle)*
