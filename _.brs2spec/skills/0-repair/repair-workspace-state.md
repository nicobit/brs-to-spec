# Prompt — Repair Workspace State

## Role

You are the orchestrator performing a diagnostic repair of the active initiative workspace.

## Purpose

Correct a corrupted or inaccurate `state/workflow-state.json` so the workflow can resume from the right stage. This prompt is the fix for workspaces where a previous session skipped required stages, advanced past gate failures, or left the state file inconsistent with the artifacts on disk.

**Do not generate new framework artifacts in this prompt.** Only read, assess, and repair the state file. The workflow runner picks up from the repaired state.

## CRITICAL — bypass the fast path

**The entire purpose of this prompt is to distrust the existing state file.**

Before doing anything else, write `"state_validated": false` into `state/workflow-state.json`. Do this immediately — before reading any artifact. This prevents the workflow runner from using the stale state file as a fast path while you are scanning.

**Do NOT use the existing `state/workflow-state.json` to determine artifact statuses.** Ignore every existing status value. Ignore every existing note. Ignore `current_stage` and `next_action` in the existing file. The only way to assign a status is to open the actual artifact file and read its content.

**`state_validated` must remain `false` until you have opened and read every artifact file in Step 3.** Only set it to `true` in Step 5 after writing the fully repaired file.

**Reject forced acceptances.** Any quality gate artifact whose `Status:` field says "Accepted (forced)", "force-accepted", or whose note contains "forced" must be treated as `triggered-incomplete`. Forced acceptance is not real acceptance — it means a previous session bypassed the gate without producing real content.

## When to run this prompt

- `workflow-state.json` is corrupted (two JSON objects, invalid status values, `state_validated: false`)
- A previous session skipped stages (e.g. quality gates created without business-rules, actors, process flows)
- The `next_action` in the state file points to a stage whose prerequisites are not met
- The state file says a stage is `complete` but the artifact on disk is missing or stub-only
- The AI keeps restarting from the wrong stage after every session

## Workspace rule

Work inside one initiative workspace at a time. All relative paths are relative to:

```text
initiatives/<initiative-id>-<slug>/
```

---

## Step 1 — Detect active initiative workspace

Identify the active workspace under `initiatives/`. If more than one exists, ask the user which is active before proceeding.

---

## Step 2 — Repair workflow-state.json structure

Read `state/workflow-state.json`.

**If the file contains two concatenated JSON objects:** truncate to keep only the first (most recent) object. If the first object has `last_updated` earlier than the second, keep the second instead. Write the corrected single-object JSON back to the file.

**If the file is missing:** initialise it from `.brs2spec/templates/state/workflow-state.json` with `state_validated: false` and `current_stage: "unknown"`. Proceed with Step 3 to determine the correct stage.

**If the file is valid JSON but has invalid status values** (e.g. `present`, `exists`, `created`, `scaffolded`, `ok`): do not correct the values yet — Step 3 will reassign them from a fresh content scan.

After structural repair, set `state_validated: false` so the orchestrator does not use stale values as a fast path.

---

## Step 3 — Scan disk to determine what actually exists

For every artifact in the stage gate chain below, check whether the file exists **and** read its content to determine its true status. Do not trust any existing status values in `workflow-state.json`.

Assign one status per artifact using only these valid values:

| Status | When to use |
|---|---|
| `missing` | File does not exist |
| `stub` | File exists but is heading-only, empty tables, or placeholder text |
| `incomplete` | File exists with real content but fails done criteria (see below) |
| `stale` | File exists with real content but still shows resolved decisions as open, carries a DRAFT notice after sign-off, or says Not ready when all blocking issues are resolved |
| `corrupt` | File exists but contains multiple versions concatenated (top-level heading appears more than once); content cannot be trusted; must be regenerated |
| `complete` | File exists, passes done criteria, no stale placeholders |
| `not-triggered` | Quality gate — not triggered for this initiative |
| `triggered-incomplete` | Quality gate triggered but no artifact or artifact not Accepted |
| `triggered-complete` | Quality gate triggered and `Status: Accepted` present in the artifact |

**Never use** `present`, `exists`, `created`, `scaffolded`, `ok`, or any value not in this table.

### Artifacts to scan (in gate chain order)

