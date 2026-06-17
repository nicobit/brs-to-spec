# Architecture and Plan — Flow Engine + BRS-to-Spec v2

**Status:** Design approved — ready to build  
**Date:** 2026-06-13  
**Context:** This document records the architecture decisions and build plan for two things:
1. `.flow-engine/` — a generic file-based event-driven orchestration engine
2. `.brs2spec2/` — brs-to-spec v2, fully built on the engine

Both live in this repository alongside the existing `.brs2spec/` (v1), which stays alive in parallel.

---

## Problem with v1

The current framework (`.brs2spec/`) works but has three structural weaknesses:

- **Orchestration is implicit.** The dispatcher (`brs-to-spec-run-workflow.md`) uses embedded if/then logic to decide what to run next. There is no explicit record of what work was planned, what ran, what failed, or why.
- **No auditability.** You cannot look at the workspace and know what was done, in what order, by which persona, or what validation was applied.
- **No parallelism.** The workflow is linear. Tasks that could run concurrently (e.g. business rules + actor extraction) must run sequentially because there is no mechanism to express independence.

---

## Core idea

Replace implicit orchestration with an **explicit event queue**.

Every unit of work is a YAML file (an event) placed in a shared queue folder. The event file carries everything needed to execute it: who does it, what to read, what to write, how to validate, what to do next. Claude reads the next unblocked event in the queue and executes it. The queue folder and a state file make the entire workflow visible and auditable at any point.

This is not a new concept — it is an event-driven message queue implemented with files and folders, designed to be operated by a chat-based AI agent (Claude Code / Copilot) rather than a server process.

---

## Two-layer architecture

```
Layer 1: .flow-engine/          Generic engine — domain-agnostic
Layer 2: .brs2spec2/            BRS-to-Spec v2 — built on the engine
```

The engine knows nothing about BRS, specs, or business analysis. It only knows how to read an event, dispatch it to the right persona, validate the output, and update the queue. Any future framework (not just brs-to-spec) could use the same engine.

### Execution model — chat-first, deterministic-later

v2.0 is **chat-operated**: Claude reads the dispatcher prompt, follows the event queue protocol, and manages file movement and state updates. This is intentional — it gets the engine working immediately without requiring a server or CLI tool.

v2.1 (future) will add a **lightweight deterministic dispatcher** that handles queue movement, validation, event creation, and state updates programmatically. The architecture is designed so Claude can be replaced as the runner without changing the event schema, persona files, or workflow definition.

The chat-operated model has one strict rule: **Claude must follow the dispatcher protocol exactly**. It must not shortcut file movement, skip validation, or update state outside the defined update-state rules. The dispatcher prompt and event-execution-rules enforce this.

---

## Repository layout

```
.flow-engine/                   Layer 1 — Generic engine
  schemas/
    event-schema.yaml           Canonical event YAML schema (DONE)
    event-result-schema.yaml    Schema for the result file a persona writes on completion
    artifact-status-schema.yaml Schema for artifact status entries in workflow-state.json
  instructions/
    dispatcher.md               Claude entry point — "read next event, execute it"
    event-execution-rules.md    How to read, validate, complete, and fail an event
    artifact-ownership.md       Conflict resolution when two personas touch same artifact
    state-update-rules.md       Who may update which state files and when
    validation-rules.md         How natural-language and machine validators are applied
  personas/                     Generic persona stubs (extended by brs2spec2)

.brs2spec2/                     Layer 2 — BRS-to-Spec v2
  agent-instructions.md         v2 behavioral rules (loads engine + workflow)
  personas/
    orchestrator.md
    product-owner.md
    architect.md
    delivery-lead.md
    qa-analyst.md
    security-reviewer.md
    engineering-lead.md
    reviewer.md
  skills/                       Domain skill prompts — one per task type, per persona
    product-owner/
    architect/
    delivery-lead/
    qa-analyst/
    security-reviewer/
    engineering-lead/
    reviewer/
  artifact-templates/           Expected output shape for each artifact type
  workflow/
    workflow-definition.yaml    Full stage graph: stage → event template → persona
    event-templates/            One YAML file per skill (~35 templates)
  prompts/
    dispatch-next.md            User entry point: "run the next pending event"
    dispatch-all.md             Run until blocked or done

initiatives/<id>-<slug>/        Per-initiative runtime (unchanged root structure)
  input/                        User-owned — unchanged from v1
  .flow/                        Engine runtime state for this initiative
    state/
      workflow-state.json       Current phase, counters, last completed, blocked events
      event-log.jsonl           Append-only log of every event outcome
      open-decisions.md         Blocking and non-blocking open decisions
    events/
      pending/                  Events ready to run (or blocked — see blocked_by)
      processing/               The event currently being executed (max 1 at a time)
      done/                     Completed events — permanent audit record
      failed/                   Events that failed validation — with failure notes

  business-intake/              Artifact folders — identical to v1 structure
  business-analysis/
  architecture/
  planning/
  engineering-readiness/
  quality-gates/
  specs/
  standalone-delivery/
  state/                        Shared with .flow/state/ (same folder)
```

