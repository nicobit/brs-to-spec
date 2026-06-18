# BRS-to-Spec v2 — Reset To Phase

Use this prompt when:
- The user says "reset to phase", "rewind to business analysis", "start again from planning", or similar
- The initiative has a `.flow/` workspace, but the user wants the queue and state rebuilt as if a chosen phase were now the starting point
- The user explicitly wants a rewind, not just a safe resume

This prompt does NOT delete `input/`.
It does NOT delete business artifacts outside `.flow/`.
It resets workflow state and clears active queue folders so the requested phase becomes the new active starting point.

Operational meaning of this reset:
- reset `.flow/state/workflow-state.json`
- reset `.flow/state/event-log.jsonl`
- reset `.flow/state/open-decisions.md`
- clear `.flow/events/pending/`
- clear `.flow/events/processing/`
- leave business artifacts on disk untouched
- leave historical `done/` and `failed/` event files untouched unless they are explicitly backed up by this prompt

---

## Step 0 — Collect missing values with bounded suggestions

If the user did not clearly provide both:
- the initiative workspace
- the target phase

then stop and ask for them in one compact message.

Build the suggestions from the repo state:
- initiative suggestions: list up to 3 likely initiative folders, preferring the most recently modified v2 workspaces
- phase suggestions: always use the supported phase list below

Use exactly this format:

```text
Reset-to-phase needs two values:

Initiative:
1. <most likely initiative>
2. <second likely initiative>
3. <third likely initiative or "latest active initiative">

Phase:
1. business analysis
2. planning
3. engineering readiness
4. quality gates
5. handoff

Reply in one line, for example:
reset I008-TEST4 to business analysis
```

Do not continue until the user replies.

If the user provided one value but not the other:
- keep the provided value
- ask only for the missing value using the same bounded style

---

## Supported phase names

Map the user's request to one of these canonical reset targets:

| User phrasing | Canonical target |
|---|---|
| after business intake, business analysis, requirements/use cases | `2b-business-analysis` |
| architecture, planning | `3-planning` |
| engineering readiness, readiness | `4-engineering-readiness` |
| quality gates, bdd/contracts/security | `4b-quality-gates` |
| handoff, openspec, standalone package | `5-handoff` |

If the user names a phase outside this list, stop:
**"Unsupported reset target: [user text]. Use one of: business analysis, planning, engineering readiness, quality gates, handoff."**

---

## Step 1 — Identify the initiative workspace

1. If the user named an initiative, locate `initiatives/<id>*/`.
2. Otherwise scan `initiatives/` and select the workspace with `.flow/` most recently modified.
3. Set `workspace_root = initiatives/<workspace_name>/`.

If no v2 workspace is found, stop:
**"No v2 initiative workspace found. Use 'new initiative' or 'restart' first."**

---

## Step 2 — Verify inputs and read current state

Confirm that at least one of these exists and is not empty:
- `<workspace_root>/input/brs.md`
- `<workspace_root>/input/brs/*.md`

If not, stop:
**"input/ has no BRS content. Add your BRS to input/brs.md before resetting to a phase."**

Read existing `<workspace_root>/.flow/state/workflow-state.json` if present and preserve:
- `delivery_mode`
- `execution_mode`
- `project_type`
- `created`

If the state file is missing, preserve `null` for the mode fields and use today for `created`.

---

## Step 3 — Validate prerequisites for the requested reset target

Resetting to a later phase is only allowed if the required upstream business artifacts already exist on disk.

### Target = `2b-business-analysis`

Required upstream artifacts:
- `business-intake/business-intake-summary.md`

If missing, stop:
**"Cannot reset to business analysis: business-intake/business-intake-summary.md is missing. Reset to an earlier phase or regenerate business intake first."**

### Target = `3-planning`

Required upstream artifacts:
- `business-analysis/requirements.md`
- `business-analysis/use-cases.puml`
- `business-analysis/gaps-and-questions.md`

If any are missing, stop:
**"Cannot reset to planning: required business-analysis artifacts are missing. Reset to business analysis first."**

### Target = `4-engineering-readiness`

Required upstream artifacts:
- `planning/delivery-structure.md`
- `architecture/architecture-review.md`

If either is missing, stop:
**"Cannot reset to engineering readiness: planning prerequisites are missing. Reset to planning first."**

### Target = `4b-quality-gates`

Required upstream artifacts:
- `engineering-readiness/readiness-check.md`

If missing, stop:
**"Cannot reset to quality gates: readiness-check.md is missing. Reset to engineering readiness first."**

### Target = `5-handoff`

Required upstream artifacts:
- `engineering-readiness/readiness-check.md`

If missing, stop:
**"Cannot reset to handoff: readiness-check.md is missing. Reset to engineering readiness first."**

---

## Step 4 — Archive the existing queue/state snapshot

Before changing anything:

1. Create `<workspace_root>/.flow/backups/` if it does not exist.
2. Create a timestamped backup folder:

