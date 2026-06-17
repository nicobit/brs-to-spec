# Enhancement 8 — C4 Architecture Views and Multi-Service API Contract

## Context

The `01-review-initial-architecture.md` skill already generates two Mermaid diagrams
(`architecture/diagrams/component.mmd` and `architecture/diagrams/deployment.mmd`)
derived strictly from `input/architecture.md`. The "do not invent components" rule is
already in place and working correctly.

The `create-api-contract.md` skill already reads `input/architecture.md` and
`architecture/architecture-review.md` as inputs. It has an Endpoints table and an
actor-endpoint traceability rule.

## What is actually wrong

### Problem 1 — No system context view; container diagram misnamed

`component.mmd` mixes internal services, data stores, and external third-party systems
in the same diagram at the same level. There is no outermost C4 view (system context)
showing the system as a black box with the human actors who use it and the external
systems it depends on.

Also, what `component.mmd` actually shows is the C4 **container** level (deployable
units). Calling it "component" is incorrect — C4 component view (level 3) shows internal
modules within a single container. This naming confusion persists downstream when
engineers try to understand what the diagram represents.

### Problem 2 — Impacted Components table in architecture-review.md has no Type column

The architecture review skill produces an "Impacted components" table. The I005 run
produced:

| Component | Impact |
|---|---|
| Loan Origination API | Central orchestrator... |
| AI Scoring Service | Must expose explainability... |

Two columns only. No Type (Service / Database / Queue / Frontend / External). No "Exposes
HTTP API?" flag. The API contract skill cannot parse this table to know how many services
to cover — it has to guess from prose.

### Problem 3 — API contract produces one flat endpoint list

`create-api-contract.md` collapses all endpoints into one flat table, ignoring service
boundaries. For I005 this produced 4 paths covering only the Loan Origination API;
AI Scoring Service, Compliance Service, and Payment Gateway Adapter were not covered.

The skill reads `architecture/architecture-review.md` as an input but has no rule to
read the Impacted Components table and segment endpoints by service.

### Problem 4 — Diagrams not referenced in architecture-review.md

The MMD files are generated into `architecture/diagrams/` but `architecture-review.md`
does not reference them. A reader of the review has no pointer to the visual aids.
The template's "Optional visual view" section is just a comment placeholder — no
structured reference to the generated files.

## Design principle

`architecture/architecture-review.md` is the authoritative normalized artifact.
`input/architecture.md` is the raw human input. Downstream stages (API contract,
readiness, handoff) must read from `architecture-review.md`, not from the raw input.
The architect who writes or refines `architecture-review.md` is responsible for ensuring
all relevant containers, services, and integration points are captured there.

MMD diagrams are visual renderings of what is already described in text in
`architecture-review.md`. They are not a separate data source.

## Fixes

### Fix 1 — Add Impacted Components structured table to template and skill

**Template:** `.brs2spec/templates/planning-and-modular-delivery/architecture-review.md`

Add a new `## Impacted Components` section with columns:
`Component | Type | Technology | Exposes HTTP API? | Publishes Events? | Owner repo (if known)`

Type values: `Service` / `Database` / `Queue` / `Frontend` / `Gateway` / `External`

**Skill:** `01-review-initial-architecture.md`

Add a rule: populate the Impacted Components table from `input/architecture.md` System
Components table. Do not invent rows. If a BRS requirement implies a component not
in `input/architecture.md`, add it as an open decision — not a table row.

### Fix 2 — Add system context diagram; rename container diagram; add diagram references

**Skill:** `01-review-initial-architecture.md`

- Add `architecture/diagrams/system-context.mmd` (C4 level 1): system node, human
  actors from `actors-and-personas.md`, external systems from Integration Points table
  in `input/architecture.md`. No internal services.
- Rename diagram guidance from `component.mmd` to `containers.mmd` (C4 level 2).
  Backward-compat: if `component.mmd` exists, add superseded notice, generate
  `containers.mmd` alongside.
- Replace "Optional visual view" comment in `architecture-review.md` with a structured
  `## Architecture diagrams` section that references all three generated MMD files.

### Fix 3 — API contract reads Impacted Components table from architecture-review.md

**Skill:** `create-api-contract.md`

Add a pre-generation step: read `architecture/architecture-review.md` Impacted
Components table. Filter rows where `Type = Service` and `Exposes HTTP API? = Yes`.
Produce one `### <Component Name>` endpoint subsection per matching row.

Outbound calls to external systems (Type = External) go in a separate
`## Outbound Integrations` section, not in the Endpoints table.

Fallback: if no Impacted Components table exists in `architecture-review.md`, derive
from BRS prose and note the fallback.

## Files to change

1. `framework_enhancement/8/01-add-system-context-diagram.md`
   → changes to `01-review-initial-architecture.md` and architecture-review template
2. `framework_enhancement/8/02-fix-api-contract-service-segmentation.md`
   → changes to `create-api-contract.md`

## Quality bar

After these changes, running the full workflow on an initiative like I005:

- `architecture-review.md` has an Impacted Components table with Type and Exposes HTTP
  columns — readable by any downstream skill without prose parsing
- Three diagrams exist: `system-context.mmd`, `containers.mmd`, `deployment.mmd` —
  all referenced by name in a `## Architecture diagrams` section of `architecture-review.md`
- API contract produces four endpoint subsections (Loan Origination API, AI Scoring
  Service, Compliance Service, Payment Gateway Adapter) because those are the four rows
  in the Impacted Components table where Type=Service and Exposes HTTP=Yes
- No downstream stage reads `input/architecture.md` to identify services — they read
  `architecture/architecture-review.md`
