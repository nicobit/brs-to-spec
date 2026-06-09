# Prompt — Maintain Workflow State

## Role

You are a delivery lead maintaining a compact machine-readable snapshot of the initiative's workflow state.

## Purpose

`planning/workflow-state.json` is a small file that Copilot reads first on every session to understand the current stage, artifact statuses, and blocking issues — without scanning 10+ full markdown files. This saves tokens and prevents Copilot from misreading artifact presence as artifact completeness.

Run this prompt after every stage that changes artifact status, readiness, or decisions.

## Workspace rule

Work inside one initiative workspace at a time. All relative paths are relative to:

```text
initiatives/<initiative-id>-<slug>/
```

## Output path

```text
planning/workflow-state.json
```

## Template

```text
templates/planning/workflow-state.json
```

## How to update the state

### Step 1 — Read planning/open-decisions.md

Set:
- `open_decisions.blocking_count` = count of rows where Blocking = Yes and Status ≠ Resolved
- `open_decisions.non_blocking_count` = count of rows where Blocking = No and Status ≠ Resolved
- `open_decisions.resolved_count` = count of rows where Status = Resolved

### Step 2 — Check each artifact and set its status

For every artifact in the `artifacts` map, read the file (if it exists) and assign one of these status values:

| Status | Meaning |
|---|---|
| `missing` | File does not exist |
| `stub` | File exists but contains only headings, empty tables, or placeholder text |
| `stale` | File exists with content but still shows resolved decisions as open, or still carries DRAFT after sign-off, or still says Not ready when blockers are cleared |
| `incomplete` | File exists and is current but fails its done criteria (e.g. delivery-structure with one story per feature) |
| `complete` | File exists, is current, and passes all done criteria |
| `not-triggered` | Quality gate file — not triggered for this initiative |
| `triggered-incomplete` | Quality gate triggered but not yet complete |
| `triggered-complete` | Quality gate triggered and complete with sign-off |

Use the `note` field to record the specific reason for any status that is not `complete` or `not-triggered`. Keep notes to one line.

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

### Step 5 — Set state_validated = true and last_updated

Set `state_validated` to `true` only when you have physically read every artifact file in this session, not just checked for existence. Set `last_updated` to today's date. Set `updated_by` to the prompt name or session identifier.

## Staleness detection rules

An artifact is `stale` if any of these are true:

| Artifact | Stale condition |
|---|---|
| `input/architecture.md` | Open Decisions table still lists D-NNN rows as open when Resolved in register; or DRAFT notice present when OD-006 Resolved |
| `architecture/architecture-rules.md` | Contains AR-OPEN-NNN entries when corresponding decision is Resolved |
| `engineering-readiness/readiness-check.md` | Says Not ready when all blocking issues listed in it are Resolved in register |
| Any artifact | Contains "TBC", "(decision pending)", or open decision placeholder for a Resolved decision |

## Done criteria (for setting status = complete)

| Artifact | Done criteria |
|---|---|
| `routing/routing-decision.md` | Delivery mode, execution mode, and rationale all stated |
| `business-intake/business-intake-summary.md` | Objectives with measures; requirements with IDs; gaps with owners |
| `architecture/architecture-review.md` | Initiative-specific constraints; open decisions with owners |
| `architecture/architecture-rules.md` | Binding rules with IDs; no AR-OPEN-* remaining for resolved decisions |
| `planning/open-decisions.md` | All decisions present; blocking summary current |
| `planning/delivery-structure.md` | Every feature has at least one well-formed user story; single-story features include a splitting justification; every story traceable to requirement ID |
| `engineering-readiness/readiness-check.md` | Explicit Ready/Not ready; every triggered gate listed; no placeholder owners |
| `engineering-readiness/initiative-context.md` | No empty rows; specific technology choices; all resolved decisions reflected |
| Quality gates | Real content, named reviewer, completed acceptance checklist |
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
