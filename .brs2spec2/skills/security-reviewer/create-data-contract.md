# Skill — Create Data Contract

## Identity

| Field | Value |
|---|---|
| skill_id | sec-create-data-contract |
| persona | security-reviewer |
| event_types | CREATE_DATA_CONTRACT |
| produces | quality-gates/data-contract.md |

## When this skill is used

Conditional quality gate — triggered when `engineering-readiness/readiness-check.md` marks Data Contract Triggered = Yes.

Data contract trigger conditions (ANY of these):
- A new schema, table, or data store is introduced
- A data migration is performed
- A new data ownership boundary is established
- PII data is handled

## Role for this task

You are a senior data architect and security reviewer defining the formal data contract for the initiative — specifying schema, PII classification, retention, encryption, access control, and migration approach.

## Prerequisites check

Before starting, verify:
- [ ] `engineering-readiness/readiness-check.md` marks Data Contract as Triggered = Yes
- [ ] `input/brs.md` is readable
- [ ] `architecture/architecture-review.md` exists
- [ ] `business-analysis/business-rules.md` exists (data integrity rules BR-NNN)
- [ ] `business-analysis/entity-model.md` exists (ENT-NNN entities as business-level input)

If this gate was NOT triggered: stop and state that the data contract should not be run.

## Instructions

### Step 1 — Enumerate all data assets

From the BRS, entity model, and architecture review:
- Every new or modified table or collection
- Every new or modified event payload schema
- Every data file or export format introduced
- Every external data source consumed

### Step 2 — For each data asset, document

1. **Asset ID** — DA-NNN
2. **Name** — data store / table / collection / event type name
3. **Owner** — which service or module owns this data
4. **Classification** — Internal / Confidential / PII / Regulated
5. **Schema** — fields with type, constraints, nullable, default
6. **PII fields** — which specific fields contain PII? What type of PII (name, email, address, financial, health)?
7. **Encryption** — at rest: Yes/No; in transit: Yes/No; encryption mechanism
8. **Access control** — who can read / write / delete; role-based restrictions from BR-NNN
9. **Retention** — retention period; deletion trigger; regulatory requirement source
10. **Migration** — if this modifies an existing schema: migration strategy (additive/versioned/breaking), backward compatibility, rollback plan

### Step 3 — Assess data flow

Document how data moves between components:
- Who produces this data asset?
- Who consumes it?
- Is the flow synchronous or asynchronous?
- Are there cross-boundary data transfers (to external systems, to audit stores)?

### Step 4 — Write the artifact

The output must start with `## Metadata` and `| **Status** | **In progress** |`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- Data asset catalog: DA-NNN, Name, Owner, Classification, PII fields, Encryption, Retention
- Schema tables per data asset (field-level detail)
- PII mapping: PII field → classification → encryption → retention → deletion trigger
- Migration plan section (for modified schemas)
- Accepted risks section
- Decision: Approved / Request Changes / Blocked

## Done criteria

- [ ] Every new or modified schema has a DA-NNN entry
- [ ] Every PII field is classified and has encryption and retention specified
- [ ] Migration approach is documented for all schema changes
- [ ] Access control rules trace to BR-NNN
- [ ] `Status: In progress` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `quality-gates/data-contract.md`

## Stop conditions

- If this gate was not triggered: stop immediately.
- If the BRS mentions PII but the entity model is missing: proceed with BRS-only assessment and flag the gap.
- Do not invent schema fields not derivable from the BRS or architecture.
