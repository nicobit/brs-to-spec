# Advanced Governance

Advanced governance is optional.

Use it only when the engineering readiness check says it is needed.

This keeps the main framework simple while preserving the stronger enterprise capabilities from earlier versions.

## When to use advanced governance

Use advanced governance when:
- the deliverable is compliance-sensitive,
- QA coverage needs to be explicit,
- security review is required,
- architecture constraints are high risk,
- test strategy must be agreed before implementation,
- release readiness must be checked formally.

## Optional prompts

```text
prompts/4-engineering-readiness/advanced/
  create-api-contract.md
  create-data-contract.md
  create-event-contract.md
  create-threat-model.md
  create-observability-plan.md
  create-bdd-scenarios.md
  create-test-strategy.md
  create-qa-review.md
  create-architecture-review.md
  create-security-review.md
  create-release-readiness-review.md
```

## Optional templates

```text
templates/advanced-governance/
  api-contract.md
  data-contract.md
  event-contract.md
  threat-model.md
  observability-plan.md
  bdd-scenarios.md
  test-strategy.md
  qa-review.md
  architecture-review.md
  security-review.md
  release-readiness-review.md
```

## Main rule

Do not put advanced governance into the standard path.

Advanced governance is a controlled escalation, not the default workflow.
