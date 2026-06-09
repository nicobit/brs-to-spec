# Conditional Quality Gates

Quality gates are not optional.

They are conditional: not always required, but mandatory when triggered by the engineering readiness check.

## Gate trigger matrix

| Gate | Trigger examples | Required before |
|---|---|---|
| BDD scenarios | Complex business rules, workflows, exception paths, state changes | Implementation |
| Test strategy | Multiple test levels, regression risk, audit/compliance validation | Implementation |
| QA review | Business-critical outcome, formal QA sign-off, unclear acceptance coverage | Merge |
| Architecture review | Module boundary, data ownership, integration, infrastructure or deployment change | Implementation |
| Security review | Authentication, authorization, sensitive data, audit, external exposure | Implementation / Merge |
| Release readiness review | Production deployment, rollback, support readiness, monitoring | Release |
| API contract | New/changed API, consumers, versioning, backward compatibility | Implementation |
| Data contract | Schema, migration, reporting, retention, data ownership | Implementation |
| Event contract | Asynchronous event, consumer impact, retries, ordering, idempotency | Implementation |
| Threat model | High-risk security/data/integration exposure | Implementation |
| Observability plan | New operational flow, SLI/SLO, alerting, diagnosis need | Release |

## Rule

If the readiness check marks:

```text
Triggered = Yes
Required = Yes
```

then the gate must be produced and reviewed before the required-before stage.

## Optional visual support

Some quality gates may include a compact embedded visual when it materially improves contract, boundary, or operational clarity.

Preferred examples:

- `API contract` -> request/response or interaction sequence
- `Data contract` -> logical ERD or data-ownership view
- `Event contract` -> producer-consumer event flow
- `Threat model` -> trust-boundary or attack-surface view
- `Observability plan` -> telemetry and alerting flow

These visuals are optional.

Use them when they help reviewers understand the governed boundary faster than text alone.
Do not create a separate diagram workflow or require visuals when the gate is already clear in text.

## Anti-pattern

Do not say:

```text
These are optional advanced prompts.
```

Say:

```text
These are conditional quality gates.
```
