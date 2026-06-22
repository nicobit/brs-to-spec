# Delivery Constitution

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I111-N11 |
| Created at | 2026-06-22 |
| Created by | governance-architect |
| Status | Draft |

---

## 1. Purpose

This constitution defines the governance rules, quality gates, and safety constraints that will shape the delivery of the AI‑Powered Loan Origination Platform (I111-N11). It ensures traceability from business requirements and architecture inputs to implementable stories, mandates human review where required, and enforces data residency, security, and AI safety constraints for regulatory compliance (FCA, GDPR).

---

## 2. Delivery Principles

| # | Principle | Rationale |
|---|---|---|
| 1 | Safety-first: preserve regulatory and data-residency constraints | BRS: NFR-004, Constraints: data residency (UK only) |
| 2 | Small, verifiable increments with traceability to BRS | Enables auditability and QA (FRs + OBJ-001..OBJ-005) |
| 3 | Automate where safe, escalate where uncertain | Supports OBJ-001 while protecting human oversight (FR-006..FR-011) |
| 4 | Immutable audit and explainability for all AI decisions | FCA requirement; supports FR-028 and model explainability constraint |
| 5 | Secure by default: managed identities, encryption, least privilege | Matches architecture and NFR-004/NFR-007 |

---

## 3. Requirement Handling Rules

| Rule | Description | Consequence of Violation |
|---|---|---|
| R-1 | Every requirement must reference at least one BRS ID (e.g., FR-006) and include acceptance criteria in Gherkin/BBD form | Story returned to author for rewrite; fails story-quality gate |
| R-2 | Open Questions must be explicit and assigned an owner and priority (see BRS `Open questions`) | Blocker until owner responds if priority=High |
| R-3 | Non-functional requirements (NFRs) must map to measurable checks (SLOs, test assertions) | Implementation blocked at readiness gate until measurable checks exist |
| R-4 | Integrations must include circuit-breaker and fallback behavior in the requirement text (e.g., Experian fallback to REFER_TO_UNDERWRITER) | Missing fallback → requirement flagged as incomplete |

---

## 4. Architecture Alignment Rules

| Rule | Description | Applies To |
|---|---|---|
| A-1 | All services must deploy to UK regions only (Azure UK South/West) | Infrastructure, services, storage |
| A-2 | AI Scoring Service must expose explainability metadata for every decision | AI Scoring, event contracts (FR-006..FR-009) |
| A-3 | Use managed identities for S2S calls; secrets are not permitted in source repos | All integrations and services |
| A-4 | Audit Log must be append-only (Cosmos DB write-once pattern) and immutable | Observability and compliance (FR-028) |

---

## 5. Story Quality Rules

| Rule | Description | Check Method |
|---|---|---|
| SQ-1 | Each story must include: business goal, acceptance criteria (Gherkin), impacted components, and required integrations | Automated validation + reviewer checklist |
| SQ-2 | Stories touching AI must include data inputs, expected outputs, failure modes, and explainability artifacts | Review by AI lead + test harness |
| SQ-3 | Performance-sensitive stories must include SLO targets and test harness for load/latency | CI performance tests |

---

## 6. BDD and Testability Rules

| Rule | Description | Applies To |
|---|---|---|
| T-1 | All acceptance criteria must be expressed as executable BDD/Gherkin scenarios | Story validation in pipeline |
| T-2 | Integration flows (Experian, HMRC, T24, DocuSign) require contract tests and DLQ/poison-message tests | Integration test suites |
| T-3 | AI scoring end-to-end must have deterministic integration tests for happy and failure paths (including model unavailability) | Integration + chaos tests (simulate timeouts) |

---

## 7. Security and Compliance Rules

| Rule | Description | Source | Blocking? |
|---|---|---|---|
| S-1 | PII stored and processed only in UK regions; no cross-border backups | BRS constraints / Data residency | Yes |
| S-2 | All at-rest and in-transit encryption required (AES-256, TLS 1.3) | NFR-004 | Yes |
| S-3 | Service-to-service uses managed identities; no secrets in code | Architecture | Yes |
| S-4 | AI model decisions must be explainable and auditable (no opaque black-box without explanation) | Constraints: FCA | Yes |

---

## 8. Documentation Rules

| Rule | Description | Applies To |
|---|---|---|
| D-1 | Every integration must include API contract, fallback behavior, and monitoring spec | Integration artifacts |
| D-2 | AI features must include model card, data lineage, and explainability notes | AI Scoring Service docs |
| D-3 | Operational runbooks for failover, DLQ handling, and incident response must be created before production | Operations |

---

## 9. AI Implementation Safety Rules

| Rule | Description | Rationale |
|---|---|---|
| AI-1 | Do not change architecture, data residency, or governance rules without an ADR and human approval | Preserves compliance |
| AI-2 | Do not make product or policy decisions (e.g., altering recommendation thresholds) — require product/PO sign-off | Prevents autonomous product drift |
| AI-3 | All AI decisions must include explainability metadata and correlationId/idempotencyKey in logs | Traceability and FCA compliance |
| AI-4 | On model or third-party failure, default routing is REFER_TO_UNDERWRITER and an audit entry must be written | Preserves human oversight and audit trail |
| AI-5 | Agents may edit implementation details (code formatting, refactors) but may not modify requirements, acceptance criteria, or gating rules | Maintain source-of-truth |

---

## 10. Definition of Ready

A story is ready for implementation when all of the following are true:

- [ ] Business goal is clear and specific (references FR-###)
- [ ] Acceptance criteria are testable and expressed as BDD/Gherkin
- [ ] Architecture impact and deployment constraints are documented
- [ ] Dependencies (integrations, data, approvals) are explicit and available
- [ ] Security, privacy, and compliance concerns are addressed or have owners assigned
- [ ] Performance targets / SLOs are specified for NFRs where applicable

---

## 11. Definition of Done

A story is done when:

- [ ] All acceptance criteria implemented and verified by automated tests
- [ ] All BDD scenarios pass in CI
- [ ] Integration contracts validated (contract tests pass)
- [ ] Observability and audit events emitted as specified
- [ ] Documentation (runbook, integration spec, model card) is committed
- [ ] Peer review and any required human gate approvals completed

---

## 12. Blocking Conditions

Implementation must stop if:

| Condition | Resolution Path |
|---|---|
| Unresolved high-priority open question (owner unresponsive) | Escalate to product owner; pause implementation |
| Non-compliant data residency or encryption configuration | Reject deployment; remediate with infra team |
| AI explainability or audit gap preventing regulatory traceability | Pause releases; require remediation and revalidation |
| Story fails quality gate repeatedly (3x) | Return to author for rewrite and re-review |

---

## 13. Human Review Checkpoints

| Checkpoint | After Phase | Owner | Purpose |
|---|---|---|---|
| Requirements review | 1-requirements | product-owner | Validate requirement completeness and accuracy |
| Architecture review | 3-architecture-context | architect | Validate architecture fit and constraints |
| AI safety review | 5-ai-design | Head of AI / Compliance | Validate explainability, model card, and fallback behavior |
| Readiness review (go/no-go) | 9-readiness-review | engineering-lead / security | Validate readiness for production rollout |

---

This constitution governs all downstream phases. Every artifact must be validated against it. Set Status: Accepted only by human approval. Never self-accept.
