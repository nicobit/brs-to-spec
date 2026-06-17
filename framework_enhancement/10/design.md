# Enhancement 10 — External Call Support (CALL_EXTERNAL event type)

## Status: DESIGN ONLY — not implemented

---

## 1. Problem statement

The flow engine today produces artifacts by writing files. Some receivers of framework output are external systems (APIs, webhooks, ticketing tools, CI pipelines) that do not consume files — they expect direct calls. Currently the user must manually copy file content and post it to those systems. This enhancement makes the dispatcher capable of calling external endpoints as a first-class event action, configured per-initiative without modifying framework files.

---

## 2. Design goals

- External calls are optional and additive — existing file-write events are unchanged
- Templates remain portable across environments; endpoint URLs/credentials are initiative-local
- The dispatcher handles calls with the same result/state machinery as file-write events
- Retry and failure follow the same on_failure pattern already in the engine
- No secrets are stored in event files or templates — only key references

---

## 3. New components

### 3.1 New event_type: CALL_EXTERNAL

Added to the type mapping table in `template-instantiation-rules.md`:

| Template `type` | Runtime `event_type` | Runtime `action` |
|---|---|---|
| `CALL_EXTERNAL` | `CALL_EXTERNAL` | `call_external` |

The dispatcher routes on `event_type: CALL_EXTERNAL` and enters **call mode** instead of persona mode. No skill_ref or persona_ref is needed (both optional for this event_type).

---

### 3.2 New field: `call:` block in event templates and runtime events

```yaml
call:
  endpoint_key: "jira.create_issue"       # resolved via integration-config.yaml
  method: POST                             # GET / POST / PUT / PATCH
  payload_template: |                      # Handlebars-style — {{artifact.field}}
    {
      "project": "{{initiative.id}}",
      "summary": "{{artifact.title}}",
      "description": "{{artifact.content}}",
      "issuetype": { "name": "Story" }
    }
  headers:
    Content-Type: application/json
  read_artifact: "business-intake/business-intake-summary.md"   # artifact to extract values from
  response_capture:
    - field: "id"
      save_as: "jira_issue_id"             # saved to workflow-state.json extras
    - field: "key"
      save_as: "jira_issue_key"
```

`endpoint_key` is a logical name resolved at runtime against `input/integration-config.yaml`. It never contains a URL directly — this keeps templates environment-agnostic.

---

### 3.3 New initiative file: `input/integration-config.yaml`

Lives in `input/` so the user controls it directly (no event needed to write it).

```yaml
# integration-config.yaml
# Place in input/ before running any CALL_EXTERNAL event.
# Never commit credentials to source control — use env var references.

version: "1.0"

endpoints:
  jira.create_issue:
    url: "https://myorg.atlassian.net/rest/api/3/issue"
    auth:
      type: basic
      username_env: JIRA_USER          # dispatcher reads from environment variable
      password_env: JIRA_API_TOKEN
    timeout_seconds: 10
    retry:
      max_attempts: 3
      backoff_seconds: 2

  teams.notify:
    url: "https://myorg.webhook.office.com/webhookb2/..."
    auth:
      type: none
    timeout_seconds: 5
    retry:
      max_attempts: 2
      backoff_seconds: 1

  github.create_issue:
    url: "https://api.github.com/repos/myorg/myrepo/issues"
    auth:
      type: bearer
      token_env: GITHUB_TOKEN
    timeout_seconds: 10
    retry:
      max_attempts: 3
      backoff_seconds: 2
```

---

### 3.4 New engine rule file: `.flow-engine/instructions/call-execution-rules.md`

Governs how the dispatcher handles CALL_EXTERNAL events. Key rules:

```
1. CALL_EXTERNAL events do NOT enter persona mode. Steps 7–14 of the standard
   dispatch sequence are replaced by call-execution steps (see section 4).

2. skill_ref and persona_ref are optional for CALL_EXTERNAL. If present, ignore them.

3. The dispatcher MUST resolve endpoint_key against input/integration-config.yaml
   before constructing the request. If the key is not found → fail with:
   "endpoint_key '<key>' not found in input/integration-config.yaml."

4. The dispatcher MUST NOT embed credential values in any file — only env var names
   are written. Credentials are read from the environment at call time only.

5. If integration-config.yaml does not exist → fail with:
   "input/integration-config.yaml missing — required for CALL_EXTERNAL events."

6. HTTP response codes 2xx → pass. 3xx → fail (no redirect following).
   4xx → fail (do not retry). 5xx → retry per config, then fail.

7. response_capture fields are saved to workflow-state.json under
   artifacts.<write_to>.extras.<save_as> — not as top-level state fields.

8. write_to for a CALL_EXTERNAL event is optional. If present, the raw response
   body is written to that path as a file. If absent, only response_capture fields
   are saved to state.

9. The result file MUST include response_status, response_body_excerpt (first 500
   chars), and all captured fields.
```

---

### 3.5 Extended result file schema

New fields added to `event-result-schema.yaml` for CALL_EXTERNAL events:

```yaml
# Additional fields for CALL_EXTERNAL results (absent for other event types)
call_result:
  endpoint_key: "jira.create_issue"
  url_called: "https://myorg.atlassian.net/rest/api/3/issue"   # resolved URL, no credentials
  method: POST
  response_status: 201
  response_body_excerpt: '{"id":"10042","key":"PROJ-123",...}'  # first 500 chars
  captured_fields:
    jira_issue_id: "10042"
    jira_issue_key: "PROJ-123"
  attempts: 1
```

