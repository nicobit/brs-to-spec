# Flow Engine — Template Instantiation Rules
# Version: 1.0
#
# Defines how an event template (.brs2spec2/workflow/event-templates/EVT-TPL-NNN-*.yaml)
# is converted into an executable runtime event (.flow/events/pending/EVT-NNNNN-*.yaml).
#
# Templates are NOT executable. The dispatcher NEVER reads a template directly from
# event-templates/ and executes it. Templates must first be instantiated into runtime events.
# Only runtime events in .flow/events/pending/ are dispatched.

---

## 1. Where things live

```
Templates (not executable):
  .brs2spec2/workflow/event-templates/EVT-TPL-NNN-<slug>.yaml

Runtime events (executable):
  initiatives/<id>-<slug>/.flow/events/pending/EVT-NNNNN-<slug>.yaml
  initiatives/<id>-<slug>/.flow/events/processing/EVT-NNNNN-<slug>.yaml
  initiatives/<id>-<slug>/.flow/events/done/EVT-NNNNN-<slug>.yaml
  initiatives/<id>-<slug>/.flow/events/failed/EVT-NNNNN-<slug>.yaml
```

Templates live at the repository root. Runtime events live inside the initiative workspace.
The dispatcher operates on the initiative workspace only. It never touches `event-templates/`.

---

## 2. Field mapping — template → runtime event

When instantiating a template, apply this field mapping exactly:

| Template field | Runtime event field | Rule |
|---|---|---|
| `event_template_id` | `meta.template_id` | Copy verbatim — **MANDATORY. Chain-repair cannot function without this field. Never omit it.** |
| `type` | `action` | See section 3 — type split |
| *(derived from type)* | `event_type` | See section 3 |
| `persona` | `persona` | Copy verbatim |
| `priority` | `priority` | Copy verbatim; default `normal` if absent |
| `description` | `task.objective` | Copy verbatim |
| *(derived from template slug)* | `task.title` | Convert slug to title case: `create-business-rules` → `Create business rules` |
| `skill_ref` | `skill_ref` | Copy verbatim |
| `persona_ref` | `persona_ref` | Copy verbatim |
| `artifact_template_ref` | `artifact_template_ref` | Copy verbatim |
| `inputs.required` | `required_inputs` AND part of `read_from` | Copy to both fields |
| `inputs.optional` | `optional_inputs` AND part of `read_from` | Copy to both fields |
| `outputs.primary` | First entry in `write_to` | Copy verbatim. **Folder-output rule:** if the value ends with `/`, the `write_to` entry must be the folder path ending with `/` (e.g. `business-analysis/use-cases/`). The persona writes one file per entity inside that folder (e.g. `UC-001.md`, `UC-002.md`). Never flatten a folder output into a single monolithic file. |
| `outputs.secondary` | Additional entries in `write_to` | Append after primary. Apply folder-output rule if any value ends with `/`. |
| `must_include` | `must_include` | Copy verbatim |
| `validation_rules` | `validation_rules` | Copy verbatim |
| `blocked_by_stage` | `blocked_by` | Resolve stage → artifact list (see section 4) |
| `blocked_by_event` | `blocked_by_events` | Copy verbatim. Allowed values are either runtime EVT-NNNNN IDs or template references EVT-TPL-NNN. |
| `on_success` | `on_success` | Copy verbatim (expand template refs — see section 5) |
| `on_failure` | `on_failure` | Copy verbatim |
| `condition` | `meta.condition` | Copy verbatim — skip instantiation if condition is false |

**Fields added during instantiation (not from the template):**

| Field | Value |
|---|---|
| `event_id` | Assigned by orchestrator: read `event_counter` from `.flow/state/workflow-state.json`, increment, format as `EVT-NNNNN` |
| `status` | `pending` |
| `meta.created_by` | `orchestrator` |
| `meta.created_at` | Current ISO-8601 datetime |
| `stage` | From the `workflow-definition.yaml` stage entry that caused this event to be created |

---

## 3. Event type split — `type` → `event_type` + `action`

Template files use domain-specific `type` values (e.g. `CREATE_BUSINESS_RULES`).
Runtime events use a two-field split to keep `.flow-engine` generic:

