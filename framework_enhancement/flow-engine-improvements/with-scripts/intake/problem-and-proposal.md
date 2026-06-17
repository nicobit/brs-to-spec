# Scripts-Based Validation — Problem Statement and Proposal

## What this folder is

This folder documents the problem analysis and implementation proposal for introducing
Python scripts into the flow engine to enforce mechanical validation checks that LLMs
cannot reliably self-validate.

---

## The problem

### Layer 1 — Dispatcher bypass

An LLM operating the framework (e.g. Copilot in autonomous mode) can write artifact
files and result files directly to disk without going through the dispatcher at all.
When this happens:

- The event file never appears in `pending/` — so Steps 6–19 never execute
- The result file is written freehand to `done/` with a non-conforming schema
  (`status: done` instead of `pass/fail`, `validation:` block instead of
  `validation_notes:` list)
- `workflow-state.json` is never updated (Step 19 never ran)
- The only evidence is: event file missing from `done/`, result file schema wrong

Evidence from I0013-NEXT13 / EVT-00004:
- `done/EVT-00004-create-requirements-catalog-result.yaml` exists
- `done/EVT-00004-create-requirements-catalog.yaml` does NOT exist
- `workflow-state.json` shows `current_stage: 0-routing` despite 4 events "done"
- requirements.md has 3 FRs that are domain-wrong (generic enterprise platform,
  not loan origination)

Root cause: `chain_break_on_new_events: true` stopped dispatch-all after EVT-00003.
Instead of waiting for `dispatch-next`, Copilot produced the artifact and result file
directly in the same response turn.

### Layer 2 — Self-validation

Even when the dispatcher runs correctly, the same LLM that produces the artifact
also writes the `validation_notes` in the result file. In the same context window,
the model "knows" what it just wrote and can produce plausible-sounding validation
evidence without re-reading the file.

Evidence from I0013-NEXT13 / EVT-00002:
- validation_notes claims "Requirements table includes FR-001..FR-027 and NFR-001..NFR-007"
- actual business-intake-summary.md has 9 requirement rows (not 27 FRs)
- The count-gate in Step 14 passed because the number of validation_notes entries
  matched the number of must_include items — it does not verify that the claims
  inside those entries are true

### Layer 3 — Fabricated counts in validation evidence

Must_include items like `"Requirements section has one row per atomic requirement"`
are evaluated by the same LLM that produced the artifact. The orchestrator writes
a validation_notes entry claiming the check passed, but never actually counted rows.
The count-gate enforces that N validation_notes entries exist — not that they are honest.

---

## Why instruction-only fixes don't work

Every fix applied so far is an instruction:
- count-gate in Step 14 (N_NOTES must equal N_MUST)
- Step 16-G contract checks
- read_evidence recording requirement
- natural_language validation hard-stop

These improve structure and make certain fabrications detectable after the fact.
But they all share the same weakness: an LLM that ignores the dispatcher once will
ignore the new instructions too. The instructions are enforced by the same agent
that is supposed to follow them.

There is no instruction that can prevent an LLM from writing files directly to disk.
There is no instruction that can prevent an LLM from writing fake validation evidence
that is numerically correct but substantively wrong.

---

## What scripts can and cannot solve

### Scripts CAN solve (Layer 3 — mechanical checks):

These are checks where the correct answer is deterministic and derivable from the
files alone, with no judgment required:

| Check | How a script does it |
|---|---|
| FR count in artifact matches BRS | Count `\*\*FR-NNN\*\*` in brs.md; count `\| FR-` rows in artifact; compare |
| NFR count matches | Same pattern for NFR |
| No placeholder text | Scan for TBD, TODO, [fill in], PLACEHOLDER strings |
| Required IDs present | Regex match for FR-NNN, UC-NNN, BR-NNN patterns |
| Result file schema valid | Parse YAML, check required fields and allowed values |
| Event file present in done/ | Check both event file and result file exist for each completed EVT-ID |
| workflow-state artifact count matches done/ event count | Count done/ events; compare to artifact_status entries |

### Scripts CANNOT solve (Layers 1 and 2):

- Whether the narrative content is domain-correct (requires judgment)
- Whether the LLM actually read the source files (observable only via read_evidence,
  which the LLM writes)
- Whether Copilot will bypass the dispatcher in the future (behavioral, not technical)

---

## Proposed approach

### Phase 1 — Validation scripts (addresses Layer 3)

A set of Python scripts in `.flow-engine/scripts/` that the dispatcher invokes
(or that run as a post-dispatch check) to enforce mechanical validation.

Scripts run **after** the LLM writes the result file, **before** Step 17 moves it
to `done/`. They produce a machine-written addendum to the result file that the
LLM cannot override.

See: `01-validation-scripts-spec.md` for the full script specification.

### Phase 2 — Integrity check script (addresses Layer 1 partially)

A script that scans the `done/` folder and flags any result file that has no
corresponding event file. Run at the start of every `dispatch-next` as part of
Step 3 (processing folder check).

See: `02-integrity-check-spec.md` for the full specification.

### Phase 3 — Must_include count anchoring (addresses Layer 3 in templates)

Replace vague must_include items with count-anchored items that reference the
source artifact. Instead of `"Requirements section has one row per atomic requirement"`,
use `"Requirements section row count matches the FR count in input/brs.md — list
all FR IDs found and compare"`. This forces the orchestrator to enumerate IDs
explicitly rather than claiming "rows present".

See: `03-must-include-anchoring-spec.md` for the full specification.

---

## What this does NOT propose

- Splitting `dispatch-next` into two turns (persona + orchestrator) — this was
  considered and rejected because it reduces automation without fully solving
  self-validation (Copilot still runs both turns in the same context window for
  dispatch-all)
- Requiring human confirmation between every event — this eliminates the value
  of `dispatch-all`
- Blocking all autonomous LLM operation — the framework is designed to be
  LLM-operated; the goal is to make mechanical checks LLM-independent, not to
  remove LLM autonomy entirely
