# Enhancement 8.1 — Structured Impacted Components Table, System Context Diagram, and Diagram References

## Problem

Three related gaps in `01-review-initial-architecture.md` and its template:

1. **No structured Impacted Components table.** The skill produces an ad-hoc "Impacted
   components" table with only `Component | Impact` columns. Downstream stages (API
   contract, readiness, handoff) cannot parse it to determine service types, HTTP
   exposure, or event publishing without reading prose.

2. **No system context diagram.** `component.mmd` mixes internal services, external
   systems, and data stores at the same level. There is no outermost C4 view showing
   the system boundary, human actors, and external dependencies as distinct from internal
   containers. Also, calling it `component.mmd` is incorrect — it shows the C4 container
   level (deployable units), not the C4 component level (internal modules within a
   container).

3. **Diagrams not referenced in `architecture-review.md`.** The MMD files are generated
   into `architecture/diagrams/` but the review document has no structured pointer to
   them. The "Optional visual view" section in the template is an empty comment. A reader
   of the review cannot find the diagrams from the document itself.

---

## What needs to change

### Change 1 — Add `## Impacted Components` section to the architecture-review template

**Location:** `.brs2spec/templates/planning-and-modular-delivery/architecture-review.md`

**Add a new section after `## Existing system impact` and before `## Integration review`:**

```markdown
## Impacted Components

> Every service, data store, queue, frontend, and gateway that this initiative builds,
> modifies, or depends on. Derived from `input/architecture.md` — do not add rows for
> components not present in the input unless explicitly decided in an open decision.
> This table is read by the API contract gate and engineering readiness to scope their outputs.

| Component | Type | Technology | Exposes HTTP API? | Publishes Events? | Owner repo |
|---|---|---|---|---|---|
```

**Type values (use exactly these):**

| Value | Meaning |
|---|---|
| `Service` | A deployable backend service that may expose HTTP endpoints |
| `Database` | A relational or document data store |
| `Queue` | A message bus, event bus, or async queue |
| `Frontend` | A web or mobile UI — consumes APIs, does not expose them |
| `Gateway` | An API gateway or ingress proxy |
| `External` | A third-party system this initiative calls (not built by this team) |

**Column rules:**
- `Exposes HTTP API?` — Yes / No / Partial (gateway handles HTTP but delegates internally)
- `Publishes Events?` — Yes / No (publishes to Queue)
- `Owner repo` — the `input/repositories/` descriptor file name without `.md`, if known; leave blank if not yet determined

---

### Change 2 — Add Impacted Components population rule to the architecture review skill

**Location:** `.brs2spec/skills/3-planning-and-modular-delivery/01-review-initial-architecture.md`

**Add a new section after the Template section, before the Mermaid syntax rules:**

```markdown
## Impacted Components table — population rule

When writing `architecture/architecture-review.md`, populate the `## Impacted Components`
table as follows:

1. Read the **System Components table** in `input/architecture.md`. For each row, create
   one row in the Impacted Components table. Assign Type using the vocabulary above.
   Assign `Exposes HTTP API?` based on the technology column (ASP.NET Core, FastAPI,
   Express, App Service, Container Apps = Yes; Cosmos DB, Azure SQL, Service Bus,
   Static Web Apps = No).

2. Read the **Integration Points table** in `input/architecture.md`. For each external
   system row, add one row with Type = `External`. These are outbound dependencies, not
   services this team builds.

3. **Do not add rows for components not in `input/architecture.md`.** If a BRS functional
   requirement implies a component that is absent from the architecture input, raise an
   open decision — do not silently add the component to the table.

4. **Do not remove or rename rows from `input/architecture.md`.** The architect's naming
   is preserved verbatim. If the name is ambiguous, add a clarifying note in the
   Technology column only.

5. If `input/architecture.md` has no System Components table, note this explicitly in
   the Impacted Components section and leave the table with a single stub row:
   `| _(derive from architecture narrative)_ | — | — | — | — | — |`