| # | Stage | Artifact | Done criteria |
|---|---|---|---|
| 1 | Routing | `state/routing-decision.md` | Delivery mode, execution mode, and rationale all stated |
| 2 | Business intake | `business-intake/business-intake-summary.md` | Objectives with success measures; requirements with IDs; gaps with owners |
| 2b | Business rules | `business-intake/business-rules.md` | BR-NNN IDs present; each rule has a BRS source reference |
| 2c | Actors | `business-analysis/actors-and-personas.md` | ACT-NNN and SYS-NNN IDs present; every named role in BRS covered |
| 2d | Process flows (draft) | `business-analysis/process-flows.md` | PF-NNN flows present; draft notice acceptable; story refs may be stubs — **must exist before stage 3 and 5** |
| 2e | Use cases (draft) | `business-analysis/use-case-spec.md` | UC-NNN specs present; draft notice acceptable; AC coverage may be stubs — **must exist before stage 5** |
| 3 | Architecture input | `input/architecture.md` | Not a stub; has system components and integration points |
| 4 | Delivery structure (draft) | `planning/delivery-structure.md` | Epics with IDs; features visible; stories may be stubs |
| 4a | Software modules (Enterprise + Modular) | `planning/software-modules.md` | Module table present with IDs, names, owning teams, capability boundaries; complete only if delivery_mode = Enterprise + Modular and file has real content |
| 4b | Capability-to-module map (Enterprise + Modular) | `planning/capability-to-module-map.md` | Every feature maps to a module; module IDs match software-modules.md; complete only if delivery_mode = Enterprise + Modular |
| 4c | Delivery increments (Enterprise + Modular) | `planning/delivery-increments.md` | Increments present with module and feature references; complete only if delivery_mode = Enterprise + Modular |
| 5 | Architecture review | `architecture/architecture-review.md` | Initiative-specific constraints; every open decision has an owner; Review Decision stated |
| 6 | Architecture rules | `architecture/architecture-rules.md` | AR-NNN rules with enforcement; no AR-OPEN-* for resolved decisions |
| 7 | Open decisions | `state/open-decisions.md` | All decisions present; blocking summary accurate |
| 8 | Engineering readiness | `engineering-readiness/readiness-check.md` | Explicit Ready/Not ready; triggered gates listed; no placeholder owners |
| 9 | Delivery structure (confirmed) | `planning/delivery-structure.md` | Every story has F-XXX.X ID, ACT-NNN actor, "As a/I want/so that", at least one AC-NNN, FR-NNN reference, BR-NNN link or explicit "none apply" note |
| 9b | BDD scenarios (three amigos) | `quality-gates/bdd/` | At least one .md per feature with SCN-NNN IDs and complete Given/When/Then blocks; acceptance-checklist.md Status: Accepted |
| 9c | Process flows (confirmed) | `business-analysis/process-flows.md` | PF-NNN flows enriched with confirmed F-XXX.X IDs and AC-NNN references; no draft notice |
| 9d | Use cases (confirmed) | `business-analysis/use-case-spec.md` | UC-NNN specs enriched with F-XXX.X story IDs and AC coverage table; no draft notice |
| 9e | Story enrichment | `planning/delivery-structure/` | All story files have enriched AC, FR-NNN, and BR-NNN links; no stub stories remaining |
| 9f | Test plans per story | `quality-gates/test-plans/` | One F-XXX.X-test-plan.md per story; TC-NNN IDs present; every row has a criticality (C1–C4); test-plan-index.md present |
| 10 | Test strategy | `quality-gates/test-strategy.md` | SCN-NNN and TC-NNN IDs referenced; C1/C2 counts stated; Status: Accepted |
| 11 | Initiative context | `engineering-readiness/initiative-context.md` | No empty rows; specific technology choices |
| 12 | Open decisions update | `state/open-decisions.md` | All pre-handoff decisions resolved or explicitly deferred with owner |
| 12b | Quality gates | Per triggered gate | `Status: Accepted` in Metadata table at top of each gate file (security, API, data, observability) |
| 13 | Handoff | `specs/` or `standalone-delivery/` | dependency-graph.md + story folders present |
| 13a | Test stubs | `quality-gates/test-stubs` | BDD stubs in `bdd/` subfolder (one per SCN-NNN); unit stubs in `unit/` subfolder (one per TC-NNN type=Unit) |
| 14 | Review package | `review-package/status.md` | Review status recorded; sign-off or outstanding items listed |

### Differentiating delivery-structure draft vs confirmed

