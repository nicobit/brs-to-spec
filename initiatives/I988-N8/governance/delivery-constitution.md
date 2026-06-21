 # Delivery Constitution

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I988-N8 |
| Created at | 2026-06-21 |
| Created by | governance-architect |
| Status | Draft |

---

## 1. Purpose

This initiative delivers an AI-assisted loan origination platform that automates intake, risk scoring, AML/KYC checks, underwriter workflows, offer generation and core-banking disbursement while preserving human oversight for complex cases. This constitution defines non-negotiable governance rules that downstream analysis, architecture, and implementation must follow to ensure regulatory compliance, data residency, security, and reproducible auditability.

---

## 2. Delivery Principles

| # | Principle | Rationale |
|---|---|---|
| 1 | Regulatory-first: every design must demonstrate compliance with FCA, AML/KYC, and UK GDPR | Initiative operates in regulated financial domain; compliance is blocking |
| 2 | UK data residency: keep all PII and audit data in UK datacenters only | GDPR/data residency constraint in BRS and architecture |
| 3 | Explainability: AI decisions must be auditable and explainable to underwriters and regulators | FCA requirement; prevents black-box-only models |
| 4 | Fail-safe routing: external integration failures route to human review | Maintain availability and correctness when third-party APIs fail |
| 5 | Minimal privilege & managed identity for service-to-service calls | Security best practice; prevents secret sprawl |

 ## 3. Requirement Handling Rules

 | Rule | Description | Consequence of Violation |
 |---|---|---|
 | RQ-001 | Every requirement must reference a BRS objective and include measurable acceptance criteria | Requirement rejected by intake if missing |
 | RQ-002 | Requirements that impact compliance/security must include required controls and owner | Implementation blocked until owner provides controls |
 | RQ-003 | No requirement may mandate AI behavior without specifying explainability and input sources | Requirement returned for clarification |
 | RQ-004 | All requirements must include data retention and residency expectations for PII | Non-compliant stories will not be scheduled |

 ---

 ## 4. Architecture Alignment Rules

 | Rule | Description | Applies To |
 |---|---|---|
 | AR-001 | Deploy services only within Azure UK South or UK West | All cloud resources, storage, and backups |
 | AR-002 | Use managed identities for all service-to-service auth; no embedded secrets | Backend services and CI/CD pipelines |
 | AR-003 | AI Scoring must export an auditable score, rationale, and input provenance for each decision | AI Scoring Service, model infra |
 | AR-004 | Credit bureau data must be transient and not persisted beyond scoring pipeline | Experian integration flow |

 ---

 ## 5. Story Quality Rules

 | Rule | Description | Check Method |
 |---|---|---|
 | SQ-001 | Story must have clear acceptance criteria and at least one BDD scenario | Review in story quality gate |
 | SQ-002 | Story must list impacted systems, required API contracts, and data residency impacts | Architectural review checklist |
 | SQ-003 | Performance constraints (latency budgets) must be included for interactions with Experian, HMRC, and T24 | Performance tests and load recipes |
 | SQ-004 | Security tasks (e.g., encryption config, RBAC) must be explicit and assigned | Security review before merge |

 ---

 ## 6. BDD and Testability Rules

 | Rule | Description | Applies To |
 |---|---|---|
 | TB-001 | Every story must include BDD scenarios for happy path and at least one negative path | Feature files and CI tests |
 | TB-002 | External integrations must be covered by contract tests and producer/consumer stubs | Experian, HMRC, DocuSign, T24 adapters |
 | TB-003 | AI scoring decisions must have unit tests for input transformations and integration tests for explainability outputs | AI scoring pipeline tests |

 ---

 ## 7. Security and Compliance Rules

 | Rule | Description | Source | Blocking? |
 |---|---|---|---|
 | SC-001 | All PII encrypted at rest (AES-256) and in transit (TLS 1.3) | BRS NFR-004 | Yes |
 | SC-002 | Audit logs must be immutable and stored in append-only Cosmos DB container | BRS FR-028 / Architecture | Yes |
 | SC-003 | Use Azure AD for human users; service identities use managed identities | Architecture security model | Yes |
 | SC-004 | Circuit breakers and timeout policies around Experian, HMRC, and T24 integrations | BRS NFR-007 | No (operationally required) |

 ---

 ## 8. Documentation Rules

 | Rule | Description | Applies To |
 |---|---|---|
 | DOC-001 | Every API or integration change must include API contract docs and example stubs | Integration adapters |
 | DOC-002 | AI model design notes must include explainability approach and training data provenance summary | AI Scoring Service |
 | DOC-003 | Operational runbooks for alerts, incident response, and DR must exist before production rollout | Ops and SRE teams |

 ---

 ## 9. AI Implementation Safety Rules

 | Rule | Description | Rationale |
 |---|---|---|
 | AI-001: Do not deploy black-box models to production without explainability outputs | Every inference must include score, top contributing features, and provenance | FCA compliance and auditability |
 | AI-002: Do not allow autonomous approval above configured risk thresholds | Human-in-the-loop required where threshold exceeded | Prevent unsafe automation |
 | AI-003: Do not allow AI agents to change architecture, security controls, or compliance rules | Architecture and security changes require ADR and human approval | Preserve governance boundaries |
 | AI-004: Always attach a machine-readable provenance record for each decision | Enables replay, audit, and root-cause analysis | Traceability requirement |
 | AI-005: Do-not-touch boundaries: PII persistence rules, audit log, and encryption settings may not be modified by automated agents | Protect regulatory controls | Blocking |

 ---

 ## 10. Definition of Ready

 A story is ready for implementation when:

 - [ ] Business goal is clear and specific and maps to a BRS objective
 - [ ] Acceptance criteria are measurable and testable
 - [ ] BDD scenarios for happy and negative paths exist
 - [ ] Architecture impact is documented and authorized (or flagged as research)
 - [ ] Required integrations and contracts are listed with fallback behaviour
 - [ ] Security and data residency implications are addressed
 - [ ] Owners and reviewers are assigned

 ---

 ## 11. Definition of Done

 A story is done when:

 - [ ] All acceptance criteria are implemented and verified
 - [ ] BDD scenarios pass in CI and staging
 - [ ] Architecture constraints and interfaces are respected and documented
 - [ ] Security checks (SAST/secret-scan/config review) are passed
 - [ ] Audit/tracing instrumentation is present for the change
 - [ ] Code review and QA sign-off completed

 ---

 ## 12. Blocking Conditions

 Implementation must stop if:

 | Condition | Resolution Path |
 |---|---|
 | Unresolved regulatory requirement or legal objection | Escalate to product owner and legal; gate release |
 | Missing ADR for architecture-impacting change | Create ADR and do not proceed until accepted |
 | AI model lacks required explainability outputs | Pause deployment; remediate model pipeline |
 | Non-compliant data residency or encryption configuration | Remediate infra before production rollout |

 ---

 ## 13. Human Review Checkpoints

 | Checkpoint | After Phase | Owner | Purpose |
 |---|---|---|---|
 | Requirements review | 2-business-intake | product-owner | Validate requirement completeness and regulatory coverage |
 | Architecture review | 3-planning | architect | Validate deployment topology, residency, and constraints |
 | Security & compliance review | pre-production | security-lead | Validate encryption, access controls, and auditability |
 | AI safety review | before model release | AI-governance | Validate explainability, bias checks, and thresholds |
 | Readiness review | release candidate | engineering-lead | Validate overall readiness for production rollout |

 ---
 +*This constitution governs all downstream phases. Every artifact must be validated against it. Set Status: Accepted only by human approval. Never self-accept.*

