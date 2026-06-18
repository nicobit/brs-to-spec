# Skill - Create Event Contract

## Identity

```text
skill_id:    engineering-lead.create-event-contract
persona:     engineering-lead
action_id:   create-event-contract
produces:    quality-gates/event-contract.md
```

## When this skill is used

Run this only when the readiness check explicitly triggers the event contract gate.

## Preconditions

Before starting, verify:
- `engineering-readiness/readiness-check.md` marks Event Contract as triggered
- BRS source files are readable
- `architecture/architecture-review.md` exists
- `architecture/architecture-rules.md` exists

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/architecture/architecture-review.md`
- `{workspace_root}/architecture/architecture-rules.md`
- All BRS source files under `{workspace_root}/input/`

Do not start writing until all available inputs are read completely.

### Step 2 - Enumerate new, changed, or removed domain events and document producer, consumers, trigger, schema, envelope, delivery guarantee, ordering, idempotency, evolution, and dead-letter handling.

## Output requirements

Write `quality-gates/event-contract.md` using `.b2s/artifact-templates/event-contract.md`.

## Done criteria

- [ ] Every new or changed event has an `EVT-SCHEMA-NNN`
- [ ] Producers and consumers are explicit
- [ ] Delivery guarantees and evolution rules are explicit
- [ ] Status is `In progress`
