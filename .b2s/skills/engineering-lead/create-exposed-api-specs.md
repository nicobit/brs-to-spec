# Skill — Create Exposed API Specifications

## Identity

```text
skill_id:    engineering-lead.create-exposed-api-specs
persona:     engineering-lead
action_id:   create-exposed-api-specs
produces:    technical-specifications/api/exposed/
```

## When this skill is used

Run after architecture review, architecture rules, delivery structure, and readiness check exist. Produces one specification file per API surface this initiative exposes.

## Role for this task

You are a senior engineering lead defining the API contract for every surface this initiative publishes. Your output must be precise enough for a consuming team to integrate against it without reading the BRS.

## Preconditions

Before starting, verify:
- `architecture/architecture-review.md` exists
- `architecture/architecture-rules.md` exists
- `planning/delivery-structure.md` exists
- `engineering-readiness/readiness-check.md` exists

If any required input is missing, stop and report the blocker.

## Instructions

### Step 1 — Read all inputs

Read every path listed in `{resolved_required_inputs}` fully before writing anything.
If `{resolved_optional_inputs}` is not empty, read those paths fully as well before writing.
Do not start writing until all available resolved inputs are read completely.

### Step 2 — Identify API surfaces

From `architecture/architecture-review.md`, extract every API surface this initiative exposes. Look for:
- "Feature Area" table rows that name a new or changed API
- "New Components / Boundaries" that introduce a new service or endpoint group
- Any consumer listed in the architecture that this initiative serves

Group endpoints by surface (e.g. Applications API, Decisions API). Each distinct surface becomes one output file.

### Step 3 — Read contract mode

From `engineering-readiness/readiness-check.md`, read `api_contract_mode`:
- `product`: produce a complete, stable specification — no placeholders allowed
- `internal`: produce a minimal draft; mark sections that will be refined after story packages as `[to refine]`
- `coordinated`: produce a complete specification and note the coordinating team in the Consumer Context section

### Step 4 — Map endpoints to stories

From `planning/delivery-structure.md`, identify which story (`F-NNN.N`) implements each endpoint. Every endpoint in the output must have a `Story ref` field.

### Step 5 — Extract architecture constraints

From `architecture/architecture-rules.md`, extract constraints that govern this API:
- authentication mechanism (do not use a generic "OAuth2" — name the specific grant type and scope)
- TLS version
- versioning policy
- rate limits if specified

These constraints must propagate verbatim into every file produced by this skill.

### Step 6 — Produce one file per API surface

For each API surface identified in Step 2, write one file at:

`technical-specifications/api/exposed/{{api-slug}}.md`

Use `.b2s/artifact-templates/exposed-api-spec.md` as the output shape.

Populate every section with content derived from inputs. Rules:
- Endpoint paths must use the versioned format (`/v1/...`) unless architecture rules specify otherwise
- Every endpoint must have an `EP-NNN` identifier, sequential within the file
- SLA values must come from the BRS or architecture constraints — do not invent numbers; record as open question if unknown
- Auth mechanism must match the architecture rules exactly
- Contract mode must be stated in the Metadata section and must match the value from the readiness check
- Open questions must be written for every field that cannot be determined from inputs
- `{{placeholder}}` text must not appear in the final output

## Output requirements

Write one file per API surface to `technical-specifications/api/exposed/`.
The `{primary_output}` resolves to this folder.

## Done criteria

- [ ] Every API surface in the architecture review has a corresponding file
- [ ] Every endpoint has an `EP-NNN`, a method, a path, a story ref, and a purpose
- [ ] Auth mechanism matches architecture rules — not generic
- [ ] SLA values come from inputs or are flagged as open questions
- [ ] Contract mode is stated and matches the readiness check
- [ ] No `{{placeholder}}` text in any produced file
- [ ] Status is `In progress` in every file
