# Framework Enhancement 9 — Flow Engine + BRS-to-Spec v2

## What this folder is

Design and implementation prompts for building two things:
1. `.flow-engine/` — a generic file-based event-driven orchestration engine
2. `.brs2spec2/` — brs-to-spec v2, fully built on the engine

Both live in this repository alongside the existing `.brs2spec/` (v1), which stays alive in parallel.

## Read first

| File | Purpose |
|---|---|
| [architecture-and-plan.md](architecture-and-plan.md) | Full architecture, decisions, and build plan — read this before anything else |
| [input.md](input.md) | Original design exploration — event-driven multi-agent architecture proposal |
| [input2.md](input2.md) | Follow-up — VS Code Chat / Claude Code constraint analysis |

## Implementation prompts — use in order

Each prompt is a self-contained instruction for one Claude session. Hand it to Claude with the relevant source files and it will produce the specified outputs.

| # | Prompt | Phase | Produces | Prerequisite |
|---|---|---|---|---|
| 1 | [impl-01-engine-schemas.md](impl-01-engine-schemas.md) | 1 — Engine | `event-result-schema.yaml`, `artifact-status-schema.yaml` | `event-schema.yaml` exists |
| 2 | [impl-02-dispatcher.md](impl-02-dispatcher.md) | 1 — Engine | `dispatcher.md` | All 3 schemas exist |
| 3 | [impl-03-engine-instructions.md](impl-03-engine-instructions.md) | 1 — Engine | `event-execution-rules.md`, `artifact-ownership.md`, `state-update-rules.md`, `validation-rules.md` | `dispatcher.md` exists |
| 4 | [impl-04-personas.md](impl-04-personas.md) | 2 — v2 Layer | 8 persona files in `.brs2spec2/personas/` | Phase 1 complete |
| 5 | [impl-05-skills-and-templates.md](impl-05-skills-and-templates.md) | 2 — v2 Layer | ~35 skill files + ~20 artifact templates | Persona files exist |
| 6 | [impl-06-workflow-and-event-templates.md](impl-06-workflow-and-event-templates.md) | 3 — Workflow | `workflow-definition.yaml` + ~39 event templates (sliced) | Slice 1 skills exist and validated |
| 7 | [impl-07-prompts-and-wiring.md](impl-07-prompts-and-wiring.md) | 4+5 — Wiring | `dispatch-next.md`, `dispatch-all.md`, `agent-instructions.md`, CLAUDE.md update, init script update | Slice 1 validated |
| 8 | [impl-08-slice1-validation.md](impl-08-slice1-validation.md) | Gate | Test checklist — 47 checks across happy path and failure path | Prompts 1–5 + Slice 1 event template done |

## Build sequence

```
prompt-1 → prompt-2 → prompt-3          (Phase 1: engine core)
     ↓
prompt-4 → prompt-5 (Slice 1 only)      (Phase 2: Slice 1 personas + skills)
     ↓
prompt-6 (EVT-TPL-001 only)             (Phase 3: first event template)
     ↓
prompt-8                                 (Slice 1 end-to-end validation — GATE)
     ↓
prompt-7                                 (Phase 4+5: wiring — can overlap with Slice 2)
     ↓
prompt-5 (remaining skills)             (Phase 2: port remaining ~33 skill files)
     ↓
prompt-6 (EVT-TPL-002, then slices 3–6) (Phase 3: remaining event templates)
```

## Current state

| Artifact | Status |
|---|---|
| `.flow-engine/schemas/event-schema.yaml` | Done |
| `.flow-engine/schemas/event-result-schema.yaml` | Not started |
| `.flow-engine/schemas/artifact-status-schema.yaml` | Not started |
| `.flow-engine/instructions/dispatcher.md` | Not started |
| `.flow-engine/instructions/event-execution-rules.md` | Not started |
| `.flow-engine/instructions/artifact-ownership.md` | Not started |
| `.flow-engine/instructions/state-update-rules.md` | Not started |
| `.flow-engine/instructions/validation-rules.md` | Not started |
| `.brs2spec2/personas/` (8 files) | Not started |
| `.brs2spec2/skills/` (~35 files) | Not started |
| `.brs2spec2/artifact-templates/` (~20 files) | Not started |
| `.brs2spec2/workflow/workflow-definition.yaml` | Not started |
| `.brs2spec2/workflow/event-templates/` (~39 files) | Not started |
| `.brs2spec2/prompts/dispatch-next.md` | Not started |
| `.brs2spec2/prompts/dispatch-all.md` | Not started |
| `.brs2spec2/agent-instructions.md` | Not started |
| `CLAUDE.md` v2 section | Not started |
| Initiative scaffolding script update | Not started |
| Slice 1 validation | Not started |

## Key decisions

- One shared event queue — routing by `persona` field inside the event file, not by folder
- Three references per event: `skill_ref` (how), `persona_ref` (who), `artifact_template_ref` (shape)
- Persona mode vs orchestrator mode are strictly separated — state files only updated in orchestrator mode
- Result file written by persona mode before switching to orchestrator mode — it is the handoff signal
- `dispatch-all` stops at 50 events — hard limit, not configurable per session
- Sliced build order — Slice 1 (1 event) must pass end-to-end before any further templates are written
- v1 stays alive — initiatives without `.flow/` use `.brs2spec/`; initiatives with `.flow/` use `.brs2spec2/`