```

---

### Change 3 — Add `system-context.mmd` as a third required diagram

**Location:** `.brs2spec/skills/3-planning-and-modular-delivery/01-review-initial-architecture.md`,
Diagram output section.

**Add before File 1:**

```markdown
### File 0 — `architecture/diagrams/system-context.mmd` (C4 level 1 — system context)

The outermost view. Shows the system as a single black-box node, the human actors who
interact with it, and the external systems it depends on. No internal services, no
databases, no queues.

**Content — derive strictly from `architecture-review.md` Impacted Components table and
`business-analysis/actors-and-personas.md`:**

- One node for the system being built (label from initiative name in `input/brs.md`)
- Human actor nodes: one per ACT-NNN from `business-analysis/actors-and-personas.md`.
  If that file does not exist yet, derive actor types from the BRS roles section.
- External system nodes: one per row in Impacted Components where Type = `External`
- Arrows: actor→system for human interactions; system→external for outbound calls.
  Label each arrow with one short phrase (e.g. `submits application`, `credit report`).

**Do not include** internal services, databases, queues, or Azure infrastructure.
**Do not invent** actors or external systems not present in the inputs.

Use `graph LR` layout.
```

---

### Change 4 — Rename `component.mmd` to `containers.mmd` with backward compatibility

**Location:** `.brs2spec/skills/3-planning-and-modular-delivery/01-review-initial-architecture.md`,
Diagram output section, File 1 block.

**Replace the File 1 heading and description:**

**Current:**
```
### File 1 — `architecture/diagrams/component.mmd`

A component-level view showing:
- Major services / applications / adapters
- Data stores (databases, queues, blob, audit store)
- External integrations (third-party systems)
- Key data flows between them

Use `graph TD` layout.
```

**Replace with:**
```
### File 1 — `architecture/diagrams/containers.mmd` (C4 level 2 — container view)

Shows all deployable units and their connections. Derives strictly from the Impacted
Components table in `architecture-review.md`.

- Internal rows (Type = Service, Database, Queue, Frontend, Gateway): one node each,
  grouped by subgraph if there are logical clusters (e.g. UI / Services / Data)
- External rows (Type = External): shown as boundary nodes in a separate `Integrations`
  subgraph — they appear here because containers call them, but they are visually
  distinct from the internal containers
- Arrows: show key data flows between nodes; label with one short phrase

Do NOT call this a "component diagram" — C4 component view (level 3) shows internal
modules within a single container and is only produced when `input/architecture.md`
explicitly describes the internal structure of a specific container.

Use `graph TD` layout.

**Backward compatibility:** if `architecture/diagrams/component.mmd` already exists
in the workspace:
- Do not delete it.
- Generate `containers.mmd` as the new canonical file.
- Add this line at the top of the existing `component.mmd`:
  `<!-- Superseded by containers.mmd (C4 container view). Preserved for reference only. -->`
```

---

### Change 5 — Replace "Optional visual view" with structured `## Architecture diagrams` section in the template

**Location:** `.brs2spec/templates/planning-and-modular-delivery/architecture-review.md`

**Replace:**
```markdown
## Optional visual view

<!-- Add only when a compact context, container, or integration-flow view makes constraints clearer than text. -->
<!-- Prefer one embedded Mermaid diagram. Reference an existing diagram instead of duplicating. -->
<!-- Delete this section if not needed. -->
```

**With:**
```markdown
## Architecture diagrams

> Generated by the architecture review skill into `architecture/diagrams/`. Do not embed
> diagram content here — reference the files. Re-run
> `.brs2spec/tools/prompts/generate-architecture-diagrams.md` to refresh them.

| Diagram | File | C4 level | What it shows |
|---|---|---|---|
| System context | `architecture/diagrams/system-context.mmd` | Level 1 | Human actors, the system boundary, external dependencies |
| Containers | `architecture/diagrams/containers.mmd` | Level 2 | Internal services, data stores, queues and their connections |
| Deployment | `architecture/diagrams/deployment.mmd` | Infrastructure | Azure topology, hosting, networking |
```