```yaml
event_type: CREATE_ARTIFACT     # generic engine type — used by dispatcher for routing
action: create_business_rules   # domain-specific action — used by skill_ref
```

**Mapping table — all registered template types:**

| Template `type` | Runtime `event_type` | Runtime `action` |
|---|---|---|
| `ROUTE_INITIATIVE` | `ROUTE_INITIATIVE` | `route_initiative` |
| `CREATE_BUSINESS_INTAKE_SUMMARY` | `CREATE_ARTIFACT` | `create_business_intake_summary` |
| `CREATE_BUSINESS_RULES` | `CREATE_ARTIFACT` | `create_business_rules` |
| `CREATE_ACTORS_AND_PERSONAS` | `CREATE_ARTIFACT` | `create_actors_and_personas` |
| `FIND_GAPS_AND_QUESTIONS` | `CREATE_ARTIFACT` | `find_gaps_and_questions` |
| `CREATE_PROCESS_FLOWS` | `CREATE_ARTIFACT` | `create_process_flows` |
| `CREATE_USE_CASE_SPECS` | `CREATE_ARTIFACT` | `create_use_case_specs` |
| `REVIEW_INITIAL_ARCHITECTURE` | `CREATE_ARTIFACT` | `review_initial_architecture` |
| `CREATE_ARCHITECTURE_RULES` | `CREATE_ARTIFACT` | `create_architecture_rules` |
| `REVIEW_EXISTING_SYSTEM_IMPACT` | `CREATE_ARTIFACT` | `review_existing_system_impact` |
| `CREATE_DELIVERY_STRUCTURE` | `CREATE_ARTIFACT` | `create_delivery_structure` |
| `CREATE_TRACEABILITY_MATRIX` | `CREATE_ARTIFACT` | `create_traceability_matrix` |
| `IDENTIFY_SOFTWARE_MODULES` | `CREATE_ARTIFACT` | `identify_software_modules` |
| `DEFINE_DELIVERY_INCREMENTS` | `CREATE_ARTIFACT` | `define_delivery_increments` |
| `CHECK_ENGINEERING_READINESS` | `CREATE_ARTIFACT` | `check_engineering_readiness` |
| `GENERATE_INITIATIVE_CONTEXT` | `CREATE_ARTIFACT` | `generate_initiative_context` |
| `CREATE_BDD_SCENARIOS` | `CREATE_ARTIFACT` | `create_bdd_scenarios` |
| `CREATE_TEST_STRATEGY` | `CREATE_ARTIFACT` | `create_test_strategy` |
| `CREATE_SECURITY_REVIEW` | `CREATE_ARTIFACT` | `create_security_review` |
| `CREATE_API_CONTRACT` | `CREATE_ARTIFACT` | `create_api_contract` |
| `CREATE_DATA_CONTRACT` | `CREATE_ARTIFACT` | `create_data_contract` |
| `CREATE_EVENT_CONTRACT` | `CREATE_ARTIFACT` | `create_event_contract` |
| `CREATE_OBSERVABILITY_PLAN` | `CREATE_ARTIFACT` | `create_observability_plan` |
| `CREATE_OPENSPEC_HANDOFF` | `GENERATE_HANDOFF` | `create_openspec_handoff` |
| `CREATE_STANDALONE_HANDOFF` | `GENERATE_HANDOFF` | `create_standalone_handoff` |
| `CREATE_COMPACT_HANDOFF` | `GENERATE_HANDOFF` | `create_compact_handoff` |
| `GENERATE_TEST_STUBS` | `CREATE_ARTIFACT` | `generate_test_stubs` |
| `CREATE_REVIEW_PACKAGE` | `CREATE_ARTIFACT` | `create_review_package` |
| `CREATE_AGILE_PLANNING_VIEW` | `CREATE_ARTIFACT` | `create_agile_planning_view` |
| `CREATE_ENTITY_MODEL` | `CREATE_ARTIFACT` | `create_entity_model` |
| `CREATE_BUSINESS_TEST_EXPECTATIONS` | `CREATE_ARTIFACT` | `create_business_test_expectations` |
| `DRAFT_ARCHITECTURE_FROM_BRS` | `CREATE_ARTIFACT` | `draft_architecture_from_brs` |
| `CREATE_BRS` | `CREATE_ARTIFACT` | `create_brs` |
| `CREATE_THREAT_MODEL` | `CREATE_ARTIFACT` | `create_threat_model` |
| `MAP_CAPABILITIES_TO_MODULES` | `CREATE_ARTIFACT` | `map_capabilities_to_modules` |
| `CREATE_TEST_PLAN_PER_STORY` | `CREATE_ARTIFACT` | `create_test_plan_per_story` |
| `CREATE_REQUIREMENTS_CATALOG` | `CREATE_ARTIFACT` | `create_requirements_catalog` |
| `CREATE_USE_CASE_DIAGRAM` | `CREATE_ARTIFACT` | `create_use_case_diagram` |
| `SENIOR_CODE_REVIEW` | `REVIEW_ARTIFACT` | `senior_code_review` |
| `ARCHITECTURE_REVIEW_IMPLEMENTATION` | `REVIEW_ARTIFACT` | `architecture_review_implementation` |
| `SPEC_CORRECTION` | `REPAIR_ARTIFACT` | `spec_correction` |
| `WAIT_HUMAN` | `WAIT_HUMAN` | `wait_human` |

