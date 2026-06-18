# Architecture Rules (AR-NNN)

These architecture rules capture reusable, non-functional, and governance constraints for the I005 Loan Origination Platform. They are authoritative for this initiative and intended to be referenced by design, implementation, and QA.

1. AR-001: Data Residency & Sovereignty
   - All production data and backups must remain within UK data centres and comply with GDPR.

2. AR-002: PII Classification & Handling
   - Use the project's entity model to mark attributes as `PII`, `Sensitive`, or `Non-PII`.
   - PII fields must be encrypted at rest (AES-256) and masked in logs and UIs unless explicitly authorised.

3. AR-003: Encryption & Transport
   - All external and internal service-to-service transport must use TLS 1.3.
   - Secrets must be stored in a managed secret store (Key Vault) and accessed via managed identities.

4. AR-004: API Design and Versioning
   - All external APIs must expose an OpenAPI v3 definition in `specs/openapi/` and include `x-privacy` metadata for PII fields.
   - Use semantic versioning for API contract changes; breaking changes require a new major version.

5. AR-005: Authentication and Authorization
   - Use OAuth2/OpenID Connect for user flows; service-to-service calls must use managed identities with least privilege role bindings.

6. AR-006: Observability and Audit
   - Emit structured logs (JSON) and correlated traces for each request; include `request_id` and `user_id` when available.
   - Immutable audit records for underwriting decisions must be written to append-only storage and retained per retention policy.

7. AR-007: Modular Boundaries
   - Define module boundaries aligned to business capabilities (Intake, Scoring, Underwriting, Offer, Disbursement). Each module exposes a narrow API surface and owns its data.

8. AR-008: Deployment & Environments
   - CI/CD pipelines must enforce infrastructure-as-code for environments; environment promotion must be gated by automated tests and QA approvals.

9. AR-009: Data Retention and Purge
   - Retention policies defined in `quality-gates/data-contract.md` must be implemented via automated retention jobs; deletions must be auditable.

10. AR-010: Model Governance
   - Any AI model used for decisioning must have an associated Model Card, explainability summary, and monitoring hooks as defined in `quality-gates/model-governance.md`.

11. AR-011: Security Controls
   - Apply least-privilege access, network segmentation (zero-trust), and regular dependency vulnerability scans; follow the project's `security-review.md` checklist.

12. AR-012: Compliance & Evidence
   - All design decisions affecting compliance must cite the relevant regulation (FCA/GDPR) and include traceable evidence in the `compliance/` folder.

13. AR-013: Testing Requirements
   - Contract tests (Schemathesis / OpenAPI) must run in CI for all public APIs and fail the build on schema violations.

14. AR-014: Performance and Resilience
   - Define SLOs for latency and availability per module; implement circuit breakers and bulkheads for external integrations.

15. AR-015: Logging & Secrets
   - Never log secrets or full PII; use redaction helpers in shared logging libraries.

Notes:
- These rules are intentionally concise; link normative procedures and templates where needed.
- Update `AR-NNN` numbers as the architect refines rule set.
# Architecture Rules (AR-NNN)

Generated from `architecture/architecture-review.md`, `input/architecture.md`, and `input/brs.md` on 2026-06-13 by architect draft.

Each rule is a binding architectural constraint for implementation and handoff. Assign AR-NNN IDs sequentially.

