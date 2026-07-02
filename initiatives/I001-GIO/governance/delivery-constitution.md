# Delivery Constitution

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I001-GIO |
| Created at | 2026-07-02 |
| Created by | governance-architect |
| Status | Draft |

---

## 1. Purpose

This initiative delivers an AI-assisted digital loan origination platform to replace a fully manual personal loan workflow at the bank. The platform will enable applicants to submit loan applications online, receive AI-driven risk scoring within minutes, undergo AML/KYC compliance checks, and — for eligible cases — receive automated loan offers and disbursements without underwriter intervention. Underwriter oversight is preserved for complex, borderline, or high-value cases. This constitution defines the governance rules, quality expectations, and safety boundaries that must be respected across all requirements, architecture decisions, stories, and implementation artifacts throughout delivery.

---

## 2. Delivery Principles

| # | Principle | Rationale |
|---|---|---|
| 1 | Regulatory compliance is non-negotiable | FCA Consumer Duty, UK GDPR, AML, and KYC requirements are hard constraints — no story may be implemented without compliance alignment |
| 2 | Explainability over accuracy | FCA prohibits black-box AI decisions — the scoring model must produce auditable, human-readable decision rationale |
| 3 | Audit first, build second | Every application state transition must produce an immutable audit record before any other side effect |
| 4 | Fail safe, not fail open | All external API failures (Experian, HMRC, DocuSign, T24) must trigger defined fallbacks — never produce undefined system behaviour |
| 5 | Human oversight is preserved | Auto-approve paths are bounded (≤£10,000, AI recommendation only, AML/KYC cleared); all other cases go to underwriter or compliance review |
| 6 | Data residency is absolute | All data, storage, and processing must remain within Azure UK South or UK West — no exceptions |
| 7 | AI agent autonomy is bounded | AI coding agents must not modify security rules, AI model parameters, compliance logic, or audit infrastructure without explicit human review |

---

## 3. Requirement Handling Rules

| Rule | Description | Consequence of Violation |
|---|---|---|
| RHR-001 | Every functional requirement must trace to at least one epic | Requirement is excluded from backlog until assigned |
| RHR-002 | Requirements involving AML, KYC, or FCA compliance must be reviewed by the compliance team before a story is written | Story is blocked from implementation gate |
| RHR-003 | Open questions (OQ-*) must be resolved before a requirement that depends on them is elaborated into a story | Story creation is blocked |
| RHR-004 | All open questions from the BRS are resolved: OQ-001 (Azure Foundry), OQ-002 (no waiver flow needed), OQ-003 (HMRC fallback: manual verification), OQ-004 (HM Treasury only), OQ-005 (T24 API contract: we define) | Treat any newly discovered question as a blocking gap requiring escalation |
| RHR-005 | Non-functional requirements (NFR-*) must be incorporated into affected story acceptance criteria — they are not optional | Story is rejected at quality gate |
| RHR-006 | Requirements referencing external APIs must specify circuit breaker behaviour and fallback path | Architecture review will reject the requirement |

---

## 4. Architecture Alignment Rules

| Rule | Description | Applies To |
|---|---|---|
| AAR-001 | All services must be deployed exclusively to Azure UK South (primary) or Azure UK West (DR) | All components |
| AAR-002 | Service-to-service communication must use Azure Managed Identities — no stored secrets or connection strings with credentials | All backend services |
| AAR-003 | All inter-service async communication must use Azure Service Bus (AMQP) — direct service-to-service HTTP calls for async flows are not permitted | Loan Origination API, AI Scoring Service, Compliance Service, Notification Service |
| AAR-004 | All external API integrations must implement circuit breakers with the fallback defined: Experian → REFER_TO_UNDERWRITER; HMRC KYC → manual verification queue; DocuSign → hold offer pending; T24 → retry once then alert ops | Compliance Service, Loan Origination API, Payment Gateway Adapter |
| AAR-005 | The Audit Log Store (Azure Cosmos DB) is append-only — no update or delete operations are permitted under any circumstance | All services writing to audit log |
| AAR-006 | PII must not appear in application logs — use masked representations only | All services |
| AAR-007 | Experian credit bureau data must not be persisted — it is used transiently during scoring and discarded after the risk score is written | AI Scoring Service |
| AAR-008 | Azure API Management is the single ingress point — no service may be exposed directly to the internet | All backend APIs |
| AAR-009 | AI Scoring Service uses Azure Foundry (resolved: OQ-001) and must produce a decision rationale alongside every score | AI Scoring Service |
| AAR-010 | React/Next.js frontends are deployed as Azure Static Web Apps — no server-side rendering infrastructure beyond Next.js built-in | Applicant Portal, Underwriter Dashboard, Admin Dashboard |

---

## 5. Story Quality Rules