The dispatcher routes on `event_type`. The skill in `skill_ref` handles the `action`.
The `action` field is informational for Claude — the actual execution is driven by `skill_ref`.

**WAIT_HUMAN special handling during instantiation:**
- Copy `gate_context` verbatim from the template into the runtime event
- `write_to` is empty (no artifact produced)
- `skill_ref` is omitted (WAIT_HUMAN does not enter persona mode)
- `persona_ref` is omitted (orchestrator handles the gate directly)
- `on_success.create_events` is copied verbatim — these are the downstream events created on approval

---

## 4. Resolving `blocked_by_stage`

Templates may declare `blocked_by_stage: "2-business-intake"`. During instantiation, resolve this
to the primary output artifact of that stage:

| Stage | Resolves to artifact |
|---|---|
| `0-routing` | `routing/routing-decision.md` |
| `2-business-intake` | `business-intake/business-intake-summary.md` |
| `2b-business-analysis` | *(all of: business-analysis/requirements.md, business-analysis/use-cases.puml, business-analysis/use-cases/, business-analysis/entity-model.md, business-analysis/business-rules.md, business-analysis/actors-and-personas.md, business-analysis/gaps-and-questions.md, business-analysis/process-flows.md)* |
| `3-planning` | `planning/delivery-structure.md` and `architecture/architecture-review.md` |
| `4-engineering-readiness` | `engineering-readiness/readiness-check.md` |
| `4b-quality-gates` | `engineering-readiness/initiative-context.md` |

Set the resolved artifact path(s) into `blocked_by` in the runtime event.

If `blocked_by_event` is set instead: copy the identifier directly into `blocked_by_events`.
Do not resolve event IDs to artifact paths.

Two forms are valid:

- `EVT-NNNNN` — runtime event ID. Satisfied when that event is in `done/`.
- `EVT-TPL-NNN` — template reference. Satisfied when any event in `done/` has
  `meta.template_id: EVT-TPL-NNN`.

Use template references when the dependency is declared in a stage graph before the runtime
EVT-NNNNN is known. Use runtime EVT-NNNNN only when an already-instantiated event is being
referenced directly (for example in a manual repair or retry scenario).

---

## 5. Expanding `on_success.create_events` template references

Templates use short references in `on_success`:

```yaml
on_success:
  create_events:
    - template: "EVT-TPL-003"
      reason: "..."
    - template: "EVT-TPL-004"
      reason: "..."
```

When the **runtime event** completes (pass) and the orchestrator processes `on_success`, it:

1. Reads the template file at `.brs2spec2/workflow/event-templates/EVT-TPL-NNN-*.yaml`
   (glob match on the number prefix — e.g. `EVT-TPL-003-*.yaml`)
2. Applies the full field mapping from section 2 above
3. Checks the `condition` field if present — skip if condition is false for this initiative
4. Assigns a new `event_id` from the `event_counter`
5. Writes the new runtime event to `.flow/events/pending/EVT-NNNNN-<slug>.yaml`

The `reason` field from the template reference is written into `meta.notes` of the new runtime event.

---

## 6. Complete instantiation example

