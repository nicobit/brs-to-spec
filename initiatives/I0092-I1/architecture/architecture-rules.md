# Architecture Rules (AR)

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I0092-I1 |
| Created at | 2026-06-22 |
| Created by | architect |
| Status | Draft |

---

## Rules Catalog

### AR-001 — Data Residency and PII Storage

**Rule statement:** All PII and audit data MUST be stored and processed only within Azure UK South or Azure UK West regions.

**Rationale:** Ensures compliance with UK GDPR and bank data residency policies.

**Source:** input/architecture.md, BRS constraints

**Scope:** All storage accounts, databases, backups, and analytics exports.

---

### AR-002 — Audit Log Immutability

**Rule statement:** The audit log MUST be implemented as an append-only, tamper-evident store (e.g., Azure Cosmos DB append-only container) and retain all required evidence for 24 hours in a write-once manner.

**Rationale:** Regulatory and audit requirements demand immutable traceability for decisions.

**Source:** FR-028, input/architecture.md

**Scope:** Audit events, state transitions, underwriter actions.

---

### AR-003 — AI Explainability Evidence

**Rule statement:** The AI Scoring Service MUST record explainability artifacts (feature contributions, model metadata, version) for every score and persist them in an auditable store.

**Rationale:** FCA requirements and internal audit necessitate explainable scoring.

**Source:** input/brs.md constraint: explainable models

**Scope:** AI Scoring Service outputs and persistence.

---

### AR-004 — Integration Circuit Breakers

**Rule statement:** All external integrations (Experian, HMRC, DocuSign, T24) MUST implement circuit breakers and defined fallback behaviours that route to conservative handling (e.g., REFER_TO_UNDERWRITER) on failure.

**Rationale:** Prevents cascading failures and unsafe automated decisions when dependencies are degraded.

**Source:** NFR-007, input/architecture.md

**Scope:** Integration adapters and service orchestration.

---

### AR-005 — Managed Identity and Secrets

**Rule statement:** Service-to-service authentication MUST use Azure Managed Identities; no long-lived credentials are stored in code or config repositories.

**Rationale:** Reduces secret leakage risk and meets security policy.

**Source:** input/architecture.md (security model)

**Scope:** All internal service calls and CI/CD pipelines.

---

### AR-006 — Audit and Access Controls

**Rule statement:** Access to full PII and audit records MUST be protected by RBAC; only elevated roles (auditors, compliance with approved justification) may retrieve raw PII.

**Rationale:** Limit exposure of sensitive data and support audit processes.

**Source:** input/architecture.md security model

**Scope:** Audit Log Store, Azure SQL, admin dashboards.

---

## Notes

- These rules are derived directly from the architecture review and BRS inputs. Any additional rule requires an ADR before acceptance.

---
## Forbidden Patterns

The following patterns are explicitly forbidden unless an ADR is issued:

- Storing any PII outside Azure UK South / UK West regions.
- Using black-box AI models without explainability artifacts.
- Writing mutable audit records that allow deletion or modification of historical events.

## Coverage

These rules cover data residency, auditability, AI explainability, integration failure handling, identity of services, and access controls. They do not mandate implementation details beyond managed identities and append-only audit storage; implementation choices must preserve rule semantics.

---
*Set Status: Draft — rules require architect acceptance to proceed.*