| ID | Rule | Rationale / Source | Owner |
|---|---|---|---|
| AR-001 | Data residency: All personal data (PII) and production backups must reside within UK data centres (Azure UK South or UK West). | input/brs.md — Data residency constraint; regulatory (GDPR) | IT Architecture |
| AR-002 | Encryption: All PII must be encrypted at rest (AES-256) and in transit (TLS 1.3). Keys must be managed by Azure Key Vault with managed identities; no long-lived secrets in code. | input/brs.md — NFR-004; security model | Security / Platform
| AR-003 | Audit immutability: Every state transition and decision must be recorded in an immutable audit store; audit records must include previous state, new state, actor, timestamp, and trace reference (for explainability where applicable). Audit writes are append-only. | input/brs.md — FR-028; OBJ-003 | Data / Compliance
| AR-004 | Explainability traces: AI scoring must emit an explainability trace per decision (inputs, feature contributions, model version). Explainability traces must be retained for the regulatory retention period (TBD) and be queryable by auditors. | input/brs.md — Explainability requirement; BR-012 | AI / Model Governance
| AR-005 | Integration SLAs & fallbacks: External integrations (Experian, HMRC) must have documented SLA expectations; implement circuit breakers and fallback routing to `REFER_TO_UNDERWRITER` or manual queues when integration is unavailable. | input/brs.md — FR-009, FR-013; architecture review | Integration Owners
| AR-006 | Disbursement idempotency & retry: Disbursement operations to T24 must be idempotent by ARN and include a single retry; duplicate disbursement must be prevented by idempotency keys and audit checks. | input/brs.md — FR-024; BR-015 | Payments / Platform
| AR-007 | Compliance hold overrides: Only authorised Compliance roles may release a `COMPLIANCE_HOLD`. Override actions must be recorded with reason, approver ID, and timestamp. | input/brs.md — FR-014; BR-013 | Compliance
| AR-008 | Secrets and identities: All service-to-service authentication must use managed identities; no static credentials in repositories. | input/architecture.md — Security model | Platform
| AR-009 | Observability: Core events (submission, scoring result, AML/KYC result, underwriter action, offer acceptance, disbursement) must be emitted as structured events and instrumented for dashboards and alerts. | input/brs.md — FR-030 | Observability / SRE
| AR-010 | Environment separation & GDPR controls: Production PII storage, backups, and audit logs must be in production-only subscriptions with restricted access; staging/test must use synthetic or masked data. | input/brs.md — Constraints (Data residency, GDPR) | Security / IT Ops

## Implementation notes

- Owners must map each AR-NNN to acceptance criteria and testable checks in the test strategy and quality gates (SAST, data-privacy, model-governance).
- AR-004 retention period is a known unknown; record as open architecture question (OQ-006) for Legal/Compliance decisions.

Status: Draft — architect to review and set owners; ARs become binding once `Status: Accepted` is set in the architecture rules file by the architect.
# Architecture Rules (AR-NNN)

Derived from `architecture/architecture-review.md`, `input/architecture.md`, and BRS constraints. Each rule includes an owner and enforcement notes.

## AR-001 — Data Residency and PII Protection
- Rule: All PII and audit data must reside within UK data centres (Azure UK South / UK West). No PII shall be exported outside UK regions.
- Owner: IT Architecture
- Enforcement: Infrastructure provisioning must restrict resource regions; automated deployment checks must fail builds that target non-UK regions.

## AR-002 — Audit Immutability
- Rule: Audit logs for application state transitions must be append-only and tamper-evident; audit entries must include ARN, actor ID, timestamp, previous and new state.
- Owner: Compliance / Architecture
- Enforcement: Use Cosmos DB append-only container with access controls and retention policy; CI gate verifies audit write path exists.

## AR-003 — Experian Integration SLAs and Fallback
- Rule: Experian CreditExpert integration must complete within 30 seconds; on timeout or error, the application must be routed to `REFER_TO_UNDERWRITER` (BR-005).
- Owner: Integration Lead
- Enforcement: Integration adapter implements a 30s timeout and circuit breaker; automated tests simulate Experian failures verifying fallback.

## AR-004 — AML/KYC Gate Precedes Offer/Disbursement
- Rule: AML and KYC checks (HM Treasury, HMRC) must complete and be `cleared` before any offer generation or disbursement instruction is executed (BR-004).
- Owner: Compliance
- Enforcement: Orchestration layer enforces gate; handoff tasks must include compliance check hooks.

## AR-005 — Auto-Approve Threshold and Audit Evidence
- Rule: Applications auto-approved by AI with loan ≤ £10,000 may bypass underwriter review only if AML/KYC cleared; all AI recommendations and inputs must be retained for explainability and audit (BR-006).
- Owner: Head of AI / Compliance
- Enforcement: Persist model inputs and explanation metadata to audit store; implement explainability tooling integration.

## AR-006 — Explainability & Model Governance
- Rule: Any AI model used for scoring must support explainability traces usable in audit and regulator review; third-party models require documented explainability mapping.
- Owner: Head of AI
- Enforcement: Model contract must include explainability API; PR review requires evidence of explainability support.

## AR-007 — Managed Identity and Secrets
- Rule: All service-to-service authentication must use managed identities; no long-lived secrets in source or deployment manifests.
- Owner: Platform Ops
- Enforcement: CI/CD linting and secret-scan gates; deployment manifests must reference managed identity resources.

## AR-008 — Observability Events and Structured Telemetry
- Rule: System must emit structured observability events for key lifecycle points (submission, scoring, AML/KYC, underwriter decision, offer acceptance, disbursement) with ARN and minimal PII.
- Owner: Observability Lead
- Enforcement: Event schema contract and schema registry; unit/integration tests validate event emission.

