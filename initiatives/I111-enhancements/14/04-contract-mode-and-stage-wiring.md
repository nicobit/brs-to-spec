# Prompt 04 — Contract Mode and Stage-Actions Wiring

## Context

You are working on the `.b2s` framework at the root of this repository.

Skills were created in prompt 03. This prompt wires them into the workflow by:
1. Introducing `api_contract_mode` as a workflow state field
2. Registering the four new actions in `stage-actions.yaml`
3. Setting the correct stage, conditions, blocked_by, and sequencing
4. Updating `state.py` to parse `api_contract_mode` from the readiness check

Before making any changes, read these files in full:
- `.b2s/workflow/stage-actions.yaml` — full file, understand stage ordering and action structure
- `.b2s/workflow/workflow-definition.yaml` — understand stage definitions
- `.b2s/scripts/b2s_engine/state.py` — understand how routing fields are parsed
- `.b2s/scripts/b2s_engine/next_step.py` — understand condition evaluation

---

## Step 1 — Add api_contract_mode to state.py

In `state.py`, the `_parse_readiness_fields` function reads `readiness-check.md` to extract
`quality_gates_triggered` and `readiness_score`. Extend it to also read `api_contract_mode`.

Add parsing for a table row labelled `API contract mode` in `readiness-check.md`.
Valid values: `product`, `internal`, `coordinated`.
Store as `state["api_contract_mode"]`.

If the row is absent, default to `internal` (safest — generates specs after stories).

Also add `api_contract_mode` to the default workflow state template at
`.b2s/templates/state/workflow-state.json` with value `null`.

---

## Step 2 — Update readiness-check artifact template

Read `.b2s/artifact-templates/readiness-check.md` in full.

Add a new row to the Gate Trigger Decisions table:

```markdown
| API contract mode | {{product / internal / coordinated}} | product = expose to external consumers, freeze early; internal = derive from stories; coordinated = draft early, refine after stories | Required |
```

This makes `api_contract_mode` a first-class decision captured during readiness.

---

## Step 3 — Register new actions in stage-actions.yaml

Read `.b2s/workflow/stage-actions.yaml` in full to understand the existing structure
around stage `4b-quality-gates` and stage `5-handoff`.

Add four new actions. Insert them AFTER `create-api-contract` in stage `4b-quality-gates`
(for `product` and `coordinated` modes) or AFTER `create-openspec-handoff` in stage `5-handoff`
(for `internal` mode). Use conditions to enforce the sequencing.

### Action: create-exposed-api-specs

```yaml
- action_id: create-exposed-api-specs
  stage_id: "4b-quality-gates"
  title: "Create exposed API specifications"
  persona: engineering-lead
  skill_ref: ".b2s/skills/engineering-lead/create-exposed-api-specs.md"
  artifact_template_ref: ".b2s/artifact-templates/exposed-api-spec.md"
  inputs:
    required:
      - "architecture/architecture-review.md"
      - "architecture/architecture-rules.md"
      - "engineering-readiness/readiness-check.md"
      - "input/brs.md"
    optional:
      - "planning/delivery-structure.md"
      - "input/brs/*.md"
  outputs:
    primary: "technical-specifications/api/exposed/"
    secondary: []
  conditions:
    - "API_CONTRACT in quality_gates_triggered"
  blocked_by_stage: []
  blocked_by_action:
    - "create-api-contract"
  human_gate:
    required: false
  status_model:
    artifact_on_pass: ai_validated
    artifact_on_gate_accept: accepted
    artifact_on_fail: failed
```

### Action: create-consumed-api-specs

