# Delivery Constitution

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I010-GB |
| Created at | 2026-06-28 |
| Created by | governance-architect |
| Status | Draft |

---

## 1. Purpose

This initiative delivers a UK-hosted, auditable, AI-assisted loan origination platform to reduce manual decision times and provide consistent, regulatory-compliant outcomes for personal loan applications (£1,000–£50,000). This constitution defines governance rules that all later artifacts and implementation steps must follow.

---

## 2. Delivery Principles

| # | Principle | Rationale |
|---|---|---|
| 1 | Regulatory-first delivery | Requirements and designs must satisfy FCA Consumer Duty, AML/KYC, and UK GDPR before implementation |
| 2 | Data residency in UK only | All PII and audit logs remain in UK datacenters as required by NFRs |
| 3 | Traceability and auditability | Every decision, model input, and human action must be recorded immutably for audit |
| 4 | Explicit architecture decisions before stories | Technical decisions (create vs modify, integrations) must be captured in ADRs before backlog generation |
| 5 | AI explainability enforced | Models must be explainable and produce rationale compatible with regulatory review |

---

## 3. Requirement Handling Rules

| Rule | Description | Consequence of Violation |
|---|---|---|
| R-1 | Every requirement must link to a BRS section and include acceptance criteria | Requirement returned to author for clarification |
| R-2 | Requirements that change architecture must reference an ADR or create one | Story blocked until ADR exists |
| R-3 | Security / compliance requirements must include required evidence and test steps | Quality gate failure until evidence added |

---

## 4. Architecture Alignment Rules

| Rule | Description | Applies To |
|---|---|---|
| A-1 | Use Experian for credit reports per BRS | Credit integration flows |
| A-2 | Use Temenos T24 payment gateway for disbursement per BRS | Disbursement service |
| A-3 | E-signature via DocuSign per BRS | Offer acceptance flows |
| A-4 | All services must document data boundaries and retention in ADRs | Integration contracts and pipelines |

---

## 5. Story Quality Rules

| Rule | Description | Check Method |
|---|---|---|
| SQ-1 | Every story must include linked BRS IDs and acceptance criteria | Checklist in story template |
| SQ-2 | Stories with AI decision logic must include model inputs, outputs, and explainability acceptance criteria | Review by `ai-model-owner` and architect |
| SQ-3 | Performance-sensitive stories must include NFR verification steps and test harness notes | Performance test evidence attached |

---

## 6. BDD and Testability Rules

| Rule | Description | Applies To |
|---|---|---|
| T-1 | Each story must include BDD scenarios for happy path and key negative cases | Functional stories |
| T-2 | Acceptance criteria must be automatable where possible and include data fixtures | Stories integrating Experian/DocuSign/T24 |
| T-3 | Test data must be sanitized and marked as non-production; no real PII in test fixtures | All test suites |

---

## 7. Security and Compliance Rules

| Rule | Description | Source | Blocking? |
|---|---|---|---|
| S-1 | Encrypt all PII at rest (AES-256) and in transit (TLS 1.3) | NFR-004 | Yes |
| S-2 | Maintain immutable, tamper-evident audit log for decisions | FR-028, NFR-005 | Yes |
| S-3 | AML/KYC checks must run before offer generation | FR-012, FR-013 | Yes |
| S-4 | Data residency: all production data in UK datacenters only | Constraints | Yes |
| S-5 | Model explainability and rationale required for every automated decision | Constraints (FCA) | Yes |

---

## 8. Documentation Rules

| Rule | Description | Applies To |
|---|---|---|
| D-1 | Every architecture change requires an ADR with owner and decision rationale | Architecture work |
| D-2 | Integrations must include API contract, SLA expectations, and fallback behaviour | Experian, HMRC, DocuSign, T24 |
| D-3 | Operational runbooks and observability playbooks must be provided for production services | Ops handoff |

---

## 9. AI Implementation Safety Rules

| Rule | Description | Rationale |
|---|---|---|
| Do not change architecture without an ADR | Prevents hidden coupling and migration risks | |
| Do not make product risk decisions in model code | Product decisions require human PO approval | |
| Do not cross governed boundaries (data residency, PII treatment) | Ensures compliance with legal constraints | |
| Include do-not-touch rules in every handoff | Protects safety-critical components and audit trails | |

---

## 10. Definition of Ready

A story is ready for implementation when:

- [ ] Business goal is clear and specific
- [ ] Acceptance criteria are testable
- [ ] Architecture impact is understood and any ADRs exist
- [ ] Dependencies are explicit
- [ ] Security and compliance concerns are addressed
- [ ] BDD scenarios exist for happy path and negative cases
- [ ] Impacted files or areas are identified

---

## 11. Definition of Done

A story is done when:

- [ ] All acceptance criteria are implemented and verified
- [ ] All BDD scenarios pass
- [ ] Architecture constraints are respected and ADRs updated
- [ ] No blocking open questions remain
- [ ] Regression risks are addressed
- [ ] Code review is complete

---

## 12. Blocking Conditions

Implementation must stop if:

| Condition | Resolution Path |
|---|---|
| Unresolved regulatory requirement or compliance gap | Escalate to product owner and compliance reviewer |
| Missing architecture decision that affects scope | Create ADR and obtain architect sign-off |
| Security risk not assessed or mitigated | Escalate to security reviewer and pause implementation |
| Story failed quality gate | Rewrite story and revalidate |

---

## 13. Human Review Checkpoints

| Checkpoint | After Phase | Owner | Purpose |
|---|---|---|---|
| Requirements review | 1-requirements | product-owner | Validate requirement completeness and accuracy |
| Architecture review | 3-architecture-context | architect | Validate architecture fit and constraints |
| Story quality review | 6-story-quality-gate | qa-analyst | Validate stories are implementation-ready |
| Readiness review | 9-readiness-review | engineering-lead | Validate initiative is ready for AI implementation |

---

## Assumptions and Unknowns

- The provided `input/brs.md` is a working BRS; any contradicting BRS content will be surfaced as open questions.
- Integration contract details (API endpoints, credentials, SLAs) for Experian, HMRC, DocuSign, and T24 must be documented in `input/repository-context.md` or ADRs before implementation.

---

## 14. Advisory Reviews

Advisory reviews provide optional expert perspectives on artifacts before gate review. When enabled, each configured persona reviews the artifact through its specific lens (testability, infrastructure, security, architecture, UI) and produces structured findings. Findings are appended to the artifact but do not block the gate.

| Setting | Value |
|---|---|
| Advisory reviews enabled | Yes |

### Enabled Personas

| Persona | Lens | Activates when |
|---|---|---|
| qa-analyst | Testability, edge cases, AC quality | Always (if enabled) |
| devops-engineer | Infrastructure gaps, pipeline needs, enablers | Always (if enabled) |
| security-reviewer | Auth, encryption, data boundaries | Always (if enabled) |
| architect | Coupling, architecture rules, NFRs | Always (if enabled) |
| ui-ux-expert | UI states, validation UX, navigation, accessibility | Epic has Frontend stories |

To disable a specific persona, remove its row from the table above. To disable all advisory reviews, set "Advisory reviews enabled" to "No".

---

*This constitution governs downstream phases. Set Status to Accepted only by human approval at the readiness gate.*
