# `.b2s` Run Workflow

## Absolute Rules

These rules override everything else. Violating any of them is a failure.

1. **Never expose CLI commands to the user.** You run them silently via your shell tool.
2. **Never ask "Proceed?", "Shall I continue?", or offer menus between steps.** Run continuously.
3. **Never invent your own execution model.** Do not create scripts, dispatch loops, or batch runners. Do not create `.py`, `.sh`, `.js`, or any executable files in `.b2s/tmp/` or anywhere else. Follow the steps below exactly.
4. **Never tell the user to run CLI commands.** You are the executor, not the instructor.
5. **Never report intermediate results** (validation pass/fail, state updates) unless a human gate requires the user's decision.
6. **Only two CLI commands exist for normal execution:** `dispatch-next` and `finalize-action`. Nothing else. Do not run `validate-artifact` or `update-state` separately — `finalize-action` combines both. Do not run `next-step` — `dispatch-next` replaces it.

## CLI Contract

Every "Run" step means: execute via your shell tool.

```
python .b2s/scripts/b2s_cli.py <command> --workspace-root WORKSPACE_ROOT
```

The CLI produces JSON/YAML output files. You read those files. That is the contract.
Do NOT fabricate `.b2s/tmp/` files, skip CLI commands, or guess what they would return.

## Execution Loop

### Step 1 — Identify workspace

Identify the active initiative workspace. Record its absolute path as `WORKSPACE_ROOT`.

### Step 2 — Check for pending gate

Read `WORKSPACE_ROOT/.b2s/state/workflow-state.json`.
If `awaiting_human: true` and `current_gate` is non-null → skip to **Step 7** (Gate Handling).

### Step 3 — Dispatch

**Run:**
```
python .b2s/scripts/b2s_cli.py dispatch-next --workspace-root WORKSPACE_ROOT
```

Read `WORKSPACE_ROOT/.b2s/tmp/dispatch-next.json`.

**Branch on `status`:**

- **`ready`** → go to Step 4.
- **`awaiting_gate`** → go to Step 7.
- **`complete`** → stop. Report "Workflow complete — no further actions."
- **`blocked`** → execute the Blocked Diagnosis Protocol (see below). If resolved, go back to Step 3. If unresolvable, stop and report the blocking reason.

**Integrity warnings:** The dispatch plan may include an `integrity_warnings` array. These are informational diagnostics, not blockers. Only the `status` field determines whether to proceed. Specifically:
- **`unlogged`** warnings mean an action's state was set outside the engine (e.g. in an earlier session). The artifacts exist and the status is valid — proceed normally.
- **`ghost`** or **`missing_artifact`** warnings are auto-repaired by `dispatch-next` before selecting the action. If they persist after dispatch, report them but do not stop unless `status` is `blocked`.

Never stop execution because of integrity warnings when `status` is `ready`.

### Step 4 — Generate the artifact

The dispatch plan provides everything you need:

- `action.rendered_skill_text` — the fully rendered skill prompt. Follow it exactly.
- `action.artifact_template_ref` — the output template. Read it if non-null.
- `action.output_paths` — where to write the artifact.
- `action.prompt_placeholders` — resolved placeholders including `current_item` and `item_folder` for per-item actions.
- The `action` object also contains `required_inputs`, `optional_inputs`, `computed_inputs` with resolved paths.

**Read all resolved inputs before generating.** Computed inputs are authoritative — do not re-derive them.

If `current_item` is present, generate output for ONLY that item.

**`item_folder` is the resolved folder path** (e.g. `epics/E-002-ai-pre-screening-scoring/`). Always use `item_folder` for file paths within the epic — never construct the path manually from `current_item`.

**Quality gate:** If the skill prompt includes a self-verification step, run it BEFORE writing. Do not write stubs that you know will fail validation.

### Step 5 — Finalize

**Run:**
```
python .b2s/scripts/b2s_cli.py finalize-action --workspace-root WORKSPACE_ROOT
```

Read `WORKSPACE_ROOT/.b2s/tmp/finalize-action.json`.

**Branch on `status`:**

- **`validation_failed`** → fix the artifact using the auto-resolve protocol (see below), then run `finalize-action` again. Do NOT go back to Step 3.
- **`gate_pending`** → go to Step 7.
- **`continue`** → check `per_item_boundary`. If `true`, apply the per-item stop rule (see below). Otherwise go back to **Step 3**.
- **`complete`** → stop. Report "Workflow complete — no further actions."

