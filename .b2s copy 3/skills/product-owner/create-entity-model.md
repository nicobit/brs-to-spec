# Skill - Create Entity Model

## Identity

```text
skill_id:    product-owner.create-entity-model
persona:     product-owner
action_id:   create-entity-model
produces:    business-analysis/entity-model.md
```

## When this skill is used

Run this after the requirements catalog exists. It models the significant business entities, their attributes, relationships, and lifecycle-level data rules.

## Role for this task

You are a senior business analyst, working at business concept level rather than database schema level. The requirements catalog is the primary index, but you must cross-check domain vocabulary against the BRS and intake summary.

## Preconditions

Before starting, verify:
- `business-analysis/requirements.md` exists and has `FR-NNN` rows

Optional context:
- `business-analysis/business-rules.md`
- `business-analysis/gaps-and-questions.md`
- `architecture/architecture-review.md`
- `business-intake/business-intake-summary.md`
- BRS source files in `input/`

If the required input is missing, stop and report the blocker.

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/business-analysis/requirements.md`
- `{workspace_root}/business-intake/business-intake-summary.md`

If optional files exist, read them too:
- `{workspace_root}/business-analysis/business-rules.md`
- `{workspace_root}/business-analysis/gaps-and-questions.md`
- `{workspace_root}/architecture/architecture-review.md`
- BRS source files under `{workspace_root}/input/`

Do not start writing until all available inputs are read completely.

### Step 2 - Identify business entities

Read `{workspace_root}/business-analysis/requirements.md` in full. Identify meaningful persistent business objects:
- named things created, updated, read, or deleted
- things with status, lifecycle, or ownership
- things referenced by multiple requirements
- things flowing between actors or systems

Prefer initiative-specific domain nouns over generic software nouns unless the source clearly uses the generic noun as a first-class entity.

### Step 3 - Define each entity

For each `ENT-NNN`, record:
- name
- one-sentence business description
- owner
- PII flag with fields if relevant
- `FR-NNN` source references

### Step 4 - Define key attributes

For each entity, provide business-meaningful attributes with:
- description
- data type
- length or precision
- validation rules

Use business constraints and `BR-NNN` references where available. Do not invent database implementation details.

### Step 5 - Map relationships

For each relationship, define:
- verb phrase
- cardinality
- optionality
- governing `BR-NNN` rule if applicable

### Step 6 - Write the ER diagram

Write one Mermaid `erDiagram` showing entities and relationships only. Do not include attribute blocks in the diagram itself.

## Output requirements

Write `business-analysis/entity-model.md` using `.b2s/artifact-templates/entity-model.md`.

The artifact must contain:
- metadata with `Status: Draft`
- entity catalog
- one entity section per `ENT-NNN`
- Mermaid ER diagram
- feature coverage table

## Done criteria

- [ ] Every persistent business object implied by the source has an `ENT-NNN`
- [ ] Every entity has owner, PII flag, and at least one `FR-NNN` source
- [ ] Every entity has an attribute table with five columns
- [ ] Relationships include cardinality and optionality
- [ ] Data integrity constraints reference `BR-NNN` where available
- [ ] The Mermaid ER diagram is syntactically valid and shows only entities and relationships
- [ ] No database implementation details are introduced
- [ ] Status is `Draft`

## Notes for the staged engine

- Do not mention event result files or dispatcher behavior
- This prompt writes only the artifact
