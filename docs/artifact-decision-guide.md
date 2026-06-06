# Artifact Decision Guide

Use the minimum number of artifacts needed for the risk level.

## Small Change — Minimal Flow

Use when:

```text
low risk
clear expected behavior
no significant security/audit/data/integration impact
```

Required:

```text
business-intake/requirements.md
business-intake/epics-and-features.md
business-intake/user-stories.md
business-intake/gaps-and-questions.md
engineering-contracts/technical-spec.md
openspec-change/proposal.md
openspec-change/design.md
openspec-change/tasks.md
```

Optional:

```text
business-intake/brs-summary.md
business-intake/business-test-expectations.md
```

## Medium Change — BDD + Test Strategy Flow

Use when:

```text
normal feature work
workflow behavior
role-based behavior
moderate frontend/backend impact
QA planning needed
```

Required:

```text
all small-flow artifacts
engineering-contracts/bdd-scenarios.md
engineering-contracts/test-strategy.md
```

Optional:

```text
engineering-contracts/test-plan.md
engineering-contracts/traceability-matrix.md
```

## Large / Risky Change — Full Framework

Use when:

```text
regulated
security-sensitive
audit/compliance-heavy
client-data-impacting
cross-system
database migration risk
multi-team
high business impact
```

Required:

```text
business-intake/brs-summary.md
business-intake/requirements.md
business-intake/epics-and-features.md
business-intake/user-stories.md
business-intake/gaps-and-questions.md
business-intake/business-test-expectations.md

engineering-contracts/technical-spec.md
engineering-contracts/bdd-scenarios.md
engineering-contracts/test-strategy.md
engineering-contracts/test-plan.md
engineering-contracts/traceability-matrix.md

openspec-change/proposal.md
openspec-change/design.md
openspec-change/tasks.md

quality-gates/business-ready-checklist.md
quality-gates/engineering-ready-checklist.md
quality-gates/ready-for-copilot-checklist.md
```

## Decision table

| Change type | Recommended flow |
|---|---|
| Minor UI copy | Small |
| Simple validation | Small or Medium |
| New field with DB migration | Medium |
| New workflow step | Medium |
| Role-based feature | Medium or Large |
| Audit/compliance feature | Large |
| External integration | Large |
| New service / architecture change | Large |
| Client-data-impacting change | Large |

## Architecture-related artifacts

Use these when an architecture draft exists:

```text
input/architecture-draft.md
business-intake/brs-architecture-alignment.md
```

For small changes:
- optional, lightweight

For medium changes:
- recommended

For large/risky changes:
- required

# Enablement Artifacts

Use these only when infrastructure, CI/CD, environment, observability, release, or operations work is needed.

## Minimal enablement

```text
enablement/enablement-scope.md
enablement/enablement-structure.md
enablement/technical-stories.md
```

## Full enablement

```text
enablement/enablement-scope.md
enablement/enablement-structure.md
enablement/technical-stories.md
enablement/infrastructure-spec.md
enablement/cicd-spec.md
enablement/environment-strategy.md
enablement/observability-spec.md
enablement/release-rollback-plan.md
enablement/operational-readiness.md
```

# Architecture & Contract Extension Artifacts

These are optional artifacts used when engineering ambiguity or risk is high.

| Artifact | Use when |
|---|---|
| `architecture-contracts/artifact-decision.md` | You need to decide which optional architecture/contract artifacts are required |
| `architecture-contracts/architecture-decisions.md` | Important architecture decisions exist |
| `architecture-contracts/adr/ADR-xxx.md` | A formal architecture decision is needed |
| `architecture-contracts/api-contract.md` | REST API endpoints are added or changed |
| `architecture-contracts/openapi.yaml` | API contract-first implementation or validation is needed |
| `architecture-contracts/domain-model.md` | Domain rules/workflows/state transitions are complex |
| `architecture-contracts/data-model.md` | Database schema or migration changes are needed |
| `architecture-contracts/event-contracts.md` | Events/messages/audit payloads are added or changed |
| `architecture-contracts/quality-attribute-scenarios.md` | NFRs need measurable validation |
| `architecture-contracts/threat-model.md` | Security-sensitive change |

# Handoff Artifacts

| Artifact | Use when |
|---|---|
| `handoff/spec-driven-handoff.md` | You want to pass enterprise-ready context to OpenSpec, Spec Kit, Kiro, or standalone execution |
| `handoff/handoff-readiness.md` | You want to verify whether the feature is ready for downstream engineering |
| `handoff/spec-kit-input.md` | GitHub Spec Kit will own downstream workflow |
| `handoff/kiro-spec-input.md` | Kiro will own downstream workflow |
| `openspec-change/*` | OpenSpec or standalone OpenSpec-like execution is used |

# gstack Handoff Artifacts

| Artifact | Use when |
|---|---|
| `handoff/gstack-brief.md` | gstack will be used for execution, review, QA, security, documentation, or shipping |
| `handoff/gstack-review-plan.md` | You want a role-based review plan for gstack |

# Planning Artifacts

| Artifact | Use when |
|---|---|
| `planning/delivery-slicing.md` | Large BRS must be split into MVP, quarters, increments, or releases |
| `planning/next-increment-scope.md` | You need to select what will be detailed next |
| `planning/increment-handoff.md` | You need a scope-controlled input for user stories, technical spec, contracts, enablement, and final handoff |
