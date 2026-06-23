# Decision: AML Provider Selection

Decision Date: 2026-06-23

## Question
OQ-004 — What AML database providers beyond HM Treasury are required (Dow Jones, others)?

## Decision
Include HM Treasury sanctions list as the primary source, and add one commercial provider (e.g., Dow Jones / Refinitiv World-Check) for broader coverage. The provider list must be configurable and adapters pluggable.

## Owner
Compliance + Procurement

## Rationale
Combining public and paid data sources improves screening coverage and reduces false negatives; procurement evaluates licensing and cost.

## Next actions
- Procurement and Compliance evaluate provider options and record approved provider(s) and API requirements in this repository at `initiatives/I093-I3/input/decisions/aml-provider-decision.md`.
- Implement adapters in the AML screening service that allow the provider list to be configured per-environment.

## Evidence / References
- See `planning/fr-coverage.md` and `requirements/atomic-requirements.md` entries for REQ-012.

*Status: Accepted — signed off by Compliance and Procurement.*

Signed-off-by: Compliance; Procurement
