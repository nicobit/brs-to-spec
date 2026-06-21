# Workflow Type: agile-delivery-flow

## When to use

Use this workflow for initiatives that require **progressive decomposition with
architecture-awareness at every phase**. This workflow transforms a BRS into
architecture-aware, testable, AI-ready delivery artifacts using explicit
governance, capability mapping, per-story quality gates, and dispatch routing.

Choose this workflow when any of the following apply:

- The initiative requires architecture impact assessment per requirement before
  delivery planning begins
- Business capabilities must be mapped before epics are generated (domain-driven
  delivery)
- Every story must pass a strict quality gate before BDD and handoff
- The team needs explicit governance rules (delivery constitution) governing all
  phases
- Architecture decisions (ADRs) must be formally identified and tracked
- Dispatch routing is needed to determine the next best action after readiness
  review

Suitable for: architecture-first delivery, AI-agent handoff workflows,
progressive decomposition, teams that need explicit story quality validation.

## When not to use

- Simple or internal initiatives — use `fast-path`
- Initiatives that do not need capability mapping or per-requirement architecture
  impact — use `enterprise-modular`
- Initiatives already in progress under another workflow type — do not switch
  mid-initiative

## Stages

```
0-governance
  → 1-requirements [HUMAN GATE]
    → 2-domain-analysis
      → 3-architecture-context [HUMAN GATE]
        → 4-architecture-impact
          → 5-delivery-planning [HUMAN GATE: elaboration plan]
            → 6-story-quality-gate [HUMAN GATE]
              → 7-bdd-and-testing
                → 8-handoff
                  → 9-readiness-review [HUMAN GATE]
                    → 10-dispatch
```

### Stage 0 — Governance

Creates the delivery constitution: governance rules, Definition of Ready,
Definition of Done, AI safety rules, and blocking conditions that all later
phases must respect.

### Stage 1 — Requirements extraction

Extracts atomic requirements (REQ-NNN) from the BRS with per-requirement
metadata: type, actor, business object, trigger, outcome, dependencies,
ambiguities, assumptions, and blocking questions. Also produces standalone
open questions and assumptions catalogues.

**Human gate:** Requirements must be reviewed before domain analysis.

### Stage 2 — Domain analysis

Builds a capability map (CAP-NNN), domain model (ENT-NNN), business rules
(BR-NNN), and domain traceability matrix. The capability map is unique to
this workflow — it bridges requirements to epics via business capabilities.

### Stage 3 — Architecture context

Drafts architecture (if no input provided), reviews architecture, and
creates architecture rules (AR-NNN).

**Human gate:** Architecture must be reviewed before impact assessment.

### Stage 4 — Architecture impact

Maps every requirement to architecture impact: impacted system, component,
API, data, integration, security, deployment, observability, performance,
backward compatibility. Identifies required ADRs and architecture risks.

### Stage 5 — Delivery planning

Creates a delivery skeleton (high-level epic/feature/story hierarchy), then
produces an elaboration plan that proposes which epics to detail first, which
can be elaborated in parallel, and a Mermaid dependency diagram. After human
approval, epic packages and per-feature story files are generated, followed
by requirement coverage validation.

**Human gate:** Elaboration plan must be reviewed before epic/story elaboration.

### Stage 6 — Story quality gate

Validates every story against 11 quality checks: business goal, size,
testability, AC specificity, traceability, dependencies, architecture impact,
data/API/UI/integration impact, security, observability, AI safety.

**Human gate:** Story quality must be reviewed before BDD generation.

### Stage 7 — BDD and testing

Generates BDD scenarios, test strategy, and test data requirements for
approved stories only.

### Stage 8 — Handoff

Generates implementation handoff packages (OpenSpec or Standalone).

### Stage 9 — Readiness review

Final readiness review across all artifacts. Produces ready/blocked story
split and fix recommendations.

**Human gate:** Readiness must be reviewed before dispatch.

### Stage 10 — Dispatch

Routes the next best action based on readiness outcomes. Produces a dispatch
log and persona message for the assigned next actor.

## Human gates

| Gate | After | Owner |
|---|---|---|
| Requirements review | Stage 1 | product-owner |
| Architecture review | Stage 3 | architect |
| Elaboration plan review | Stage 5 (after skeleton) | delivery-lead |
| Story quality review | Stage 6 | qa-analyst |
| Readiness review | Stage 9 | engineering-lead |

## Quality gates

BDD and test strategy are always generated (not conditional). The story quality
gate at stage 6 is the primary quality control — stories must pass 11 checks
before BDD generation.

## Delivery modes supported

- OpenSpec (full story packages)
- Standalone (standalone handoff document)

## Key differences from enterprise-modular

| Aspect | enterprise-modular | agile-delivery-flow |
|---|---|---|
| Governance | Distributed policies | Delivery constitution (stage 0) |
| Requirements | FR/NFR/Constraints catalogue | Atomic requirements with per-item metadata |
| Capability mapping | No equivalent | CAP-NNN capability map (stage 2) |
| Architecture impact | System-level impact | Per-requirement impact map (stage 4) |
| ADRs | Not tracked | ADR-NNN catalogue (stage 4) |
| Story quality | Initiative-level readiness | Per-story 11-check quality gate (stage 6) |
| BDD | Conditional | Always generated |
| Dispatch | Engine-internal | Explicit artifacts (stage 10) |

## Workspace folder structure

```
governance/
requirements/
domain/
architecture/
planning/
quality/
specs/ or standalone-delivery/
review/
dispatch/
```
