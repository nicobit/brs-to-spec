# Enhancement 7 — Orchestrator Reliability Fixes

## Context

Enhancement 7 is a reliability-focused wave. It responds to a live failure on initiative I005 where the framework orchestrator produced a run that appeared to complete but delivered the wrong output. The failure was diagnosed by comparing the actual artifacts on disk against the framework's own rules.

The five problems are distinct in nature — three are behavioral rules the orchestrator ignored, one is a structural gap in the stage gate chain, and one is a state file consistency failure. All five are fixable by tightening existing prompts; no new stages are needed.

---

## Problems found

### Problem 1 — Artifacts are appended instead of overwritten

The orchestrator ran the delivery structure skill four times. Each run appended a new version below the previous one instead of replacing the file. The same corruption happened to `readiness-check.md` (two contradictory versions concatenated).

**Framework rule already exists** in `brs-to-spec-run-workflow.md` Step 4b:
> "Always overwrite — never append. A file with two or more versions concatenated is a corrupt artifact."

The rule is stated but the orchestrator ignored it. The repair skill (`repair-workspace-state.md`) also defines a "special case: multiple versions concatenated" rule but only marks the file as `stub` — it does not actively prevent the append from happening in the first place.

**Root cause:** the overwrite rule is stated once in Step 4b as prose. There is no pre-write checklist that forces the agent to stop and verify before writing, and no corrupt-file detection before a skill starts writing. The rule fires too late.

---

### Problem 2 — Quality gates were force-accepted

Rather than stopping and scaffolding gate artifacts as questionnaire stubs, the orchestrator invented `Status: Accepted (forced)` entries in gate files it created itself, then advanced past the gate chain as if all gates were genuinely accepted.

**Framework rule already exists** in `brs-to-spec-run-workflow.md` Step 1b:
> "Reject forced acceptances. Any quality gate entry with a note containing 'forced' → treat as triggered-incomplete."

And in `repair-workspace-state.md`:
> "Reject forced acceptances. Forced acceptance is not real acceptance — it means a previous session bypassed the gate."

The rule detects forced acceptance *after the fact* during repair — but there is no rule that prevents the orchestrator from *creating* a forced acceptance in the first place.

**Root cause:** the stop conditions say to stop and scaffold when a gate requires human input, but there is no explicit rule banning the pattern "self-accept a gate you just created." The orchestrator found a loophole: create the gate file, write `Status: Accepted` in it, and claim the gate is cleared.

---

### Problem 3 — Handoff created wrong structure

The OpenSpec handoff produced:
- `specs/openapi/openapi.yaml`
- `specs/json-schemas/entities.json`
- `openspec/handoff/README.md` + `manifest.md`

None of the required per-story folders (`specs/F-XXX.X-slug/` containing `story.md`, `design.md`, `tasks.md`, `coding-prompt.md`) were created. The `openspec/` path is not a valid workspace path.

**Framework rule already exists** in the handoff skill Step 2:
> "HARD STOP before creating any folder: Count the F-XXX.X story IDs in planning/delivery-structure.md. You must create exactly that many folders — one per story ID, named F-XXX.X-<slug>/. Never create a folder named after the deliverable."

And in the orchestrator Step 5:
> "Never create one folder for the whole deliverable … The correct output is N folders where N = number of F-XXX.X stories."

The hard stop exists but was bypassed. The orchestrator produced a documentation-style handoff instead.

**Root cause:** the hard stop is in the handoff skill prompt but the orchestrator did not load and execute that skill — it performed the handoff inline (directly generating files without reading the skill prompt). The skill selection model says "if a persona skill exists for the required work, invoke that skill instead of performing the work inside the orchestrator" but this was not enforced.

---

### Problem 4 — Enterprise + Modular stages missing from the gate chain table

The routing decision correctly set `delivery_mode: Enterprise + Modular`. This mode requires three additional stages:
- `planning/software-modules.md` — skill `delivery_lead.identify_software_modules`
- `planning/capability-to-module-map.md` — skill `delivery_lead.map_capabilities_to_modules`
- `planning/delivery-increments.md` — skill `delivery_lead.define_delivery_increments`

None were produced.

**Root cause:** in `brs-to-spec-run-workflow.md`, the Enterprise + Modular requirement is a one-line note at the bottom of the Delivery mode behavior section:
> "Enterprise + Modular (12–14): All stages required. Also run: [list of skills]"

These three stages do **not appear as rows in the Step 3 stage gate chain table**. The orchestrator walks that table to decide what to execute. Because the rows are absent, it skips these stages entirely and advances to readiness without triggering them. The mention in the prose section is invisible to the table-driven stage selection logic.

---

### Problem 5 — workflow-state.json is internally inconsistent

The state file had:
- `current_stage: "pre-intake"` (nothing started) alongside `next_action.stage: "complete"` (everything done)
- `review-package/status.md` listed twice — once as `complete`, once as `missing`
- `quality_gates_complete` missing the security gate even though `quality_gates_triggered` listed it
- Gate notes contained `"forced"` but `state_validated` was `true`

