# GitLab Planning View

> This file is a planning projection.
> It is not the source of truth.
> User stories provide business context and traceability.
> Engineers implement from approved standalone tasks, not from user stories alone.

## Metadata

| Field | Value |
|---|---|
| Initiative | I001 Client Onboarding |
| Active deliverable | D1 Guided Onboarding |
| Delivery mode | Enterprise + Modular Delivery |
| Execution mode | Standalone |
| Readiness status | Ready with triggered gates completed |
| View status | Draft |

## Planning Summary

This view helps the delivery team map initiative artifacts into Agile planning items without creating a second source of truth.

Stories in this view are projected from `planning/delivery-structure.md`.

## User Story Projection

| Story ID | Suggested GitLab title | User story in format `As a <persona>, I want <capability>, so that <business value>.` | Source artifact path | Source requirement ID | Acceptance source | Quality gate references | Labels |
|---|---|---|---|---|---|---|---|
| US-01 | Submit onboarding request | As a compliance analyst, I want onboarding requests to include verified identity and documents, so that I can review complete submissions. | `planning/traceability-matrix.md` | BRS-01 | `quality-gates/bdd-scenarios.md` | `quality-gates/security-review.md`, `quality-gates/test-strategy.md` | onboarding, compliance |

## Engineering Notes

| Note area | Summary | Source artifact | Source ID / reference |
|---|---|---|---|
| Components affected | Guided onboarding flow, document upload, reviewer queue | `standalone-delivery/D1-guided-onboarding/delivery-spec.md` | D1 |
| Architecture constraints | Identity validation and document checks must remain auditable | `architecture/architecture-rules.md` | AR-01 |
| Security considerations | PII handling and reviewer access control require security-review actions | `quality-gates/security-review.md` | SG-01 |

## Enablement Needs

| Need | Reason / trigger | Source artifact | Suggested GitLab item | Owner / role | Required before |
|---|---|---|---|---|---|
| Monitoring and alerting | Operational visibility is required for onboarding failures | `quality-gates/test-strategy.md` | Child issue under onboarding epic | SRE / Platform | Release |

## Engineering Consumption Model

```text
Agile item:
Epic / Feature / User Story

Engineering input:
Standalone delivery package for D1

Engineer implementation source:
One approved standalone task at a time
```

## Sync Notes

| Item | Source of truth | What to do if this changes |
|---|---|---|
| User story projection | `planning/traceability-matrix.md` | Regenerate the planning view |
| Engineering implementation contract | `standalone-delivery/D1-guided-onboarding/tasks.md` | Update the delivery package first, then regenerate the planning view |
