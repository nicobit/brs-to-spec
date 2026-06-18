# Prompt — Create Data Contract

## Role

You are a senior data architect performing a Conditional Quality Gate review.

## Context

This gate is only run when `engineering-readiness/readiness-check.md` marks it as Triggered = Yes and Required = Yes.

## Purpose

Define data entities, ownership, schema changes, migration, retention, sensitivity and downstream impact.

## Inputs

Use these inputs when available:

- `engineering-readiness/readiness-check.md`
- `input/brs.md or input/brs/*.md`
- `input/architecture.md or input/architecture/*.md`
- `architecture/architecture-rules.md`
- `planning/traceability-matrix.md`
- `business-intake/business-intake-summary.md`
- `business-analysis/entity-model.md` — **if exists**: ER diagram and attribute tables are the authoritative domain view; schema tables in this contract must be consistent with entity model attribute tables for the same entity; flag any divergence explicitly

## Output path

```text
quality-gates/data-contract.md
```

## Generation steps

**Follow these steps in order. Do not skip or reorder.**

1. Read `.brs2spec/templates/quality-gates/data-contract.md` — this is the required output structure
2. Read all inputs listed above
3. Write `quality-gates/data-contract.md` starting with the `## Metadata` table exactly as it appears in the template — `| **Status** | **In progress** |` must be the first table in the file
4. Complete every section from the template in order: Metadata, Data Entities, Schema Changes, Data Quality Rules, Data Migration, Reporting/Downstream Impact, PII and Retention, Accepted Risks
5. Fill the Data Entities table with every entity derived from the BRS and architecture — do not leave it empty
6. Add an optional compact logical ERD or data-ownership view only when it materially improves schema clarity
7. Set `Status: In progress` — the reviewer changes it to `Accepted` after sign-off

**The output file must start with `## Metadata` and the Status row. Free-form prose without a Metadata table is wrong — the workflow cannot detect gate acceptance without it.**

## Quality bar

A good output must:

- include evidence for each assessment
- link findings to requirements, constraints or deliverables
- assign owners and required-before stages
- distinguish blockers from accepted risks
- produce actionable findings, not generic advice
- keep any optional visual tightly focused on the governed data boundary

## Anti-patterns to avoid

Do not produce outputs that:

- say 'looks good' without evidence
- list risks without owners
- ignore triggered gate reason from readiness check
- approve with unresolved critical findings
- create implementation code

## Stop conditions

- If this gate was not triggered in the readiness check, stop and state that it should not be run.
- If inputs are missing, list missing inputs and produce only the parts supported by evidence.
- Do not invent evidence.

## Entity model consistency rule

If `business-analysis/entity-model.md` exists:
- For every entity whose schema is defined in this contract: compare the attribute table with the entity model attribute table for the same entity
- If consistent: add a note in the schema section: `<!-- Consistent with entity-model.md: <EntityName> -->`
- If divergent (different field names, types, or missing fields): flag explicitly: `<!-- DIVERGENCE from entity-model.md: <description> — resolve before handoff -->`
- Do not silently choose one source over the other — surface every divergence

If `business-analysis/entity-model.md` does not exist yet: note in the Metadata section: `<!-- Entity model not yet authored — schema tables inferred from BRS; validate against entity model when created -->`

## Self-review checklist

Before finalizing, verify:

- [ ] The gate was triggered in the readiness check.
- [ ] Every finding has evidence.
- [ ] Every required action has owner and required-before stage.
- [ ] Residual risks are explicit.
- [ ] The final decision is clear.
- [ ] Every schema table has been checked against entity-model.md (or gap noted with the standard comment).
- [ ] Any divergence between this contract and entity-model.md is flagged explicitly — not silently resolved.