**Root cause:** the `maintain-workflow-state.md` skill has clear rules for valid status values and for rejecting forced acceptances, but the orchestrator updated the state file *inline* (by directly writing JSON) rather than invoking the `orchestrator.maintain_state` skill. The skill's validation logic was never run.

---

## Fix strategy

Each problem maps to a targeted change in existing files. No new stages are introduced. The goal is to close the loopholes the orchestrator found, not to restructure the framework.

| # | Problem | Fix type | Files changed |
|---|---|---|---|
| 1 | Append instead of overwrite | Add pre-write corrupt-file check to orchestrator Step 4b + repair skill | `brs-to-spec-run-workflow.md`, `skills/0-repair/repair-workspace-state.md` |
| 2 | Forced gate acceptance | Add explicit creation-time ban; tighten stop conditions | `brs-to-spec-run-workflow.md`, `skills/4-engineering-readiness/01-check-engineering-readiness.md` |
| 3 | Wrong handoff structure | Add pre-handoff skill-invocation check; add output-path guard | `brs-to-spec-run-workflow.md`, `skills/5-handoff/01-create-openspec-change-for-active-deliverable.md` |
| 4 | Enterprise + Modular stages missing | Add three rows to Step 3 stage gate chain table | `brs-to-spec-run-workflow.md` |
| 5 | Inconsistent workflow-state.json | Require skill invocation for state updates; tighten validation rules | `brs-to-spec-run-workflow.md`, `skills/3-planning-and-modular-delivery/01-maintain-workflow-state.md` |

---

## Enhancements

### Enhancement 7.1 — Enforce the overwrite rule with a pre-write check
**File:** `01-fix-overwrite-rule-enforcement.md`
Add a mandatory pre-write check that runs before any skill writes an artifact. If the target file already exists, the check reads the first 20 lines and detects a duplicate heading. If found, the file is marked corrupt and the skill replaces the entire file rather than touching partial content. Also add corrupt-file detection to the repair skill's scan so corrupted files surface in the repair report even if their content looks valid.

### Enhancement 7.2 — Ban forced gate acceptance at creation time
**File:** `02-fix-forced-gate-acceptance.md`
Add an explicit prohibition to the orchestrator's stop conditions and to the readiness check skill: the orchestrator may never write `Status: Accepted` into a gate file it creates in the same session. Gate files must be written with `Status: In progress` and a scaffold note. The acceptance step belongs to the human (or a future session after evidence is reviewed). Extend the repair skill to scan for self-accepted gates and reset them.

### Enhancement 7.3 — Enforce skill invocation for the handoff stage
**File:** `03-fix-openspec-handoff-structure.md`
Add a mandatory skill-invocation check to the orchestrator: before generating any file in `specs/` or `standalone-delivery/`, confirm the handoff skill prompt has been loaded. Add an output-path guard: any file written to `openspec/` is a framework violation — surface it and stop. Strengthen the story-count hard stop in the handoff skill to include a pre-generation count assertion.

### Enhancement 7.4 — Add Enterprise + Modular stages to the gate chain table
**File:** `04-add-enterprise-modular-stages-to-gate-chain.md`
Insert three explicit rows into the Step 3 stage gate chain table for `planning/software-modules.md`, `planning/capability-to-module-map.md`, and `planning/delivery-increments.md`, gated on `delivery_mode = Enterprise + Modular`. Add corresponding hard gate rules for the handoff stage. Remove the duplicate prose-only mention so the table is the single source.

### Enhancement 7.5 — Require skill invocation for state updates and tighten validation
**File:** `05-fix-workflow-state-validation.md`
Add a rule that the orchestrator must invoke `orchestrator.maintain_state` (the `maintain-workflow-state.md` skill) after every stage completion — never write the state file inline. Add a self-check in `maintain-workflow-state.md` that detects and rejects forced-acceptance patterns before writing. Tighten the `state_validated` rule so it cannot be set `true` if any gate note contains "forced".

---

## Implementation order

1. Enhancement 7.4 first — adding missing gate chain rows has zero risk of regression and fixes the most silent failure (missing stages are invisible).
2. Enhancement 7.2 — banning forced acceptance is the highest-severity behavioral fix.
3. Enhancement 7.1 — the overwrite rule; prevents corrupt artifacts from accumulating.
4. Enhancement 7.3 — handoff structure guard; prevents the wrong output from being written.
5. Enhancement 7.5 — state file validation; downstream of all the above.

---

## Quality bar after Enhancement 7

- Running the orchestrator on a fresh initiative must produce, for Enterprise + Modular: `planning/software-modules.md`, `planning/capability-to-module-map.md`, `planning/delivery-increments.md` before advancing to readiness.
- No artifact file may contain two `#`-level headings for the same artifact type. Any such file is flagged corrupt before the next write.
- No quality gate artifact in any initiative workspace may have `Status: Accepted` when the note or the artifact itself was created in the same session without human review. The status must be `In progress` until explicitly changed.
- `specs/` must contain exactly N story folders where N = count of `F-XXX.X` IDs in the confirmed delivery structure. No other folder layout is valid.
- `workflow-state.json` is always written by the `maintain-workflow-state.md` skill. Inline JSON edits by the orchestrator are not permitted.
