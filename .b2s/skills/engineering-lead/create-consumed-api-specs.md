# Skill — Create Consumed API Specifications

## Identity

```text
skill_id:    engineering-lead.create-consumed-api-specs
persona:     engineering-lead
action_id:   create-consumed-api-specs
produces:    technical-specifications/api/consumed/
```

## When this skill is used

Run after architecture review, architecture rules, and delivery structure exist. Produces one specification file per external system this initiative consumes.

## Role for this task

You are a senior engineering lead documenting the integration contract for every external system this initiative depends on. Your output must be precise enough for the implementation team to handle auth, PII, and fallback without reading the BRS.

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

### Step 2 — Identify consumed external systems

From `architecture/architecture-review.md`, extract every external system this initiative consumes. Look for:
- "Existing Components Touched" listing third-party or external services
- "New Components / Boundaries" that introduce a new integration dependency
- Any named external provider in the integration map

For each system, record its name and whether this initiative only calls it (`consumed`), only receives calls from it (`exposed`), or both (`bidirectional`). Only systems that are consumed or bidirectional produce a file from this skill.

### Step 3 — Map systems to stories

From `planning/delivery-structure.md`, identify which story (`S-NNN.N`) depends on each external system. Record these story refs for the Traceability and Dependent Stories sections.

### Step 4 — Extract integration constraints

From `architecture/architecture-rules.md`, extract constraints that govern external integrations:
- timeout and retry policies (e.g. ARCH-C-005)
- circuit breaker requirements
- credential storage rules
- enterprise contract references (e.g. ARCH-C-003)

These constraints must appear in the Integration Behaviour and Compliance sections of each file.

### Step 5 — Identify PII transmitted

For each external system, determine which fields containing personal or financial data are transmitted. PII field names must be listed explicitly — "see BRS" is not acceptable. If the field list cannot be determined from inputs, record it as an open question.

### Step 6 — Specify fallback behaviour

For every external system, state the fallback when the system is unavailable. Choose from:
- `refer-to-underwriter` — route for manual handling
- `degrade gracefully` — return partial result without the external data
- `hard fail` — return error to the caller
- `circuit breaker` — stop calls, return cached or fallback response

If the BRS or architecture rules do not specify a fallback, derive the most conservative option consistent with the architecture constraints and flag it as a recommended default open question.

### Step 7 — Produce one file per consumed system

For each external system identified in Step 2, write one file at:

`technical-specifications/api/consumed/{{system-slug}}.md`

Use `.b2s/artifact-templates/consumed-api-spec.md` as the output shape.

Populate every section with content derived from inputs. Rules:
- If the provider's actual API spec URL or document reference is unknown, record it as an open question — do not invent endpoint paths
- Fallback behaviour must be one concrete value from Step 6 — "unknown" or "TBD" is not acceptable
- PII section must list field names — not a reference to another document
- Auth mechanism must be specific (e.g. "OAuth2 client credentials — client_id from Azure Key Vault")
- `{{placeholder}}` text must not appear in the final output

## Output requirements

Write one file per consumed external system to `technical-specifications/api/consumed/`.
The `{primary_output}` resolves to this folder.

## Done criteria

- [ ] Every consumed or bidirectional external system in the architecture review has a corresponding file
- [ ] Systems that are only exposed to (not consumed) are excluded with a note
- [ ] PII fields are listed explicitly in every file — no "see BRS" references
- [ ] Fallback behaviour is concrete and actionable in every file
- [ ] Auth mechanism is specific — not generic
- [ ] Integration constraints from architecture rules are referenced by constraint ID
- [ ] No `{{placeholder}}` text in any produced file
- [ ] Status is `In progress` in every file
