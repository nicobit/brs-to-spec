# Prompt 02 — Add read_evidence to event-result-schema.yaml

## Target file

`.flow-engine/schemas/event-result-schema.yaml`

## What to do

Read the file first. Then add the `read_evidence` field definition immediately after
the `artifacts_written` block and before `validation_notes`. Also update the
PASS EXAMPLE to include a `read_evidence` block in the same position.

The position is after `artifacts_written` because read evidence records what was read
during execution (Steps 10–11), before validation runs (Steps 14–16). Placing it after
`validation_notes` would imply it is a validation output — it is not.

## Field definition to insert

Insert this block after the `artifacts_written` block and before `validation_notes`:

---

read_evidence: REQUIRED when event.read_from is non-empty
# One entry per read_from item. Records observable metadata captured at the moment
# each file was read during Step 10. Enables post-run verification that inputs were
# actually read before the artifact was produced or the event was failed.
#
# COUNT RULE: the number of read_evidence entries must equal the number of read_from
# items in the event file. A result file with fewer entries than read_from items is
# INVALID — treat as status: fail with failure_reason "incomplete read_evidence".
#
# Entry for a file that exists:
#   read_evidence:
#     - path: "input/brs.md"
#       required: true
#       exists: true
#       lines: 132
#       bytes: 11014
#       first_nonempty_line: "# Business Requirements Specification"
#       read_at: "2026-06-15T11:24:10Z"
#
# Entry for a glob pattern:
#     - path: "input/brs/*.md"
#       required: false
#       matched_files:
#         - "input/brs/appendix.md"
#       read_at: "2026-06-15T11:24:11Z"
#
# Entry for an optional file that does not exist:
#     - path: "input/architecture.md"
#       required: false
#       exists: false
#       read_at: "2026-06-15T11:24:12Z"
#
# HARD RULE: if read_from is non-empty and read_evidence is absent or empty,
# the result file is invalid. The dispatcher Step 16-G will fail the event with:
# failure_reason: "read_evidence missing — Step 10 was not executed or was not
# recorded. Every read_from file must have a corresponding read_evidence entry."

---

## Update the PASS EXAMPLE

In the PASS EXAMPLE section, add a `read_evidence` block after `artifacts_written`
and before `validation_notes`:

---

# read_evidence:                                        # one entry per read_from item
#   - path: "business-intake/business-intake-summary.md"
#     required: true
#     exists: true
#     lines: 87
#     bytes: 4312
#     first_nonempty_line: "# Business Intake Summary"
#     read_at: "2026-06-13T10:21:55Z"
#   - path: "input/brs.md"
#     required: true
#     exists: true
#     lines: 159
#     bytes: 11014
#     first_nonempty_line: "# Business Requirements Specification"
#     read_at: "2026-06-13T10:21:56Z"

---

## Verification

After making the change, confirm:
1. `read_evidence` appears after `artifacts_written` and before `validation_notes`
   in BOTH the field definition section AND the PASS EXAMPLE — positions must match
2. It is marked `REQUIRED when event.read_from is non-empty`
3. The PASS EXAMPLE includes a `read_evidence` block with two entries
4. All field names match exactly: `path`, `required`, `exists`, `lines`, `bytes`,
   `first_nonempty_line`, `read_at`, `matched_files`
