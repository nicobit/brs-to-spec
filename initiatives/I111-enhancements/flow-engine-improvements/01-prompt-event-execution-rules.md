# Prompt 01 — Strengthen event-execution-rules.md Section 2

## Target file

`.flow-engine/instructions/event-execution-rules.md`

## What to do

Read the file first. Then replace Section 2 ("Reading inputs") with the strengthened
version below. Do not change any other section.

## Replacement for Section 2

Replace the existing "## 2. Reading inputs" section with this exact text:

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

**Reading constraint:** read only files listed in `read_from` (plus skill_ref, persona_ref,
artifact_template_ref). Do not read other files during persona mode, even if they seem relevant.

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

For each file that does not exist (optional files only — required missing files stop execution):
- `path` — the path attempted
- `required` — false
- `exists` — false
- `read_at` — ISO-8601 datetime

**This evidence must be recorded at the time of reading, not reconstructed afterwards.**
If the evidence block is absent from the result file, Step 16-G will treat the event as
having skipped Step 10 and will fail it.

---

## Verification

After making the change, confirm:
1. Section 2 now contains the "Read evidence — mandatory" subsection
2. The fields `path`, `required`, `exists`, `lines`, `bytes`, `first_nonempty_line`,
   `read_at`, `matched_files` are all listed
3. No other section was modified
