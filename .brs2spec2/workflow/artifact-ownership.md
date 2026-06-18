# BRS-to-Spec v2 — Artifact Ownership Table
# Version: 1.0
#
# Domain-specific artifact ownership for brs-to-spec v2.
# Loaded by the dispatcher during Step 9b (artifact ownership check).
# Engine-protected paths (.flow/state/*, input/*) are enforced separately
# by .flow-engine/instructions/artifact-ownership.md — do not duplicate them here.

---

## 1. Artifact ownership by persona

| Artifact path pattern | Owner persona | Notes |
|---|---|---|
| `routing/routing-decision.md` | orchestrator | Written by ROUTE_INITIATIVE only |
| `business-intake/business-intake-summary.md` | product-owner | |
| `business-analysis/requirements.md` | product-owner | Canonical analysis spine entry point — all other business-analysis artifacts derive from this |
| `business-analysis/use-cases.puml` | product-owner | Co-produced with use-cases.md — UC-NNN IDs must stay identical in both files |
| `business-analysis/use-cases.md` | product-owner | Co-produced with use-cases.puml — Mermaid version for GitLab Pages / IDE preview |
| `business-analysis/use-cases/*` | product-owner | Per-UC detail files — one file per UC-NNN |
| `business-analysis/business-rules.md` | product-owner | |
| `business-analysis/gaps-and-questions.md` | product-owner | |
| `business-intake/business-test-expectations.md` | product-owner | |
| `business-analysis/actors-and-personas.md` | product-owner | |
| `business-analysis/process-flows.md` | product-owner | |
| `business-analysis/use-cases/*` | product-owner | One file per UC-NNN — see use-cases.puml for the authoritative UC list |
| `business-analysis/use-case-spec.md` | product-owner | DEPRECATED — replaced by use-cases/UC-NNN.md. Existing initiatives keep this file as-is; new initiatives must not produce it. |
| `business-analysis/entity-model.md` | architect | First-class artifact — produced in stage 2b after requirements.md; blocks data-contract for data-relevant initiatives; does not block architecture review |
| `architecture/architecture-review.md` | architect | |
| `architecture/architecture-rules.md` | architect | |
| `architecture/existing-system-impact.md` | architect | |
| `planning/delivery-structure.md` | delivery-lead | |
| `planning/software-modules.md` | delivery-lead | |
| `planning/capability-module-map.md` | delivery-lead | |
| `planning/delivery-increments.md` | delivery-lead | |
| `planning/traceability-matrix.md` | delivery-lead | |
| `quality-gates/bdd/*` | qa-analyst | |
| `quality-gates/test-strategy.md` | qa-analyst | |
| `quality-gates/test-plans/*` | qa-analyst | |
| `quality-gates/security-review.md` | security-reviewer | |
| `quality-gates/threat-model.md` | security-reviewer | |
| `quality-gates/data-contract.md` | security-reviewer | |
| `quality-gates/api-contract.md` | engineering-lead | |
| `quality-gates/event-contract.md` | engineering-lead | |
| `quality-gates/observability-plan.md` | engineering-lead | |
| `engineering-readiness/readiness-check.md` | engineering-lead | |
| `engineering-readiness/initiative-context.md` | engineering-lead | |
| `specs/*` | engineering-lead | OpenSpec handoff folder |
| `standalone-delivery/*` | engineering-lead | Standalone handoff folder |
| `handoff/*` | engineering-lead | Compact handoff |
| `review-package/*` | delivery-lead | |
| `perspectives/*` | delivery-lead | |
| `reviews/implementation/*` | reviewer | Post-implementation reviews |

---

## 2. Shared artifacts — read by many, written by one

Write ownership is absolute. Read access is unrestricted.

| Artifact | Written by | Key readers |
|---|---|---|
| `routing/routing-decision.md` | orchestrator | All personas (delivery_mode, execution_mode) |
| `architecture/architecture-review.md` | architect | engineering-lead, delivery-lead, qa-analyst, security-reviewer |
| `architecture/architecture-rules.md` | architect | engineering-lead, qa-analyst, security-reviewer, reviewer |
| `planning/delivery-structure.md` | delivery-lead | All personas during quality gates and handoff |
| `engineering-readiness/readiness-check.md` | engineering-lead | qa-analyst, security-reviewer, orchestrator |
| `engineering-readiness/initiative-context.md` | engineering-lead | engineering-lead (self-reference in handoff), reviewer |