| Rule | Description | Check Method |
|---|---|---|
| SQR-001 | Every story must state a clear user role, goal, and benefit in standard "As a / I want / So that" format | Story quality gate automated check |
| SQR-002 | Acceptance criteria must use EARS notation (WHEN / THE SYSTEM SHALL) — plain English criteria are rejected | Story quality gate |
| SQR-003 | Every story must reference the FR-* requirement(s) it implements | Traceability matrix check |
| SQR-004 | Stories touching AML, KYC, audit log, or AI scoring must include a compliance-specific acceptance criterion | Manual compliance review |
| SQR-005 | Every story must identify the impacted service(s) from the architecture component list | Architecture alignment check |
| SQR-006 | Stories involving external API calls must include a negative scenario covering the circuit breaker / fallback path | BDD scenario review |
| SQR-007 | A story must not cross more than one bounded domain without explicit justification and architecture sign-off | Architecture review |

---

## 6. BDD and Testability Rules

| Rule | Description | Applies To |
|---|---|---|
| BDD-001 | Every story must include at least one Gherkin scenario for the happy path and at least one for a failure or edge case | All stories |
| BDD-002 | BDD scenarios for AML/KYC and AI scoring decisions must be deterministic — no probabilistic assertions | Compliance Service, AI Scoring Service stories |
| BDD-003 | AI model scoring scenarios must use fixed mock inputs and expected outputs — never call live model inference in automated tests | AI Scoring Service stories |
| BDD-004 | Audit log scenarios must assert that a log entry was created as part of the same test — audit correctness is not an afterthought | All stories that trigger state transitions |
| BDD-005 | Performance thresholds from NFR-001 (2s page load), NFR-002 (90s AI pipeline), NFR-003 (500 concurrent) must have acceptance test coverage at integration level | Performance-sensitive stories |
| BDD-006 | All circuit breaker fallback paths from AAR-004 must have a failing-dependency test scenario | Integration test suite |

---

## 7. Security and Compliance Rules

| Rule | Description | Source | Blocking? |
|---|---|---|---|
| SCR-001 | All PII must be encrypted at rest using AES-256 and in transit using TLS 1.3 | NFR-004 / Architecture | Yes |
| SCR-002 | AML screening against HM Treasury sanctions and PEP database must complete before any loan offer is generated | FR-012 / OQ-004 resolved | Yes |
| SCR-003 | KYC identity verification against HMRC identity API must complete before any offer is generated; fallback is manual verification queue (OQ-003 resolved) | FR-013 | Yes |
| SCR-004 | Applications in COMPLIANCE_HOLD must not receive a loan offer under any code path | FR-014 | Yes |
| SCR-005 | AI scoring model must produce an explainable rationale with every decision — FCA prohibits black-box models | FCA Consumer Duty / BRS Constraints | Yes |
| SCR-006 | All underwriter and admin access must be authenticated via Azure AD with RBAC enforced at API layer | Architecture security model | Yes |
| SCR-007 | Applicant status checks use ARN + date of birth — no account registration — with rate limiting enforced at APIM | FR-005 / Architecture | Yes |
| SCR-008 | UK GDPR data residency: all storage and processing must remain in Azure UK South or UK West | BRS Constraints | Yes |
| SCR-009 | Cooling-off period waiver does not require a separate legal sign-off UI step (OQ-002 resolved) | OQ-002 | No |
| SCR-010 | Audit log entries are immutable — no update or delete operations permitted; Cosmos DB container configured accordingly | NFR-005 / FR-028 | Yes |

---

## 8. Documentation Rules

| Rule | Description | Applies To |
|---|---|---|
| DCR-001 | Every epic must have an implementation contract summarising scope, impacted services, and integration dependencies | All epics |
| DCR-002 | Every integration point (Experian, HMRC, DocuSign, T24) must have an API contract document covering request/response schema, auth model, circuit breaker config, and fallback | Integration stories |
| DCR-003 | Every open architecture decision must produce an ADR (Architecture Decision Record) before implementation of the affected story begins | Architecture-impacting stories |
| DCR-004 | The AI scoring model approach (Azure Foundry) must be documented with its explainability mechanism before AI Scoring Service stories are implemented | AI Scoring Service epic |
| DCR-005 | The compliance team must sign off on AML and KYC story artifacts before they enter implementation | Compliance epic stories |

---

## 9. AI Implementation Safety Rules