`planning/delivery-structure.md` serves two stages (4 and 9). Determine which status to assign:

- **Draft** (`incomplete` at stage 4): file has epics and features but stories are stubs, bullet lists, or missing F-XXX.X IDs
- **Confirmed** (`complete` at stage 9): every story has an `F-XXX.X` ID, a well-formed "As a ACT-NNN / I want / so that" statement, at least one `AC-NNN`, a `FR-NNN` reference, and a `BR-NNN` link or explicit "none apply" note

### Special case: multiple versions concatenated in one file

If any artifact file contains two or more document versions concatenated (e.g. two `# Delivery Structure` headings, two `# Metadata` tables, two sets of epics), that file is corrupt. Set its status to `corrupt` — the orchestrator cannot safely read it. Add it to `stale_artifacts`. The repair report must call this out explicitly so the user knows the file needs to be regenerated cleanly. Do not attempt to read the content to determine a version — a corrupt file has no authoritative version and must be replaced entirely.

### Special case: gates accepted without human review (self-accepted gates)

A gate artifact is self-accepted if any of the following are true:
- `Status:` field contains "forced" (e.g. "Accepted (forced)", "force-accepted", "force accepted")
- `Status: Accepted` is present AND the acceptance note says the status was set by the orchestrator, a script, or an automated process in the same session that created the file
- The gate file was created AND accepted in the same session (visible from creation-date notes in the file)

**Action:**
1. Set status to `triggered-incomplete` regardless of what the file says.
2. Do not delete the file — the content may still be useful as a draft.
3. Change the Status field in the Metadata table to `In progress`.
4. Add a repair note to the file: `"> REPAIR: Status was reset from forced/self-accepted to In progress by repair run on YYYY-MM-DD. Gate owner must review content and set Status to Accepted."`
5. Add the gate path to `stale_artifacts` in `workflow-state.json`.
6. In the repair report, list every self-accepted gate in a `### Self-accepted gates (reset)` section.

**The repair skill must not re-accept the gate.** Leave it at `In progress` and stop. The human gate owner must review the content and explicitly set `Status: Accepted`.

---

### Special case: quality gates exist without prerequisites

If quality gate artifacts exist (`quality-gates/bdd/`, `quality-gates/test-plans/`, `quality-gates/test-strategy.md`, `quality-gates/security-review.md`, etc.) but any of the following are missing: `business-intake/business-rules.md`, `business-analysis/actors-and-personas.md`, `business-analysis/process-flows.md` (draft), `planning/delivery-structure/` (confirmed stories) — flag these gate artifacts as **premature** in the repair report. Set their status to `triggered-incomplete` regardless of their `Status:` field. They were produced without valid inputs and cannot be trusted until the prerequisite stages are complete and a re-run confirms their content is still accurate.

Similarly, if `quality-gates/test-strategy.md` exists but `quality-gates/bdd/` or `quality-gates/test-plans/` are missing or incomplete — the test strategy is premature; set to `triggered-incomplete`.

---

## Step 4 — Determine the correct `current_stage` and `next_action`

The correct `current_stage` is the **last stage where the artifact is `complete`**.

The correct `next_action` is the **first stage in gate chain order where the artifact is not `complete`**. Walk the gate chain in order from stage 1. Stop at the first gap. That is `next_action`. Do not skip ahead to a later stage even if its artifact file exists on disk — a downstream artifact produced without its prerequisites is invalid.

**The existence of a downstream artifact (e.g. specs/handoff, quality gates) does NOT mean upstream stages are complete.** If `business-rules.md` is missing, `next_action` is stage 2b — regardless of what else exists.

Apply this priority order:

1. If `state/open-decisions.md` has any decision where Blocking = Yes and Status ≠ Resolved → `next_action` = resolve blocking decisions
2. Otherwise → walk the gate chain from stage 1 and stop at the first artifact that is not `complete`

**Gate chain walk — use this exact order:**

```
1 → 2 → 2b → 2c → 2d → 2e → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 9b (BDD) → 9c (process flows) → 9d (use cases) → 9e (story enrichment) → 9f (test plans) → 10 (test strategy) → 11 → 12 → 12b → 13 → 13a (test stubs) → 14
```

Stop at the first stage where the artifact is `missing`, `stub`, `incomplete`, `stale`, or `triggered-incomplete`. Set `next_action` to that stage. Do not advance past it.

**Absolute rule: if any of these are missing, `next_action` cannot be set to any stage after them:**

