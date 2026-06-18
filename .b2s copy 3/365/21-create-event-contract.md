# Prompt 21 - Create Event Contract

## Inputs to give Copilot

Required:

- `initiatives/<id>-<slug>/engineering-readiness/readiness-check.md`
- `initiatives/<id>-<slug>/architecture/architecture-review.md`
- `initiatives/<id>-<slug>/architecture/architecture-rules.md`
- `initiatives/<id>-<slug>/input/brs.md`
- any additional BRS markdown files under the initiative input folder
- `.b2s/artifact-templates/event-contract.md`

## Output file to create

- `initiatives/<id>-<slug>/quality-gates/event-contract.md`

## Prompt for Office 365 Copilot

You are following the `.b2s` framework action `create-event-contract`.

Run this only when `Event Contract` is explicitly triggered in the readiness
check. If not triggered, stop and say the action does not apply.

Read all provided inputs in full before writing anything.

Enumerate every new, changed, or removed domain event and document:

- producer
- consumers
- trigger
- schema
- envelope
- delivery guarantee
- ordering
- idempotency
- evolution
- dead-letter handling

Write `quality-gates/event-contract.md` using the provided template.

Before finalizing, ensure every event has an `EVT-SCHEMA-NNN`, producers and
consumers are explicit, and delivery guarantees and evolution rules are clear.
Status must be `In progress`.