---

## The event file — how it works

Every event is a YAML file in `pending/`. The filename encodes the event ID and title for human readability:

```
EVT-00023-create-business-rules.yaml
```

Inside the file (defined by `.flow-engine/schemas/event-schema.yaml`):

```yaml
event_id: EVT-00023
type: CREATE_ARTIFACT
persona: product-owner          # ← routing: tells dispatcher which persona to load
stage: "2b"

task:
  title: Create business rules
  objective: >
    Extract BR-NNN business rules from the BRS and business intake summary.
    Record ambiguous rules as open decisions.

# References — what to load before executing
skill_ref: .brs2spec2/skills/product-owner/create-business-rules.md
persona_ref: .brs2spec2/personas/product-owner.md
artifact_template_ref: .brs2spec2/artifact-templates/business-rules.md

read_from:
  - input/brs.md
  - business-intake/business-intake-summary.md
  - state/open-decisions.md                    # OPTIONAL

required_inputs:
  - input/brs.md
  - business-intake/business-intake-summary.md

write_to:
  - business-intake/business-rules.md

must_include:
  - every rule has a BR-NNN identifier
  - every rule maps to at least one FR-NNN
  - ambiguous rules recorded in state/open-decisions.md

validation_rules:
  natural_language:
    - no BR-NNN row has an empty Description
    - no placeholder text (TBD / TODO) in output
  machine:
    - validator: no_placeholders
    - validator: id_pattern
      args:
        pattern: "BR-[0-9]{3}"
    - validator: traceability_links
      args:
        from: "BR-[0-9]{3}"
        to: "FR-[0-9]{3}"

blocked_by:
  - business-intake/business-intake-summary.md

on_success:
  create_events:
    - EVT-TPL-005-create-actors-and-personas
  update_state:
    current_stage: "2c"

on_failure:
  raise_decision:
    question: "BR-NNN to FR-NNN mapping incomplete — PO must review BRS source."
    owner: product-owner
    blocking: false
```

**Key design principle:** the `persona` field is the router. There are no per-persona inbox folders. One shared queue, routing determined by file content.

**Reference separation:** every event carries three references that separate concerns cleanly:
- `skill_ref` — the "how to do this specific task" prompt (domain logic)
- `persona_ref` — the "who is acting and what they care about" definition (role + quality standards)
- `artifact_template_ref` — the expected output shape (structure contract)

---

## How dispatch works (step by step)

When the user says "run the next event" (or "dispatch-next"), Claude follows this sequence:

