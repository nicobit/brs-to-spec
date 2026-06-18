# Flow Engine — Event Execution Rules
# Version: 1.0
#
# Governs persona mode behaviour: loading refs, reading inputs, executing,
# and writing the result file. Read by the dispatcher at Step 1.

---

## 1. Loading order

Load in this exact order before executing any task:

1. `skill_ref` — the how. Contains task-specific instructions.
2. `persona_ref` — the who. Contains role definition and quality standards.
3. `artifact_template_ref` — the shape (optional). Contains expected output structure.

**If skill_ref is missing from the event or the file does not exist:**
Write result file: `status: fail`, `failure_reason: "skill_ref not found: <path>"`. Stop. Do not execute.

**If persona_ref file does not exist:**
Derive default: `.brs2spec2/personas/<persona>.md` using the `persona` field.
If the default also does not exist: write result file with `failure_reason: "persona_ref not found"`. Stop.

**If artifact_template_ref does not exist:**
Log in result file `notes`: "artifact_template_ref not found — proceeding without template."
Continue. The template is optional.

---

## 2. Reading inputs

Read `read_from` files in list order before writing any output.

**Required files** (listed in the event's `required_inputs` field):
- Must exist on disk before execution starts.
- If missing: write result file `status: fail`, `failure_reason: "required input missing: <path>"`. Stop.

**Optional files** (listed in the event's `optional_inputs` field, or in `read_from`
but absent from `required_inputs`):
- Skip silently if not found.
- Note skipped optional files in result file `notes`.

**Glob patterns** (e.g. `input/brs/*.md`):
- Read all matching files as a set.
- If the glob is required and no files match: treat as missing required input.
- If the glob is optional and no files match: skip silently.

**Reading constraint:** read only files listed in `read_from` (plus skill_ref, persona_ref, artifact_template_ref). Do not read other files during persona mode, even if they seem relevant.

**Read evidence — mandatory for every file read:**

After reading each file (or attempting to read it), immediately record the following
observable evidence. This evidence is written into the result file at Step 15 as the
`read_evidence` block — one entry per `read_from` item.

For each file successfully read:
- `path` — the exact path from `read_from` (or resolved glob path)
- `required` — true if in `required_inputs`, false otherwise
- `exists` — true
- `lines` — total number of lines in the file
- `bytes` — approximate byte count (character count is acceptable)
- `first_nonempty_line` — the first line that is not blank or whitespace-only
- `read_at` — ISO-8601 datetime of the read

For each glob pattern:
- `path` — the glob pattern as written in `read_from`
- `required` — true/false
- `matched_files` — list of file paths that matched (empty list if none)
- `read_at` — ISO-8601 datetime

For each optional file that does not exist:
- `path` — the path attempted
- `required` — false
- `exists` — false
- `read_at` — ISO-8601 datetime

**This evidence must be recorded at the time of reading, not reconstructed afterwards.**
If the evidence block is absent from the result file, Step 16-G will treat the event as
having skipped Step 10 and will fail it.

---

## 3. Execution constraints (persona mode)

While executing (steps 10–15 of dispatch):

- Adopt the persona's role and quality standards from `persona_ref`.
- Follow `skill_ref` instructions exactly for this task type.
- Use `artifact_template_ref` as the structural contract for output shape.
- Write **only** to the paths listed in `write_to`. No other paths.
- **Always overwrite** when writing to a `write_to` path. If a file already exists at that path, replace its full content. Never append to an existing file — appending produces doubled or corrupted artifacts when re-running after a crash.
- **Folder outputs** (path ends with `/`): write one file per entity (e.g. `UC-001.md`) inside the folder. Never merge all entities into a single file.
- Do **not** update any `.flow/state/` files. Not workflow-state.json, not event-log.jsonl, not open-decisions.md.
- If information needed to complete the task is not available in `read_from` files: produce what can be produced, note the gap in result file `notes`, set result status to fail if a required section cannot be populated.
- Do not invent facts not present in source files.

---

## 4. Result file requirements

Write `.flow/events/processing/<event_id>-result.yaml` before switching to orchestrator mode.
The result file must contain:

- `event_id` — matching the event being processed
- `status` — `pass` (tentative; may be changed to `fail` after validation in step 16)
- `completed_at` — current ISO-8601 datetime
- `artifacts_written` — every file path written to disk (empty list `[]` if nothing written)
- `failure_reason` — present and specific if any failure occurred during execution
- `notes` — optional; skipped optional inputs, assumptions made, partial content warnings

Do not set `validation_notes` or `events_created` — these are added by the orchestrator.

---

## 5. Done criteria by event type

What constitutes a complete, valid execution for each event type:

| Event type | Execution is complete when |
|---|---|
| `CREATE_ARTIFACT` | Every path in `write_to` exists on disk and is not empty or heading-only |
| `UPDATE_ARTIFACT` | Every path in `write_to` exists and its content differs from pre-execution state |
| `VALIDATE_ARTIFACT` | No new file required; result file includes explicit `pass` or `fail` judgement on the artifact reviewed, with reasoning |
| `REVIEW_ARTIFACT` | At least one finding document written to `write_to`; each finding has a Finding ID (FND-NNN) |
| `RAISE_DECISION` | At least one entry written to `.flow/state/open-decisions.md` with ID, question, owner, and blocking flag |
| `RESOLVE_DECISION` | The referenced decision entry in `open-decisions.md` has been updated with `resolved_at` and `resolution` fields |
| `GENERATE_HANDOFF` | All paths in `write_to` exist — dependency graph and all story folders with required files |
| `ENRICH_ARTIFACT` | Every path in `write_to` exists; the sections listed in `must_include` are present and populated |
| `REPAIR_ARTIFACT` | Every path in `write_to` exists; the validation rules that previously failed now pass |
| `ROUTE_INITIATIVE` | `write_to` artifact exists; `delivery_mode` and `execution_mode` fields are populated with allowed values |
| `RETRY_FAILED_TASK` | Apply the done criteria of the original event type being retried |
| `WAIT_HUMAN` | Human has replied 'approved' or 'rejected: <reason>' (handled by Step 6a — never enters persona mode) |

**Content over existence rule:** an artifact that exists but is empty, heading-only, or stub-only (contains only template headings with no real content) is not complete. It must have substantive content in every required section.
