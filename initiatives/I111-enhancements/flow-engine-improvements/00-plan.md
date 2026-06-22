# Flow Engine Improvement — read_evidence Contract

## Problem

When an AI agent (Claude or Copilot) executes a dispatcher event, Step 10 requires
reading every `read_from` file as an explicit tool call. There is currently no way to
verify after the fact whether the files were actually read. An agent can write
`status: fail` with a fabricated `failure_reason` (e.g. "BRS has no content") without
ever opening the file. The framework cannot distinguish a truthful failure from a lazy one.

## Solution

Add a required `read_evidence` block to the event result file for every event that has
a non-empty `read_from` list. The agent must record observable metadata for each file
read during Step 10. This makes the read either provably happened or provably faked.

## Files to change

| # | File | Change |
|---|---|---|
| 1 | `event-execution-rules.md` | Strengthen Section 2 — capture evidence per file read |
| 2 | `event-result-schema.yaml` | Add `read_evidence` as REQUIRED field |
| 3 | `dispatcher.md` | Step 10: record evidence; Step 16-G: validate evidence count and content |
| 4 | `validation-rules.md` | Add Section 6: suspicious-failure rule for content-insufficient claims |

## Execution order

Apply in order 1 → 2 → 3 → 4. Each prompt is self-contained and references the
current file content — read the file before applying the prompt.

## Prompt files

- `01-prompt-event-execution-rules.md`
- `02-prompt-event-result-schema.md`
- `03-prompt-dispatcher.md`
- `04-prompt-validation-rules.md`

## Refinements applied before implementation

Four refinements were incorporated into the prompt files based on review:

1. **read_evidence count maps to read_from items, not files** — one entry per
   `read_from` item; globs get one entry with `matched_files` list, not one per match
2. **lines > 20 rejects generic emptiness claims, not semantic failure** — a long file
   can still be wrong content; the check rejects "empty file" claims, not "wrong content"
3. **bytes kept loose** — "approximate byte count / character count acceptable"
   to avoid false failures from counting differences in phase 1
4. **Added first_nonempty_line contradiction check** — if evidence shows a meaningful
   first line and failure claims "file empty", that is an explicit contradiction (check 6
   in prompt 03, step 3 in prompt 04)

## Verification after each change

After each prompt, verify the change by reading the modified file and confirming:
- The `read_evidence` field/block is present and correctly described
- Cross-references to other files use the exact field names defined in prompt 02
- No existing rules were accidentally removed or overwritten
