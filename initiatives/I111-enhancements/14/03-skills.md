# Prompt 03 — Skills for Technical Specifications

## Context

You are working on the `.b2s` framework at the root of this repository.

Artifact templates for technical specifications were created in prompt 02.
This prompt creates four skill files — one per specification type.
Skills are the executable instructions the AI follows to produce each artifact.

Before writing any skill, read these files in full:
- `.b2s/skills/engineering-lead/create-api-contract.md` — existing API contract skill (style reference)
- `.b2s/skills/delivery-lead/create-delivery-structure.md` — style reference
- `.b2s/workflow/stage-actions.yaml` — to understand how skills are referenced
- `initiatives/I013-NEXT13/architecture/architecture-review.md` — real example of the primary input

---

## Skill 1 — Create Exposed API Specifications

Create `.b2s/skills/engineering-lead/create-exposed-api-specs.md`:

The skill must:

1. Read `architecture/architecture-review.md` — extract the "Feature Area" table rows to identify which API surfaces exist in this initiative
2. Read `planning/delivery-structure.md` — map each API surface to the stories that implement it
3. Read `engineering-readiness/readiness-check.md` — read `api_contract_mode` (product / internal / coordinated); if mode is `internal`, note that this spec will be refined after story packages and generate a minimal draft only
4. Read `input/brs.md` — extract any explicit API requirements or external consumer mentions
5. Read `architecture/architecture-rules.md` — extract constraints that apply to API design (auth, TLS, versioning)
6. For each distinct API surface identified: generate one file at `technical-specifications/api/exposed/{{api-slug}}.md` using `.b2s/artifact-templates/exposed-api-spec.md` as the output shape
7. Populate every section — do not leave placeholder text. If a field cannot be determined from inputs, write an explicit open question in the Open Questions section
8. Endpoint paths must use the versioned format (`/v1/...`) unless the architecture rules specify otherwise
9. Every endpoint must have a `Story ref` linking to the story that implements it
10. SLA values must come from the BRS or architecture constraints — do not invent numbers; use open questions if unknown

**Quality rules:**
- At least one endpoint per story that has an API surface
- Auth mechanism must match the architecture rules (not generic "OAuth2")
- Contract mode must be explicitly stated and must match the value from readiness-check.md
- No `{{placeholder}}` text in the final output

**Output:** one file per API surface at `technical-specifications/api/exposed/`

---

## Skill 2 — Create Consumed API Specifications

Create `.b2s/skills/engineering-lead/create-consumed-api-specs.md`:

The skill must:

1. Read `architecture/architecture-review.md` — find the "Existing Components Touched" and "New Components / Boundaries" columns; identify all external systems listed (e.g. Experian, HMRC, DocuSign, Temenos T24)
2. Read `planning/delivery-structure.md` — identify which stories reference each external system
3. Read `input/brs.md` — extract any explicit external system requirements, SLAs, or constraints
4. Read `architecture/architecture-rules.md` — extract constraints on external integrations (ARCH-C-003, ARCH-C-005, etc.)
5. For each external system that this initiative CONSUMES: generate one file at `technical-specifications/api/consumed/{{system-slug}}.md` using `.b2s/artifact-templates/consumed-api-spec.md`
6. If the provider's actual API spec URL or document reference is unknown: record it as an open question — do not invent endpoint paths
7. PII fields must be identified for every external system that receives applicant data
8. Fallback behaviour must be explicitly specified for every external system — "unknown" is not acceptable; use the architecture constraints or flag as an open question

**Quality rules:**
- Every external system in the architecture review must have a corresponding consumed-api-spec or an explicit note that it is not consumed (only exposed to)
- PII section must list which fields are transmitted — not "see BRS"
- Fallback behaviour must be one of: refer-to-underwriter / degrade gracefully / hard fail / circuit breaker

**Output:** one file per consumed external system at `technical-specifications/api/consumed/`

---

## Skill 3 — Create Database Schema Specifications

Create `.b2s/skills/engineering-lead/create-database-schema-specs.md`:

The skill must:

1. Read `planning/delivery-structure.md` — identify which stories create or modify data
2. Read `business-analysis/requirements.md` — extract data requirements (FR-NNN related to storage, retention, PII)
3. Read `architecture/architecture-review.md` — identify data layer components and any shared database concerns
4. Read `architecture/architecture-rules.md` — extract data residency and PII constraints (ARCH-C-001, etc.)
5. Read `business-analysis/business-rules.md` if present — extract rules that translate to database constraints (CHECK constraints, NOT NULL, unique)
6. Group data by domain (e.g. Applications, Decisions, Audit, Users) — one file per domain
7. For each domain: generate one file at `technical-specifications/database/{{domain-slug}}-schema.md` using `.b2s/artifact-templates/database-schema-spec.md`
8. Every table must have at minimum: id (uuid PK), created_at, updated_at columns
9. Status enumerations must list ALL valid values — no "etc." or "..."
10. PII columns must be identified explicitly; retention period must come from the BRS or be flagged as an open question

**Quality rules:**
- No table without a primary key
- Every story that persists data must map to at least one table in the schema
- Shared schemas (used by multiple teams) must be explicitly flagged with coordination notes
- Migration strategy must be stated — not left as placeholder

**Output:** one file per data domain at `technical-specifications/database/`

---

## Skill 4 — Create Integration Specifications

Create `.b2s/skills/engineering-lead/create-integration-specs.md`:

The skill must:

1. Read `architecture/architecture-review.md` — extract all external systems and their blast radius
2. Read `architecture/architecture-rules.md` — extract integration SLA constraints (ARCH-C-005 etc.) and enterprise contract references (ARCH-C-003)
3. Read `planning/delivery-structure.md` — identify which stories depend on each external system
4. Read `input/brs.md` — extract any explicit integration requirements (retry policy, timeout, fallback)
5. For each external system (consumed or bidirectional): generate one file at `technical-specifications/integrations/{{system-slug}}-integration.md` using `.b2s/artifact-templates/integration-spec.md`
6. Timeout and retry values must come from architecture constraints or BRS — if not specified, flag as open question with a recommended default (5s timeout, 3 retries exponential)
7. Fallback behaviour must be determined for every integration — never leave as placeholder
8. Observability: every integration must have a named success event and failure event that will be emitted to the audit store
9. If an enterprise contract exists (ARCH-C-003 type constraint): set `Enterprise contract: yes` and reference the constraint ID

**Quality rules:**
- Every external system in the architecture review must have an integration spec
- No placeholder timeout or retry values — use constraints or open questions
- Fallback behaviour must be actionable (not "TBD")
- Compliance notes must reference architecture constraints explicitly

**Output:** one file per external system at `technical-specifications/integrations/`

---

## Done criteria

- [ ] `.b2s/skills/engineering-lead/create-exposed-api-specs.md` created
- [ ] `.b2s/skills/engineering-lead/create-consumed-api-specs.md` created
- [ ] `.b2s/skills/engineering-lead/create-database-schema-specs.md` created
- [ ] `.b2s/skills/engineering-lead/create-integration-specs.md` created
- [ ] Each skill references the correct artifact template from prompt 02
- [ ] Each skill has explicit quality rules that prevent placeholder output
- [ ] All existing tests pass