```
1.  Read .flow-engine/instructions/dispatcher.md
2.  Scan .flow/events/pending/ — list all YAML files
3.  For each pending event, check blocked_by (artifacts) and blocked_by_events (EVT-IDs)
4.  Select the highest-priority unblocked event
5.  Move it from pending/ → processing/
6.  Load skill_ref file (how to do the task)
7.  Load persona_ref file (role + quality standards)
8.  Load artifact_template_ref file if present (expected output shape)
9.  Read all files listed in read_from (skip optional ones that don't exist)
10. Execute the task — produce write_to artifacts
11. Write event result file to .flow/events/processing/<event_id>-result.yaml
    (status: pass|fail, artifacts_written, failure_reason if failed)
12. Validate output against must_include and validation_rules (natural_language layer)
13. If valid:   move event + result to done/   → execute on_success actions
14. If invalid: move event + result to failed/ → execute on_failure actions
15. Switch to orchestrator mode:
    - Append entry to .flow/state/event-log.jsonl
    - Update .flow/state/workflow-state.json
    - If on_success.create_events: instantiate new events from templates into pending/
    - If on_failure.raise_decision: write entry to .flow/state/open-decisions.md
16. Return to step 2 (dispatch-all, max 50 events) or stop (dispatch-next)
```

**Result file** (step 11) is written by Claude in persona mode before switching to orchestrator mode. It is the handoff signal between the two modes. Schema defined in `.flow-engine/schemas/event-result-schema.yaml`.

---

## Event type registry

| Type | What the persona does |
|---|---|
| `CREATE_ARTIFACT` | Produces a new artifact that does not yet exist |
| `UPDATE_ARTIFACT` | Updates or enriches an existing artifact |
| `VALIDATE_ARTIFACT` | Reviews and accepts/rejects an artifact — no new file written |
| `REVIEW_ARTIFACT` | Produces a review finding document from an existing artifact |
| `RAISE_DECISION` | Surfaces a blocking open decision to state/open-decisions.md |
| `RESOLVE_DECISION` | Records resolution of an open decision |
| `GENERATE_HANDOFF` | Produces the full handoff package for the initiative |
| `ENRICH_ARTIFACT` | Adds detail to an existing artifact without overwriting other sections |
| `REPAIR_ARTIFACT` | Corrects a malformed or incomplete existing artifact |
| `ROUTE_INITIATIVE` | Orchestrator selects delivery mode and execution mode |
| `RETRY_FAILED_TASK` | Re-runs a previously failed event with corrected inputs |

---

## Persona model

Each persona is defined in `.brs2spec2/personas/<persona>.md`. The file contains:

- **Role** — who this persona is and what they care about
- **Capabilities** — which event types they can handle
- **Quality standards** — what "done" means for this persona's artifacts
- **Domain rules** — specialist knowledge the persona applies (e.g. every BDD scenario needs a SCN-NNN ID)
- **Stop conditions** — when to stop and raise a decision instead of proceeding

The dispatcher loads only the active persona's file — not all eight. This mirrors v1's load-only-what-you-need rule.

**Personas in scope for v2:**

| Persona | Primary responsibilities |
|---|---|
| `orchestrator` | Selects next event, validates completion, creates chained events, maintains state |
| `product-owner` | Business intake, business rules, actors, process flows, use cases, user stories |
| `architect` | Architecture review, architecture rules, entity model, existing system impact |
| `delivery-lead` | Delivery structure, software modules, capability map, increments, traceability matrix |
| `qa-analyst` | BDD scenarios, test plans, test strategy, test stubs |
| `security-reviewer` | Security review, threat model, data contract |
| `engineering-lead` | Readiness check, initiative context, OpenSpec handoff, standalone handoff, implementation |
| `reviewer` | Code review, architecture review of implementation, spec correction |

---

## Workflow definition (stage graph)

`.brs2spec2/workflow/workflow-definition.yaml` defines the default event sequence. The orchestrator reads this to know which event templates to instantiate at each stage transition.

High-level stage graph:

