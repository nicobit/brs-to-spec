# Implementation Prompt — Phase 1: Engine Schemas

**Target:** `.flow-engine/schemas/`  
**Prerequisite:** `.flow-engine/schemas/event-schema.yaml` already exists (DONE)  
**Produces:** 2 new schema files

---

## Context

You are building the `.flow-engine/` generic orchestration engine for the brs-to-spec v2 framework. The engine uses a file-based event queue where every unit of work is a YAML file. Two supporting schemas are needed alongside the event schema that already exists.

Read `.flow-engine/schemas/event-schema.yaml` first — these two schemas are companions to it.

---

## File 1: `.flow-engine/schemas/event-result-schema.yaml`

This file is written by the **persona** (in persona mode) at step 11 of the dispatch lifecycle, immediately after executing the task and before validation. It lives in `.flow/events/processing/<event_id>-result.yaml` during execution, then moves with the event to `done/` or `failed/`.

It is the handoff signal between persona mode and orchestrator mode. The orchestrator reads it to know whether to execute `on_success` or `on_failure` actions.

Write the schema with the following fields, each documented with its purpose, required/optional status, allowed values, and an example:

**Required fields:**
- `event_id` — the EVT-NNNNN of the event this result belongs to
- `status` — `pass` or `fail`
- `completed_at` — ISO-8601 datetime

**Required when status is `pass`:**
- `artifacts_written` — list of file paths actually written (relative to initiative workspace root)

**Required when status is `fail`:**
- `failure_reason` — plain-English description of what validation failed and why
- `artifacts_written` — list of any partial artifacts written before failure (may be empty list)

**Optional fields:**
- `validation_notes` — list of specific validation_rules that passed or failed, one entry per rule checked
- `open_decisions_raised` — list of decision IDs written to open-decisions.md by this event
- `events_created` — list of EVT-IDs instantiated in pending/ by on_success chaining
- `notes` — free-text notes from the persona, not read by dispatcher, for human audit only

Include a complete pass example and a complete fail example at the end.

---

## File 2: `.flow-engine/schemas/artifact-status-schema.yaml`

This defines the allowed values and structure for the `artifacts` map inside `workflow-state.json`. Each key is an artifact path (relative to initiative workspace root), each value is a status object.

Write the schema documenting:

**Status values (the `status` field):**
- `missing` — artifact does not exist
- `draft` — artifact exists but is not yet accepted (still being worked)
- `accepted` — artifact exists and has passed validation / been accepted
- `failed` — artifact was attempted but failed validation
- `stale` — artifact exists but a dependency has changed since it was produced
- `blocked` — artifact cannot be produced because a required input is missing or a decision is unresolved

**Full status object fields:**
- `status` — REQUIRED, one of the values above
- `produced_by` — OPTIONAL, the EVT-ID that produced this artifact
- `accepted_at` — OPTIONAL, ISO-8601 datetime when status became `accepted`
- `last_updated` — OPTIONAL, ISO-8601 datetime of last status change
- `notes` — OPTIONAL, reason for current status (especially useful for `blocked` and `failed`)

Show the full `artifacts` block from `workflow-state.json` using this schema as an example, covering at least 5 different artifacts in different statuses.

---

## Quality bar

- Both files must be YAML with clear section headers and inline comments
- Field documentation style must match `event-schema.yaml` (REQUIRED/OPTIONAL labels, example values, purpose explanations as comments)
- The result schema complete example must show a realistic `fail` case with `failure_reason` and empty `artifacts_written`
- The artifact status schema must be usable directly by a future Python dispatcher to validate `workflow-state.json` entries
