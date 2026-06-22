# Delivery Constitution

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I011-N2 |
| Created at | 2026-06-21 |
| Created by | governance-architect |
| Status | Draft |

---

## 1. Purpose

This constitution establishes the governance rules and non-negotiable constraints for delivering a UK-resident, regulatory-compliant AI-powered personal loan origination platform that reduces decision time, preserves human oversight for complex cases, and provides an immutable audit trail for regulatory review.

---

## 2. Delivery Principles

| # | Principle | Rationale |
|---|---|---|
| 1 | Data residency and encryption in UK only | UK GDPR and deployment constraint in architecture
| 2 | Explainable scoring models only | FCA requirement: no black-box models
| 3 | Fail-safe routing to human review on external dependency failure | Maintain service continuity and compliance (Experian/HMRC fallbacks)
| 4 | Immutable audit trail for every decision and state transition | Regulatory auditability requirement
| 5 | Minimal scope per increment, design for vertical slices | Faster feedback and lower risk

---

## 3. Requirement Handling Rules

| Rule | Description | Consequence of Violation |
|---|---|---|
| R-1 | Every requirement must include a measurable success criterion | Story cannot pass readiness gate without it |
| R-2 | All acceptance criteria must be testable via BDD scenarios | Story rejected by story-quality gate if missing |
| R-3 | Requirements that affect PII, AML/KYC, or scoring must include compliance notes and data flows | Implementation blocked until compliance sign-off |

---

## 4. Architecture Alignment Rules

| Rule | Description | Applies To |
|---|---|---|
| A-1 | All services must remain within UK regions (primary: UK South, DR: UK West) | Deployment and infra
| A-2 | AI Scoring must provide explanation metadata for every decision | AI Scoring Service
| A-3 | External integrations must implement circuit breakers and documented fallbacks | Experian, HMRC, DocuSign, T24

---

## 5. Story Quality Rules

| Rule | Description | Check Method |
|---|---|---|
| SQ-1 | Story includes impact analysis on architecture and data residency | Review checklist
| SQ-2 | Story lists all dependent integrations and error-handling behaviours | Manual review
| SQ-3 | Story includes Definition of Done with observability and audit verification steps | Automated tests + review

---

## 6. BDD and Testability Rules

| Rule | Description | Applies To |
|---|---|---|
| T-1 | Every acceptance criterion must map to one or more BDD scenarios (happy + negative paths) | All user-facing and scoring behaviours
| T-2 | Tests must include performance assertions for end-to-end scoring latency (NFR-002) | AI pipeline
| T-3 | Compliance flows must have automated checks that assert AML/KYC routing and audit entries | Compliance Service

---

## 7. Security and Compliance Rules

| Rule | Description | Source | Blocking? |
|---|---|---|---|
| S-1 | All PII encrypted at rest and transit (AES-256, TLS 1.3) | NFR-004 | Yes |
| S-2 | Data residency enforced — no data outside UK regions | Constraints | Yes |
| S-3 | AML/KYC screening must complete within defined latency budgets; failures route to compliance queue | FR-012/FR-013, NFR-007 | Yes |
| S-4 | Audit log writes are append-only and tamper-evident | FR-028, NFR-005 | Yes |

---

## 8. Documentation Rules

| Rule | Description | Applies To |
|---|---|---|
| D-1 | Every integration must have API contract, retry strategy, and fallback documented | Experian, HMRC, T24, DocuSign
| D-2 | ADRs must be created for architecture decisions that change service boundaries or data flows | Architecture and infra

---

## 9. AI Implementation Safety Rules

| Rule | Description | Rationale |
|---|---|---|
| Do not change architecture without an ADR | Ensures traceability and review |
| Do not make product decisions | Product-owner owned |
| Do not cross governed boundaries (data residency, encryption, audit immutability) | Regulatory safety |
| Include do-not-touch rules in every handoff | Prevent unsafe automated edits by agents |
| Require explicit human approval for any automatic model-retraining that affects decision thresholds | Prevent drift without governance |

---

## 10. Definition of Ready

A story is ready for implementation when:

- [ ] Business goal is clear and specific
- [ ] Acceptance criteria are testable and expressed as BDD scenarios
- [ ] Architecture impact is documented and low-risk or has mitigation
- [ ] Dependencies and external contracts are listed
- [ ] Security and compliance concerns are addressed or have owners assigned
- [ ] Observability and audit requirements are specified

---

## 11. Definition of Done

A story is done when:

- [ ] All acceptance criteria are implemented and verified
- [ ] All BDD scenarios pass in CI
- [ ] Architecture constraints are respected and ADRs updated if needed
- [ ] No open blocking compliance or security items
- [ ] Audit entries created and verified for the covered flows
- [ ] Code review and QA sign-off completed

---

## 12. Blocking Conditions

Implementation must stop if:

| Condition | Resolution Path |
|---|---|
| Unresolved regulatory requirement or non-compliance risk | Escalate to Compliance and Product Owner; stop implementation |
| External integration contract missing or unavailable | Defer feature behind feature flag or escalate to procurement |
| AI model lacks required explainability evidence | Block model deployment until explainability assurances are provided |
| Data residency breach risk | Stop and remediate with security lead |

---

## 13. Human Review Checkpoints

| Checkpoint | After Phase | Owner | Purpose |
|---|---|---|---|
| Requirements review | 1-requirements | product-owner | Validate requirement completeness and alignment to objectives (OBJ-001..)
| Architecture review | 3-architecture-context | solution-architect | Validate deployment, data residency, and integration approaches
| Security & compliance review | 4-security | compliance-officer | Validate AML/KYC, GDPR, FCA obligations
| Story quality review | 6-story-quality-gate | qa-analyst | Validate story readiness for implementation
| Readiness review | 9-readiness-review | engineering-lead | Validate initiative is ready for incremental AI implementation

---

*This constitution is the governance source for downstream phases. Its Status becomes `Accepted` only after a human approval gate.*