```
0-input-preparation
  → EVT-TPL-001  ROUTE_INITIATIVE       orchestrator     routing-decision.md
  → EVT-TPL-002  CREATE_ARTIFACT        product-owner    business-intake-summary.md

2-business-intake
  → EVT-TPL-003  CREATE_ARTIFACT        product-owner    business-rules.md
  → EVT-TPL-004  CREATE_ARTIFACT        product-owner    actors-and-personas.md
  → EVT-TPL-005  CREATE_ARTIFACT        product-owner    process-flows.md
  → EVT-TPL-006  CREATE_ARTIFACT        product-owner    use-case-spec.md
  → EVT-TPL-007  CREATE_ARTIFACT        architect        entity-model.md

3-planning
  → EVT-TPL-008  CREATE_ARTIFACT        delivery-lead    delivery-structure.md  [draft]
  → EVT-TPL-009  REVIEW_ARTIFACT        architect        architecture-review.md
  → EVT-TPL-010  CREATE_ARTIFACT        architect        architecture-rules.md
  → EVT-TPL-011  UPDATE_ARTIFACT        delivery-lead    delivery-structure.md  [confirmed]
  → EVT-TPL-012  CREATE_ARTIFACT        delivery-lead    traceability-matrix.md
  (Enterprise+Modular only)
  → EVT-TPL-013  CREATE_ARTIFACT        delivery-lead    software-modules.md
  → EVT-TPL-014  CREATE_ARTIFACT        delivery-lead    capability-to-module-map.md
  → EVT-TPL-015  CREATE_ARTIFACT        delivery-lead    delivery-increments.md

4-engineering-readiness
  → EVT-TPL-016  CREATE_ARTIFACT        engineering-lead readiness-check.md
  → EVT-TPL-017  CREATE_ARTIFACT        engineering-lead initiative-context.md
  (gates — conditional on readiness-check triggers)
  → EVT-TPL-018  CREATE_ARTIFACT        qa-analyst       bdd/
  → EVT-TPL-019  CREATE_ARTIFACT        qa-analyst       test-plans per story
  → EVT-TPL-020  CREATE_ARTIFACT        qa-analyst       test-strategy.md
  → EVT-TPL-021  CREATE_ARTIFACT        security-reviewer security-review.md
  → EVT-TPL-022  CREATE_ARTIFACT        security-reviewer threat-model.md
  → EVT-TPL-023  CREATE_ARTIFACT        security-reviewer data-contract.md
  → EVT-TPL-024  CREATE_ARTIFACT        engineering-lead api-contract.md
  → EVT-TPL-025  CREATE_ARTIFACT        engineering-lead event-contract.md
  → EVT-TPL-026  CREATE_ARTIFACT        engineering-lead observability-plan.md

5-handoff
  → EVT-TPL-027  GENERATE_HANDOFF       engineering-lead specs/ (OpenSpec)
  → EVT-TPL-028  GENERATE_HANDOFF       engineering-lead standalone-delivery/ (Standalone)
  → EVT-TPL-029  GENERATE_HANDOFF       engineering-lead compact handoff (FastPath)

6-review-package
  → EVT-TPL-030  CREATE_ARTIFACT        delivery-lead    review-package/

7-perspectives
  → EVT-TPL-031  CREATE_ARTIFACT        delivery-lead    agile-planning/gitlab-planning-view.md

8-implementation
  → EVT-TPL-032  CREATE_ARTIFACT        engineering-lead implement one task
  → EVT-TPL-033  UPDATE_ARTIFACT        engineering-lead fix review comments
  → EVT-TPL-034  CREATE_ARTIFACT        qa-analyst       test stubs from BDD

9-review
  → EVT-TPL-035  REVIEW_ARTIFACT        reviewer         senior code review
  → EVT-TPL-036  REVIEW_ARTIFACT        reviewer         architecture review
  → EVT-TPL-037  REVIEW_ARTIFACT        qa-analyst       qa review
  → EVT-TPL-038  REVIEW_ARTIFACT        security-reviewer security review of implementation
  → EVT-TPL-039  REPAIR_ARTIFACT        reviewer         spec correction
```

Stages 2 through 4 contain **parallelizable events**: events that share no `blocked_by` dependencies have no sequencing requirement and can be executed in any order. In the chat-operated model (v2.0) these still run sequentially via `dispatch-all` — the parallelism is in the data model, not the execution. A future deterministic dispatcher (v2.1) can exploit this to run truly concurrent workers.

