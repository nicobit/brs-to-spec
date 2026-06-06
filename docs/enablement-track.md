# Optional Enablement Track

The Enablement Track extends the framework for work that is needed to deploy, operate, secure, monitor, and release a feature.

It does **not** replace the existing business flow.

It adds a parallel technical/operational track for:

```text
Infrastructure
CI/CD
Environment configuration
Secrets management
Observability
Operational readiness
Release and rollback
SRE / support readiness
Platform governance
```

## Why this exists

Many features are not only application code.

A complete delivery may also require:

```text
Azure resources
databases
queues/topics
storage accounts
Key Vault entries
network/private endpoints
pipeline changes
deployment approvals
monitoring dashboards
alerts
runbooks
rollback procedures
```

Those should not be forced into normal business user stories.

## Core principle

Keep two tracks:

```text
Product Delivery Track
  Business Objective
  Epic
  Feature / Capability
  Requirement
  User Story
  Acceptance Criteria

Enablement Delivery Track
  Enablement Objective
  Enablement Epic
  Enablement Feature / Capability
  Technical / Operational Requirement
  Technical Story
  Operational Acceptance Criteria
```

Both tracks feed into:

```text
Engineering Contracts
  ↓
OpenSpec Proposal / Design / Tasks
  ↓
Implementation
```

## When to use the Enablement Track

Use it if the feature needs any of:

```text
new infrastructure
new Azure resources
new database or storage
new queue/topic/event stream
new CI/CD pipeline
pipeline modification
environment configuration
secret management
monitoring/alerting
logging/audit setup
release/rollback procedure
operational support model
SRE readiness
platform governance
```

Skip it if:

```text
the change is purely business logic
existing infrastructure is enough
existing pipelines are enough
no deployment/configuration/monitoring change is needed
```

## How it fits the workflow

```text
Business intake
  ↓
Architecture alignment
  ↓
Delivery structure
  ↓
User stories

Optional Enablement Track
  ↓
Enablement scope
  ↓
Enablement structure
  ↓
Technical stories
  ↓
Infrastructure / CI-CD / Ops specs

Both feed into:
  ↓
OpenSpec proposal / design / tasks
  ↓
Implementation
```

## Recommended artifacts

Minimal enablement:

```text
enablement/enablement-scope.md
enablement/enablement-structure.md
enablement/technical-stories.md
```

Full enablement:

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

## Requirement categories

The Enablement Track introduces these optional requirement IDs:

```text
INFRA-xxx  Infrastructure requirements
CICD-xxx   CI/CD requirements
ENV-xxx    Environment requirements
OPS-xxx    Operational requirements
OBS-xxx    Observability requirements
REL-xxx    Release / rollback requirements
SEC-xxx    Security requirements, reused from main model
```

## Technical stories

Use technical stories when the "user" is engineering, platform, deployment, SRE, or operations.

Example:

```markdown
## TS-001 — Provision required Azure resources

Parent enablement epic:
- EPIC-EN-001 — Infrastructure and Deployment Enablement

Parent enablement feature:
- FEAT-EN-001 — Infrastructure Provisioning

As a Platform Engineer,  
I want the required Azure resources provisioned through IaC,  
so that the feature can be deployed consistently across environments.

### Requirements Covered
- INFRA-001
- ENV-001
- SEC-001

### Acceptance Criteria

#### AC-TS-001 — IaC deployment succeeds
Given the IaC pipeline runs for AIT  
When the deployment completes  
Then all required resources are created  
And naming/tagging standards are applied  
And no secrets are stored in code.
```

## OpenSpec tasks

OpenSpec tasks should include both application and enablement tasks:

```text
Application tasks
Infrastructure-as-Code tasks
Pipeline tasks
Environment configuration tasks
Observability tasks
Release/rollback tasks
Operational readiness tasks
```