| If this is missing | next_action cannot be later than |
|---|---|
| `business-intake/business-rules.md` | stage 2b |
| `business-analysis/actors-and-personas.md` | stage 2c |
| `business-analysis/process-flows.md` (draft) | stage 2d |
| `business-analysis/use-case-spec.md` (draft) | stage 2e |
| `architecture/architecture-review.md` | stage 5 |
| `engineering-readiness/readiness-check.md` with Ready | stage 8 |
| `quality-gates/bdd/acceptance-checklist.md` missing or not Accepted | stage 9b |
| `quality-gates/test-plans/` missing or empty | stage 9f |
| `quality-gates/test-strategy.md` missing or not Accepted | stage 10 |
| Any triggered gate not `triggered-complete` | stage 13 |
| `planning/software-modules.md` missing AND delivery_mode = Enterprise + Modular | stage 4a |
| `planning/capability-to-module-map.md` missing AND delivery_mode = Enterprise + Modular | stage 4b |
| `planning/delivery-increments.md` missing AND delivery_mode = Enterprise + Modular | stage 4c |

### Consistency check — run after determining current_stage and next_action

Before writing the repaired state file, verify:

1. **Stage consistency:** `next_action.stage` must be at a later position in the gate chain than `current_stage`. If `next_action.stage = "complete"` then `current_stage` must be the last completed stage for this delivery mode. If they contradict: use the gate chain walk result as authoritative — ignore the prior values.

2. **No duplicate keys:** scan the artifacts block for duplicate path keys. If any path appears twice, keep the entry with the lower-trust status (prefer `missing` over `complete`, `incomplete` over `complete`) and log the duplicate in the repair report.

3. **Gate consistency:** `quality_gates_complete` must be a subset of `quality_gates_triggered`. A gate cannot be complete if it was not triggered. Remove any entries in `quality_gates_complete` that are not in `quality_gates_triggered`.

4. **Forced-acceptance gates:** any gate name in `quality_gates_complete` whose corresponding artifact has a forced-acceptance note must be moved from `quality_gates_complete` to `quality_gates_triggered` (triggered but not genuinely complete).

Add a `### Consistency checks` section to the repair report, listing every consistency violation found and how it was resolved.

---

## Step 5 — Write the repaired workflow-state.json

Write `state/workflow-state.json` with:

- All artifact statuses from Step 3 (never copy old values — always use the fresh scan)
- `current_stage` from Step 4
- `next_action` from Step 4 (stage + prompt path + one-sentence reason)
- `next_skill` pointing to the correct persona + skill for `next_action`
- `stale_artifacts` listing every artifact where status = `stale`
- `blocking_issues` listing any blocking decisions
- `quality_gates_triggered` and `quality_gates_complete` updated from the readiness-check.md scan
- `state_validated: true` — only set this after you have physically read every artifact file above
- `last_updated` = today's date in ISO-8601
- `updated_by` = "orchestrator.repair_workspace_state"

**Preserve** `delivery_mode`, `execution_mode`, and `readiness_decision` from the original file if they were set and you found matching evidence on disk. If contradicted by artifact content, use the artifact content.

---

## Step 6 — Produce a repair report

After writing the state file, output a short repair report in this format:

```
## Workspace Repair Report — {{initiative ID}}

### Artifacts scanned: {{N}}
### Problems found: {{N}}

| Artifact | Old status | New status | Reason |
|---|---|---|---|
| ... | ... | ... | ... |

### Premature artifacts (produced without prerequisites)
{{list any quality gate or downstream artifacts that were created before their prerequisites were complete}}

### Next action
Stage: {{stage number and name}}
Skill: {{skill ID}}
Prompt: {{prompt path}}
Reason: {{one sentence}}

### What the workflow will do next
{{2–3 sentences describing what happens when the workflow runner picks up from the repaired state}}
```

Do not generate any framework content beyond this report and the repaired `state/workflow-state.json`. The workflow runner takes it from here.

---

## Anti-patterns — never do these

- Do not create business-rules, actors, process flows, or any other framework artifact in this prompt
- Do not set `next_action` to a downstream stage while prerequisites are missing
- Do not set `state_validated: true` without reading every artifact file
- Do not copy old status values from the corrupted state file
- Do not mark a quality gate `triggered-complete` if its prerequisites were missing when it was created
- Do not ask "shall I proceed?" — write the repair report and stop
