# Prompt - Review Initial Architecture

## Role

You are a solution architect reviewing whether the initial architecture supports the BRS.

## Context

This prompt is the initiative-specific architecture review step. It uses the early delivery shape plus the initial architecture input to refine concrete constraints, conflicts, and risks.

## Purpose

Review architecture constraints, conflicts, missing decisions, brownfield impact, and delivery impact against the initiative's current delivery shape.

## Inputs

Use these inputs when available:

- `input/brs.md or input/brs/*.md`
- `input/architecture.md or input/architecture/*.md`
- `business-intake/business-intake-summary.md`
- `planning/delivery-structure.md`
- `architecture/existing-system-impact.md` when brownfield impact is material

## Output path

```text
architecture/architecture-review.md
```

## Template

Use:

```text
.brs2spec/templates/planning-and-modular-delivery/architecture-review.md
```

Preserve the template headings. Expand the tables only where the available evidence requires more detail.
Prefer sharp decisions and evidence over broad explanatory prose.
Treat the initial architecture input as high-level solution context unless the evidence already makes initiative-specific decisions explicit.
Use it to understand systems, containers, integrations, boundaries, and major constraints before refining what matters for this initiative specifically.
Add an optional compact context, container, or integration-flow view only when it materially improves understanding of boundaries, constraints, or impacted areas.
Do not add a visual that merely restates simple tables or already-clear text.

## Impacted Components table — population rule

When writing `architecture/architecture-review.md`, populate the `## Impacted Components` table as follows:

1. Read the **System Components table** in `input/architecture.md`. For each row, create one row in the Impacted Components table. Assign `Type` using these values:
   - `Service` — deployable backend service that may expose HTTP (ASP.NET Core, FastAPI, Express, App Service, Container Apps, Functions with HTTP trigger)
   - `Database` — relational or document data store (Azure SQL, Cosmos DB, PostgreSQL, etc.)
   - `Queue` — message bus or async event infrastructure (Azure Service Bus, Event Hub, RabbitMQ, etc.)
   - `Frontend` — web or mobile UI that consumes APIs but does not expose them (React, Next.js, Static Web Apps)
   - `Gateway` — API gateway or ingress proxy (Azure APIM, nginx, etc.)
   - `External` — third-party system this initiative calls but does not own
2. Assign `Exposes HTTP API?` from the technology/role column: `Yes` for Service types with REST/HTTP technology; `No` for Database, Queue, Frontend; `Partial` for Gateway (handles HTTP but delegates internally).
3. Assign `Publishes Events?`: `Yes` if the component publishes to a Queue; `No` otherwise.
4. Read the **Integration Points table** in `input/architecture.md`. For each external system row, add one row with `Type = External`. These are outbound dependencies, not services this team builds.
5. **Do not add rows for components not in `input/architecture.md`.** If a BRS functional requirement implies a component absent from the architecture input, raise an open decision — do not add the component to the table.
6. **Do not remove or rename rows from `input/architecture.md`.** Preserve the architect's naming verbatim.
7. If `input/architecture.md` has no System Components table, leave the Impacted Components table with one stub row: `| _(derive from architecture narrative)_ | — | — | — | — | — |` and note the gap.

## Mermaid syntax rules

> Apply the canonical Mermaid syntax rules and self-review checklist from `.brs2spec/agent-instructions.md` → **Mermaid syntax rules — canonical source**. Do not duplicate them here.

## Context preservation rule

The architecture review is the first artifact where assumptions, rationale, and unknowns are explicit. These must be recorded so they survive the transition to readiness → handoff → implementation.

Populate the three new sections in the template:

