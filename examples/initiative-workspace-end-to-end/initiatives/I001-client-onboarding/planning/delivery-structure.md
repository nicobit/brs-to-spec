# Delivery Structure

## Business Capabilities

- Guided client onboarding
- Identity and document verification
- Reviewer decision support

## Epic Breakdown

| Epic ID | Epic title | Business objective | Source requirement(s) | Notes |
|---|---|---|---|---|
| EP-01 | Guided Client Onboarding | Allow complete onboarding submissions with required identity evidence | BRS-01, BRS-02 | Primary delivery theme for D1 |

## Feature / Capability Breakdown

| Feature ID | Parent epic | Feature / capability | Business value | Source requirement(s) | Notes |
|---|---|---|---|---|---|
| FEAT-01 | EP-01 | Submit onboarding request with required documents | Reduce incomplete submissions and compliance rework | BRS-01 | Supports guided onboarding flow |
| FEAT-02 | EP-01 | Audit onboarding submission outcome | Preserve operational and compliance traceability | BRS-02 | Depends on event and logging controls |

## User Story Breakdown

| Story ID | Parent feature | User story | Source requirement(s) | Acceptance / validation reference | Architecture constraints | Likely quality gates | Likely enablement needs |
|---|---|---|---|---|---|---|---|
| US-01 | FEAT-01 | As a compliance analyst, I want onboarding requests to include verified identity and documents, so that I can review complete submissions. | BRS-01 | `quality-gates/bdd-scenarios.md`, `standalone-delivery/D1-guided-onboarding/validation-plan.md` | Identity validation must use approved service controls | Security review, test strategy | Monitoring, alerting |
| US-02 | FEAT-02 | As an operations reviewer, I want successful onboarding submissions to emit an auditable event, so that downstream teams can trace onboarding outcomes. | BRS-02 | `standalone-delivery/D1-guided-onboarding/validation-plan.md` | Audit event must preserve approved schema and controls | Data contract, event contract, observability plan | Logging, support handover |

## Story Traceability Rules

Stories map back to source requirements and become planning parents for downstream engineering tasks.

Handoff tasks must preserve links to:

- requirement ID
- story ID
- acceptance / validation reference
- architecture constraint
- quality gate reference

## Acceptance / Validation References

- `quality-gates/bdd-scenarios.md`
- `standalone-delivery/D1-guided-onboarding/validation-plan.md`
- `planning/traceability-matrix.md`

## Governed Boundaries

| Boundary ID | Boundary type | Producer / Owner | Consumer(s) | Created / Changed? | Why governed? | Likely contract gate |
|---|---|---|---|---|---|---|
| GB-01 | Service / API | Onboarding service | Reviewer portal | Changed | Submission validation is a governed service boundary | API contract |
| GB-02 | Event | Onboarding service | Audit and operations consumers | Created | Submission audit event is a governed asynchronous boundary | Event contract |

## Candidate Modules

- Onboarding intake
- Identity verification
- Audit event publishing

## Candidate Delivery Slices

- D1 Guided onboarding submission
- D2 Reviewer workflow enrichment