## Notes
- These rules are binding for downstream design and implementation. Any proposed deviation must be recorded in `state/open-decisions.md` with an owner and rationale.
# Architecture Rules

| Rule ID | Rule | Enforcement / Mechanism | Owner | Notes |
|---|---|---|---|---|
| AR-001 | All PII must be stored and processed only within UK data centres. | Deployment guardrails: infra templates must target Azure UK South / UK West; CI/CD checks for region settings. | Architecture / Security | Related to GDPR constraint in input/brs.md |
| AR-002 | Audit records must be append-only and tamper-evident. | Use Cosmos DB container with immutability controls; restrict write/update permissions; automated ingestion pipeline writes audit events only. | Architecture / Ops | Tied to OBJ-003 and FR-028 |
| AR-003 | Experian integration must implement a circuit breaker and fallback to `REFER_TO_UNDERWRITER`. | Integration library standard with retry/circuit-breaker pattern; fallback route implemented in Loan Origination API. | Integrations team | Enforces FR-009 and NFR-007 |
| AR-004 | AI scoring decisions must be explainable; model implementations must provide per-decision rationale. | Acceptable model interfaces include feature-level explanations or explainability wrapper; model selection gated by compliance sign-off. | Head of AI / Compliance | Tied to OD-001 and compliance requirements (FCA) |

## Implementation Notes

- AR-001: Ensure backups, logs, and secondary storage also comply with UK-only residency.
- AR-002: Audit schema should include ARN, previous_state, new_state, actor, timestamp, and a checksum for tamper-evidence.
- AR-003: Circuit breaker thresholds and retry policies should be documented in the integration contract with Experian.
- AR-004: Define the minimal explainability payload required for downstream display to underwriters and audit storage.
# Architecture Rules — AI-Powered Loan Origination Platform

## Purpose
Binding architecture rules (AR-NNN) that constrain design and implementation for this initiative. Each rule includes an enforcement note and owner where applicable.

| Rule ID | Rule | Enforcement / Owner |
|---|---|---|
| AR-001 | All personal data and PII must reside and be processed only within UK data centres (Azure UK South / UK West). | Enforce via deployment pipelines and Azure subscription constraints. Owner: Security/Cloud Platform. |
| AR-002 | Audit trail must be immutable and tamper-evident. Use Cosmos DB append-only container and deny delete/update operations at the application layer. | Enforcement: storage policy + PR review. Owner: Compliance. |
| AR-003 | AI scoring outputs must include explainability metadata (features contributing to score, model version, confidence) persisted with each scoring event. Black-box models without explainability are disallowed. | Enforcement: AI model pipeline contract and schema; owner: Head of AI. |
| AR-004 | Third-party integrations (Experian, HMRC, DocuSign, T24) must implement circuit breakers and retry policies; failures must degrade to `REFER_TO_UNDERWRITER` or manual flows as specified. | Enforcement: shared library and infra config. Owner: Integration/API team. |
| AR-005 | No credit-bureau raw reports shall be persisted beyond the scoring pipeline — only derived score and permitted transient data may be retained. | Enforcement: data retention policy and pipeline review. Owner: Data Governance. |
| AR-006 | All service-to-service calls must use managed identities; no long-lived secrets in code or config. | Enforcement: pipeline checks, secret scanning. Owner: Cloud Platform. |
| AR-007 | Admin and underwriter access uses Azure AD with RBAC mapping; audit logs must record actor ID for every manual action. | Enforcement: Azure AD integration and RBAC policy. Owner: Identity/Access. |
| AR-008 | Observability events and structured telemetry must include ARN and minimal PII token only when necessary; logs must be PII-masked unless access-controlled via audit roles. | Enforcement: logging library and log retention policy. Owner: Observability. |
| AR-009 | The payment disbursement adapter must validate T24 contract surface and support at-least-once delivery with idempotency keys. | Enforcement: adapter tests and contract verification. Owner: Payments. |
| AR-010 | Any architectural decision left as DRAFT that is resolved in `state/open-decisions.md` must be reflected by removing `DRAFT` notices and updating artifacts before handoff. | Enforcement: orchestrator stale-checks. Owner: Orchestrator/Delivery Lead. |

## Notes

- These rules are initiative-binding and must be referenced in `engineering-readiness/readiness-check.md` and in every story's `design.md` where relevant.
- If a proposed implementation cannot comply with a rule, record a proposed exception in `state/open-decisions.md` with an owner and mitigation.
# Architecture Rules

