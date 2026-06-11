# Routing Decision

## Decision Summary

| Decision | Selected value | Reason | Confidence |
|---|---|---|---|
| Delivery mode | Standard | Multiple stakeholders and integrations (ServiceNow, Azure AD, CI/CD) require formal planning and quality gates; not narrow enough for Fast Path and not multi-product enough for Enterprise+Modular. | High |
| Execution mode | Standalone | No evidence an OpenSpec process or repo descriptors are in use; handoff will be a standalone delivery package. | Medium |
| Small-change path applicable? | No | Scope includes integrations, compliance and multi-team coordination — not a single small change. | High |

## Delivery Mode Assessment

| Criterion | Low / Medium / High | Evidence | Impact |
|---|---|---|---|
| Requirement ambiguity | Medium | BRS lists clear workflows and acceptance criteria but has open questions: ticketing provider confirmation and source-of-truth for assets. | May require clarifying scope before final slicing. |
| Architecture impact | High | Integrations with ServiceNow CMDB, identity provider (Azure AD), CI/CD and runbook/run-time hooks; cross-cutting concerns (audit, secrets, observability). | Significant design and integration effort; impacts interfaces and contracts. |
| Compliance / audit relevance | High | BRS requires immutable audit trails, retention and PII handling; Security & Compliance are primary stakeholders. | Triggers security review and data-contract gate. |
| Business criticality | High | Portal is single-pane for IT operations; SLA & MTTA targets indicate operational importance. | Requires careful testing, rollback planning and high availability. |
| Number of teams | Medium | Stakeholders: IT Operations, Platform/DevOps, Security, Service Desk — multiple owners but contained within IT and Platform orgs. | Coordination overhead for interfaces and handoffs. |
| Delivery size | Medium/High | Suggested increments span authentication, intake, CMDB sync, CI/CD linking and dashboards. | Multiple sprints; not trivial. |
| AI context saturation risk | Medium | AI assistant planned for dev/qa scopes with RAG; introduces data selection and PII risks. | Requires explicit controls in readiness and data-contract. |
| Change narrow enough for small-change path | Low | Scope includes multiple integrations and compliance gates. | Fast Path inappropriate. |
| Regression / contract sensitivity despite small scope | High | External integrations (ServiceNow, CI systems) and APIs risk regressions. | Requires contract testing and integration tests. |

## Execution Mode Assessment

| Criterion | OpenSpec | Standalone | Business Copilot |
|---|---:|---:|---:|
| Available in project? | No | Yes | No |
| Recommended? | No | Yes | No |
| Reason | No repository descriptors or existing OpenSpec handoff found in workspace; initiative structure shows a standalone delivery approach in `planning/delivery-structure.md`. | Standalone handoff suits an initiative of this scope where the team will produce a delivery package and story folders. | Business Copilot is not the primary delivery/execution mode for this type of infra+integration project. |

## Required Next Prompts

| Step | Prompt | Required? | Reason |
|---|---|---|---|
| 1 | 0-input-preparation/04-draft-architecture-from-brs.md | Yes | `input/architecture.md` is currently a stub; draft architecture is required to define interfaces, boundaries and DRAFT diagrams before review. |
| 2 | 3-planning-and-modular-delivery/01-review-initial-architecture.md | Yes | Architect must review the draft architecture and capture constraints and open decisions. |
| 3 | 3-planning-and-modular-delivery/03-create-delivery-structure.md | Conditional | Draft exists but features/stories should be reviewed and expanded after architecture review. |

## Prompts Not Needed

| Prompt | Reason not needed |
|---|---|
| Fast Path routing prompts | Scope and integrations make Fast Path unsafe. |
| OpenSpec handoff prompts | No evidence of OpenSpec repository descriptors; handoff will be standalone. |

## Risks of Under-Processing

- Missed compliance or audit requirements leading to rework.
- Unclear integration contracts with ServiceNow/CI providers causing regressions.
- Insufficient readiness checks for secrets and PII exposure in AI assistant.

## Risks of Over-Processing

- Excessive governance delaying delivery unnecessarily.
- Over-specified architecture that prevents pragmatic incremental delivery.

## Small-Change Path Notes

| Item | Decision / note |
|---|---|
| Is Fast Path acceptable? | No — integrations and compliance requirements exceed small-change criteria. |
| Minimum required artifacts | `input/architecture.md` (draft), `architecture/architecture-review.md`, `planning/delivery-structure.md` (confirmed), `engineering-readiness/readiness-check.md` |
| Readiness still required? | Yes — readiness gate must run and any triggered quality gates (security, data-contract) must be Accepted before handoff. |
| Gates that still may trigger | Security review, data-contract, API contract, observability plan, BDD scenarios |
