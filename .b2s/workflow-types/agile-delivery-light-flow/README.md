# Workflow Type: agile-delivery-light-flow

## When to use

Use this workflow for initiatives that need **architecture-aware progressive
delivery with minimal overhead**. It produces epic-centric output — one
folder per epic containing an overview and lean user stories with embedded
BDD acceptance criteria. Implementation contracts and coding handoff are
generated later, only for selected epics.

Choose this workflow when:

- The team wants a BMAD-style structure: one folder per epic, work through
  them in priority order
- Story quality and BDD are embedded in acceptance criteria, not separate
  artifacts
- Adoption friction of the full `agile-delivery-flow` is a concern
- The initiative needs architecture-aware planning but not full domain
  analysis

## When not to use

- Regulated industries needing full traceability — use `agile-delivery-flow`
  or `enterprise-modular`
- Simple or internal initiatives — use `fast-path`
- Initiatives requiring OpenSpec story packages with design.md, tasks.md,
  and coding-prompt.md per story — use `agile-delivery-flow`

## Stages

```
Phase A - initiative planning
0-governance
  → 1-requirements-and-architecture [HUMAN GATE]
    → 2-delivery-planning [HUMAN GATE]

Phase B - epic elaboration
      → 3-epic-elaboration [HUMAN GATE]

Phase C - implementation prep (on demand)
      → human-triggered implementation contracts / coding handoff
```

### Stage 0 — Governance

Creates the delivery constitution.

### Stage 1 — Requirements and architecture

Extracts atomic requirements, reviews architecture, creates architecture
rules — all in a single gated stage.

**Human gate:** Architecture must be reviewed before delivery planning.

### Stage 2 — Delivery planning

Creates a delivery skeleton (high-level epic/feature/story hierarchy) then
produces an elaboration plan with wave ordering, parallel groups, and a
Mermaid dependency diagram.

**Human gate:** Elaboration plan must be reviewed before epic elaboration.

### Stage 3 — Epic elaboration

Generates one folder per epic containing `epic.md` (overview, scope, risks,
dependencies) and individual lean story files with embedded Given/When/Then
acceptance criteria. Validates requirement coverage across all stories.

**Human gate:** Epic folders must be reviewed before the workflow completes.

### Phase C — Implementation prep

After epic review, generate `implementation-contract.md` and
`coding-handoff.md` only for the epics selected for implementation.

## Human gates

| Gate | After | Owner |
|---|---|---|
| Architecture review | Stage 1 | architect |
| Elaboration plan review | Stage 2 | delivery-lead |
| Epic review | Stage 3 | delivery-lead |

## Output structure

```
epics/
  E-001-<slug>/
    epic.md
    stories/
      F-001.1-<slug>.md
      F-001.2-<slug>.md
    implementation-contract.md   ← generated later on demand
    coding-handoff.md            ← generated later on demand
  E-002-<slug>/
    epic.md
    stories/
      F-003.1-<slug>.md
```

## Comparison with other workflow types

| Aspect | agile-delivery-flow | agile-delivery-light-flow | fast-path |
|---|---|---|---|
| Artifact-producing actions | 27 | 8 default + on-demand prep | 6 |
| Human gates | 4 | 3 | 0 |
| Total steps | 31 | 11 | 6 |
| Output structure | Scattered (5 folders) | Epic-centric (1 folder) | Single handoff |
| Domain analysis | Yes | No | No |
| Architecture impact | Yes | No | No |
| Elaboration plan | Yes | Yes | No |
| BDD | Separate files | Embedded in AC | No |
| OpenSpec handoff | Yes | On-demand per epic coding handoff | No |

## Workspace folder structure

```
governance/
requirements/
architecture/
planning/
epics/          ← the primary deliverable
```
