# Delivery Constitution

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I944-DINA |
| Created at | 2026-07-02 |
| Created by | governance-architect |
| Status | Draft |

---

## 1. Purpose

This initiative delivers an internal Digital Transfer Agent (DTA) platform that orchestrates investor servicing, transfer agency workflows, compliance decisioning, and onchain interoperability for tokenized funds. The constitution defines governance rules that ensure safe, traceable, and auditable transformation of the business requirements into implementation artifacts.

---

## 2. Delivery Principles

| # | Principle | Rationale |
|---|---|---|
| 1 | Internal ownership of business decisions | The bank/asset manager retains product, policy, and compliance ownership — Chainlink is infrastructure only |
| 2 | Authoritative offchain golden record | Internal books remain the legal source-of-truth unless an explicit legal model changes that |
| 3 | Least-privilege onchain interactions | Smart contracts execute approved actions; policy and eligibility remain internal |
| 4 | Incremental, testable delivery | Start focused (one fund/chain) and expand; ensure BDD and measurable coverage |
| 5 | Explicit, verifiable governance rules | Every rule must be traceable to BRS or architecture inputs |

---

## 3. Requirement Handling Rules

| Rule | Description | Consequence of Violation |
|---|---|---|
| Canonical requirement source | All requirement statements must reference `input/brs.md` sections or an explicit requirement ID | Reject downstream artifacts until references fixed |
| Testable acceptance criteria | Each requirement must include testable acceptance criteria (BDD when applicable) | Story rejected at story-quality gate |
| No implicit scope expansion | New functional scope requires an approved change request and ADR | Implementation paused until approval |

---

## 4. Architecture Alignment Rules

| Rule | Description | Applies To |
|---|---|---|
| Use Chainlink as infrastructure only | Chainlink DTA standard, CRE, CCIP, NAVLink used for onchain integration; business logic remains in internal DTA | Integration patterns, smart contract interactions |
| Golden record authority | Internal DTA ledger is authoritative unless ADR specifies onchain legal model | Reconciliation, reporting, audit |
| Controlled rollout | Start with one fund and one controlled chain; require ADR to expand to public chains | Deployment and release plans |

---

## 5. Story Quality Rules

| Rule | Description | Check Method |
|---|---|---|
| Definition of Ready enforced | Stories must satisfy the Definition of Ready checklist below | Automated gate + human review |
| Traceability to BRS | Every story must list referenced BRS sections/IDs | Coverage report verification |
| BDD for critical flows | Subscriptions, redemptions, mint/burn, reconciliation must include BDD scenarios | CI BDD tests or documented scenarios |

---

## 6. BDD and Testability Rules

| Rule | Description | Applies To |
|---|---|---|
| BDD for happy & negative paths | Provide Gherkin scenarios for main flows and common failure modes | Core flows (subscription, redemption, reconciliation) |
| Observable outcomes | Each test must assert reconciliation status and onchain/offchain evidence | Reconciliation tests |
| Idempotent orchestration tests | CRE workflows must be tested for retry and eventual consistency behavior | CRE integration tests |

---

## 7. Security and Compliance Rules

| Rule | Description | Source | Blocking? |
|---|---|---|---|
| Sensitive data offchain | Personal data and KYC/AML data remain offchain; only hashes/attestations onchain | BRS section 4.2.2 | Yes |
| Compliance policy owner | Internal compliance service remains policy owner; Chainlink ACE may enforce checks but not own policy | BRS eligibility section | Yes |
| Access controls and allowlists | Wallets, distributor roles and operator actions must be allowlisted and audited | Architecture constraints | Yes |

---

## 8. Documentation Rules

| Rule | Description | Applies To |
|---|---|---|
| Traceability sections required | All artifacts must include `Requirements Referenced` and `Open Questions` sections | All artifacts |
| Operational runbooks | Reconciliation, exception handling, and incident runbooks must be authored before production rollout | Operations artifacts |

---

## 9. AI Implementation Safety Rules

| Rule | Description | Rationale |
|---|---|---|
| Do not change architecture without an ADR | Any architecture change requires an ADR and human sign-off | Prevent drift and unsafe changes |
| Do not make product decisions | Agents may propose changes but product/PO approves scope changes | Preserve business ownership |
| Do not cross governed boundaries | Agents must not modify security, compliance, or legal controls without explicit human approval | Prevent unauthorized changes |
| Include do-not-touch rules in every handoff | Each implementation artifact must list invariants and do-not-touch boundaries | Ensures downstream safety |

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
| Unresolved blocking gap | Escalate to product owner and pause delivery |
| Missing architecture decision | Create ADR and obtain architect sign-off |
| Security risk not assessed | Escalate to security reviewer; perform threat assessment |
| Story failed quality gate | Rewrite story and re-run validation |

---

## 13. Human Review Checkpoints

| Checkpoint | After Phase | Owner | Purpose |
|---|---|---|---|
| Requirements review | 1-requirements | product-owner | Validate requirement completeness and accuracy |
| Architecture review | 3-architecture-context | architect | Validate architecture fit and constraints |
| Story quality review | 6-story-quality-gate | qa-analyst | Validate stories are implementation-ready |
| Readiness review | 9-readiness-review | engineering-lead | Validate initiative is ready for AI-assisted implementation |

---

## 14. Advisory Reviews

Advisory reviews provide optional expert perspectives on artifacts before gate review. When enabled, configured personas (qa-analyst, devops-engineer, security-reviewer, architect, ui-ux-expert) review artifacts and append structured findings. Findings are informational and do not block the gate unless explicitly configured in `stage-actions.yaml`.

| Setting | Value |
|---|---|
| Advisory reviews enabled | Yes |

*Status: Draft — set to Accepted only after the human acceptance gate.*