### Step 6 — Advisory reviews (optional)

After `finalize-action` returns `continue` or `gate_pending`, check whether advisory reviews apply:

a. Read `governance/delivery-constitution.md` and check `## Advisory Reviews`.
   If "Advisory reviews enabled" is "No" or absent, skip to Step 3 or Step 7.
b. Read the "Enabled Personas" table to determine which personas are active.
c. Check whether the current action has `advisory_reviews: true` in `stage-actions.yaml`.
   If not, skip.
d. For each enabled persona:
   - Read the advisory review skill from `.b2s/skills/{persona}/advisory-review.md`.
   - Read the primary output artifact and required context files.
   - Generate findings and append to the artifact under `## Advisory Reviews`.
e. Advisory reviews are informational. They do not trigger re-validation.

### Step 7 — Gate handling

Read `workflow-state.json` to get `current_gate`.

**If `current_gate.interaction_mode == "collect_answers"`** — run the Interactive Clarification flow (see below).

**Otherwise** — present a readable summary of the artifact and ask:
**"Do you approve this artifact? Reply `approve` or `reject: <reason>`."**

Wait for the user's response. **Do NOT proceed until the user replies.**

- On **approve**: run `python .b2s/scripts/b2s_cli.py approve-current-gate --workspace-root WORKSPACE_ROOT` (silently — never show this to the user)
- On **reject**: run `python .b2s/scripts/b2s_cli.py reject-current-gate --workspace-root WORKSPACE_ROOT --reason "<reason>"` (silently)

After the gate command completes:
- If approved → go back to **Step 3**.
- If rejected → stop. Report the rejection.

---

## Auto-Resolve Protocol

When `finalize-action` returns `validation_failed`, fix the artifact and retry. **Do not ask the user for permission to fix. Do not report the failures and wait. Apply the fix immediately and run `finalize-action` again.**

**Hard rule — never create new files during auto-resolve.** Only edit the existing artifact that failed validation. Never create placeholder, stub, or wrapper files to satisfy a validator. If coverage is below threshold, report the gap honestly — do not fabricate story files or rename existing files to game the metric.

**Filename preservation rule:** When fixing a story or agent contract, always edit the existing file at its current path. If the failing file is `S-002.0-scoring-e2e.md`, edit that file — do not create `S-002.0.md` alongside it. The same applies to `.agent.yaml` files. List the files in the stories directory first to find the correct filename before writing.

1. Read `finalize-action.json` — the `validation.failures` array contains every failure with its name and detail.
2. **Classify failures:**
   - **Minor** (wrong ID, missing title, count mismatch, missing open question, tag issue) → edit to fix.
   - **Structural** (entire section missing, no Gherkin block, missing required subsections) → regenerate the affected file from scratch using the skill prompt.
3. **Fix:**
   - `no_unknown_requirement_references`: find unknown IDs, remove or replace with canonical IDs from `atomic-requirements.md`.
   - `requirement_title_consistency`: read canonical title from `atomic-requirements.md`, update to match.
   - `open_questions_propagated`: read blocking questions from `atomic-requirements.md`, add to `## Open Questions`.
   - `coverage_claim_matches_evidence`: re-read story files, rebuild matrix from evidence.
   - `requirement_semantics_preserved`: ensure User Story and AC contain keywords from the linked requirement.
   - `coverage_percentage_acceptable`: do NOT create placeholder stories and do NOT game coverage by adding IDs to `## Requirements Referenced`.
     1. Read `.b2s/tmp/computed-coverage.json` — the `suggested_fixes` array contains advisory fix hints for each uncovered or weakly-covered requirement.
     2. If a fix has `action: "needs_implementation_story"`, `"needs_non_spike_implementation_story"`, `"no_epic_assigned"`, or `"no_stories_in_epic"`, these are **not auto-resolvable honestly** without changing delivery scope or story structure. Regenerate `fr-coverage.md` so the gap is reported clearly and evidence-based.
     3. If a requirement is classified as `Referenced Only` or `Spike Only`, keep that status explicit in the coverage report. Do not convert it to `Covered`.
     4. **Delete the stale `fr-coverage.md` and regenerate it from scratch** using the skill prompt. The computed coverage data will be refreshed by the engine on the next `finalize-action`. Do NOT try to patch individual cells in the existing report — the matrix and summary will be inconsistent with the updated story files.
     5. Run `finalize-action` again.
     6. After 3 consecutive failures, stop and report the unresolved coverage gap instead of fabricating stronger traceability.
   - `fr_coverage_no_placeholders`: the validator checks that template placeholders like `{{initiative_id}}`, `{{date}}`, `{{canonical title}}`, `[fill in]`, `Goal Title`, `Actor Name` are **absent** from the final artifact. If this check fails, find and replace all `{{...}}` patterns with real values from the initiative state or computed data. **Never add placeholders to fix this check — remove them.**
   - For any other failure: read the `detail` field and fix accordingly.