The following binding architecture rules apply to I005 and must be enforced during implementation and reviews.

| Rule ID | Rule | Enforcement / Notes |
|---|---|---|
| AR-001 | Data residency: all production data and backups must reside in UK data centres only. | CI/CD pipeline must target UK regions; infra review required. |
| AR-002 | Audit trail: all state transitions and human actions must be recorded in an append-only, tamper-evident audit store. | Use Cosmos DB append-only container and restrict delete/update operations; access RBAC controls. |
| AR-003 | AI explainability: models used for scoring must provide explainability evidence per decision suitable for FCA review. | Model selection gate; include explainability extracts in audit events. |
| AR-004 | Integration resilience: all outbound third-party calls (Experian, HMRC, DocuSign, T24) must use circuit breakers and defined fallbacks. | Libraries and retry policies standardised; fallback = REFER_TO_UNDERWRITER or manual verification. |
| AR-005 | Secrets and identities: no long-lived credentials in code; use managed identities and Key Vault for any secrets. | Enforce in code review and pipeline policies. |
| AR-006 | Observability: core business events (submission, scoring, AML/KYC, underwriter action, disbursement) must emit structured events for dashboards and audit. | Define event schema and retention policy; include ARN in all events. |
# Architecture Rules — AI-Powered Loan Origination Platform (I005)

This file lists authoritative architecture rules (AR-NNN) that govern design, enforcement, and verification for I005.

| AR ID | Rule | Enforcement / Owner |
|---|---|---|
| AR-001 | Data residency: All PII and sensitive data must be stored and processed only in UK data centres (Azure UK South / UK West). | Enforce via subscription/resource tagging and Terraform pre-deploy checks. Owner: IT Architecture |
| AR-002 | Explainability: All AI model decisions affecting applicant outcome must include explainability artifacts (feature attributions, input snapshot) stored in the immutable audit log. Black-box-only models are disallowed. | Enforce via model contract & inference pipeline integration tests. Owner: Head of AI |
| AR-003 | Audit log immutability: Audit log must be append-only, tamper-evident, and accessible only via privileged read roles; retention policy and export controls must meet compliance. | Enforce via Cosmos DB configuration (append-only container) and RBAC. Owner: Security / Compliance |
| AR-004 | Integration resilience: All external integrations (Experian, HMRC, DocuSign, T24) must implement circuit breakers, retries with exponential backoff, and defined fallbacks (route to `REFER_TO_UNDERWRITER` or manual verification). | Enforce via API gateway policies, adapter contract tests, and integration test suites. Owner: Integration Lead |
| AR-005 | Authentication & secrets: All service-to-service authentication must use managed identities; no long-lived secrets stored in repos. | Enforce via PR checks and IaC policy (Azure Policy). Owner: Platform Engineering |
| AR-006 | Performance budget: Scoring pipeline end-to-end latency must meet ≤90s under normal load; Experian call ≤30s, AML/KYC ≤60s. | Enforce via performance tests and SLOs; monitor via observability plan. Owner: SRE / Performance Lead |
| AR-007 | Payment gateway contract: The Temenos T24 adapter shall implement a versioned adapter interface with mocked fallback for development; contract must be finalised before D3 handoff. | Enforce via API contract artifact and integration staging tests. Owner: IT Architecture |

Notes:
- Each AR-NNN must include a short enforcement mechanism and a named owner. The `architecture` persona will convert these rules into the `architecture/architecture-rules.md` canonical format and add traceable IDs to design documents.
- ARs are authoritative constraints — when conflicts occur, AR wins over lower-ranked artifacts.

Generated by architect-orchestrator on 2026-06-13.
# Architecture Rules

## Status

CONFIRMED — architect reviewed and assigned owners.

| Confirmed by | Role | Date |
|---|---|---|
| Solution Architect | Architect | 2026-06-12 |

## Rules

- **AR-001 — Data residency:** All PII and audit data must remain in UK datacenters. Owner: Architecture.
- **AR-002 — Secrets & identities:** All service-to-service authentication must use managed identities; no long-term secrets in code or configs. Owner: Security.
- **AR-003 — Audit immutability:** Audit log store shall be append-only; no delete or update operations allowed; retention policy to be defined by Compliance. Owner: Data Governance.

## Enforcement

- Architecture reviews, CI gating, and deployment pipeline templates will validate rule adherence. Exceptions must be logged in `planning/open-decisions.md` with an owner and remediation plan.
