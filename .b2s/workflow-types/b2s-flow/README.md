# Workflow Type: b2s-flow

## When to use

Controlled progressive decomposition for **BRS + architecture + existing systems** initiatives.
Forces explicit technical reasoning before backlog generation.

Use this workflow when:

- The initiative has a BRS and an architecture document (or needs one derived)
- The team needs to know where changes go before writing stories
- The initiative touches multiple repositories or services
- New infrastructure, APIs, or schemas are likely needed
- Stories must be grounded in concrete technical decisions, not just business requirements
- Frontend portals, dashboards, or admin UIs are in scope
- You want explicit human gates on architecture, solution decisions, and delivery plan

## Required inputs

- `input/brs.md` - the business requirements specification
- `input/architecture.md` - the architecture document (recommended; if absent, the workflow derives provisional architecture and marks solution decisions as draft/needs-review)

## Optional inputs

- `input/repository-context.md` - existing repository structure
- `input/brs/*.md` - additional BRS sections

## When not to use

- Simple or internal initiatives with a single codebase - use `fast-path`
- Initiatives where architecture is already fully documented and decisions are obvious - use `agile-delivery-light-flow`
- Full domain analysis with capability mapping and ADRs is needed - use `agile-delivery-flow`

## Stages

```text
Phase A - initiative planning
0-governance
  -> 1-requirements-and-architecture [HUMAN GATE]

Phase B - solution design (NEW)
    -> 2-solution-design [HUMAN GATE]

Phase C - delivery planning
      -> 3-delivery-planning [HUMAN GATE]

Phase D - epic elaboration
        -> 4-epic-elaboration [HUMAN GATE]

Phase E - coding handoff
        -> 5-coding-handoff

Phase F - readiness review
          -> 6-readiness-review
```

### Stage 0 - Governance

Creates the delivery constitution.

### Stage 1 - Requirements and architecture

Extracts atomic requirements, reviews architecture, creates architecture
rules - all in a single gated stage.

**Human gate:** Architecture must be reviewed before solution design.

### Stage 2 - Solution design

Produces up to four artifacts in sequence:

1. **Technical Landscape** - structured inventory of existing repositories,
   services, APIs, data stores, and pipelines
2. **Impacted Systems** - per-requirement mapping showing which existing
   systems are impacted and what new components are needed
3. **UI Specification** (conditional - only when the technical landscape identifies frontend applications) -
   page-first specs with fields, validation, states, data binding, and user flows
4. **Solution Decisions** - explicit create-vs-modify decisions for every
   component, with repository assignment and rationale

**Human gate:** Solution decisions must be reviewed before delivery planning.

### Stage 3 - Delivery planning

Creates a delivery skeleton (high-level epic/feature/story hierarchy) then
produces an elaboration plan with wave ordering and dependency diagram.
Now informed by solution decisions.

**Human gate:** Elaboration plan must be reviewed before epic elaboration.

### Stage 4 - Epic elaboration

Split into two per-item actions for context isolation:

1. **Epic shells** - generates `epic.md` + `implementation-contract.md` per epic
   (one invocation per epic, fresh context each time)
2. **Epic stories** - generates story files per epic, reading the already-written
   contract as input (one invocation per epic, fresh context each time)

Then validates requirement coverage and gates for review.

**Human gate:** Epic folders must be reviewed before coding handoff.

### Stage 5 - Coding handoff

After epic review, generate `coding-handoff.md` for the epics
selected for implementation.

### Stage 6 - Implementation readiness

Produces a final `implementation-readiness.md` report with explicit
`Ready`, `Partial`, and `Blocked` signals per epic before coding begins.

## Human gates

| Gate | After | Owner |
|---|---|---|
| Architecture review | Stage 1 | architect |
| Solution design review | Stage 2 | architect |
| Elaboration plan review | Stage 3 | delivery-lead |
| Epic review | Stage 4 | delivery-lead |

## Output structure

```text
governance/
  delivery-constitution.md
requirements/
  atomic-requirements.md
architecture/
  architecture-review.md
  architecture-rules.md
  technical-landscape.md
  impacted-systems.md
  solution-decisions.md
  ui-specification.md             <- conditional (frontend only)
planning/
  delivery-skeleton.md
  elaboration-plan.md
  fr-coverage.md
  implementation-readiness.md
epics/
  E-001-<slug>/
    epic.md
    implementation-contract.md
    stories/
      S-001.1-<slug>.md
    coding-handoff.md             <- generated in the main flow for selected epics
```

## Scale

| Metric | Count |
|---|---|
| Default workflow actions | 22 (including gate/orchestration actions) |
| Human-triggered actions | 2 (create-brs, spec-correction) |
| Total registered actions | 24 |
| Human gates | 4 |
| Per-item actions | 2 (epic shells, epic stories - fresh context per epic) |

## Comparison with other workflow types

| Aspect | agile-delivery-flow | b2s-flow | agile-delivery-light-flow | fast-path |
|---|---|---|---|---|
| Artifact-producing actions | 27 | 17 default | 8 default + on-demand | 6 |
| Human gates | 4 | 4 | 3 | 0 |
| Total registered actions | 31 | 24 | 11 | 6 |
| Technical landscape | Via impact map | Dedicated mandatory stage | No | No |
| Solution decisions | No | Yes (gated) | No | No |
| UI specification | No | Conditional (frontend) | No | No |
| Domain analysis | Yes | No | No | No |
| Architecture review/rules | Yes | Yes | Yes | No |
| Elaboration plan | Yes | Yes | Yes | No |
| BDD | Separate files | Embedded in AC | Embedded in AC | No |
| Per-item context isolation | No | Yes (epic shells + stories) | No | No |
| Final implementation readiness report | Yes | Yes | No | No |