4. For structural failures, **rewrite the existing file from scratch** — re-read inputs, re-apply skill instructions, and write the complete replacement to the same file path. Do not create a new file with a different name.
5. Run `finalize-action` again.
6. After **3 consecutive failures on the SAME rule for the SAME file**, stop and report.

---

## Interactive Clarification

When `current_gate.interaction_mode == "collect_answers"`:

**1. Read the clarification request artifact** at `current_gate.artifact_path`. Extract every row from the `## Blocking Questions` table.

Also read `current_gate.clarification_file` if it exists — skip questions already answered there.

**2. Present questions one at a time:**

```
Question [SDQ-001]: <question text>
Context: <why it matters>
Suggested options (if any): <suggested resolution>

What is your answer?
```

Wait for the reply before the next question. Ask follow-ups if the answer is ambiguous. Record "skip" or "I don't know yet" as unresolved.

**3. Write the clarification file** at `current_gate.clarification_file`.

For **solution-design clarifications** (`input/clarifications/solution-design.yaml`):

```yaml
- id: SDQ-001
  answer: <the user's answer>
  answered_at: <YYYY-MM-DD>
  answered_by: human
  rationale: |
    <rationale from user's answer and context>
  owner: <owner from question table>
  artefacts_to_update:
    - <artifact paths to update>
```

For **epic clarifications** (`input/clarifications/E-NNN.yaml`):

```yaml
epic_id: E-NNN
status:
  resolution_mode: <full or partial>
  last_updated: <YYYY-MM-DD>
source_context:
  implementation_contract: epics/E-NNN-<slug>/implementation-contract.md
  ui_specification: architecture/ui-specification.md
answers:
  - question_id: UIQ-NNN
    route: <route>
    page: <page name>
    topic: <topic>
    answer: <answer>
    impact: <impact>
    resolved_by: human
    resolved_at: <YYYY-MM-DD>
unresolved:
  - question_id: UIQ-NNN
    reason: <reason>
```

Merge with existing answers — do not overwrite.

**4. Summarize and ask for approval:**

```
Clarification summary:
- Answered: N questions
- Skipped: M questions

Do you approve these clarifications to continue?
```

**5. On approval, run `approve-current-gate` silently. On rejection, run `reject-current-gate` silently.**

---

## Per-Item Iteration

Some actions run once per item (e.g., one epic at a time). The engine handles item tracking:

- `dispatch-next` returns `current_item`, `pending_items`, and `total_items`
- You generate output for ONLY the `current_item` the engine gives you
- `finalize-action` marks that item as done

**Context isolation rule:** When `finalize-action` returns `per_item_boundary: true` (more items remain), you MUST stop. Report the completed item and remaining count. Each item starts in a fresh conversation to avoid context exhaustion.

---

## Blocked Diagnosis Protocol

When `dispatch-next` returns `status: blocked`:

1. Note `blocking_reason` from the dispatch output.
2. Read `WORKSPACE_ROOT/.b2s/workflow/stage-actions.yaml`.
3. Find the blocking cause (look at `blocked_by_stage` and `blocked_by_action`).
4. Classify each action in the cause stage: `needs_execution`, `stale`, `already_done`, `skipped`, `failed`.
5. Act:
   - `needs_execution` → run `dispatch-next` again (the engine should now select it).
   - `stale` → run `finalize-action` to re-validate, then `dispatch-next`.
   - `failed` → stop and report.
   - All done/skipped → run `repair-state --workspace-root WORKSPACE_ROOT`, then `dispatch-next`.

---

## Source of Truth

Trust:
- `workflow-state.json` for state
- `stage-actions.yaml` for action definitions
- CLI-produced files in `.b2s/tmp/` and `.b2s/state/`

Do NOT trust:
- Your own summaries of what should happen next
- Guessed action statuses
- Manually written state files
