# Prompt — Maintain Workflow State

## Role

You are a delivery lead maintaining a compact machine-readable snapshot of the initiative's workflow state.

## Purpose

`state/workflow-state.json` is a small file that Copilot reads first on every session to understand the current stage, artifact statuses, and blocking issues — without scanning 10+ full markdown files. This saves tokens and prevents Copilot from misreading artifact presence as artifact completeness.

Run this prompt after every stage that changes artifact status, readiness, or decisions.

## Workspace rule

Work inside one initiative workspace at a time. All relative paths are relative to:

```text
initiatives/<initiative-id>-<slug>/
```

## Output path

```text
state/workflow-state.json
```

## Template

```text
.brs2spec/templates/state/workflow-state.json
```

## How to update the state

### Step 1 — Read state/open-decisions.md

Set:
- `open_decisions.blocking_count` = count of rows where Blocking = Yes and Status ≠ Resolved
- `open_decisions.non_blocking_count` = count of rows where Blocking = No and Status ≠ Resolved
- `open_decisions.resolved_count` = count of rows where Status = Resolved

### Step 1b — Set Enterprise + Modular artifact statuses

After reading `state/routing-decision.md` (or determining delivery mode from context), check whether `delivery_mode` contains "Modular". If yes:

- Change the status of `planning/software-modules.md` from `not-triggered` to `missing` (if the file does not exist) or its actual content-based status (if the file exists).
- Change the status of `planning/capability-to-module-map.md` from `not-triggered` to `missing` or actual status.
- Change the status of `planning/delivery-increments.md` from `not-triggered` to `missing` or actual status.

These three entries default to `not-triggered` in the template but must be treated as required stages once the routing decision confirms Enterprise + Modular mode.

### Step 2 — Populate quality_gates_triggered from readiness-check.md

Before checking individual artifact statuses, read `engineering-readiness/readiness-check.md` (if it exists) and parse its **Triggered Quality Gates** table. For every row in that table where the gate is listed as triggered (i.e. not "Not triggered"):

- Add the gate name to `quality_gates_triggered` if it is not already present.
- Do this regardless of whether the gate artifact file exists yet — a gate that is triggered but not yet created is still triggered.

This ensures `quality_gates_triggered` reflects what the readiness check decided, not just what files happen to exist.

### Step 2b — Check each artifact and set its status

For every artifact in the `artifacts` map, read the file (if it exists) and assign one of these status values:

| Status | Meaning |
|---|---|
| `missing` | File does not exist |
| `stub` | File exists but contains only headings, empty tables, or placeholder text |
| `stale` | File exists with content but still shows resolved decisions as open, or still carries DRAFT after sign-off, or still says Not ready when blockers are cleared |
| `incomplete` | File exists and is current but fails its done criteria (e.g. delivery-structure with one story per feature) |
| `corrupt` | File exists but contains multiple versions concatenated (top-level heading appears more than once); content cannot be trusted; must be regenerated |
| `complete` | File exists, is current, and passes all done criteria |
| `not-triggered` | Quality gate file — not triggered for this initiative |
| `triggered-incomplete` | Quality gate triggered but not yet complete |
| `triggered-complete` | Quality gate triggered and complete with sign-off |

Use the `note` field to record the specific reason for any status that is not `complete` or `not-triggered`. Keep notes to one line.

**Never use any other status value.** Values like `present`, `exists`, `created`, `scaffolded`, `ok` are not valid — they prevent the orchestrator from assessing stage readiness and will cause the state file to be treated as unvalidated on the next run.

### Step 3 — Build stale_artifacts list

List every artifact path where status = `stale`. This is what Copilot reads to know what to fix first.

### Step 4 — Set current_stage and next_action

`current_stage` = the last stage where all artifacts are `complete` or `not-triggered`.

`next_action.stage` = the first stage where an artifact is not `complete`.
`next_action.prompt` = the `.brs2spec/` prompt path for that stage.
`next_action.reason` = one sentence explaining why this is the next action.

Priority order for next_action:
1. If `open_decisions.blocking_count` > 0 → next_action is "resolve-blocking-decisions"
2. If `stale_artifacts` is non-empty → next_action is "fix-stale-artifacts"
3. Otherwise → first incomplete stage in the workflow sequence

### Step 5 — Update artifact_timestamps

For every artifact whose status changed to `complete` or `stale` in this session, set its entry in `artifact_timestamps` to the current UTC datetime in ISO-8601 format (e.g. `"2026-06-12T14:30:00Z"`). Do not update timestamps for artifacts you did not read in this session — leave their existing value unchanged. Timestamps are used by drift detection (Step 2 of the orchestrator) to determine objectively whether a downstream artifact predates an upstream change.

