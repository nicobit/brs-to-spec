# Skill — Create Event Contract

## Identity

| Field | Value |
|---|---|
| skill_id | eng-create-event-contract |
| persona | engineering-lead |
| event_types | CREATE_EVENT_CONTRACT |
| produces | quality-gates/event-contract.md |

## When this skill is used

Conditional quality gate — triggered when `engineering-readiness/readiness-check.md` marks Event Contract Triggered = Yes.

Event contract trigger condition: a new domain event, message, or async notification is introduced or an existing event schema is changed.

## Role for this task

You are a senior engineering lead defining the formal event contract for the initiative — specifying event types, schemas, producers, consumers, delivery guarantees, ordering, and schema evolution rules.

## Prerequisites check

Before starting, verify:
- [ ] `engineering-readiness/readiness-check.md` marks Event Contract as Triggered = Yes
- [ ] `input/brs.md` is readable
- [ ] `architecture/architecture-review.md` exists (async architecture decisions)
- [ ] `architecture/architecture-rules.md` exists (AR-NNN for messaging constraints)

If this gate was NOT triggered: stop.

## Instructions

### Step 1 — Enumerate all events

From the BRS and architecture review:
- Every new domain event introduced
- Every modified event schema
- Every removed event (deprecation plan needed)
- Every notification or webhook payload

### Step 2 — For each event, document

1. **Event ID** — EVT-SCHEMA-NNN (not to be confused with workflow event files)
2. **Event type** — exact event name string (e.g. `loan.application.submitted`)
3. **Purpose** — one line: what business fact this event communicates
4. **Producer** — which service/component publishes this event
5. **Consumers** — which services/components subscribe to this event
6. **Trigger** — what action or state change causes this event to be published
7. **Schema** — all fields with type, required/optional, constraints
8. **Envelope** — message envelope format (correlation ID, timestamp, event version, source)
9. **Delivery guarantee** — at-least-once / at-most-once / exactly-once
10. **Ordering guarantee** — unordered / ordered per partition key
11. **Idempotency** — how should consumers handle duplicate delivery?
12. **Schema evolution** — what is the backward compatibility rule for this event type? (additive only / versioned / breaking-with-migration)
13. **Dead letter handling** — what happens to unprocessable events?

### Step 3 — Write the artifact

The output must start with `## Metadata` and `| **Status** | **In progress** |`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- Event catalog: EVT-SCHEMA-NNN, Type, Producer, Consumers, Trigger, Delivery Guarantee
- Full event definition per EVT-SCHEMA-NNN
- Schema evolution rules section
- Consumer impact: which consumers are affected by schema changes

## Done criteria

- [ ] Every new or modified event has an EVT-SCHEMA-NNN entry
- [ ] Every event has producer and consumers documented
- [ ] Delivery and ordering guarantees are specified
- [ ] Schema evolution rules are explicit
- [ ] Idempotency handling documented
- [ ] `Status: In progress` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `quality-gates/event-contract.md`

## Stop conditions

- If this gate was not triggered: stop immediately.
- Do not invent events not derivable from the BRS or architecture.
