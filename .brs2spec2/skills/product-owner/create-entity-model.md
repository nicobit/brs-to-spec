# Skill — Create Entity Model

## Identity

| Field | Value |
|---|---|
| skill_id | po-create-entity-model |
| persona | product-owner |
| event_types | CREATE_ENTITY_MODEL |
| produces | business-analysis/entity-model.md |

## When this skill is used

After `CREATE_REQUIREMENTS_CATALOG` completes and `business-analysis/requirements.md` exists. Runs in parallel with `CREATE_USE_CASE_DIAGRAM`, `CREATE_BUSINESS_RULES`, and `FIND_GAPS_AND_QUESTIONS` — these events do not block each other. The entity model is a first-class business-analysis artifact for initiatives with meaningful domain data. It feeds `CREATE_DATA_CONTRACT` and informs architecture review.

## Role for this task

You are a senior business analyst (with architect collaboration) identifying and modelling every significant business entity, their attributes, relationships, and data rules — at business concept level, not database schema level. The requirements catalog is the primary index, but you must cross-check entity names, relationships, and domain vocabulary against the BRS and intake summary before finalizing.

## Prerequisites check

Before starting, verify:
- [ ] `business-analysis/requirements.md` exists and has FR-NNN rows

Optional inputs (read if available, do not block if missing):
- [ ] `business-analysis/business-rules.md` (data integrity and validation rules BR-NNN)
- [ ] `business-analysis/gaps-and-questions.md` (ambiguities that may affect entity scope)
- [ ] `architecture/architecture-review.md` (optional: architecture feedback on data ownership and boundaries)
- [ ] `business-intake/business-intake-summary.md` (fallback context if requirements need clarification)
- [ ] `input/brs.md` or `input/brs/*.md` (authoritative domain vocabulary and lifecycle context)

If the required input is missing, stop and report what is absent.

## Instructions

### Step 1 — Identify business entities from requirements

Read `business-analysis/requirements.md` in full. Identify every noun that represents a persistent, meaningful business object. Signals to look for:
- Named things that are created, updated, read, or deleted in FR-NNN rows
- Things that have status, lifecycle, or ownership
- Things referenced by multiple functional requirements
- Things that flow between actors or systems

Then cross-check the candidate entity list against the BRS and intake summary:
- Prefer initiative-specific domain nouns from the BRS over generic software nouns like `User`, `Account`, or `Request` unless the BRS explicitly uses them as first-class entities
- If the initiative spans a lifecycle (for example application, scoring, compliance, review, offer, disbursement), the entity set must reflect that lifecycle breadth rather than only the first intake object

Assign entity IDs sequentially: ENT-001, ENT-002, ...

### Step 2 — Define each entity

For each ENT-NNN:
1. **Name** — business name (not table name, not technical identifier)
2. **Description** — one sentence of what this entity represents in the business domain
3. **Owner** — which actor or system creates and owns this entity (ACT-NNN or SYS-NNN if known)
4. **PII flag** — does this entity contain personally identifiable information? Yes / No — list which attributes if Yes
5. **BRS source** — FR-NNN references from requirements.md

### Step 3 — Define attributes for each entity

For each ENT-NNN, define the key business-meaningful attributes:

| Attribute | Description | Data Type | Length/Precision | Validation Rules |
|---|---|---|---|---|

Use concrete validation phrases:
- `Primary Key`, `Not Null`, `Not Null, Unique`, `Optional`
- `Not Null, Min: X, Max: Y`, `Not Null, Values: A, B, C`, `Not Null, Format: Email`

Reference BR-NNN rules from `business-rules.md` where available. Do not invent constraints not in the requirements or business rules.

Do not include database implementation details: no foreign key names, no index definitions, no physical storage choices.

### Step 4 — Map relationships

For each pair of entities that interact:
1. Relationship name (verb phrase: "belongs to", "contains", "initiates")
2. Cardinality: 1:1, 1:N, M:N
3. Optionality: required / optional
4. BR-NNN rule governing the relationship (if any)

### Step 5 — Write the ER diagram

Generate one Mermaid `erDiagram` block showing all entities and their relationships.

Rules:
- Show entity names and relationships only — do not list attributes in the diagram
- Entity names: PascalCase, no spaces, no hyphens
- Relationship lines: `||--o{` (one-to-many), `||--||` (one-to-one), `}o--o{` (many-to-many)
- Use valid Mermaid `erDiagram` syntax
- Show cardinality in every relationship

### Step 6 — Write the artifact

Use the artifact template at `.brs2spec2/artifact-templates/entity-model.md`. Preserve all headings. Set `Status: Draft`.

Include in the artifact:
- Metadata table
- Entity Catalog table (ENT-NNN, Name, Description, Owner, PII, BRS Source)
- One `### ENT-NNN: Name` section per entity with description and attribute table
- ER diagram in Mermaid erDiagram syntax
- Feature Coverage table mapping ENT-NNN to FR-NNN sources

## Output requirements

The artifact must contain:
- Metadata table with Status: Draft, Initiative ID, and creation date
- ENT-NNN catalog table
- Full entity section per ENT-NNN with attribute table (5 columns exactly)
- One Mermaid erDiagram covering all entities and relationships
- Feature Coverage table
- No database implementation details anywhere

## Done criteria

- [ ] Every persistent business object implied by requirements.md has an ENT-NNN entry
- [ ] Every ENT-NNN has Owner, PII flag, and at least one FR-NNN source
- [ ] Every ENT-NNN has an attribute table with 5 columns
- [ ] Relationships have cardinality and optionality defined
- [ ] Data integrity constraints reference BR-NNN rules where available
- [ ] Mermaid erDiagram is syntactically valid and covers all entities
- [ ] Mermaid erDiagram contains entities and relationships only — no inline attribute blocks
- [ ] No database implementation details (no FK names, no indexes)
- [ ] `Status: Draft` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `business-analysis/entity-model.md`

## Stop conditions

- If `requirements.md` is missing, stop and report the blocker.
- If the initiative has no persistent entities (pure event-driven or stateless), produce the artifact with an explanation instead of inventing entities.
- If requirements are too vague to determine entities cleanly, record the ambiguity and reflect it in `gaps-and-questions.md`.
- Do not invent entities not derivable from requirements.md.
- Do not introduce database implementation details.
