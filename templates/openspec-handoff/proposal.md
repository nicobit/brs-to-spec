# Proposal — {{Deliverable ID}}: {{Deliverable Name}}

> OpenSpec change proposal. Drive implementation with `/opsx:apply` against this folder.
> Copy this folder (`openspec/changes/{{deliverable-id}}-{{slug}}/`) into the target code repository before applying.

## Why

<!-- One paragraph: business driver, who is affected, what breaks if this is not built. -->

## What changes

<!-- Bullet list of the concrete system changes this deliverable introduces. -->
<!-- One line per change. No implementation detail — that belongs in design.md. -->

## Scope

### In scope

| Feature | User story summary | Requirement |
|---|---|---|

### Out of scope (explicitly)

<!-- List features or integrations deferred to a later increment. -->
<!-- Being explicit here prevents scope creep during implementation. -->

## Success criteria

| Criterion | Target | Source |
|---|---|---|

## Constraints inherited from upstream

| Constraint | Source artifact |
|---|---|

## Reference artifacts

All detail is in `specs/` (distilled from quality gates) and the links below.
Do not copy these files — reference them by path from the initiative workspace.

| Artifact | Path | What to read there |
|---|---|---|
| Architecture review | `input/architecture.md` | Deployment topology, integration decisions |
| Architecture rules | `architecture/architecture-rules.md` | Binding rules engineers must follow |
| Data contract | `quality-gates/data-contract.md` | Full schema DDL, PII mapping, retention |
| API contract | `quality-gates/api-contract.md` | Full endpoint specs, auth, error codes |
| Security review | `quality-gates/security-review.md` | Security checklist and accepted risks |
| Observability plan | `quality-gates/observability-plan.md` | Full telemetry catalog, alert rules, runbooks |