---

## Dynamic event creation

The orchestrator is not limited to the static workflow definition. It can create new events at runtime when:

- An artifact reveals a gap not covered by the default workflow (e.g. architecture review finds a missing API boundary → new engineering-lead event)
- A validation failure on one event requires a corrective event on a related artifact
- A human decision resolves an open decision and unblocks a previously blocked event chain

Dynamic events follow the same YAML schema. They are created in `pending/` with `meta.created_by: orchestrator` and no `template_id`.

---

## State ownership rules

State files are owned by the **orchestrator**, not by domain personas. When a domain persona (product-owner, architect, etc.) completes a task, it writes the business artifact (`write_to`) and signals completion. The orchestrator — running as the next step in the dispatch cycle — updates `workflow-state.json`, `event-log.jsonl`, and `open-decisions.md`.

This separation prevents domain personas from corrupting workflow state. In the chat-operated model, Claude switches into orchestrator mode for state updates after each persona task completes. The `state-update-rules.md` instruction file enforces exactly what may be updated and when.

---

## State file

`.flow/state/workflow-state.json` — updated after every event:

```json
{
  "initiative_id": "INIT-001",
  "initiative_slug": "payment-gateway-integration",
  "current_stage": "2-business-intake",
  "delivery_mode": "OpenSpec",
  "execution_mode": "Enterprise",
  "last_completed_event": "EVT-00003",
  "active_events": ["EVT-00004", "EVT-00005"],
  "blocked_events": ["EVT-00006"],
  "failed_events": [],
  "artifacts": {
    "input/brs.md": "accepted",
    "state/routing-decision.md": "accepted",
    "business-intake/business-intake-summary.md": "accepted",
    "business-intake/business-rules.md": "missing",
    "business-analysis/actors-and-personas.md": "missing"
  },
  "open_decisions": 2,
  "blocking_decisions": 0,
  "event_counter": 5
}
```

---

## Event log

`.flow/state/event-log.jsonl` — one JSON line per completed event:

```jsonl
{"event_id":"EVT-00001","type":"ROUTE_INITIATIVE","persona":"orchestrator","status":"done","completed_at":"2026-06-13T10:01:00Z","artifacts_written":["state/routing-decision.md"]}
{"event_id":"EVT-00002","type":"CREATE_ARTIFACT","persona":"product-owner","status":"done","completed_at":"2026-06-13T10:14:00Z","artifacts_written":["business-intake/business-intake-summary.md"]}
{"event_id":"EVT-00003","type":"CREATE_ARTIFACT","persona":"product-owner","status":"failed","completed_at":"2026-06-13T10:22:00Z","failure_reason":"BR-NNN to FR-NNN mapping missing for 4 rules","artifacts_written":[]}
```

---

## What stays the same from v1

- Initiative workspace folder structure (artifact paths are identical)
- Skill content — domain logic lives in `skills/<persona>/<skill>.md` files, referenced by `skill_ref` in each event. Persona files carry role definition and quality standards only, not task instructions.
- `input/` boundary rule — users write only to `input/`
- Artifact authority and precedence model (quality gates > architecture rules > readiness > ...)
- The "content over existence" validation principle

---

## What changes from v1

| v1 | v2 |
|---|---|
| Implicit orchestration in `brs-to-spec-run-workflow.md` | Explicit event queue in `.flow/events/` |
| Stage progression tracked in `workflow-state.json` (current_stage string) | Full event lifecycle: pending → processing → done / failed |
| No audit trail of what ran | `event-log.jsonl` — append-only record of every event |
| Skills invoked by orchestrator reading a prompt file | Skills invoked by dispatcher reading an event + persona file |
| No parallelism | Parallel execution for events with no shared dependencies |
| Dynamic routing via embedded if/then in run-workflow.md | Dynamic event creation: orchestrator writes new YAML files to pending/ |
| Repair is a special skill | Repair is a first-class event type (REPAIR_ARTIFACT) |

---

## Build plan

### Phase 1 — Engine core (`.flow-engine/`)

