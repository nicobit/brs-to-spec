# Delivery Constitution

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I011-MB |
| Created at | 2026-06-28 |
| Created by | governance-architect |
| Status | Draft |

---

## 1. Purpose

Deliver a governed, auditable pathway to transform the provided Business Requirements Specification into implementation-ready artifacts for a UK-focused AI-assisted loan origination platform. This constitution sets non-negotiable rules for requirement authoring, architecture alignment, AI safety, testing, and human review checkpoints that all downstream phases must observe.

---

## 2. Delivery Principles

| # | Principle | Rationale |
|---|---|---|
| 1 | Compliance-first delivery | Initiative operates in a regulated UK banking domain (FCA, GDPR) and must prioritise traceability and auditability |
| 2 | Architecture-aware stories | Every story must state architecture impacts and constraints to avoid emergent coupling |
| 3 | Evidence-driven traceability | All acceptance criteria must link to specific BRS items to enable verifiable coverage |
| 4 | Minimal AI autonomy without oversight | AI may make recommendations but human oversight is required for high-impact/edge decisions |
| 5 | Reproducible, testable outputs | Artifacts must enable automated verification (BDD/observability) and clear rollback paths |

---

## 3. Requirement Handling Rules

| Rule | Description | Consequence of Violation |
|---|---|---|
| Canonical references required | Every requirement must include a unique ID and be referenced from stories and coverage artifacts | Fails story quality gate |
| Testable ACs only | Acceptance criteria must be measurable and include BDD scenarios for happy and negative paths | Validation failure — reopen for rewrite |
| No ambiguous scope growth | Any scope change must be recorded as a formal decision and impact ADR | Delay and re-evaluation at readiness gate |

---

## 4. Architecture Alignment Rules

| Rule | Description | Applies To |
|---|---|---|
| Platform and data residency | All services and data must remain within UK datacentres and follow specified platform constraints | Integrations, deployment, storage |
| Integration contracts honoured | Use Experian, DocuSign, and Temenos T24 as specified by the BRS unless an ADR dictates change | Integration workstreams |
| ADR required for changes | Any change that affects core banking integration, data residency, or model vendor requires an ADR | Architecture/ops teams |

---

## 5. Story Quality Rules

| Rule | Description | Check Method |
|---|---|---|
| ID and title consistency | Story IDs and titles must match the canonical requirement references | Automated lint check |
| Implementation checklist | Each story must include dependencies, impacted services, rollback plan, and owner | Story template validation |
| Security & privacy annotations | Stories touching PII must declare data handling and encryption requirements | Peer review |

---

## 6. BDD and Testability Rules

| Rule | Description | Applies To |
|---|---|---|
| BDD scenarios required | Happy path plus at least one negative/error path per story | Feature tests and CI |
| Observable events | Critical state transitions (submission, scoring, decision, disbursement) must emit structured events | Observability pipelines |
| Automated acceptance gating | CI must run BDD scenarios and fail when regressions are detected | CI pipelines |

---

## 7. Security and Compliance Rules

| Rule | Description | Source | Blocking? |
|---|---|---|---|
| Data residency enforcement | All PII and audit logs stored within UK-only datacentres | UK GDPR | Yes |
| Encryption at rest and in transit | AES-256 for at-rest and TLS 1.3 for in-transit | NFRs | Yes |
| AML/KYC handling | AML and KYC checks are mandatory pre-offer; failures route to compliance team | BRS (FR-012, FR-013) | Yes |
| Explainability for AI decisions | Models used for scoring must be explainable and auditable | FCA requirements | Yes |

---

## 8. Documentation Rules

| Rule | Description | Applies To |
|---|---|---|
| Artifact provenance | Every artifact must include metadata: author, created_at, source BRS IDs referenced | All primary artifacts |
| ADRs for design changes | Architecture decisions must be captured as ADRs and linked from the relevant artifacts | Architecture and integration changes |

---

## 9. AI Implementation Safety Rules

| Rule | Description | Rationale |
|---|---|---|
| Do not change architecture without an ADR | AI or agents must not alter architecture artifacts or decisions | Prevent drift and unsafe changes |
| Do not make product decisions | Agents must not accept changes to scope or product rules without human sign-off | Preserve product governance |
| Do not cross governed boundaries | Agents must not move data or trigger flows that violate data residency or compliance rules | Regulatory compliance |
| Include do-not-touch rules in every handoff | Handoffs must list system components and data domains that are immutable for the implementation | Clear operational constraints |

---

## 10. Definition of Ready

A story is ready for implementation when:

- [ ] Business goal is clear and specific
- [ ] Acceptance criteria are testable
- [ ] Architecture impact is understood
- [ ] Dependencies are explicit
- [ ] Security and compliance concerns are addressed
- [ ] BDD scenarios exist for happy path and negative cases
- [ ] Impacted files or areas are identified

---

## 11. Definition of Done

A story is done when:

- [ ] All acceptance criteria are implemented and verified
- [ ] All BDD scenarios pass
- [ ] Architecture constraints are respected
- [ ] No blocking open questions remain
- [ ] Regression risks are addressed
- [ ] Code review is complete

---

## 12. Blocking Conditions

Implementation must stop if:

| Condition | Resolution Path |
|---|---|
| Unresolved blocking gap | Escalate to product owner and pause affected work |
| Missing architecture decision | Create ADR and rerun readiness review |
| Security risk not assessed | Escalate to security reviewer and halt release |
| Story failed quality gate | Rewrite story and re-submit for review |

---

## 13. Human Review Checkpoints

| Checkpoint | After Phase | Owner | Purpose |
|---|---|---|---|
| Requirements review | 1-requirements | product-owner | Validate requirement completeness and accuracy |
| Architecture review | 3-architecture-context | architect | Validate architecture fit and constraints |
| Story quality review | 6-story-quality-gate | qa-analyst | Validate stories are implementation-ready |
| Readiness review | 9-readiness-review | engineering-lead | Validate initiative is ready for AI implementation |

---

## 14. Advisory Reviews

Advisory reviews provide optional expert perspectives on artifacts before gate review. When enabled, configured personas review artifacts through their specific lens and produce structured findings appended to the artifact.

| Setting | Value |
|---|---|
| Advisory reviews enabled | No |

### Enabled Personas

| Persona | Lens | Activates when |
|---|---|---|
| qa-analyst | Testability, edge cases, AC quality | Always (if enabled) |
| devops-engineer | Infrastructure gaps, pipeline needs, enablers | Always (if enabled) |
| security-reviewer | Auth, encryption, data boundaries | Always (if enabled) |
| architect | Coupling, architecture rules, NFRs | Always (if enabled) |
| ui-ux-expert | UI states, validation UX, accessibility | Epic has Frontend stories |

---
*This constitution governs all downstream phases. Every artifact must be validated against it. Set Status: Accepted only by human approval. Never self-accept.*
