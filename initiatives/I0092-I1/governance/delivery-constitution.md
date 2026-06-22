# Delivery Constitution

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I0092-I1 |
| Created at | 2026-06-22 |
| Created by | governance-architect |
| Status | Draft |

---

## 1. Purpose

This initiative delivers a digital, AI-assisted personal loan origination platform that replaces the current manual underwriting flow with a repeatable, auditable, and regulated process. This constitution defines the governance rules that all upstream and downstream artifacts (requirements, stories, architecture, and handoffs) must follow to ensure regulatory compliance, data residency, explainability, and safe AI-assisted automation.

---

## 2. Delivery Principles

| # | Principle | Rationale |
|---|---|---|
| 1 | Data residency and privacy-first | All PII and audit data remain in UK data centres to satisfy GDPR and bank policy |
| 2 | Explainability and auditability | AI scoring must be explainable; every decision must have an immutable audit trail |
| 3 | Human-in-the-loop for risk cases | Automated decisions limited by rules; refer-to-underwriter for complex, high-risk, or external-failure cases |
| 4 | Safety-first AI automation | AI agents may automate routine approvals only within bounded, verifiable rules and monitoring |
| 5 | Fail-safe integration behaviour | External API failures route to conservative flows (refer or manual review) to avoid unsafe automation |

---

## 3. Requirement Handling Rules

| Rule | Description | Consequence of Violation |
|---|---|---|
| R-1 | Every functional requirement must reference the BRS ID and map to one or more atomic requirements | Requirement will be returned for correction |
| R-2 | Requirements must include acceptance criteria and traceable success measures (see BRS objectives OBJ-001..OBJ-005) | Fails story readiness checks |
| R-3 | Any requirement that affects data residency, encryption, or regulatory obligations must include a compliance statement and owner | Work cannot proceed until owner signs off |

---

## 4. Architecture Alignment Rules

| Rule | Description | Applies To |
|---|---|---|
| A-1 | All services and storage must be deployed to Azure UK South or UK West | Deployment artifacts, IaC, service manifests |
| A-2 | Audit log storage must be append-only and tamper-evident (Cosmos DB append-only container) | Audit and operations teams |
| A-3 | External integrations (Experian, HMRC, DocuSign, T24) must implement circuit breakers and fallbacks | Integration contracts and adapters |
| A-4 | AI Scoring Service must expose model explainability artifacts for every score | AI service, model infra |

---

## 5. Story Quality Rules

| Rule | Description | Check Method |
|---|---|---|
| SQ-1 | Each story must include a single, testable acceptance criterion and BDD scenarios | Automated checklist during story validation |
| SQ-2 | Any story that modifies scoring, AML/KYC, or e-sign flows must list impacted integrations and security controls | Architecture-impact review |
| SQ-3 | Stories must include data masking requirements for logs and descriptions of audit events emitted | Static validation and code review |

---

## 6. BDD and Testability Rules

| Rule | Description | Applies To |
|---|---|---|
| T-1 | Provide BDD scenarios for happy path and key negative cases (e.g., Experian unavailable, AML match) | Functional stories and acceptance tests |
| T-2 | Provide synthetic test data templates that preserve PII constraints (use masked/anon datasets) | QA pipelines |
| T-3 | Automated pipelines must run core BDD scenarios for PR validation | CI pipeline configuration |

---

## 7. Security and Compliance Rules

| Rule | Description | Source | Blocking? |
|---|---|---|---|
| S-1 | All PII encrypted at rest (AES-256) and in transit (TLS 1.3) | NFR-004, architecture | Yes |
| S-2 | AML/KYC checks required before any offer generation | FR-012, FR-013 | Yes |
| S-3 | Immutable audit trail for all state changes within 24h | OBJ-003, FR-028 | Yes |
| S-4 | Model explainability evidence retained and available for audits | Constraint: explainable models only | Yes |

---

## 8. Documentation Rules

| Rule | Description | Applies To |
|---|---|---|
| D-1 | Every integration must publish a lightweight contract (endpoints, SLAs, fallback) | Integration adapters |
| D-2 | ADRs required for any architecture decision that changes deployment, data residency, or core integrations | Architecture repo |
| D-3 | Open questions and decisions must be tracked in `.b2s/state/open-decisions.md` | Governance artifacts |

---

## 9. AI Implementation Safety Rules

| Rule | Description | Rationale |
|---|---|---|
| Do not change architecture without an ADR | Any architectural change must be documented and approved |
| Do not make product decisions | AI agents may not alter business rules or acceptance criteria |
| Do not cross governed boundaries | AI must not update audit logs, compliance flags, or legal text directly |
| Include do-not-touch rules in every handoff | Engineers and agents must respect these boundaries |
| AI decisions must be explainable and retain evidence | Supports FCA compliance and audits |

---

## 10. Definition of Ready

A story is ready for implementation when:

- [x] Business goal is clear and specific
- [x] Acceptance criteria are testable
- [x] Architecture impact is understood and documented
- [x] Dependencies are explicit
- [x] Security and compliance concerns are addressed or have owners
- [x] BDD scenarios exist for happy path and key negative cases
- [x] Impacted integrations and fallbacks are identified

---

## 11. Definition of Done

A story is done when:

- [ ] All acceptance criteria are implemented and verified
- [ ] All BDD scenarios pass in CI
- [ ] Architecture constraints are respected
- [ ] No blocking open questions remain
- [ ] Regression risks are addressed
- [ ] Code review and security review are complete

---

## 12. Blocking Conditions

Implementation must stop if:

| Condition | Resolution Path |
|---|---|
| Unresolved regulatory or data-residency gap | Escalate to legal / architecture owners; do not proceed |
| Missing architecture decision that affects deployments | Create ADR and wait for approval |
| External integration with no fallback | Implement conservative fallback (refer to underwriter) or block |
| Story failed quality gate repeatedly | Rework story and re-validate |

---

## 13. Human Review Checkpoints

| Checkpoint | After Phase | Owner | Purpose |
|---|---|---|---|
| Requirements review | 1-requirements | product-owner | Validate requirement completeness and alignment to objectives |
| Architecture review | 1-requirements-and-architecture | architect | Validate architecture fit and constraints |
| Story quality review | per-story gate | qa-analyst | Validate stories are implementation-ready and testable |
| Readiness review | pre-implementation | engineering-lead | Validate initiative is ready for AI-assisted implementation |

---
*This constitution governs all downstream phases. Every artifact must be validated against it. Set Status: Accepted only by human approval. Never self-accept.*
