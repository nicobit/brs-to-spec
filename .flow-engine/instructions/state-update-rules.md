# Flow Engine — State Update Rules
# Version: 1.0
#
# Defines who may update which state files and exactly what to write.
# Applied by the orchestrator during dispatch steps 18–19.

---

## 1. Orchestrator-only rule

Only the orchestrator (Claude in orchestrator mode, steps 16–21 of dispatch) may write to:

- `.flow/state/workflow-state.json`
- `.flow/state/event-log.jsonl`
- `.flow/state/open-decisions.md`

Domain personas (product-owner, architect, delivery-lead, qa-analyst, security-reviewer, engineering-lead, reviewer) must not write to these files. If a domain skill needs to raise a decision, it records the decision in the result file under `open_decisions_raised`. The orchestrator writes it to `open-decisions.md` in step 18.

Violation of this rule is a dispatcher protocol error. If it occurs, mark the event as failed and log the violation in `failure_reason`.

---

## 2. workflow-state.json — update rules

Update only the fields listed below. Do not touch unlisted fields.

**Always update after every event (pass or fail):**

| Field | Rule |
|---|---|
| `last_updated` | Set to current ISO-8601 datetime |
| `active_events` | Remove completed EVT-ID; add any new EVT-IDs from on_success.create_events |
| `event_counter` | Already incremented in step 18 when events were created; do not re-increment |

**On pass only:**

| Field | Rule |
|---|---|
| `last_completed_event` | Set to the EVT-ID that just passed |
| `current_stage` | Set to `on_success.update_state.current_stage` if present in the event |
| `artifacts.<path>.status` | See artifact status rule below |
| `artifacts.<path>.produced_by` | Set to the EVT-ID |
| `artifacts.<path>.accepted_at` | Set to current ISO-8601 datetime |
| `artifacts.<path>.last_updated` | Set to current ISO-8601 datetime |
| `delivery_mode` | Set ONLY if event type is `ROUTE_INITIATIVE` and result is pass |
| `execution_mode` | Set ONLY if event type is `ROUTE_INITIATIVE` and result is pass |

**Artifact status rule on pass (ai_validated vs accepted):**

Set `artifacts.<path>.status` based on the event type:

| Event type | Artifact status set on pass |
|---|---|
| `WAIT_HUMAN` (human approved) | `accepted` — human has reviewed and approved |
| `ROUTE_INITIATIVE` | `accepted` — routing decisions are always accepted |
| Any other event type | `ai_validated` — AI produced and validated, flow continues |

This means: AI-generated artifacts flow automatically without human blocking. Human approval via WAIT_HUMAN gates upgrades status to `accepted`. Both `ai_validated` and `accepted` satisfy `blocked_by` checks (see artifact-status-schema.yaml).

**On fail only:**

| Field | Rule |
|---|---|
| `failed_events` | Append EVT-ID to the array |
| `artifacts.<path>.status` | Set to `"failed"` for each path in `write_to` (even if the file was partially written) |
| `artifacts.<path>.produced_by` | Set to the EVT-ID |
| `artifacts.<path>.last_updated` | Set to current ISO-8601 datetime |

**After any open-decisions.md update (pass or fail):**

| Field | Rule |
|---|---|
| `open_decisions` | Recount non-resolved entries in open-decisions.md |
| `blocking_decisions` | Recount entries with `blocking: true` and no `resolved_at` in open-decisions.md |

**Fields that must NEVER be changed by the orchestrator during dispatch:**

| Field | Reason |
|---|---|
| `initiative_id` | Set at init, immutable |
| `initiative_slug` | Set at init, immutable |
| `delivery_mode` | Set only by ROUTE_INITIATIVE — not by any other event |
| `execution_mode` | Set only by ROUTE_INITIATIVE — not by any other event |

---

## 3. event-log.jsonl — append format

Append exactly one JSON line per event after every dispatch cycle (pass or fail).
Never rewrite or delete existing lines — append only.

Before appending, scan existing lines for the same `event_id`.
If that `event_id` is already present:

- do not append a duplicate line
- treat the situation as queue/state corruption
- stop the dispatch cycle and surface a repair-needed failure

The event log is append-only, but it is not allowed to contain multiple completion records
for the same EVT-ID.

**Line format:**

```json
{"event_id":"EVT-NNNNN","event_type":"CREATE_ARTIFACT","action":"create_business_rules","persona":"persona-name","status":"done","completed_at":"2026-06-13T10:22:00Z","artifacts_written":["path1","path2"]}
```

```json
{"event_id":"EVT-NNNNN","event_type":"CREATE_ARTIFACT","action":"create_business_rules","persona":"persona-name","status":"failed","completed_at":"2026-06-13T10:22:00Z","artifacts_written":[],"failure_reason":"specific reason"}
```

Rules:
- `event_type` is the generic engine type (e.g. `CREATE_ARTIFACT`); `action` is the domain action (e.g. `create_business_rules`)
- `status` is `"done"` on pass, `"failed"` on fail (not `"pass"` / `"fail"` — use `"done"` for log consistency)
- `failure_reason` key is only present when status is `"failed"`
- `artifacts_written` is always present, even as empty array `[]`
- Each line must be valid JSON — no trailing commas, no multiline

---

## 4. open-decisions.md — entry format

When `on_failure.raise_decision` is present in the event and the event failed, append one entry:

**ID assignment:** read the file for the last `DEC-AUTO-NNN` entry. Increment N by 1. If no DEC-AUTO entries exist yet, start at `DEC-AUTO-001`.

**Entry format (append to end of file):**

```markdown
## DEC-AUTO-NNN

**Question:** <question from on_failure.raise_decision.question>
**Owner:** <owner from on_failure.raise_decision.owner>
**Blocking:** <true|false from on_failure.raise_decision.blocking>
**Raised by:** <EVT-ID>
**Raised at:** <ISO-8601 datetime>
**Status:** Open
```

**When a decision is resolved** (via a RESOLVE_DECISION event):
Add these fields to the existing entry — do not delete the entry:

```markdown
**Resolved at:** <ISO-8601 datetime>
**Resolution:** <resolution text>
**Status:** Resolved
```

**Rule:** decisions are never deleted from open-decisions.md. Resolved decisions remain with Status: Resolved.
