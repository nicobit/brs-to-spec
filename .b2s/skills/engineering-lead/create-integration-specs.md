# Skill — Create Integration Specifications

## Identity

```text
skill_id:    engineering-lead.create-integration-specs
persona:     engineering-lead
action_id:   create-integration-specs
produces:    technical-specifications/integrations/
```

## When this skill is used

Run after architecture review, architecture rules, and delivery structure exist. Produces one specification file per external system this initiative integrates with (consumed or bidirectional).

## Role for this task

You are a senior engineering lead specifying the reliability contract for every external integration. Your output must be precise enough for the implementation team to configure timeouts, retries, circuit breakers, fallback behaviour, and observability without reading the BRS.

## Preconditions

Before starting, verify:
- `architecture/architecture-review.md` exists
- `architecture/architecture-rules.md` exists
- `planning/delivery-structure.md` exists

If any required input is missing, stop and report the blocker.

## Instructions

### Step 1 — Read all inputs

Read every path listed in `{resolved_required_inputs}` fully before writing anything.
If `{resolved_optional_inputs}` is not empty, read those paths fully as well before writing.
Do not start writing until all available resolved inputs are read completely.

### Step 2 — Identify integrations

From `architecture/architecture-review.md`, extract every external system this initiative integrates with. Classify each as:
- `consumed` — this initiative calls the external system
- `exposed` — the external system calls this initiative only (no integration spec needed for this direction)
- `bidirectional` — both directions exist

Produce an integration spec for every system classified as `consumed` or `bidirectional`.

### Step 3 — Extract architecture integration constraints

From `architecture/architecture-rules.md`, extract:
- timeout and retry policies per integration or globally (e.g. ARCH-C-005: max 5s timeout, 3 retries)
- circuit breaker requirements
- enterprise contract references (e.g. ARCH-C-003)
- credential storage rules (e.g. Azure Key Vault only)

Record the constraint ID alongside every value derived from it in the output.

### Step 4 — Map integrations to stories

From `planning/delivery-structure.md`, identify which story (`S-NNN.N`) depends on each external system. Record these for the Dependent Stories section.

### Step 5 — Specify reliability contract

For each integration, determine:

- **Timeout**: use the architecture constraint value. If not specified, use 5000ms as recommended default and flag as open question.
- **Retries**: use the architecture constraint value. If not specified, use 3 retries with exponential backoff and flag as open question.
- **Circuit breaker**: use the architecture constraint threshold. If not specified, recommend 5 failures in 30 seconds and flag as open question.
- **Fallback**: must be one concrete value — `refer-to-underwriter`, `degrade gracefully`, `hard fail`, or `queue`. Derive from BRS or architecture constraints. If unspecified, choose the most conservative option consistent with the architecture rules and flag it as a recommended default open question. "TBD" or "placeholder" is not acceptable.

### Step 6 — Define observability signals

For each integration, define:
- a named success event (e.g. `EXPERIAN_CREDIT_CHECK_SUCCESS`) that is emitted to the audit store on every successful call
- a named failure event (e.g. `EXPERIAN_CREDIT_CHECK_FAILURE`) that is emitted on every failed call after retries are exhausted
- a latency metric name (e.g. `experian.credit_check.duration_ms`)
- an alert threshold (e.g. P99 > 4000ms triggers on-call alert)

### Step 7 — Check for enterprise contracts

From `architecture/architecture-rules.md`, identify any constraint that indicates an enterprise-level contract with the external system (e.g. ARCH-C-003: "Experian integration governed by enterprise contract"). If found, set `Enterprise contract: Yes — ref ARCH-C-NNN` in the Metadata section.

### Step 8 — Produce one file per integration

For each system identified in Step 2 (consumed or bidirectional), write one file at:

`technical-specifications/integrations/{{system-slug}}-integration.md`

Use `.b2s/artifact-templates/integration-spec.md` as the output shape.

Populate every section with content derived from inputs. Rules:
- Timeout, retry, and circuit breaker values must come from architecture constraints or be flagged as open questions with a recommended default
- Fallback behaviour must be actionable — never "TBD" or placeholder
- Every integration must have a named success event and failure event
- Compliance notes must reference architecture constraints by ID
- `{{placeholder}}` text must not appear in the final output

## Output requirements

Write one file per consumed or bidirectional integration to `technical-specifications/integrations/`.
The `{primary_output}` resolves to this folder.

## Done criteria

- [ ] Every consumed or bidirectional external system in the architecture review has an integration spec
- [ ] Systems that are only exposed to are excluded with a note
- [ ] Timeout and retry values come from architecture constraints or are flagged as open questions with recommended defaults
- [ ] Fallback behaviour is concrete and actionable in every file
- [ ] Every integration has a named success event, failure event, and latency metric
- [ ] Enterprise contracts are referenced by constraint ID where applicable
- [ ] Compliance notes reference architecture constraints explicitly
- [ ] No `{{placeholder}}` text in any produced file
- [ ] Status is `In progress` in every file