**Also update the skill** to populate this table after generating the diagrams, rather than printing a freeform message to the user.

---

### Change 6 — Update diagram notification and self-review checklist

**Location:** `.brs2spec/skills/3-planning-and-modular-delivery/01-review-initial-architecture.md`

**Replace current notification:**
```
After writing both files, tell the user: "Diagrams saved to `architecture/diagrams/component.mmd` and `architecture/diagrams/deployment.mmd`..."
```

**With:**
```
After writing all diagram files and populating the `## Architecture diagrams` table in
`architecture-review.md`, tell the user:

"Architecture diagrams saved and referenced in `architecture/architecture-review.md`:
- `architecture/diagrams/system-context.mmd` — C4 level 1: actors, system boundary, external dependencies
- `architecture/diagrams/containers.mmd` — C4 level 2: internal services, stores, queues
- `architecture/diagrams/deployment.mmd` — Infrastructure: Azure topology

Re-run `.brs2spec/tools/prompts/generate-architecture-diagrams.md` at any time to refresh them."
```

**Replace the last two self-review checklist items:**

Current:
```
- [ ] `architecture/diagrams/component.mmd` and `architecture/diagrams/deployment.mmd` have been generated or skipped with a stated reason.
```

Replace with:
```
- [ ] Impacted Components table populated from `input/architecture.md` — one row per component/integration; no invented rows; Type and Exposes HTTP columns filled.
- [ ] `architecture/diagrams/system-context.mmd` generated — contains only human actors, the system node, and external systems (Type=External). No internal services.
- [ ] `architecture/diagrams/containers.mmd` generated — contains internal components (Type=Service/Database/Queue/Frontend/Gateway) and external boundary nodes. Derives from Impacted Components table.
- [ ] `architecture/diagrams/deployment.mmd` generated — Azure infrastructure topology.
- [ ] `## Architecture diagrams` table in `architecture-review.md` references all three diagram files.
- [ ] If `architecture/diagrams/component.mmd` already existed: superseded notice added; `containers.mmd` generated alongside it.
```

---

## Implementation steps

1. Open `.brs2spec/templates/planning-and-modular-delivery/architecture-review.md`.
   - Add the `## Impacted Components` table after `## Existing system impact` (Change 1).
   - Replace `## Optional visual view` with `## Architecture diagrams` reference table (Change 5).

2. Open `.brs2spec/skills/3-planning-and-modular-delivery/01-review-initial-architecture.md`.
   - Add the Impacted Components population rule after the Template section (Change 2).
   - In the Diagram output section: insert File 0 (`system-context.mmd`) before File 1 (Change 3).
   - Replace File 1 heading and description to use `containers.mmd` with backward-compat note (Change 4).
   - Replace diagram notification message (Change 6).
   - Update self-review checklist (Change 6).

---

## Quality bar

After these changes, running the architecture review skill on I005 produces:

- `architecture-review.md` has an Impacted Components table with 10 rows (8 internal
  components + 2 frontend UIs) and 5 external system rows — Type and Exposes HTTP columns
  filled for each
- `architecture-review.md` has a `## Architecture diagrams` section referencing all three
  MMD files by path and C4 level
- `system-context.mmd`: system node + 3 actor nodes (Applicant, Underwriter, Admin) +
  5 external system nodes (Experian, HMRC, HM Treasury, DocuSign, T24). No internal
  services appear.
- `containers.mmd`: 10 container nodes grouped into UI / Services / Data subgraphs +
  Integrations boundary subgraph. Replaces `component.mmd`.
- `deployment.mmd`: unchanged from current correct output.
- No component invented that was not in `input/architecture.md`.