| # | Artifact | Description |
|---|---|---|
| 1.1 | `.flow-engine/schemas/event-schema.yaml` | Event YAML schema — **DONE** |
| 1.2 | `.flow-engine/schemas/event-result-schema.yaml` | Schema for the result file a persona writes on completion |
| 1.3 | `.flow-engine/schemas/artifact-status-schema.yaml` | Schema for artifact status entries in workflow-state.json |
| 1.4 | `.flow-engine/instructions/dispatcher.md` | Claude entry point — reads next event, executes, validates, chains |
| 1.5 | `.flow-engine/instructions/event-execution-rules.md` | How to read, validate, complete, and fail an event |
| 1.6 | `.flow-engine/instructions/artifact-ownership.md` | Conflict resolution when two events touch the same artifact |
| 1.7 | `.flow-engine/instructions/state-update-rules.md` | Who may update which state files and when (orchestrator-only rule) |
| 1.8 | `.flow-engine/instructions/validation-rules.md` | How natural-language and machine validators are applied |

### Phase 2 — BRS-to-Spec v2 personas and skills (`.brs2spec2/`)

Persona files define **who** acts and **what quality standards** they apply. Skill files define **how** to perform a specific task. Artifact templates define the **expected output shape**.

| # | Artifact | Port from v1 |
|---|---|---|
| 2.1 | `personas/orchestrator.md` | `module-personas/orchestrator.md` + run-workflow.md logic |
| 2.2 | `personas/product-owner.md` | `module-personas/product-owner.md` |
| 2.3 | `personas/architect.md` | `module-personas/architect.md` |
| 2.4 | `personas/delivery-lead.md` | `module-personas/delivery-lead.md` |
| 2.5 | `personas/qa-analyst.md` | `module-personas/qa-analyst.md` |
| 2.6 | `personas/security-reviewer.md` | `module-personas/security-reviewer.md` |
| 2.7 | `personas/engineering-lead.md` | `module-personas/engineering-lead.md` |
| 2.8 | `personas/reviewer.md` | `module-personas/reviewer.md` |
| 2.9 | `skills/<persona>/<skill>.md` (~35 files) | Port from `.brs2spec/skills/` — one file per v1 skill prompt |
| 2.10 | `artifact-templates/<artifact>.md` (~20 files) | Port from `.brs2spec/templates/` |

### Phase 3 — Workflow definition (`.brs2spec2/workflow/`)

> **Implementation strategy — sliced, not all-at-once.** Build and validate the engine on the smallest possible working case before porting more templates. Each slice must pass an end-to-end test (event created → dispatched → result written → state updated → next event chained) before the next slice begins.

**Slice 1 — Engine proof (1 event):**
- EVT-TPL-001: ROUTE_INITIATIVE → orchestrator → routing-decision.md
- Goal: prove the full dispatch lifecycle end-to-end on the simplest possible event (no domain complexity, no blocked_by dependencies, single write_to artifact)
- Done criteria: event moves pending → processing → done, result file written, event-log.jsonl updated, workflow-state.json updated, next event instantiated in pending/
- Do not proceed to Slice 2 until Slice 1 passes completely on a real initiative

**Slice 2 — First real artifact (1 event):**
- EVT-TPL-002: CREATE_ARTIFACT → product-owner → business-intake-summary.md
- Goal: prove skill_ref + persona_ref + artifact_template_ref loading works; prove natural_language validation works; prove on_failure/raise_decision path works
- Done criteria: same as Slice 1, plus validation failure path tested deliberately

**Slice 3 — Business analysis (5 events):**
- EVT-TPL-003 through EVT-TPL-007: business-rules, actors-and-personas, process-flows, use-case-spec, entity-model
- Goal: prove parallelizable events (no shared blocked_by) work correctly in dispatch-all sequential mode

**Slice 4 — Planning and architecture (8 events):**
- EVT-TPL-008 through EVT-TPL-015: delivery structure, architecture review/rules, traceability, modular planning