---

### 3.6 Dispatch sequence changes (CALL_EXTERNAL path)

The 21-step dispatcher sequence is unchanged for file-write events. For CALL_EXTERNAL, steps 7–14 are replaced:

```
Step 7  — Load integration-config.yaml (required). Fail if missing.
Step 8  — Resolve endpoint_key → URL + auth config. Fail if key not found.
Step 9  — Read read_artifact (if specified). Extract template variables.
Step 10 — Render payload_template with extracted values.
Step 11 — Execute HTTP call with retry per config.
Step 12 — Evaluate response: 2xx = pass, otherwise fail.
Step 13 — Capture response fields per response_capture config.
Step 14 — If write_to present, write raw response body to that path.
Step 15 — Write result file (includes call_result block).
Steps 16–21 — Unchanged (orchestrator mode, on_success/on_failure, state update).
```

---

## 4. Example: notify Teams when business intake is complete

### Event template (new file in event-templates/)

```yaml
event_template_id: EVT-TPL-043
type: CALL_EXTERNAL
priority: normal
description: "Post a Teams notification when business intake summary is accepted."

call:
  endpoint_key: "teams.notify"
  method: POST
  payload_template: |
    {
      "@type": "MessageCard",
      "summary": "Business intake complete for {{initiative.id}}",
      "text": "Initiative **{{initiative.id}}** has completed business intake. Review: {{artifact.path}}"
    }
  read_artifact: "business-intake/business-intake-summary.md"

inputs:
  required:
    - "business-intake/business-intake-summary.md"

outputs:
  primary: null    # no file written — call only

blocked_by_stage: "2-business-intake"

on_success:
  update_state:
    artifacts."notifications/teams-intake-notify.json".status: "accepted"

on_failure:
  raise_decision:
    question: "Teams notification failed. Check integration-config.yaml and TEAMS_WEBHOOK env var."
    blocking: false
    owner: human
```

### Instantiated runtime event

```yaml
event_id: EVT-00012
event_type: CALL_EXTERNAL
action: call_external
stage: "2-business-intake"
priority: normal

task:
  title: "Notify Teams — business intake complete"
  objective: "Post a Teams notification when business intake summary is accepted."

call:
  endpoint_key: "teams.notify"
  method: POST
  payload_template: |
    {
      "@type": "MessageCard",
      "summary": "Business intake complete for {{initiative.id}}",
      "text": "Initiative **{{initiative.id}}** has completed business intake."
    }
  read_artifact: "business-intake/business-intake-summary.md"

read_from:
  - "business-intake/business-intake-summary.md"
  - "input/integration-config.yaml"

required_inputs:
  - "business-intake/business-intake-summary.md"
  - "input/integration-config.yaml"

write_to: []

blocked_by:
  - "business-intake/business-intake-summary.md"

on_success:
  update_state: {}

on_failure:
  raise_decision:
    question: "Teams notification failed. Check integration-config.yaml and TEAMS_WEBHOOK env var."
    blocking: false
    owner: human

status: pending

meta:
  template_id: EVT-TPL-043
  created_by: orchestrator
  created_at: "2026-06-14T17:00:00Z"
  notes: "Triggered by EVT-00002 on_success chain."
```

---

## 5. Files to create/modify when implementing

| File | Action | Notes |
|---|---|---|
| `.flow-engine/instructions/call-execution-rules.md` | **CREATE** | New engine rule file governing CALL_EXTERNAL dispatch path |
| `.flow-engine/schemas/event-schema.yaml` | **MODIFY** | Add `call:` block definition; make skill_ref optional for CALL_EXTERNAL |
| `.flow-engine/schemas/event-result-schema.yaml` | **MODIFY** | Add `call_result:` block |
| `.flow-engine/instructions/dispatcher.md` | **MODIFY** | Add CALL_EXTERNAL branch at Step 7; reference call-execution-rules.md |
| `.brs2spec2/workflow/template-instantiation-rules.md` | **MODIFY** | Add CALL_EXTERNAL to type mapping table (section 3) |
| `.brs2spec2/agent-instructions.md` | **MODIFY** | Add note: CALL_EXTERNAL events skip persona mode |
| `.brs2spec2/workflow/event-templates/EVT-TPL-043-notify-teams.yaml` | **CREATE** | Example template (optional — ship as sample) |
| `initiatives/<id>/input/integration-config.yaml` | **USER CREATES** | Per-initiative, not a framework file |

---

## 6. What is NOT in scope for this enhancement

- Streaming responses
- OAuth2 token refresh (bearer token from env var only)
- Calling multiple endpoints in one event (one call per event)
- Conditional calls based on response content (use on_success chaining instead)
- UI or dashboard for monitoring calls

---

## 7. Open questions before implementation

1. Should `response_capture` fields be accessible as template variables in downstream events? If yes, how are they referenced (`{{extras.jira_issue_key}}`)?
2. Should `integration-config.yaml` support multiple environments (dev/prod) with a selector in `workflow-state.json`?
3. Should there be a `DRY_RUN` flag in `integration-config.yaml` that logs the payload without sending, for testing?
