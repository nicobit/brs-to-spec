# Prompt 06 Decision Note

## Existing partial coverage

- `check-engineering-readiness` already decides whether downstream quality gates are needed and captures readiness evidence.
- `create-security-review` covers security-specific concerns.
- `create-observability-plan` covers observability, alerting, and support diagnostics.
- `create-openspec-handoff` and `create-standalone-handoff` already produce implementation-oriented handoff packages for coding agents.

## Remaining gaps

- There is no single artifact that consolidates cross-cutting NFR coverage across security, availability, resiliency, observability, supportability, scalability, and compliance.
- Readiness decides that gates are needed, but it does not produce explicit NFR requirements with identifiers, measures, and follow-up actions.
- The handoff actions are already close to an AI coding handoff, but the contract does not state that role explicitly enough and does not consistently require NFR-derived constraints and impacted areas.

## Decision

- `NFR assessment` -> `add-new-action`
  - Reason: extending readiness would overload the readiness gate with a second purpose and still would not create the requested dedicated artifact `nfr-assessment.md`.
- `AI coding handoff` -> `extend-existing-action`
  - Reason: dedicated handoff actions already exist. Adding another parallel handoff action would duplicate intent and create ambiguous ownership between near-identical outputs.

## Implementation direction

- Add `create-nfr-assessment` in `4b-quality-gates`.
- Extend `create-openspec-handoff` and `create-standalone-handoff` so they explicitly consume `quality-gates/nfr-assessment.md` and produce stronger AI-agent-ready output contracts.