**Slice 5 — Readiness and quality gates (11 events):**
- EVT-TPL-016 through EVT-TPL-026: readiness check, context, BDD, test plans/strategy, security, data/API/event/observability contracts

**Slice 6 — Handoff through review (13 events):**
- EVT-TPL-027 through EVT-TPL-039: handoffs, review package, perspectives, implementation, review

| # | Artifact | Description |
|---|---|---|
| 3.1 | `workflow-definition.yaml` | Full stage graph — stages, dependencies, gate conditions |
| 3.2 | `event-templates/` (sliced per above) | One YAML event template per skill (~35 files total) |

### Phase 4 — User entry points (`.brs2spec2/prompts/`)

| # | Artifact | Description |
|---|---|---|
| 4.1 | `dispatch-next.md` | "Run the next pending event" — single-event execution, stops after one event regardless of outcome |
| 4.2 | `dispatch-all.md` | "Run until blocked or done" — sequential, stops when all pending events are blocked or done, or after **50 events** (runaway guard) |

### Phase 5 — Framework wiring

| # | Artifact | Description |
|---|---|---|
| 5.1 | `.brs2spec2/agent-instructions.md` | v2 behavioral rules — loads engine + workflow on session start |
| 5.2 | `CLAUDE.md` addition | Reference `.brs2spec2/agent-instructions.md` alongside existing `.brs2spec/` |
| 5.3 | Initiative scaffolding script | Update `new_initiative.py` to create `.flow/` structure alongside workspace |

### Phase 6 — Deterministic dispatcher (future, v2.1)

| # | Artifact | Description |
|---|---|---|
| 6.1 | `tools/dispatcher.py` (or similar) | Lightweight script: scan pending/, check blocked_by, move files, validate, log |
| 6.2 | Engine integration test | Prove dispatcher produces identical behavior to chat-operated v2.0 |

Phase 6 is not scheduled. It is named so the architecture is designed to support it from the start.

---

## Decisions made

| Decision | Choice | Reason |
|---|---|---|
| Engine location | Same repo as `.brs2spec/`, in `.flow-engine/` | Faster to start; engine and v2 can be separated later if needed |
| v1 fate | Stays alive in parallel | Existing initiatives must keep running |
| v2 scope | Full — all 8 personas, all stages | No partial implementation; v2 must be a complete replacement when ready |
| Queue topology | One shared queue, routing by `persona` field in event file | Simpler than per-persona mailboxes; easier to audit; fewer folders |
| Parallelism | Parallelizable in the data model; sequential in chat-operated v2.0 | True parallel execution requires v2.1 deterministic dispatcher |
| Dynamic events | Orchestrator can create new events at runtime | Needed for gap detection, retry, and escalation |
| Artifact paths | Identical to v1 | Existing initiatives can migrate without moving files |
| DEC-003: skill references | External skill files, referenced by `skill_ref` in the event | Keeps event as work order; skill file carries domain logic; persona file carries role standards |
| Execution model | Chat-operated first (v2.0); deterministic dispatcher later (v2.1) | Gets the engine working immediately; architecture supports replacement of Claude as runner |
| State ownership | Orchestrator-only rule — domain personas do not update state files | Prevents domain personas from corrupting workflow state; enforced by `state-update-rules.md` |
| Validation schema | Dual-layer: `natural_language` (Claude-evaluated) + `machine` (future validators) | Schema is ready for automation; natural language validators work today |
| v2 build order | Sliced — 1-event Slice 1 proves engine end-to-end before porting more templates | Validates the full dispatch lifecycle (result file, state update, chaining) on the simplest possible case |
| DEC-002: dispatch-all max count | 50 events per session | Enough for a full initiative run; prevents runaway loops; Claude must stop and report if limit reached |
| Event result file | Explicit step in dispatch lifecycle — written by persona before orchestrator mode | Provides a clean handoff signal between persona execution and orchestrator state update |

---

## Open decisions

| ID | Question | Owner | Blocking |
|---|---|---|---|
| DEC-001 | Should the engine be extracted to a separate repo once v2 is stable? | Nicola | No |
