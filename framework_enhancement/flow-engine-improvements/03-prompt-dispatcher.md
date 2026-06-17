# Prompt 03 — Update dispatcher.md Steps 10 and 16-G

## Target file

`.flow-engine/instructions/dispatcher.md`

## Context

This change has two parts:
1. Strengthen Step 10 to require recording read_evidence at read time
2. Add read_evidence validation to Step 16-G (result contract checks)

Read the full file before making changes. Make only the two edits described below.

---

## Edit 1 — Step 10

Find the existing Step 10 section:

```
### Step 10 — Read input files
```

At the end of Step 10 (after the existing bullet points and before the MODE boundary
comment), add this paragraph:

---

**Read evidence recording — mandatory:**

As each file is read, immediately record the following for inclusion in the result file
`read_evidence` block at Step 15:
- `path`: exact path from `read_from`
- `required`: true if in `required_inputs`, false otherwise
- `exists`: true/false
- `lines`: line count (for existing files)
- `bytes`: approximate byte count (for existing files)
- `first_nonempty_line`: first non-blank line (for existing files)
- `read_at`: current ISO-8601 datetime

For glob patterns: record `matched_files` (list of resolved paths) instead of
`lines`/`bytes`/`first_nonempty_line`.

This evidence is NOT optional. If the result file reaches Step 16-G without a
`read_evidence` entry for every `read_from` item, the event will be failed automatically.

---

## Edit 2 — Step 16-G (result contract checks)

Find the existing Step 16-G section (or the section that lists result contract checks
before proceeding to Step 17). Add these checks to the existing list:

---

**read_evidence checks (add to Step 16-G contract validation):**

4. **read_evidence count check:** if the event has a non-empty `read_from` list,
   count the `read_from` items and count the `read_evidence` entries in the result file.
   If `read_evidence` is absent or the count is less than the `read_from` count:
   - set `status: fail`
   - set `failure_reason: "read_evidence incomplete: event has [N] read_from items but
     result file has [M] read_evidence entries. Step 10 was not fully executed."`

5. **generic emptiness claim check:** if result `status` is `fail` AND `failure_reason`
   contains a generic emptiness or content-quality claim (e.g. "no extractable content",
   "no requirements found", "BRS is empty", "insufficient content", "source file does
   not contain"):
   - find the corresponding `read_evidence` entry for the referenced input file
   - if the entry shows `exists: true` AND `lines > 20`:
     - the generic claim is invalid — a file with 20+ lines is not empty
     - note: this does NOT mean the file is semantically sufficient — it means a
       generic "empty file" claim is not acceptable for a non-empty file
     - set `status: fail` (keep fail, but replace the reason)
     - set `failure_reason: "generic emptiness claim rejected: '[original reason]' —
       read_evidence shows [path] exists with [lines] lines. A non-empty file requires
       a specific failure_reason quoting the sections found and explaining exactly what
       was missing or insufficient. Re-run with a specific failure_reason."`
   - if the entry shows `exists: true` AND `lines <= 20`:
     - the claim may be plausible but still requires specificity
     - `failure_reason` must quote at least one specific line from the file
     - if no specific line is quoted: same rejection as above

6. **first_nonempty_line contradiction check:** if `read_evidence` shows a meaningful
   `first_nonempty_line` (e.g. `"# Business Requirements Specification"`) AND
   `failure_reason` claims the file was empty or had no content:
   - this is a direct contradiction — a file with a meaningful first line is not empty
   - set `failure_reason: "contradictory failure: read_evidence shows first_nonempty_line
     '[value]' for [path] but failure_reason claims the file was empty or had no content.
     These cannot both be true. Re-run with honest failure evidence."`

7. **required input missing vs exists mismatch:** if `read_evidence` shows
   `exists: true` for a path but `failure_reason` claims that path was missing:
   - set `failure_reason: "contradictory failure: read_evidence shows [path] exists
     but failure_reason claims it was missing. Investigate and re-run."`

---

## Verification

After making the change, confirm:
1. Step 10 ends with the "Read evidence recording — mandatory" paragraph
2. Step 16-G contains checks 4 (count), 5 (generic emptiness), 6 (first_nonempty_line
   contradiction), and 7 (exists vs missing mismatch)
3. Check 5 uses the phrase "generic emptiness claim" — not "suspicious failure"
4. Check 5 notes that lines > 20 rules out "empty file" claims but NOT semantic failure
5. The field names in the dispatcher match exactly those in the schema:
   `path`, `required`, `exists`, `lines`, `bytes`, `first_nonempty_line`, `read_at`,
   `matched_files`
6. No existing Step 10 bullets or Step 16-G checks were removed