| Rule | Description | Rationale |
|---|---|---|
| Do not change architecture without an ADR | AI coding agents must not modify the Azure deployment topology, component boundaries, or service communication patterns without a human-authored ADR | Architecture integrity is required for GDPR data residency and security model |
| Do not make product decisions | AI agents must not alter loan eligibility thresholds (e.g. the £10,000 auto-approve limit), risk score bands, AML database selection, or cooling-off period logic | These are regulated business rules requiring human and compliance approval |
| Do not cross governed boundaries | AI agents must not write code that bypasses the audit log, skips AML/KYC checks, or removes the COMPLIANCE_HOLD gate — even as a workaround for test scenarios | These boundaries are FCA and GDPR compliance requirements |
| Include do-not-touch rules in every handoff | Every story handoff artifact must explicitly list files and components that AI agents must not modify without a new story | Prevents unintended regression in compliance-critical code |
| Do not modify AI model parameters | AI agents must not alter the Azure Foundry model configuration, score thresholds, or feature weights — these require a documented model change process | FCA explainability and consistency requirements |
| Do not suppress or alter audit log writes | AI agents must not refactor, optimise, or remove audit log write operations from any service | Audit trail immutability is a legal requirement (NFR-005, FR-028) |
| Do not store Experian data | AI agents must not add persistence logic for credit bureau data beyond the transient scoring pipeline | GDPR and architecture constraint AAR-007 |

---

## 10. Definition of Ready

A story is ready for implementation when:

- [ ] Business goal is clear and specific with reference to the BRS FR-* requirement
- [ ] Acceptance criteria are in EARS notation (WHEN / THE SYSTEM SHALL)
- [ ] Architecture impact is identified — impacted services named from the component list
- [ ] Dependencies on other stories or external APIs are explicit
- [ ] Security and compliance concerns are addressed (AML, KYC, FCA, GDPR checks where applicable)
- [ ] BDD scenarios exist for at least one happy path and one failure / edge case
- [ ] Circuit breaker / fallback behaviour is defined for any external API call
- [ ] Audit log requirement is stated where a state transition occurs
- [ ] No unresolved blocking open questions remain for this story
- [ ] Performance thresholds from NFRs are incorporated into acceptance criteria where applicable
- [ ] Compliance team sign-off obtained for AML, KYC, and scoring stories

---

## 11. Definition of Done

A story is done when:

- [ ] All acceptance criteria are implemented and verified by automated tests
- [ ] All BDD scenarios pass in CI
- [ ] Architecture constraints (data residency, managed identities, APIM ingress, append-only audit) are respected
- [ ] No blocking open questions remain
- [ ] Regression risks are addressed — no existing tests broken
- [ ] Code review is complete with at least one senior reviewer
- [ ] Security checklist passed: PII not in logs, TLS enforced, RBAC applied
- [ ] Audit log entry produced for every state transition covered by the story
- [ ] Performance thresholds validated if the story touches a latency-sensitive path
- [ ] Documentation updated: API contract, ADR (if architecture change), compliance sign-off recorded

---

## 12. Blocking Conditions

Implementation must stop if:

| Condition | Resolution Path |
|---|---|
| AML or KYC compliance gate not passed | Escalate to compliance team; do not proceed |
| FCA explainability requirement not met for AI scoring changes | Escalate to AI governance; create ADR |
| Architecture decision outstanding that blocks a story | Create ADR; get architect sign-off before proceeding |
| Story failed quality gate | Rewrite story; re-submit to quality gate |
| Unresolved blocking open question discovered | Escalate to product owner; stop story implementation |
| Audit log write removed or bypassed | Revert immediately; raise as compliance incident |
| Data residency boundary violated (non-UK storage/processing) | Halt deployment; escalate to security and compliance |
| AI model produces unexplainable decision path | Block AI Scoring Service release; escalate to AI governance |

---

## 13. Human Review Checkpoints

| Checkpoint | After Phase | Owner | Purpose |
|---|---|---|---|
| Requirements review | 1-requirements | Product Owner | Validate FR coverage, open question resolution, and compliance alignment |
| Architecture review | 3-architecture-context | Architect | Validate Azure topology fit, integration contracts, circuit breaker coverage |
| Compliance sign-off | Before AML/KYC/AI stories | Compliance Team | Validate FCA, AML, KYC, GDPR alignment per story |
| Story quality review | Story quality gate | QA Analyst | Validate stories are implementation-ready per Definition of Ready |
| AI model governance review | Before AI Scoring Service stories | AI Governance / Head of AI | Validate explainability mechanism and FCA compliance |
| Readiness review | Pre-implementation | Engineering Lead | Validate initiative is ready for AI implementation handoff |

---

## 14. Advisory Reviews

Advisory reviews provide optional expert perspectives on artifacts before gate review. When enabled, each configured persona reviews the artifact through its specific lens and produces structured findings. Findings are appended to the artifact but do not block the gate.

| Setting | Value |
|---|---|
| Advisory reviews enabled | No |

### Enabled Personas

| Persona | Lens | Activates when |
|---|---|---|
| qa-analyst | Testability, edge cases, AC quality | Not active |
