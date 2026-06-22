# Prompt 5 — Add Delivery Modes

Add delivery modes to the `.b2s` framework.

Current problem:

The framework can feel too heavy because all artifacts appear equally important. But enterprise initiatives have different levels of complexity and governance need.

Implement three delivery modes:

1. Compact
2. Standard
3. Full Governance

## Compact Mode

Use for low-risk, small, localized changes.

Mandatory outputs:

- source-summary.md
- requirements.md
- delivery-structure.md
- story packages
- compact-handoff.md

BDD:

- optional
- required only when triggered by readiness check

Security/threat model:

- optional
- required only when security impact exists

API/data/event contracts:

- optional
- required only if impacted

## Standard Mode

Use for normal enterprise features.

Mandatory outputs:

- business-intake-summary.md
- requirements.md
- business-rules.md
- architecture-review.md
- delivery-structure.md
- epic packages
- feature packages
- story packages
- traceability-matrix.md
- bdd-scenarios.md
- test-strategy.md
- readiness-check.md
- compact-handoff.md or standalone-handoff.md

BDD:

- mandatory for all business-facing stories

## Full Governance Mode

Use for regulated, multi-team, cross-system, client-impacting, data-sensitive, or high-risk changes.

Mandatory outputs:

- all Standard outputs
- security-review.md
- threat-model.md
- api-contract.md where applicable
- data-contract.md where applicable
- event-contract.md where applicable
- observability-plan.md
- openspec-handoff.md
- review-package.md

BDD:

- mandatory and traceable
- must include happy path, negative path, authorization, business rule, integration failure, and audit/compliance scenarios where applicable

## Mode Selection

Add a mode-selection rule based on the BRS and architecture impact.

Full Governance should be selected if any of these are true:

- regulatory impact
- security impact
- personal/sensitive data impact
- new or changed integration
- cross-team dependency
- data model change
- workflow/state transition change
- audit/compliance requirement
- external client impact
- production operational impact

Standard should be selected for normal business features.

Compact should be selected only when the change is low-risk and localized.

Update validators so mandatory artifacts depend on the selected mode.