```
.flow/backups/reset-to-phase-YYYYMMDD-HHMMSS/
```

3. Copy these into that backup folder if they exist:
- `.flow/state/workflow-state.json`
- `.flow/state/event-log.jsonl`
- `.flow/state/open-decisions.md`
- `.flow/events/pending/`
- `.flow/events/processing/`

Do not skip the backup step.

---

## Step 5 — Clear active queue folders only

Delete all files from:
- `.flow/events/pending/`
- `.flow/events/processing/`

Leave the folders themselves in place.
Do not touch `.flow/backups/`.
Do not delete files from `done/` or `failed/`.

---

## Step 6 — Rebuild workflow-state.json for the chosen phase

Write a new `.flow/state/workflow-state.json` with:

- `initiative_id`: preserved from previous state or workspace name
- `created`: preserved if known
- `current_stage`: the target phase
- `delivery_mode`: preserved
- `execution_mode`: preserved
- `project_type`: preserved
- `readiness_score`: null
- `quality_gates_triggered`: []
- `optional_artifacts_requested`: []
- `artifact_status`: rebuild minimally from the prerequisite artifacts for the target phase, marking each as:
  - `accepted` for `routing/routing-decision.md` and the business-intake gate-reviewed summary when applicable
  - `ai_validated` for other prerequisite artifacts that exist on disk
- `event_counter`: start from 1 and reassign fresh runtime EVT IDs for the new queue
- `active_events`: list of the newly instantiated pending EVT IDs
- `failed_events`: []
- `last_completed_event`: null
- `open_decisions`: 0
- `blocking_decisions`: 0
- `last_updated`: now

Also reset:
- `.flow/state/event-log.jsonl` to empty
- `.flow/state/open-decisions.md` to a fresh empty header table

This is a queue/state reset. Old active state is intentionally moved to backup rather than preserved as active state.
Historical `done/` and `failed/` folders remain on disk for inspection only and are no longer treated as authoritative active state after the reset.

---

## Step 7 — Instantiate the phase-entry events

Instantiate fresh runtime events into `.flow/events/pending/` for the requested target.

Use the full field mapping rules from:
- `.flow-engine/instructions/template-instantiation-rules.md`

For every instantiated runtime event, perform both checks:
- pre-write: verify `must_include`, `validation_rules`, `on_success`, and `on_failure` were copied from the template where present
- post-write: read the event back and verify the `must_include` count matches the template exactly

If either check fails, stop and fix the instantiation before continuing.

### Target = `2b-business-analysis`

Instantiate:
- `EVT-TPL-043` create requirements

Do not instantiate downstream business-analysis events yet. They should be created by normal `on_success` chaining from requirements and use-case diagram events.

### Target = `3-planning`

Instantiate:
- `EVT-TPL-008` review initial architecture

If `project_type == brownfield`, also instantiate:
- `EVT-TPL-010` review existing system impact

Do not instantiate delivery-structure yet unless the queue model already expects it from the chain after architecture review.

### Target = `4-engineering-readiness`

Instantiate:
- `EVT-TPL-015` check engineering readiness

### Target = `4b-quality-gates`

Instantiate only the quality-gate templates that are applicable from the current readiness artifact and state.
If gate applicability cannot be determined safely from `readiness-check.md` and state alone, stop:
**"Cannot reset to quality gates safely: triggered gates are not explicit enough. Reset to engineering readiness first."**

### Target = `5-handoff`

Instantiate the correct handoff event based on preserved `delivery_mode`:
- `OpenSpec` → `EVT-TPL-024`
- `Standalone` → `EVT-TPL-025`
- `FastPath` → `EVT-TPL-026`

If delivery mode is missing or incompatible, stop:
**"Cannot reset to handoff: delivery_mode is unknown or incompatible. Reset to routing or planning first."**

After instantiating all target events:
- set `active_events`
- set `event_counter` to the highest assigned EVT number

---

## Step 8 — Report

```
Phase reset complete: <workspace_name>
Target phase:         <canonical target>
Backup created at:    .flow/backups/reset-to-phase-YYYYMMDD-HHMMSS/
Queue rebuilt with:   <list of EVT-IDs and titles>
Current stage:        <canonical target>
Event counter:        <N>
done/ and failed/:    preserved
Artifacts on disk:    untouched

Say "dispatch-next" to continue one event, or "dispatch-all" to continue the flow.
```

Nothing else. No menus. No extra options.

---

## Stop conditions

- Do not delete `input/` or anything inside it
- Do not delete business artifacts outside `.flow/`
- Do not reset to a phase whose prerequisite artifacts are missing
- Do not bypass WAIT_HUMAN by pretending a gate was approved if its reviewed artifact does not already exist
- Do not preserve old event-log or open-decisions as active state after a phase reset; move them to backup instead
- Do not delete `done/` or `failed/` during this reset
