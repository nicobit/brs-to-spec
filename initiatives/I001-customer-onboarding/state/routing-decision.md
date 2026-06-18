# Routing Decision

## Decision Summary

| Decision | Selected value | Reason | Confidence |
|---|---|---|---|
| Delivery mode | Standard | Initiative introduces a new customer-facing onboarding flow with external integrations (IDP, payment), compliance considerations (GDPR), and non-functional targets (availability, latency). Standard balances necessary rigor without Enterprise overhead. | High |
| Execution mode | OpenSpec | The workspace contains `openspec/changes` artifacts indicating OpenSpec is the project's default downstream handoff. OpenSpec enables traceable, reviewable tasks for multi-team delivery. | High |
| Small-change path applicable? | No | Integration surface, compliance constraints, and availability requirements exceed a trivial small-change scope. | High |

## Delivery Mode Assessment

| Criterion | Low / Medium / High | Evidence | Impact |
|---|---|---|---|
| Requirement ambiguity | Medium | BRS contains clear FRs and NFRs but some measurable targets need numeric confirmation. | Requires clarification but does not block Standard mode |
| Architecture impact | High | Integrations with Identity Provider B, Payment Provider A, and PII handling materially affect design and contracts. | Requires architecture review and integration contract validation |
| Compliance / audit relevance | High | GDPR and PII encryption requirements present regulatory obligations. | Requires legal/security review and gating where triggered |
| Business criticality | Medium | Improving onboarding conversion is high-value but not a critical system-wide change. | Prioritize reliability and observability in delivery |
| Number of teams | Medium | Likely requires backend, frontend, security, and operations collaboration. | Standard mode appropriate for cross-team coordination |
| Delivery size | Medium | Full new flow with integrations — moderate scope. | Standard mode to structure epics and features |
| AI context saturation risk | Low | No AI-specific risks noted in BRS. | Not material |
| Change narrow enough for small-change path | No | Multiple external integrations and compliance needs exceed small-change criteria. | Small-change path not recommended |

## Execution Mode Assessment

| Criterion | OpenSpec | Standalone | Business Copilot |
|---|---|---|---|
| Available in project? | Yes (openspec/changes exists) | Yes (standalone supported) | No evidence in this workspace | 
| Recommended? | Yes | No | No |
| Reason | OpenSpec provides traceable tasks and reviews suitable for multi-team delivery and handoff. Existing `openspec/changes` shows usage. | Standalone is unnecessary overhead where OpenSpec is available. | Business Copilot not indicated by workspace artifacts. |

## Required Next Prompts

| Step | Prompt | Required? | Reason |
|---|---|---|---|
| Business intake | .brs2spec/skills/2-business-intake/01-create-business-intake-summary.md | Yes | `business-intake/business-intake-summary.md` is a stub and must be populated with owners, acceptance, and gaps. |
| Architecture review | .brs2spec/skills/3-planning-and-modular-delivery/01-review-initial-architecture.md | Yes | Draft architecture was generated; review must be completed and architect must mark review status. |

## Prompts Not Needed

| Prompt | Reason not needed |
|---|---|
| Fast Path routing prompts | Not applicable — change is not narrow enough for Fast Path |

## Risks of Under-Processing

- Missing integration contract details with Identity Provider B could cause late rework and blocking integration bugs.
- Incomplete compliance validation (data residency, PII handling) risks regulatory non-conformance.

## Risks of Over-Processing

- Selecting Enterprise + Modular unnecessarily would add coordination overhead and delay delivery without proportional risk reduction.

## Small-Change Path Notes

| Item | Decision / note |
|---|---|
| Is Fast Path acceptable? | No |
| Minimum required artifacts | `business-intake/business-intake-summary.md`, `architecture/architecture-review.md`, `engineering-readiness/readiness-check.md` |
| Readiness still required? | Yes — readiness gate must be explicit before handoff |
| Gates that still may trigger | Security review, data/privacy gate, and operational readiness |