### Step 6 — Set state_validated and last_updated

Set `state_validated` to `true` **only when ALL of the following are true:**

1. You have physically read (opened and checked content of) every artifact file listed in the `artifacts` block.
2. No artifact has status `corrupt`. A corrupt artifact cannot be read reliably — set `state_validated: false` if any `corrupt` entries exist.
3. No quality gate has a note containing any of these patterns: `"forced"`, `"force-accepted"`, `"Accepted (forced)"`, `"force accepted"`. If any gate note matches: set `state_validated: false`. A state file with forced-acceptance notes is not validated — it is a record of a bypass.
4. `current_stage` and `next_action.stage` are logically consistent:
   - `next_action.stage` must be at a later position in the gate chain than `current_stage`, OR equal to `current_stage` if the stage is still in progress.
   - If `next_action.stage = "complete"` then `current_stage` must be the last required stage for the delivery mode (not `"pre-intake"`, `"routing"`, or any early stage).
   - If these contradict each other: set `state_validated: false`; add a `_validation_errors` entry explaining the contradiction.
5. No artifact path appears more than once in the `artifacts` block. Duplicate keys indicate a JSON merge error — remove the duplicate and keep the entry with the less-trusting status (prefer `missing` over `complete`, `incomplete` over `complete`).

**If any of conditions 1–5 fail:** set `state_validated: false`. Add a `_validation_errors` array to `workflow-state.json` listing each failure reason. The orchestrator will detect `state_validated: false` on the next session and trigger a full artifact scan before advancing.

Set `last_updated` to today's date in ISO-8601. Set `updated_by` to `"orchestrator.maintain_state"` (never `"orchestrator.run"` — the maintain skill, not the orchestrator, owns the state file).

## Staleness detection rules

An artifact is `stale` if any of these are true:

| Artifact | Stale condition |
|---|---|
| `input/architecture.md` | Open Decisions table still lists D-NNN rows as open when Resolved in register; or DRAFT notice present when OD-006 Resolved |
| `architecture/architecture-rules.md` | Contains AR-OPEN-NNN entries when corresponding decision is Resolved |
| `engineering-readiness/readiness-check.md` | (a) Says Not ready when all blocking issues listed in it are Resolved in register; OR (b) Says Not ready when every gate in its Triggered Quality Gates table has `Status: Accepted` in its gate artifact file — read each gate file to verify. When stale for reason (b): set status to `stale`, add to `stale_artifacts`, and set `next_action` to re-run `skills/4-engineering-readiness/01-check-engineering-readiness.md`. |
| Any artifact | Contains "TBC", "(decision pending)", or open decision placeholder for a Resolved decision |

## Done criteria (for setting status = complete)

| Artifact | Done criteria |
|---|---|
| `state/routing-decision.md` | Delivery mode, execution mode, and rationale all stated |
| `business-intake/business-intake-summary.md` | Objectives with measures; requirements with IDs; gaps with owners |
| `architecture/architecture-review.md` | Initiative-specific constraints; open decisions with owners |
| `architecture/architecture-rules.md` | Binding rules with IDs; no AR-OPEN-* remaining for resolved decisions |
| `state/open-decisions.md` | All decisions present; blocking summary current |
| `planning/delivery-structure.md` | Every feature has at least one well-formed user story; single-story features include a splitting justification; every story traceable to requirement ID |
| `engineering-readiness/readiness-check.md` | Explicit Ready/Not ready; every triggered gate listed; no placeholder owners. Status is stale (not complete) if it says Not ready but all triggered gates are now Accepted — see staleness detection rules above. |
| `engineering-readiness/initiative-context.md` | No empty rows; specific technology choices; all resolved decisions reflected |
| Quality gates | Real content; `Status: Accepted` in the Metadata table at the top of the file — not "Accepted (forced)" or any forced variant. No named reviewer required — the git commit is the audit trail. A gate with "forced" in its Status or note is `triggered-incomplete`, not `triggered-complete`. |
| Handoff | Proposal + design + tasks all have real content traceable to stories |

## Quality bar

A good workflow-state.json must:

- Reflect the actual file content — not just file existence
- Have `state_validated: true` only when content was physically read
- Have `stale_artifacts` listing every artifact that needs fixing
- Have `next_action` pointing to the highest-priority unblocked action
- Never set an artifact to `complete` when it has stub content or stale decisions

## Anti-patterns

- Do not set `state_validated: true` without reading file content
- Do not set status to `complete` based on file existence alone
- Do not leave `stale_artifacts` empty when upstream artifacts have unresolved open decisions
- Do not set `next_action` to a quality gate stage while stale artifacts exist