```yaml
- action_id: create-consumed-api-specs
  stage_id: "4b-quality-gates"
  title: "Create consumed API specifications"
  persona: engineering-lead
  skill_ref: ".b2s/skills/engineering-lead/create-consumed-api-specs.md"
  artifact_template_ref: ".b2s/artifact-templates/consumed-api-spec.md"
  inputs:
    required:
      - "architecture/architecture-review.md"
      - "architecture/architecture-rules.md"
      - "input/brs.md"
    optional:
      - "planning/delivery-structure.md"
      - "input/brs/*.md"
  outputs:
    primary: "technical-specifications/api/consumed/"
    secondary: []
  conditions:
    - "API_CONTRACT in quality_gates_triggered"
  blocked_by_stage: []
  blocked_by_action:
    - "create-exposed-api-specs"
  human_gate:
    required: false
  status_model:
    artifact_on_pass: ai_validated
    artifact_on_gate_accept: accepted
    artifact_on_fail: failed
```

### Action: create-database-schema-specs

```yaml
- action_id: create-database-schema-specs
  stage_id: "4b-quality-gates"
  title: "Create database schema specifications"
  persona: engineering-lead
  skill_ref: ".b2s/skills/engineering-lead/create-database-schema-specs.md"
  artifact_template_ref: ".b2s/artifact-templates/database-schema-spec.md"
  inputs:
    required:
      - "architecture/architecture-review.md"
      - "architecture/architecture-rules.md"
      - "planning/delivery-structure.md"
    optional:
      - "business-analysis/requirements.md"
      - "business-analysis/business-rules.md"
      - "input/brs.md"
  outputs:
    primary: "technical-specifications/database/"
    secondary: []
  conditions:
    - "DATA_CONTRACT in quality_gates_triggered"
  blocked_by_stage: []
  blocked_by_action:
    - "create-data-contract"
  human_gate:
    required: false
  status_model:
    artifact_on_pass: ai_validated
    artifact_on_gate_accept: accepted
    artifact_on_fail: failed
```

### Action: create-integration-specs

```yaml
- action_id: create-integration-specs
  stage_id: "4b-quality-gates"
  title: "Create integration specifications"
  persona: engineering-lead
  skill_ref: ".b2s/skills/engineering-lead/create-integration-specs.md"
  artifact_template_ref: ".b2s/artifact-templates/integration-spec.md"
  inputs:
    required:
      - "architecture/architecture-review.md"
      - "architecture/architecture-rules.md"
    optional:
      - "planning/delivery-structure.md"
      - "input/brs.md"
      - "technical-specifications/api/consumed/"
  outputs:
    primary: "technical-specifications/integrations/"
    secondary: []
  conditions:
    - "API_CONTRACT in quality_gates_triggered or DATA_CONTRACT in quality_gates_triggered"
  blocked_by_stage: []
  blocked_by_action:
    - "create-consumed-api-specs"
  human_gate:
    required: false
  status_model:
    artifact_on_pass: ai_validated
    artifact_on_gate_accept: accepted
    artifact_on_fail: failed
```

---

## Step 4 — Update create-openspec-handoff optional inputs

Read the `create-openspec-handoff` action definition in `stage-actions.yaml`.

Add the following to its `optional` inputs:

```yaml
- "technical-specifications/api/exposed/"
- "technical-specifications/api/consumed/"
- "technical-specifications/database/"
- "technical-specifications/integrations/"
```

This allows story packages to be enriched with concrete endpoint paths, field names,
table structures, and integration constraints from the technical specifications.

---

## Step 5 — Verify

Run the full test suite:

```
python -m pytest .b2s/tests/ -q
```

Confirm all existing tests pass. The new actions have no test coverage yet — that is
addressed in prompt 05.

---

## Done criteria

- [ ] `api_contract_mode` parsed from readiness-check.md in state.py
- [ ] `api_contract_mode` added to workflow-state.json template with value null
- [ ] `readiness-check.md` artifact template has API contract mode row
- [ ] All four actions registered in stage-actions.yaml with correct conditions and blocked_by
- [ ] `create-openspec-handoff` optional inputs include all four technical-specifications/ paths
- [ ] All existing tests pass
