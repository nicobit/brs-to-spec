# Validation Scripts — Specification

## Purpose

Python scripts that run mechanical checks on produced artifacts and result files.
These checks are deterministic — the answer is derivable from file content alone,
no LLM judgment required. The LLM cannot override or fake their output.

---

## Where scripts live

```
.flow-engine/scripts/
  validate-result-file.py       — check result file schema conformance
  validate-artifact-counts.py   — count IDs in artifact vs source BRS
  validate-no-placeholders.py   — scan for TBD/TODO/[fill in] strings
  check-integrity.py            — verify event file + result file both exist in done/
```

---

## When scripts run

The dispatcher invokes scripts at **Step 16-G** (after the LLM writes the result
file, before Step 17 moves it to done/failed/).

The dispatcher instruction in Step 16-G becomes:

> "After completing checks 1–11, run the validation scripts for this event type.
> Read the script output file at `.flow/events/processing/<event_id>-script-check.yaml`.
> If any script check has `result: fail`, set the event result to fail regardless
> of what the LLM-written result file says. The script output is authoritative
> for the checks it covers."

The script output is a separate file — the LLM reads it but cannot modify it
(it was written by the script process, not by the LLM).

---

## Script 1 — validate-result-file.py

**What it checks:**
- `status` is exactly `pass` or `fail` (not `done`, `complete`, etc.)
- `event_id` is present and matches `EVT-NNNNN` pattern
- `completed_at` is present and ISO-8601 formatted
- `artifacts_written` is present and is a list
- If `status: pass` and `artifacts_written` is empty — flag as suspicious
  (pass with no artifacts written is only valid for WAIT_HUMAN and ROUTE_INITIATIVE)
- If event has `read_from` entries, `read_evidence` is present and count matches

**Invocation:**
```
python .flow-engine/scripts/validate-result-file.py \
  --result-file .flow/events/processing/EVT-00004-result.yaml \
  --event-file .flow/events/processing/EVT-00004-create-requirements-catalog.yaml \
  --output .flow/events/processing/EVT-00004-script-check.yaml
```

**Output format:**
```yaml
script: validate-result-file
ran_at: "2026-06-15T14:00:00Z"
checks:
  - name: status_field_valid
    result: fail
    detail: "status field is 'done' — must be 'pass' or 'fail'"
  - name: event_id_present
    result: pass
    detail: "event_id: EVT-00004"
  - name: read_evidence_count
    result: pass
    detail: "read_from has 2 entries; read_evidence has 2 entries"
overall: fail
```

---

## Script 2 — validate-artifact-counts.py

**What it checks:**

For events that produce a requirements catalog or business intake summary,
counts ID patterns in both the source BRS and the produced artifact and compares.

Checks:
- Count `**FR-NNN**` occurrences in `input/brs.md` (source truth)
- Count `| FR-` rows in the produced artifact (rows in a markdown table starting with `| FR-`)
- If artifact count < BRS count: fail with specific numbers
- Count `**NFR-NNN**` in BRS vs `| NFR-` rows in artifact — same check
- List which FR-NNN IDs appear in BRS but not in artifact (the missing ones)

**Invocation:**
```
python .flow-engine/scripts/validate-artifact-counts.py \
  --brs input/brs.md \
  --artifact business-intake/business-intake-summary.md \
  --artifact-type intake-summary \
  --workspace-root initiatives/I0013-NEXT13 \
  --output .flow/events/processing/EVT-00002-script-check.yaml
```

**Output format:**
```yaml
script: validate-artifact-counts
ran_at: "2026-06-15T14:00:00Z"
checks:
  - name: fr_count_match
    result: fail
    detail: |
      BRS contains 30 FR IDs (FR-001 through FR-030).
      Artifact contains 7 FR rows.
      Missing: FR-004, FR-005, FR-008, FR-010, FR-011, FR-013, FR-014,
               FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021,
               FR-022, FR-023, FR-024, FR-025, FR-026, FR-027, FR-028,
               FR-029, FR-030
  - name: nfr_count_match
    result: fail
    detail: |
      BRS contains 7 NFR IDs (NFR-001 through NFR-007).
      Artifact contains 2 NFR rows.
      Missing: NFR-003, NFR-004, NFR-005, NFR-006, NFR-007
overall: fail
```

