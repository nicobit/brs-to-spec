# Architecture Rules (AR)

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I011-N2 |
| Created at | 2026-06-21 |
| Created by | architect |
| Status | Draft |

---

## Rules Catalog

### AR-001 — Data Residency

**Rule statement:** All persistent and transient processing of applicant PII, credit bureau data, audit logs, and telemetry MUST occur within Azure UK South or Azure UK West; no PII or sensitive data shall be transferred or processed outside UK data centres.

**Rationale:** UK GDPR and documented constraints in the BRS.

**Source:** BRS constraints; architecture draft

**Scope:** All services, storage, and third-party integrations handling PII.

---

### AR-002 — Explainable AI Outputs

**Rule statement:** The AI Scoring Service MUST produce per-decision explanation metadata sufficient for regulatory review (features used, weightings or contributing signals, recommendation label), and make that metadata available to the audit log for every decision.

**Rationale:** FCA requirement for explainability; BRS constraint forbidding black-box models.

**Source:** BRS constraints; architecture review

**Scope:** AI Scoring Service, Audit Log Store.

---

### AR-003 — Circuit Breakers and Fallbacks

**Rule statement:** All external API integrations (Experian, HMRC, DocuSign, T24) MUST implement circuit breakers with documented retry/backoff and explicit fallback routing to human review when necessary.

**Rationale:** Ensure availability and safe failure modes; meets NFR-007.

**Source:** NFRs; architecture review

**Scope:** Integration layer and Loan Origination API.

---

### AR-004 — Immutable Audit Trail

**Rule statement:** The audit log MUST be append-only and tamper-evident; every state transition and decision MUST be recorded with actor, timestamp, previous and new state, and a snapshot of the relevant data.

**Rationale:** Regulatory auditability (FR-028) and forensic traceability.

**Source:** BRS FR-028; architecture review

**Scope:** All services that change application state.

---

### AR-005 — Encryption and Key Management

**Rule statement:** All PII in transit MUST use TLS 1.3; all persistent PII MUST be encrypted at rest using AES-256. Keys MUST be managed using Azure Key Vault with defined rotation policy.

**Rationale:** Align to NFR-004 and platform best practices.

**Source:** NFRs; architecture draft

**Scope:** Data storage, backups, and inter-service transport.

---

### AR-006 — Observability Event Contract

**Rule statement:** The system MUST emit structured observability events for key lifecycle milestones (submission, scoring completion, AML/KYC result, underwriter action, offer acceptance, disbursement) including ARN and minimal required context for tracing and metrics.

**Rationale:** Support monitoring, alerting, and traceability (FR-029, FR-030).

**Source:** BRS; architecture review

**Scope:** Event bus producers and monitoring pipelines.

---

### AR-007 — Forbidden Pattern: Black-box Models

**Rule statement:** Do NOT deploy AI models that cannot provide sufficient explainability metadata as required by AR-002; black-box-only models are forbidden for scoring decisions.

**Rationale:** Regulatory requirement and product constraints.

**Source:** BRS constraints

**Scope:** Model selection and deployment pipelines.

---

## Forbidden Patterns

- Black-box-only AI models that cannot produce explainability metadata (see AR-002).

| Pattern ID | Forbidden Pattern | Rationale |
|---|---|---|
| FP-001 | Black-box-only AI models for scoring | Violates explainability requirement (AR-002) |

## Coverage

The rules above cover Data Residency, Explainability, Integration resilience, Audit immutability, Encryption, Observability, and Forbidden Patterns derived from the architecture review and BRS constraints. Additional rules will be added as ADRs and specific integration contracts are finalized.

*Status: Draft — rules must be reviewed and accepted by architecture gate.*
