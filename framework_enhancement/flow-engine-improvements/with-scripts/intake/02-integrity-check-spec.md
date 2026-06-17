# Integrity Check — Specification

## Purpose

Detect events that were produced outside the dispatcher (Layer 1 bypass).
The signature of a bypass is: a result file exists in `done/` with no corresponding
event file. This script makes that condition visible and blocking.

---

## The bypass signature

When an LLM bypasses the dispatcher it typically:

1. Writes the artifact directly to the initiative workspace
2. Writes a result file directly to `done/` (or `processing/`)
3. Does NOT create or move an event file through `pending/ → processing/ → done/`

Result: `done/EVT-NNNNN-<slug>-result.yaml` exists, but `done/EVT-NNNNN-<slug>.yaml`
does not.

Secondary signature: `workflow-state.json → artifact_status` is not updated
(Step 19 never ran), so the artifact map is stale relative to what's actually
in `done/`.

---

## What the integrity check script does

```
python .flow-engine/scripts/check-integrity.py \
  --workspace-root <path-to-initiative-workspace> \
  --output .flow/state/integrity-check.yaml
```

### Check 1 — Orphan result files

For every file matching `*.yaml` in `.flow/events/done/` whose name ends with
`-result.yaml`:
- Derive the expected event filename by removing `-result` from the stem
  (e.g. `EVT-00004-create-requirements-catalog-result.yaml` →
   `EVT-00004-create-requirements-catalog.yaml`)
- Check whether that event file exists in `done/`
- If not: record as orphan

### Check 2 — Artifact status consistency

For every key in `workflow-state.json → artifact_status`:
- Find the `produced_by` EVT-ID
- Check whether a file `EVT-NNNNN-*.yaml` (event file, not result file) exists
  in `done/`
- If not: record as inconsistency

### Check 3 — Processing folder orphans

For every result file in `processing/`:
- Check whether the corresponding event file is also in `processing/`
- If not: this is an interrupted dispatch (Step 3 auto-repair handles this,
  but flag it here too for visibility)

---

## Output format

```yaml
script: check-integrity
ran_at: "2026-06-15T14:22:00Z"
workspace: "initiatives/I0013-NEXT13"

orphan_results:
  - result_file: ".flow/events/done/EVT-00004-create-requirements-catalog-result.yaml"
    expected_event_file: ".flow/events/done/EVT-00004-create-requirements-catalog.yaml"
    issue: "result file in done/ has no matching event file — produced outside dispatcher"

artifact_status_inconsistencies:
  - artifact: "business-analysis/requirements.md"
    produced_by: "EVT-00004"
    issue: "EVT-00004 event file not found in done/ — artifact_status entry is unverifiable"

processing_orphans: []

overall: warn   # warn = issues found but not blocking; fail = blocking issues found
                # orphan_results → fail; artifact_status_inconsistencies → warn
```

`overall: fail` blocks the dispatcher. `overall: warn` is reported but does not block.

---

## Dispatcher integration point

**Step 3** (processing folder check) is extended:

After the existing processing/ auto-repair logic, add:

> "Run `check-integrity.py` for the initiative workspace. Read the output at
> `.flow/state/integrity-check.yaml`.
>
> If `overall: fail` (orphan_results is non-empty):
> Stop dispatch. Report:
> 'Integrity check failed: [N] result file(s) in done/ have no matching event file.
> These artifacts were produced outside the dispatcher and cannot be trusted.
> See .flow/state/integrity-check.yaml for the list.
>
> To resolve: for each orphan result, either:
>   (a) Delete the result file and the artifact, reset the EVT-ID to pending, and
>       re-run dispatch-next to produce the artifact through the framework; or
>   (b) If the artifact is correct, manually create the event file in done/ by
>       instantiating the template — but the result file must then be rewritten
>       to conform to the schema before dispatch can continue.'
>
> If `overall: warn` (artifact_status_inconsistencies only):
> Log the warning in the dispatch report but continue. Do not block."

---

## Why this catches the I0013 / EVT-00004 case

Running check-integrity.py on I0013-NEXT13 would produce:

```yaml
orphan_results:
  - result_file: ".flow/events/done/EVT-00004-create-requirements-catalog-result.yaml"
    expected_event_file: ".flow/events/done/EVT-00004-create-requirements-catalog.yaml"
    issue: "result file in done/ has no matching event file — produced outside dispatcher"
overall: fail
```

The next `dispatch-next` call would stop immediately with a clear explanation,
rather than silently treating the fabricated result as valid and chaining
downstream events from a stub artifact.

---

## Limitations

This script catches **after-the-fact** bypasses — when the LLM has already
written files freehand. It cannot prevent the bypass from happening.

The prevention mechanism remains: `chain_break_on_new_events: true` stops
dispatch-all and requires the user to type `dispatch-next`. The gap is that
an LLM in autonomous mode (Copilot) fills that gap by producing artifacts
directly instead of waiting. The integrity check makes that visible on the
next dispatch invocation rather than letting it propagate silently.
