# Workflow Type: enterprise-modular

## When to use

Use this workflow for initiatives that require the full staged delivery process:
business intake, detailed business analysis, architecture review, quality gates,
and full story package handoff.

Suitable for: regulated industries, complex multi-team deliveries, initiatives
with external integrations, initiatives requiring audit trails.

## Stages

0-routing → 2-business-intake → 2b-business-analysis → 3-planning →
4-engineering-readiness → 4b-quality-gates → 5-handoff → 6-review-package

## Quality gates

All quality gates are conditional — triggered only if the engineering readiness
check determines they are needed (BDD, test strategy, security review, API contract,
data contract, event contract, observability plan).

## Delivery modes supported

- OpenSpec (full story packages)
- Standalone (standalone handoff document)
- FastPath (compact handoff)
