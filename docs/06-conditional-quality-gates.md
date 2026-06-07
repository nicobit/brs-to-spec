# Conditional Quality Gates

Conditional Quality Gates replace the older "optional advanced governance" idea.

They are **not** always required. But when **triggered** by the engineering
readiness check, they become **mandatory** before implementation, merge, or
release (depending on the gate).

This keeps the main framework simple while preserving the stronger enterprise
capabilities recovered from earlier versions (0.0.2 / 0.0.4).

## The rule

```text
Not triggered  → skipped
Triggered      → required (mandatory)
```

The engineering readiness check decides which gates are triggered, using the
Conditional Quality Gates table:

```markdown
| Quality Gate | Triggered? | Required? | Reason | Owner | Output |
```

## The gates

```text
prompts/4-engineering-readiness/quality-gates/
  create-bdd-scenarios.md
  create-test-strategy.md
  create-qa-review.md
  create-architecture-review.md
  create-security-review.md
  create-release-readiness-review.md
  create-api-contract.md
  create-data-contract.md
  create-event-contract.md
  create-threat-model.md
  create-observability-plan.md
```

## Templates

```text
templates/quality-gates/
  bdd-scenarios.md
  test-strategy.md
  qa-review.md
  architecture-review.md
  security-review.md
  release-readiness-review.md
  api-contract.md
  data-contract.md
  event-contract.md
  threat-model.md
  observability-plan.md
```

## Outputs

Triggered gates write to:

```text
quality-gates/<gate-name>.md
```

## When gates typically trigger

- BDD scenarios / test strategy — explicit behavioural or coverage agreement needed.
- QA review — formal quality sign-off needed.
- Architecture review — high architecture risk or conflicts.
- Security review / threat model — compliance- or security-sensitive deliverable.
- API / data / event contract — integration boundaries are touched.
- Observability plan — operational visibility is required.
- Release readiness — formal go/no-go before release.

## Main rule

Do not put Conditional Quality Gates into the default workflow. They are a
controlled escalation. But once triggered, they are not optional.
