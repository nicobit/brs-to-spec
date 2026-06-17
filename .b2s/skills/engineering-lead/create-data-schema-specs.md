# Skill — Create Data Schema Specifications

## Identity

```text
skill_id:    engineering-lead.create-data-schema-specs
persona:     engineering-lead
action_id:   create-data-schema-specs
produces:    technical-specifications/data/
```

## When this skill is used

Run after architecture review, architecture rules, delivery structure, and requirements exist. Produces one specification file per data domain this initiative introduces or modifies.

## Role for this task

You are a senior engineering lead documenting every data entity this initiative owns. Your output must be precise enough for the implementation team to define storage, migrations, PII handling, and retention without reading the BRS.

## Preconditions

Before starting, verify:
- `architecture/architecture-review.md` exists
- `architecture/architecture-rules.md` exists
- `planning/delivery-structure.md` exists
- `business-analysis/requirements.md` exists

Optional:
- `business-analysis/business-rules.md` — rules that translate to schema constraints

If any required input is missing, stop and report the blocker.

## Instructions

### Step 1 — Read all inputs

Read every path listed in `{resolved_required_inputs}` fully before writing anything.
If `{resolved_optional_inputs}` is not empty, read those paths fully as well before writing.
Do not start writing until all available resolved inputs are read completely.

### Step 2 — Identify data domains

From `architecture/architecture-review.md`, identify which data layer components this initiative introduces or modifies. Group entities into domains (e.g. Applications, Decisions, Audit, Users). Each domain becomes one output file.

Use `business-analysis/requirements.md` to identify FR-NNN that drive storage, retention, or PII requirements. Use `planning/delivery-structure.md` to confirm which stories create or modify data in each domain.

### Step 3 — Extract data constraints from architecture rules

From `architecture/architecture-rules.md`, extract:
- data residency constraints (e.g. UK-only storage)
- PII handling requirements (masking, encryption, pseudonymisation)
- retention periods when specified
- shared-database rules (coordination requirements for cross-team schemas)

These constraints must appear in the PII Inventory and Migration Strategy sections of each file.

### Step 4 — Derive schema constraints from business rules

From `business-analysis/business-rules.md` (if present), extract rules that translate directly to database constraints:
- validation rules → `CHECK` constraints or `NOT NULL`
- uniqueness rules → unique indexes
- state machine rules → enumeration values

Every business rule that constrains a field must be referenced by `BR-NNN` in the relevant field row.

### Step 5 — Produce one file per data domain

For each domain identified in Step 2, write one file at:

`technical-specifications/data/{{domain-slug}}-schema.md`

Use `.b2s/artifact-templates/data-schema-spec.md` as the output shape.

Populate every section with content derived from inputs. Rules:
- Every entity must have at minimum: `id` (uuid PK), `created_at` (timestamp), `updated_at` (timestamp)
- Status enumerations must list ALL valid values — no "etc." or "..."
- PII field names must be listed explicitly — "see BRS" is not acceptable
- Retention period must come from the BRS or architecture rules — if not specified, record as open question
- Shared schemas (used by multiple teams) must be flagged with a coordination note in the Migration Strategy section
- Migration approach must be stated — "additive only", "blue-green", or "feature flag" — not left as placeholder
- Every story that persists data must map to at least one entity in the domain file
- `{{placeholder}}` text must not appear in the final output

## Output requirements

Write one file per data domain to `technical-specifications/data/`.
The `{primary_output}` resolves to this folder.

## Done criteria

- [ ] Every data layer component in the architecture review maps to a domain file
- [ ] Every entity has a primary key, created_at, and updated_at
- [ ] PII fields are listed explicitly with retention and deletion trigger
- [ ] Every enumeration lists all valid values — no "..." entries
- [ ] Business rules that constrain fields are referenced by BR-NNN
- [ ] Migration approach is stated in every file
- [ ] Shared schemas are flagged with coordination notes
- [ ] No `{{placeholder}}` text in any produced file
- [ ] Status is `In progress` in every file
