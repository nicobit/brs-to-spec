# Change Size Decision Model

Use this guide to decide how much of the framework to apply.

The goal is to avoid unnecessary bureaucracy while keeping enough control for risky changes.

## Summary

```text
Small change  → Minimal flow
Medium change → Add BDD + test strategy
Large/risky change → Full framework
```

## Small Change — Minimal Flow

Use this for:

```text
small UI text changes
simple validation rule
small API change with no integration impact
minor bug fix with clear expected behavior
small configuration change
low-risk internal improvement
```

Use these artifacts:

```text
business-intake/
  brs-summary.md                optional if input is already clear
  requirements.md
  epics-and-features.md          lightweight, can contain one feature only
  user-stories.md
  gaps-and-questions.md

engineering-contracts/
  technical-spec.md             lightweight

openspec-change/
  proposal.md
  design.md                     lightweight
  tasks.md
```

Optional:

```text
business-test-expectations.md
```

Do not force:

```text
full test strategy
full test plan
full traceability matrix
formal architecture contract
formal API/event contracts
```

## Medium Change — BDD + Test Strategy Flow

Use this for:

```text
new feature in an existing module
moderate backend + frontend change
new workflow step
changes with role-based behavior
changes with non-trivial validation
changes that need QA planning
```

Use all small-change artifacts plus:

```text
engineering-contracts/
  bdd-scenarios.md
  test-strategy.md
```

Optional depending on risk:

```text
test-plan.md
traceability-matrix.md
```

## Large / Risky Change — Full Framework

Use this for:

```text
regulated feature
client-data-impacting feature
audit/compliance-heavy feature
security-sensitive change
cross-system integration
database migration with risk
new service / major architecture change
external API/event contract
performance-sensitive change
multi-team delivery
high business impact
```

Use the full artifact set:

```text
business-intake/
  brs-summary.md
  requirements.md
  epics-and-features.md
  user-stories.md
  gaps-and-questions.md
  business-test-expectations.md

engineering-contracts/
  technical-spec.md
  bdd-scenarios.md
  test-strategy.md
  test-plan.md
  traceability-matrix.md

openspec-change/
  proposal.md
  design.md
  tasks.md

quality-gates/
  business-ready-checklist.md
  engineering-ready-checklist.md
  ready-for-copilot-checklist.md

reviews/
  code-review.md
  qa-review.md
  architecture-review.md
```

Add specific security or release reviews where required.

## Decision Questions

Answer these before choosing the flow.

| Question | If yes |
|---|---|
| Does it affect client/customer data? | Large/risky |
| Does it affect authorization or roles? | Medium or Large |
| Does it affect audit/compliance/regulatory evidence? | Large/risky |
| Does it add or change integrations? | Medium or Large |
| Does it require database migration? | Medium or Large |
| Does it affect multiple teams or systems? | Large/risky |
| Is expected behavior already very clear? | Small possible |
| Is QA/UAT needed beyond developer testing? | Medium or Large |
| Could a mistake cause financial, regulatory, security, or client impact? | Large/risky |

## Default rule

If unsure, choose **Medium**.

Use **Large/Risky** only when the additional artifacts genuinely reduce risk.

Use **Small** only when the change is genuinely low risk and well understood.

## Anti-pattern

Do not apply the full framework to every small change.

That creates process fatigue and people will stop using the system.

## Recommended adoption

Start with:

```text
1 real small change
1 real medium feature
1 real risky feature
```

Then adjust the artifact set based on what actually helped.

## Architecture document impact

If a draft architecture exists, use it during change classification.

The change may become Medium or Large/Risky if the architecture shows:

```text
new integration
database migration
security boundary change
audit/compliance implications
new service/component
deployment/environment change
cross-system dependency
performance/availability impact
```

For medium and large/risky changes, run:

```text
prompts/01-business-intake/03-review-brs-and-requirements-against-architecture.md
```

# Enablement Track Decision

Use the Enablement Track if any of these are needed:

```text
new infrastructure
new Azure/cloud resources
database/storage changes
new queue/topic/event stream
network/private endpoint changes
identity or managed identity changes
Key Vault/secrets/certificates
CI/CD pipeline changes
environment configuration
observability / dashboards / alerts
release or rollback procedure
operational readiness or runbook
```

## By change size

### Small change

Usually skip Enablement Track unless pipeline/configuration is affected.

### Medium change

Run at least:

```text
prompts/08-enablement/01-identify-enablement-scope.md
```

Then decide whether technical stories are needed.

### Large/risky change

Run the full Enablement Track.

# Architecture & Contract Extensions by Change Size

## Small change

Usually skip architecture-contract artifacts.

Possible exception:
- A small API change may still need a lightweight API contract update.

## Medium change

Consider:
- API contract for API changes
- Data model for database changes
- ADR for important decisions
- Event contract for event/message changes

## Large/risky change

Run:

```text
prompts/09-architecture-contracts/00-decide-architecture-contract-artifacts.md
```

Then create only the required artifacts.

# Handoff by Change Size

## Small change
Usually use standalone mode unless the team already uses a downstream framework.

## Medium change
Create a lightweight handoff package if another team/tool owns implementation.

## Large/risky change
Create the full handoff package and readiness assessment before downstream execution.

# Large / Multi-Quarter BRS Decision

If the BRS may span more than one quarter, classify it as a large initiative and use:

```text
prompts/06-planning/01-create-delivery-slicing-and-roadmap.md
prompts/06-planning/02-select-next-increment-scope.md
prompts/06-planning/03-create-increment-handoff.md
```

This planning track should run before detailed user-story generation for implementation.
