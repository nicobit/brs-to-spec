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
