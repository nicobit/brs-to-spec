# Skill - Analyze Technical Landscape

## Identity

```text
skill_id:    architect.analyze-technical-landscape
persona:     architect
action_id:   analyze-technical-landscape
produces:    architecture/technical-landscape.md
```

## When this skill is used

Run after architecture rules are created. This skill produces a structured inventory of all existing and proposed technical components (repositories, services, APIs, data stores, pipelines) that the initiative will touch. Downstream actions use this inventory to map requirements to concrete systems.

## Role for this task

You are a senior architect producing a comprehensive technical landscape inventory. Your output must be precise enough that a delivery lead can determine exactly where each change will be implemented.

## Preconditions

Before starting, verify that all files listed in `{resolved_required_inputs}` exist and are readable.

If `input/repository-context.md` exists, treat it as the authoritative source for existing repository details. If `input/architecture.md` exists, use it as the authoritative source for system components and integration points.

If neither optional input exists, derive the landscape entirely from the architecture review — but flag this as "derived, not verified" in the artifact.

## Hard constraints

- Do not invent repositories or services not mentioned in any input document
- **Do NOT invent repository names or repository structure** when `input/repository-context.md` is absent. If the inputs do not specify how components map to repositories, set the repository field to `needs-clarification` for every component. Do not assume one-repo-per-service or any other structure — repository layout is a decision that belongs to the user or to `input/repository-context.md`
- Every component in the architecture review's system components table must appear in the landscape
- If a component's technology or responsibility is unclear, mark it as `needs-clarification` — do not guess
- Do not create epics, features, or stories
- Do not make implementation decisions (that is the next action's job)
- If the initiative uses a single repository (monorepo), still list it with all its component types (api, ui, db, worker, etc.) — downstream actions need to know what layers exist within the repo
- Every repository entry must include its component type (api / ui / service / worker / library / monorepo) and technology stack — these are consumed by story generation to produce actionable technical scope

## Instructions

### Step 1 — Read all inputs

Read every file listed in `{resolved_required_inputs}` in full before writing anything.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
If `{resolved_policy_inputs}` is non-empty, read every policy file in full.
Do not start writing until all inputs are read completely.

### Step 2 — Identify all system components

From the architecture review and input documents, identify every:
- Repository (existing or proposed)
- Service / microservice
- API (exposed and consumed)
- Data store (database, cache, queue, blob store)
- Integration point (external APIs)
- CI/CD pipeline or deployment target

### Step 3 — Classify each component

For each component, determine:
- **Status**: `existing` (already built and deployed) or `proposed` (new in this initiative)
- **Type**: `api`, `ui`, `service`, `database`, `queue`, `storage`, `integration`, `pipeline`
- **Technology**: tech stack (e.g., `.NET 8`, `React/Next.js`, `Azure SQL`)
- **Responsibilities**: what business capabilities it owns
- **Deployment target**: where it runs (e.g., `Azure App Service`, `Container Apps`)

**Repository mapping rules:**
- If `input/repository-context.md` exists, use the exact repository names and structure from that file
- If `input/repository-context.md` does NOT exist, set all repository fields to `needs-clarification` — do not invent repo names or assume a structure
- If the user explicitly states a single repository (monorepo) in any input, list it once as type `monorepo` and then list each logical component within it as a separate service entry referencing the same repository name. Example: a monorepo `loan-platform` might contain services `loan-api` (api, .NET 8), `loan-ui` (ui, React), and migrations `loan-db` (database, Azure SQL) — all pointing to the same repository

### Step 4 — Write the artifact

Write `architecture/technical-landscape.md` using the artifact template at `.b2s/artifact-templates/technical-landscape.md`.

## Output requirements

Write `architecture/technical-landscape.md` following the artifact template structure exactly.

## Done criteria

- [ ] Every component from the architecture review appears in the inventory
- [ ] Each component has status, type, technology, responsibilities, and deployment target
- [ ] Integration points list protocol, direction, and contract status
- [ ] No components invented beyond what input documents describe
- [ ] If landscape is derived (no `input/repository-context.md`), this is flagged

## Stop conditions

- A required input file is missing → stop, report the blocker
- The architecture review does not list system components → stop, report

## Notes for the staged engine

- Do not emit event completion messages
- Do not manage state files
- Do not advance the workflow