The runtime event must be a complete copy of all template fields. The example below shows ALL fields — nothing is optional to omit. A runtime event missing `must_include` or `validation_rules` is a defective instantiation and will cause stubs to pass validation.

**Template** (`.brs2spec2/workflow/event-templates/EVT-TPL-043-create-requirements.yaml`) — abbreviated for brevity, but all fields present:

```yaml
event_template_id: EVT-TPL-043
type: CREATE_REQUIREMENTS_CATALOG
persona: product-owner
priority: high
description: "Produce the canonical requirements catalog..."
skill_ref: ".brs2spec2/skills/product-owner/create-requirements.md"
persona_ref: ".brs2spec2/personas/product-owner.md"
artifact_template_ref: ".brs2spec2/artifact-templates/requirements.md"
inputs:
  required:
    - "business-intake/business-intake-summary.md"
    - "input/brs.md"
  optional:
    - "routing/routing-decision.md"
outputs:
  primary: "business-analysis/requirements.md"
must_include:
  - "## Metadata table is present with Status: Draft"
  - "## Functional Requirements table is present with multiple FR-NNN rows (not a single stub row)"
  - "Every FR-NNN uses user story format: As a [role], I want [goal] so that [benefit]"
  - "... (all N items from the template — none omitted)"
validation_rules:
  natural_language: >
    Step A — Read input/brs.md now. Count FR-NNN lines...
    (full rule text — none omitted)
```

**Instantiated runtime event** — every field from the template must appear verbatim:

```yaml
event_id: EVT-00004
event_type: CREATE_ARTIFACT
action: create_requirements_catalog
persona: product-owner
stage: "2b-business-analysis"
priority: high

task:
  title: "Create requirements catalog"
  objective: "Produce the canonical requirements catalog..."

skill_ref: ".brs2spec2/skills/product-owner/create-requirements.md"
persona_ref: ".brs2spec2/personas/product-owner.md"
artifact_template_ref: ".brs2spec2/artifact-templates/requirements.md"

read_from:
  - "business-intake/business-intake-summary.md"
  - "input/brs.md"
  - "routing/routing-decision.md"

required_inputs:
  - "business-intake/business-intake-summary.md"
  - "input/brs.md"

optional_inputs:
  - "routing/routing-decision.md"

write_to:
  - "business-analysis/requirements.md"

blocked_by:
  - "business-intake/business-intake-summary.md"

must_include:
  - "## Metadata table is present with Status: Draft"
  - "## Functional Requirements table is present with multiple FR-NNN rows (not a single stub row)"
  - "Every FR-NNN uses user story format: As a [role], I want [goal] so that [benefit]"
  - "... (ALL items from the template — count must match exactly)"

validation_rules:
  natural_language: >
    Step A — Read input/brs.md now. Count FR-NNN lines...
    (FULL rule text copied verbatim from template — no truncation, no paraphrase)
  machine:
    file_exists: "business-analysis/requirements.md"

on_success:
  create_events:
    - template: "EVT-TPL-044"
      reason: "Requirements catalog complete — trigger use-case diagram"
  update_state:
    artifact_status:
      "business-analysis/requirements.md": "ai_validated"

on_failure:
  raise_decision:
    question: "Requirements catalog creation failed."
    blocking: true
    owner: "product-owner"

meta:
  template_id: EVT-TPL-043
  created_by: orchestrator
  created_at: "2026-06-14T10:00:00Z"
  notes: "Instantiated from EVT-TPL-043 on_success"
```

**Verification before writing:** Count the items in `must_include` in the template file. Count the items in `must_include` in the runtime event you are about to write. If the counts differ → do not write — re-read the template and copy the full list.

---

## 7. What the dispatcher must never do

- Never read from `event-templates/` and execute it directly as a runtime event
- Never skip the field mapping — `inputs.required` is NOT the same as `required_inputs` at runtime
- Never truncate `must_include` — every item in the template must appear in the runtime event
- Never omit `validation_rules` — if the template has it, the runtime event must have it verbatim
- Never paraphrase `natural_language` rule text — copy it character-for-character from the template
- Never instantiate a template whose `condition` evaluates to false for this initiative
- Never assign duplicate `event_id` values — always read and increment `event_counter` from workflow-state.json
- Never omit `event_type` in a runtime event — the generic dispatcher routes on this field