**Why this is definitive:** the script reads the files character by character.
It cannot be convinced by a validation_notes entry that says "FR-001..FR-027 present"
when the file has 7 rows.

---

## Script 3 — validate-no-placeholders.py

**What it checks:**
Scans artifact files for placeholder strings:
- Exact strings: `TBD`, `TODO`, `[fill in]`, `PLACEHOLDER`, `[INSERT]`, `[TBD]`
- Case-insensitive
- Reports line number and the matching line for each hit

Exceptions (do not flag):
- Lines inside a `## Gaps and Questions` section (named gaps are intentional)
- Lines that contain `GAP-NNN` (named open items)

**Output format:**
```yaml
script: validate-no-placeholders
ran_at: "2026-06-15T14:00:00Z"
checks:
  - name: no_placeholder_strings
    result: fail
    detail: |
      Found 2 placeholder strings:
      Line 34: "| FR-005 | TBD | Medium | input/brs.md |"
      Line 67: "| NFR-004 | [fill in] | High | input/brs.md |"
overall: fail
```

---

## Script 4 — check-integrity.py

**What it checks:**
For every result file in `done/`, verifies that a corresponding event file exists
in the same folder. A result file without an event file means the event was
produced outside the dispatcher.

Also checks: for every EVT-ID in `workflow-state.json → artifact_status`, a
corresponding event file exists in `done/`.

**Invocation:** run at Step 3 (processing folder check) at the start of every
dispatch-next.

```
python .flow-engine/scripts/check-integrity.py \
  --workspace-root initiatives/I0013-NEXT13 \
  --output .flow/state/integrity-check.yaml
```

**Output format:**
```yaml
script: check-integrity
ran_at: "2026-06-15T14:00:00Z"
orphan_results:
  - path: ".flow/events/done/EVT-00004-create-requirements-catalog-result.yaml"
    issue: "result file exists in done/ but no matching event file found"
    recommendation: "EVT-00004 was produced outside the dispatcher. Reset to pending
      by creating the event file from the template and re-running dispatch-next."
overall: warn
```

---

## Integration with the dispatcher

Step 3 (processing folder check) adds:

> "After the existing processing/ repair logic, run `check-integrity.py` for the
> initiative workspace. Read `.flow/state/integrity-check.yaml`. If `orphan_results`
> is non-empty, stop dispatch with:
> 'Integrity check failed: [N] result file(s) found in done/ with no matching event
> file. These were produced outside the dispatcher. See .flow/state/integrity-check.yaml
> for details. Resolve before continuing.'"

Step 16-G adds (after existing checks 1–11):

> "Run `validate-result-file.py` for this event. Read the script output. If
> `overall: fail`, set event result to fail. The script output is appended to the
> result file as a `script_checks` field — the LLM may not remove or modify it."

Step 16-G also adds (for events whose `write_to` includes a requirements or intake artifact):

> "Run `validate-artifact-counts.py` for this event. Read the script output. If
> `overall: fail`, set event result to fail with failure_reason that quotes the
> script output's `detail` field verbatim."

---

## Cross-platform compatibility

All scripts use only Python standard library (no pip dependencies):
- `pathlib` for file paths (Windows/Mac/Linux compatible)
- `re` for regex
- `yaml` — use `import json` as fallback if PyYAML not available (parse YAML
  as text for simple cases)
- No shell commands, no subprocess calls

Python 3.8+ required (available on all target platforms).

Scripts are invoked by the dispatcher as instructions to the LLM:
> "Run this command: `python .flow-engine/scripts/validate-result-file.py --result-file ... --output ...`"

The LLM executes the command via its tool (Bash/PowerShell), reads the output file,
and applies the results. The script output file is written by the Python process —
the LLM reads it but did not produce it.
