# Delivery Constitution

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I093-I3 |
| Created at | 2026-06-22 |
| Created by | governance-architect |
| Status | Draft |

---

## 1. Purpose

This initiative delivers an AI-assisted digital loan origination platform to replace manual underwriting for personal loans. The constitution defines governance rules, safety boundaries, and quality gates that all downstream artifacts (requirements, stories, architectures, and code) must follow to ensure regulatory compliance, data residency, explainability, and safe AI-assisted delivery.

---

## 2. Delivery Principles

| # | Principle | Rationale |
|---|---|---|
| 1 | Regulatory-first delivery | Must meet FCA, AML/KYC, and UK GDPR requirements before production launch |
| 2 | Data residency and encryption | All PII remains in UK data centres and is encrypted at rest and in transit (AES-256/TLS1.3) |
| 3 | Explainable AI & human oversight | AI recommendations must be explainable and human-underwritable; humans retain final authority for non-straight-through cases |
| 4 | Traceability and immutable audit | Every state transition and underwriter action is recorded immutably for auditability |
| 5 | Lean, review-driven delivery | Produce minimal artifacts required for safe implementation, with fast feedback loops and quality gates |

---

## 3. Requirement Handling Rules

| Rule | Description | Consequence of Violation |
|---|---|---|
| `REQ-ID` required | Every requirement must have a canonical ID (e.g. FR-### / NFR-###) and map to BRS sections | Requirement is rejected from downstream catalogs |
| Traceable source | Each rule must cite the BRS paragraph or architecture source that justifies it | Editor must add citation or the rule is moved to assumptions |
| Testable acceptance criteria | AC must be measurable (timing, thresholds, boolean outcomes) | Story fails the quality gate until AC is fixed |
| No product decisions in governance | Governance defines constraints; it does not choose vendor or detailed UI flows | Out-of-scope product decisions remain with product owner |

---

## 4. Architecture Alignment Rules

| Rule | Description | Applies To |
|---|---|---|
| Integrations contract-first | Experian, HMRC, DocuSign, and Temenos T24 integrations require explicit API contracts and error/fallback behaviours | Integration workstreams |
| Data boundary enforcement | All PII processing must occur within UK-hosted environments and be marked in dataflow diagrams | Services handling PII |
| Circuit-breakers and fallbacks | External API calls (Experian, HMRC) must implement circuit breakers and deterministic fallback routing (refer to BRS FR-009/FR-013) | Integration adapters |
| ADR requirement | Any deviation from these rules requires an Architecture Decision Record (ADR) | Architecture team |

---

## 5. Story Quality Rules

| Rule | Description | Check Method |
|---|---|---|
| Clear intent | Story has single, testable business outcome | AC and BDD scenarios review |
| Acceptance criteria present | AC covering success and key failure modes | Automated gate checks |
| BDD scenarios | At least happy-path and one negative case exist | Gherkin scenarios reviewed by QA |
| Non-functional targets | Relevant NFRs (latency, throughput, availability) referenced | Performance test or annotation |

---

## 6. BDD and Testability Rules

| Rule | Description | Applies To |
|---|---|---|
| Gherkin-first | BDD scenarios drive automated tests and acceptance criteria | Feature stories and end-to-end flows |
| Observability hooks | Stories must specify emitted observability events (ARN, timestamps, status) | All story outputs specified |
| Test data classification | Test datasets must be synthetic or consented; no real PII in test environments | QA pipelines |

---

## 7. Security and Compliance Rules

| Rule | Description | Source | Blocking? |
|---|---|---|---|
| Mandatory AML/KYC | AML (HM Treasury lists) and KYC (HMRC check) required before offer generation | BRS FR-012/FR-013 | Yes |
| PII encryption | All PII encrypted at rest and in transit (AES-256/TLS1.3) | NFR-004 | Yes |
| Data residency | All production data remains in UK datacenters | Constraints | Yes |
| Immutable audit | All underwriter and system actions are immutably logged | FR-028 | Yes |

---

## 8. Documentation Rules

| Rule | Description | Applies To |
|---|---|---|
| ADRs for deviations | Any architectural deviation requires an ADR with owner and impact | Architecture and infra changes |
| API contracts in repo | All external integration contracts stored in `input/repository-context.md` or repo contracts folder | Integration workstreams |
| Security runbook | Security and incident runbooks must be published before production | Operations and security teams |

---

## 9. AI Implementation Safety Rules

| Rule | Description | Rationale |
|---|---|---|
| Do not change architecture without an ADR | AI agents may suggest but cannot commit architectural changes | Prevent unauthorized design drift |
| Do not make product decisions | Agents cannot alter scope, pricing, or eligibility rules (product owner only) | Preserve business intent |
| Do not cross governed boundaries | Agents must not move PII outside UK regions or remove encryption flags | Regulatory compliance |
| Include do-not-touch rules in every handoff | Hand-offs must list fields, services, and data that are off-limits for automated edits | Prevent accidental changes |
| Log all agent actions | Every automated change must record agent id, prompt, timestamp, and diff | Auditability and rollback |

---

## 10. Definition of Ready

A story is ready for implementation when:

- [ ] Business goal is clear and specific
- [ ] Acceptance criteria are testable
- [ ] Architecture impact is understood and ADRs identified where needed
- [ ] Dependencies are explicit and tracked
- [ ] Security and compliance concerns are addressed or have owners assigned
- [ ] BDD scenarios exist for happy path and negative cases
- [ ] Impacted files or areas are identified

---

## 11. Definition of Done

A story is done when:

- [ ] All acceptance criteria are implemented and verified
- [ ] All BDD scenarios pass in CI
- [ ] Architecture constraints are respected and any required ADRs are closed
- [ ] No blocking open questions remain
- [ ] Regression risks are addressed and smoke tests pass
- [ ] Code review and security scan are complete

---

## 12. Blocking Conditions

Implementation must stop if:

| Condition | Resolution Path |
|---|---|
| Unresolved blocking gap (regulatory or security) | Escalate to product owner and compliance; pause implementation |
| Missing or failing integration contract (Experian/HMRC/T24) | Create or fix API contract; integration tests must pass |
| Security risk not assessed | Escalate to security reviewer; do not proceed until mitigated |
| Story failed quality gate | Rework story to satisfy requirements |

---

## 13. Human Review Checkpoints

| Checkpoint | After Phase | Owner | Purpose |
|---|---|---|---|
| Requirements review | 1-requirements | product-owner | Validate requirement completeness and accuracy |
| Architecture review | 1-requirements-and-architecture | architect | Validate architecture fit and constraints |
| Story quality review | 3-epic-elaboration | qa-analyst | Validate stories are implementation-ready |
| Readiness review | 2-delivery-planning | engineering-lead | Validate initiative is ready for AI implementation |

---

## 14. Advisory Reviews

Advisory reviews provide optional expert perspectives on artifacts before gate review. When enabled, each configured persona reviews the artifact through its specific lens and produces structured findings appended to the artifact. Findings do not block gates.

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
| ui-ux-expert | UI states, validation UX, accessibility | Epic has Frontend stories |

---

This constitution governs all downstream phases. Every artifact must be validated against it. Set Status: Accepted only by human approval. Never self-accept.