- **Active assumptions** — any assumption the review depends on that could be invalidated. Examples: "Auth will use Azure AD", "Load is below X req/s", "No schema migration required". If you find phrases like "we assume", "assuming", "subject to", "pending confirmation of" — extract those as rows. Do not leave this section empty if such phrases appear anywhere in the review.
- **Rejected alternatives** — record only when the rejection is non-obvious or the alternative is likely to resurface (e.g. a rejected third-party vendor, a rejected deployment pattern). Skip when the rejection is self-evident.
- **Known unknowns** — things not yet determined that could affect delivery. Distinct from open decisions (which are pending choices). Examples: "Final SLA targets not confirmed", "Third-party API rate limits unknown". Scan for "TBD", "not yet determined", "unclear", "depends on" phrases in the inputs.

These sections flow into `initiative-context.md` → Carried-Forward Context when the initiative context is generated.

## Quality bar

A good output must:

- respect the initial architecture constraints
- keep business traceability visible
- evaluate the architecture against the initiative's planned epics, features, stories, and slices
- distinguish clearly between early solution context and later initiative-specific delivery implications
- identify initiative-specific impacted components, interface implications, contract implications, governed boundaries, rollout / rollback constraints, and validation implications when the evidence supports them
- surface affected components, contract impacts, and compatibility risks when the initiative changes an existing system
- mark conflicts instead of resolving them silently
- assign owners for gaps and decisions
- avoid creating low-level implementation tasks
- keep each section focused on decisions, conflicts, risks, and constraints that affect downstream delivery
- populate the Impacted Components table with one row per component from `input/architecture.md` — do not add rows for components not present in the input
- populate Active assumptions, Rejected alternatives, and Known unknowns — never leave them silently empty

## Anti-patterns to avoid

Do not produce outputs that:

- invent architecture not present in the inputs
- slice work only by technical layer
- create tasks for all future deliverables
- ignore brownfield contract, schema, or operational impact when evidence exists
- ignore architecture conflicts
- produce a table without evidence or owner
- treat the high-level architecture input as if it already fully resolves initiative-specific delivery questions

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Multi-repository signal

While reviewing `input/architecture.md`, check whether the initiative spans multiple repositories (e.g. separate repos for API, UI, database, background workers, or shared libraries owned by different teams).

If yes, surface this to the user at the end of the review output:

> **Multi-repo initiative detected.** The architecture describes components across multiple repositories. Before the handoff stage, create one descriptor file per repository in `input/repositories/` using `.brs2spec/templates/repositories/_template.md`. The file name (without `.md`) becomes the subfolder name inside each story's handoff folder. Doing this now — while the architecture boundaries are fresh — produces more accurate handoff scoping than deferring it to handoff time.
>
> Repositories identified from the architecture: {{list repo names or system components that map to separate repos}}

If the initiative is single-repo or the architecture does not distinguish repo boundaries, omit this notice entirely.

## Diagram output (mandatory when architecture has components or integrations)

After producing `architecture/architecture-review.md`, generate three Mermaid diagram files into `architecture/diagrams/`. Derive all content strictly from the **Impacted Components table in `architecture-review.md`** — do not re-read `input/architecture.md` for diagram generation; the review is the authoritative source.

Skip a diagram only if the initiative is so narrow that the diagram would be a single node with no connections — note the skip reason.

### File 0 — `architecture/diagrams/system-context.mmd` (C4 level 1 — system context)

The outermost view. Shows the system as a single black-box node, the human actors who interact with it, and the external systems it depends on. No internal services, databases, or queues appear here.

Content — derive from Impacted Components table and `business-analysis/actors-and-personas.md`:
- One node for the system being built (use the initiative name from `input/brs.md`)
- Human actor nodes: one per ACT-NNN from `business-analysis/actors-and-personas.md`. If that file does not exist yet, derive actor types from the BRS roles section.
- External system nodes: one per row in Impacted Components where `Type = External`
- Arrows: actor→system for human interactions; system→external for outbound calls. Label each arrow with one short phrase (e.g. `submits application`, `credit report`).
- **Do not include** internal services, databases, queues, or Azure infrastructure.
- **Do not invent** actors or external systems not present in the inputs.

Use `graph LR` layout.

