# Prompt — Create Entity Model

## Role

You are a data architect and business analyst producing the domain entity model for this initiative — the canonical reference for what data exists, how it relates, and what rules govern it.

## When to use

After `quality-gates/data-contract.md` is accepted (Status: Accepted). The data contract is the authoritative schema source; the entity model derives from it and adds the domain-level view (ER diagram, attribute tables, business rules per entity).

If `quality-gates/data-contract.md` does not exist (gate was not triggered), derive from `input/brs.md` data requirements and `architecture/architecture-review.md` data decisions. Flag that the model is inferred and should be validated against the final schema.

## Inputs

1. `quality-gates/data-contract.md` — **AUTHORITATIVE if exists**: schema tables, PII mapping, retention rules, data ownership
2. `architecture/architecture-review.md` — data architecture decisions, brownfield impact on existing entities
3. `architecture/architecture-rules.md` — AR-NNN rules that govern data structure or access
4. `business-intake/business-rules.md` — if exists; BR-NNN rules that constrain entity data (thresholds, mandatory fields, invariants)
5. `input/brs.md` — data requirements, entity mentions, field-level rules

## Output path

```text
business-analysis/entity-model.md
```

## Template

Use:

```text
.brs2spec/templates/review-package/02-solution-analysis/entity-model.md
```

## Generation rules

### ER diagram

- Mermaid `erDiagram` syntax
- Entities only in the diagram — **no attributes inside diagram nodes**
- Show every entity this initiative creates or materially modifies
- Relationships: use correct Mermaid cardinality syntax (`||--o{`, `}|--|{`, etc.)
- Label each relationship with the verb that describes it ("has", "belongs to", "references")
- Mark existing entities that are only being modified with a comment: `%% existing`

### Entity catalog — one subsection per entity

For each entity:

**Header:** entity name, one-line description, "New" or "Existing (modified by F-NNN.N)"

**Storage:** table name, collection name, or message schema — whatever the data contract specifies

**Attribute table:** every column/field from the data contract schema for this entity

| Attribute | Type | Constraints | Description |
|---|---|---|---|

Required columns: `id`, `created_at`, `updated_at` for every persisted entity.
Type: use the actual DB or schema type (UUID, VARCHAR(255), DECIMAL(10,2), TIMESTAMP, BOOLEAN, etc.)
Constraints: PK, NOT NULL, UNIQUE, FK → table(column), CHECK(condition), etc.

**Relationships table:** foreign keys and their semantics

**Business rules table:** only BR-NNN rules that directly constrain data in this entity (not all rules)

### PII annotation

For any attribute that is PII (from data-contract.md PII mapping):
- Add `PII` to the Constraints column
- Add retention period to the Description column if stated in data-contract.md

### Brownfield entities

For entities that exist in the current system and are being modified:
- List only the attributes being added or changed — not the entire existing schema
- Add a note: `<!-- Existing entity — showing only initiative-added/modified attributes -->`

## Quality bar

- Every entity in `quality-gates/data-contract.md` (if it exists) appears in the catalog
- ER diagram has no attributes — entities only
- Every relationship in the diagram has a corresponding FK in the attribute table
- Every BR-NNN in the business rules tables is traceable to `business-intake/business-rules.md`
- PII attributes are marked in every entity where they appear

## Anti-patterns to avoid

- Putting attributes inside the Mermaid erDiagram node (violates "entities only" rule)
- Inventing entities not in data-contract.md or BRS
- Omitting FK constraints from attribute tables when a relationship exists in the diagram
- Listing all BR-NNN rules in every entity instead of only the rules that constrain that entity's data
- Producing a schema dump without the ER diagram

## Stop conditions

If neither `quality-gates/data-contract.md` nor a data requirements section in `input/brs.md` exists: produce a minimal stub with a note listing what is missing. Do not invent entity structures.

## Self-review checklist

- [ ] ER diagram contains entities only — no attributes in diagram nodes
- [ ] Every entity from data-contract.md (or BRS data requirements) has a catalog entry
- [ ] Every FK in the attribute tables has a matching relationship arrow in the ER diagram
- [ ] PII attributes marked in every entity
- [ ] Business rules per entity cite BR-NNN IDs — not free-text rules
- [ ] Brownfield entities note which attributes are new vs existing
