# Spec-Driven Handoff Package

## 1. Feature Summary

Feature name:

Business objective:

Recommended downstream mode:
- OpenSpec
- GitHub Spec Kit
- Kiro
- gstack
- Standalone

Recommended reason:

## 2. Source Inputs

| Artifact | Path | Status |
|---|---|---|
| Original BRS | `input/brs-original.md` |  |
| Architecture draft | `input/architecture-draft.md` |  |
| Requirements | `business-intake/requirements.md` |  |
| BRS / requirements / architecture alignment | `business-intake/brs-architecture-alignment.md` |  |
| Delivery structure | `business-intake/epics-and-features.md` |  |
| User stories | `business-intake/user-stories.md` |  |
| Gaps and questions | `business-intake/gaps-and-questions.md` |  |
| Technical spec | `engineering-contracts/technical-spec.md` |  |

## 3. Business Scope

### In scope

### Out of scope

## 4. Requirements Summary

| Requirement | Summary | Priority | Notes |
|---|---|---|---|

## 5. User Stories Summary

| Story | Summary | Priority | Notes |
|---|---|---|---|

## 6. Architecture Alignment Summary

### Supported requirements

### Requirements not clearly supported

### Contradictions

### Missing architecture decisions

### Constraints

## 7. Architecture & Contract Artifacts

| Artifact | Path | Required for implementation? | Notes |
|---|---|---|---|
| Artifact decision | `architecture-contracts/artifact-decision.md` |  |  |
| ADRs | `architecture-contracts/architecture-decisions.md` |  |  |
| API contract | `architecture-contracts/api-contract.md` |  |  |
| OpenAPI | `architecture-contracts/openapi.yaml` |  |  |
| Domain model | `architecture-contracts/domain-model.md` |  |  |
| Data model | `architecture-contracts/data-model.md` |  |  |
| Event contracts | `architecture-contracts/event-contracts.md` |  |  |
| Quality scenarios | `architecture-contracts/quality-attribute-scenarios.md` |  |  |
| Threat model | `architecture-contracts/threat-model.md` |  |  |

## 8. Enablement Summary

Infrastructure needed:

CI/CD changes needed:

Environment/configuration changes needed:

Observability needed:

Release/rollback needed:

Operational readiness needed:

## 9. Open Questions and Risks

| ID | Question / Risk | Owner | Blocks implementation? |
|---|---|---|---|

## 10. Acceptance / Validation Expectations

Business acceptance:

Technical validation:

Security validation:

Operational validation:

## 11. Downstream Handoff Instructions

### If using OpenSpec

Use `prompts/11-downstream-adapters/openspec/01-create-openspec-from-handoff.md`.

### If using GitHub Spec Kit

Use `prompts/11-downstream-adapters/spec-kit/01-create-speckit-input-from-handoff.md`.

### If using Kiro

Use `prompts/11-downstream-adapters/kiro/01-create-kiro-spec-input-from-handoff.md`.

### If using standalone mode

Continue with:

```text
prompts/03-openspec-handoff/
prompts/04-copilot-implementation/
prompts/05-reviewers/
```

## 12. Handoff Approval

Business owner:

Architecture owner:

Engineering owner:

QA owner:

Security owner if applicable:

Platform/SRE owner if applicable:


### If using gstack

Use:

```text
prompts/11-downstream-adapters/gstack/01-create-gstack-brief-from-handoff.md
prompts/11-downstream-adapters/gstack/02-create-gstack-review-plan.md
```