### File 1 — `architecture/diagrams/containers.mmd` (C4 level 2 — container view)

Shows all deployable units and their connections. Derives from Impacted Components table rows where `Type` is Service, Database, Queue, Frontend, or Gateway.

- Internal rows: one node each, grouped by subgraph where logical (e.g. `UI`, `Services`, `Data`)
- External rows (Type = External): shown as boundary nodes in a separate `Integrations` subgraph — they appear here because containers call them, but visually distinct from internal containers
- Arrows: key data flows between nodes; label with one short phrase

**Do not call this a "component diagram"** — C4 component view (level 3) shows internal modules within a single container and is only produced when `input/architecture.md` explicitly describes internal structure for a specific container.

Use `graph TD` layout. Follow Mermaid syntax rules — quote any label with `()`, `/`, or `,`.

**Backward compatibility:** if `architecture/diagrams/component.mmd` already exists:
- Do not delete it.
- Generate `containers.mmd` as the new canonical file.
- Add this line at the top of `component.mmd`: `<!-- Superseded by containers.mmd (C4 container view). Preserved for reference only. -->`

### File 2 — `architecture/diagrams/deployment.mmd` (infrastructure topology)

A deployment topology view showing:
- Infrastructure components (hosting platform, gateway, CDN, key vault, monitoring)
- How services map to infrastructure
- Environment-level groupings if relevant

Use `graph LR` layout. Follow the Mermaid syntax rules above.

### Rules for all diagrams

- Derive content strictly from the Impacted Components table in `architecture-review.md` — do not invent nodes.
- Keep node labels short (3–5 words max). Use subgraphs to group related components.
- Do not duplicate review text in diagrams — diagrams show structure, text shows decisions.
- After writing all diagram files, populate the `## Architecture diagrams` table in `architecture-review.md` with the three file paths and C4 levels (the template already has this table).
- Then tell the user: "Architecture diagrams saved and referenced in `architecture/architecture-review.md`: system-context.mmd (C4 L1), containers.mmd (C4 L2), deployment.mmd (infrastructure). Re-run `.brs2spec/tools/prompts/generate-architecture-diagrams.md` at any time to refresh them independently."

## Self-review checklist

Before finalizing, verify:

- [ ] Architecture constraints are referenced.
- [ ] Business requirements remain traceable.
- [ ] The review clearly references the initiative delivery shape it assessed.
- [ ] The output makes clear what came from high-level architecture context versus initiative-specific refinement.
- [ ] The output is specific enough to shape readiness, contracts, and handoff.
- [ ] Brownfield impact is summarized when relevant.
- [ ] Open decisions include owners.
- [ ] Risks and gaps are visible.
- [ ] Active assumptions section is populated or explicitly noted as none found.
- [ ] Known unknowns section is populated or explicitly noted as none found.
- [ ] Mermaid self-review checklist from `agent-instructions.md` applied to every diagram.
- [ ] The output supports architecture rule creation and delivery planning.
- [ ] If the initiative spans multiple repositories, the multi-repo signal notice was included in the output.
- [ ] Impacted Components table populated — one row per component from `input/architecture.md`; Type and Exposes HTTP API? columns filled; no invented rows; External systems included from Integration Points table.
- [ ] `architecture/diagrams/system-context.mmd` generated — contains only human actor nodes, the system node, and External rows from Impacted Components. No internal services or infrastructure.
- [ ] `architecture/diagrams/containers.mmd` generated — contains internal component rows (Service/Database/Queue/Frontend/Gateway) and External boundary nodes. Derives from Impacted Components table.
- [ ] `architecture/diagrams/deployment.mmd` generated — Azure infrastructure topology.
- [ ] `## Architecture diagrams` table in `architecture-review.md` references all three diagram files by path and C4 level.
- [ ] If `architecture/diagrams/component.mmd` already existed: superseded notice added at top; `containers.mmd` generated alongside it.
