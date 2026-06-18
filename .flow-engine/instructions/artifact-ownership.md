# Flow Engine — Artifact Ownership Rules
# Version: 1.1
#
# Generic ownership protocol for the flow engine.
# Domain-specific ownership tables live in the domain layer, NOT here.
# For brs-to-spec v2: see .brs2spec2/workflow/artifact-ownership.md

---

## 1. Engine-protected paths (unconditional — all domains)

These paths are protected by the engine regardless of what domain layer is loaded.
No persona may write to them in persona mode. Ever.

| Path pattern | Owner | Rule |
|---|---|---|
| `input/*` | human | Read-only for all engine personas. Never written by any event. |
| `.flow/state/workflow-state.json` | orchestrator | Orchestrator mode only. Never written in persona mode. |
| `.flow/state/event-log.jsonl` | orchestrator | Append-only. Orchestrator mode only. |
| `.flow/state/open-decisions.md` | orchestrator | Written by orchestrator (on_failure) or RAISE_DECISION events only. |
| `.flow/events/*` | orchestrator | Event queue management is orchestrator-only. Personas never move event files. |

---

## 2. Domain ownership table

Each domain layer that uses this engine must provide its own ownership table at:

```
<domain-layer>/workflow/artifact-ownership.md
```

For brs-to-spec v2, this file is at:

```
.brs2spec2/workflow/artifact-ownership.md
```

The dispatcher loads the domain ownership table during Step 9b (artifact ownership check).
If no domain ownership table exists, the engine enforces only the engine-protected paths above.

---

## 3. Write conflict rules (generic — all domains)

These rules apply to all domain layers. The dispatcher enforces them during Step 9b.

**Rule A — Cross-persona CREATE_ARTIFACT:**
If an event's `write_to` path is owned by a different persona AND `event_type` is `CREATE_ARTIFACT`:
→ fail. `failure_reason: "artifact <path> is owned by <owner>. Use UPDATE_ARTIFACT or ENRICH_ARTIFACT for cross-persona writes."`

**Rule B — Cross-persona UPDATE_ARTIFACT or ENRICH_ARTIFACT:**
If an event's `write_to` path is owned by a different persona AND `event_type` is `UPDATE_ARTIFACT` or `ENRICH_ARTIFACT`:
→ allowed. Note the cross-persona write in the result file `notes` field.

**Rule C — Engine-protected paths:**
If `write_to` includes any path matching section 1 patterns:
→ unconditional fail regardless of event type. `failure_reason: "write to <path> is not permitted in persona mode — engine-protected path."`

**Rule D — Unknown path:**
If `write_to` includes a path not in section 1 and not in the domain ownership table:
→ allowed. Log a warning in the result file `notes`: `"write_to path <path> has no declared owner — proceeding without ownership check."`

---

## 4. Open decisions protocol (generic — all domains)

A persona that needs to raise a decision must never write directly to `.flow/state/open-decisions.md`.

Instead, the persona records the decision in the result file under `open_decisions_raised`:

```yaml
open_decisions_raised:
  - question: "..."
    owner: "product-owner"
    blocking: true
```

The orchestrator reads `open_decisions_raised` from the result file and writes the entry to `.flow/state/open-decisions.md` during Step 18.
