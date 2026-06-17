# Implementation Prompt — Phase 3: Workflow Definition and Event Templates

**Target:** `.brs2spec2/workflow/`  
**Prerequisites:** Engine complete; all persona files complete; Slice 1 skills complete and validated  
**Produces:** `workflow-definition.yaml` + event template files, built slice by slice

---

## Context

You are writing the workflow definition and event templates for brs-to-spec v2. These are the files the orchestrator reads to know what to do next and how to instantiate new events when a stage completes.

Read before writing:
- `.flow-engine/schemas/event-schema.yaml` — event template files follow this schema exactly
- `.flow-engine/instructions/dispatcher.md` — understand how templates are instantiated
- `.brs2spec2/workflow/workflow-definition.yaml` (write this first — it governs everything else)
- The architecture-and-plan.md stage graph for the full template list

**Build slice by slice. Do not write Slice 3 templates until Slice 1 and 2 are validated.**

---

## File 1: `workflow-definition.yaml`

Write this file first. It is the stage graph — the orchestrator reads it to know which templates to instantiate at each stage transition.

Structure:

```yaml
version: 2
framework: brs-to-spec
description: >
  Default workflow definition for brs-to-spec v2. Defines the stage sequence,
  which event templates to instantiate at each stage, dependencies between stages,
  and gate conditions for conditional stages.

stages:

  - id: "0-routing"
    name: "Initiative routing"
    description: "Determine delivery mode and execution mode"
    events:
      - template: EVT-TPL-001-route-initiative
        auto_create: true        # create immediately on initiative init
    gates: []
    next_stages:
      - id: "2-business-intake"
        condition: always

  - id: "2-business-intake"
    name: "Business intake"
    description: "Create business intake summary"
    events:
      - template: EVT-TPL-002-create-business-intake-summary
        blocked_by_stage: "0-routing"
    gates: []
    next_stages:
      - id: "2b-business-analysis"
        condition: always

  - id: "2b-business-analysis"
    name: "Business analysis"
    description: "Extract business rules, actors, process flows, use cases, entity model"
    events:
      - template: EVT-TPL-003-create-business-rules
        blocked_by_stage: "2-business-intake"
      - template: EVT-TPL-004-create-actors-and-personas
        blocked_by_stage: "2-business-intake"
      - template: EVT-TPL-005-create-process-flows
        blocked_by_stage: "2-business-intake"
      - template: EVT-TPL-006-create-use-case-specs
        blocked_by_stage: "2-business-intake"
      - template: EVT-TPL-007-create-entity-model
        blocked_by_stage: "2-business-intake"
    parallelizable: true          # all 5 events can run without dependencies on each other
    gates: []
    next_stages:
      - id: "3-planning"
        condition: always
```

Continue this pattern for all stages through stage 9. For each stage include:
- `id`, `name`, `description`
- `events` list with template IDs and `blocked_by_stage` or `blocked_by_artifacts`
- `parallelizable: true` where applicable (stages 2b, some of stage 4 gates)
- `gates` — list of gate names that are conditional (e.g. BDD gate, security gate)
- `gate_conditions` — what triggers each gate (copy from readiness-check logic in v1)
- `next_stages` with conditions

For gate-conditional events, add:
```yaml
  - template: EVT-TPL-018-create-bdd-scenarios
    condition: "readiness-check.gates.bdd == triggered"
    blocked_by_artifacts:
      - engineering-readiness/readiness-check.md
```

---

## Event template files — Slice 1

Write these two templates first. Run an end-to-end test before writing more.

### `event-templates/EVT-TPL-001-route-initiative.yaml`

```yaml
template_id: EVT-TPL-001-route-initiative
# When instantiated, the orchestrator fills in event_id, created_at, and initiative context.

type: ROUTE_INITIATIVE
persona: orchestrator
stage: "0-routing"
priority: critical

task:
  title: Route initiative — select delivery and execution mode
  objective: >
    Analyse the BRS and available inputs to select the correct delivery mode
    (OpenSpec / Standalone / FastPath / BusinessCopilot) and execution mode
    (Enterprise / Enterprise+Modular / Standard). Produce state/routing-decision.md
    with the decision, rationale, and any routing constraints.

skill_ref: .brs2spec2/skills/orchestrator/route-initiative.md
persona_ref: .brs2spec2/personas/orchestrator.md
artifact_template_ref: .brs2spec2/artifact-templates/routing-decision.md

read_from:
  - input/brs.md
  - input/brs/*.md                                     # OPTIONAL — glob if split BRS
  - input/architecture.md                              # OPTIONAL
  - input/input-package.md                             # OPTIONAL

required_inputs:
  - input/brs.md

write_to:
  - state/routing-decision.md

must_include:
  - delivery_mode field is present with one of: OpenSpec, Standalone, FastPath, BusinessCopilot
  - execution_mode field is present with one of: Enterprise, Enterprise+Modular, Standard
  - rationale for each decision is present
  - evidence section lists the criteria scored

validation_rules:
  natural_language:
    - delivery_mode is one of the four allowed values
    - execution_mode is one of the three allowed values
    - rationale is not empty for either decision
    - no placeholder text in output
  machine:
    - validator: no_placeholders
    - validator: status_field_required
      args:
        field: delivery_mode
        allowed: [OpenSpec, Standalone, FastPath, BusinessCopilot]

blocked_by: []

on_success:
  create_events:
    - EVT-TPL-002-create-business-intake-summary
  update_state:
    current_stage: "2-business-intake"
  append_log: true

on_failure:
  raise_decision:
    question: >
      Initiative routing failed — BRS does not have enough information to determine
      delivery mode. Review BRS objectives and functional requirements scope.
    owner: product-owner
    blocking: true

meta:
  created_by: orchestrator
  template_id: EVT-TPL-001-route-initiative
```

### `event-templates/EVT-TPL-002-create-business-intake-summary.yaml`

Write this following the same pattern as EVT-TPL-001. Key fields:

```yaml
template_id: EVT-TPL-002-create-business-intake-summary
type: CREATE_ARTIFACT
persona: product-owner
stage: "2-business-intake"
priority: high

skill_ref: .brs2spec2/skills/product-owner/create-business-intake-summary.md
persona_ref: .brs2spec2/personas/product-owner.md
artifact_template_ref: .brs2spec2/artifact-templates/business-intake-summary.md

read_from:
  - input/brs.md
  - input/brs/*.md                                     # OPTIONAL
  - state/routing-decision.md
  - input/architecture.md                              # OPTIONAL
  - input/input-package.md                             # OPTIONAL

required_inputs:
  - input/brs.md
  - state/routing-decision.md

write_to:
  - business-intake/business-intake-summary.md

must_include:
  - objectives section with measurable success criteria
  - scope section with explicit in-scope and out-of-scope statements
  - functional requirements with FR-NNN identifiers
  - gaps and open questions with owners
  - Status field in Metadata

validation_rules:
  natural_language:
    - every objective has at least one measurable success criterion
    - every gap has an assigned owner
    - scope boundaries are explicit (what is in scope and out of scope)
    - Status in Metadata is Draft or Accepted
    - no placeholder text (TBD / TODO / [fill in]) in output
  machine:
    - validator: no_placeholders
    - validator: id_pattern
      args:
        pattern: "FR-[0-9]{3}"
    - validator: status_field_required
      args:
        allowed: [Draft, Accepted]

blocked_by:
  - state/routing-decision.md

on_success:
  create_events:
    - EVT-TPL-003-create-business-rules
    - EVT-TPL-004-create-actors-and-personas
    - EVT-TPL-005-create-process-flows
    - EVT-TPL-006-create-use-case-specs
    - EVT-TPL-007-create-entity-model
  update_state:
    current_stage: "2b-business-analysis"
  append_log: true

on_failure:
  raise_decision:
    question: >
      Business intake summary failed validation. BRS may be too vague to extract
      measurable objectives. PO must review BRS and resolve gaps before continuing.
    owner: product-owner
    blocking: false
```

---

## Event templates — Slices 3–6

Write one template per skill in the skills list. Follow the exact same pattern as the two templates above. For each template:

1. Set `template_id` matching the file name
2. Set `type` from the event type registry (check architecture-and-plan.md stage graph)
3. Set `persona` from the stage graph
4. Set `skill_ref`, `persona_ref`, `artifact_template_ref` using the paths from impl-05
5. Set `read_from` and `required_inputs` — port from the v1 skill's `## Inputs` section
6. Set `write_to` — port from the v1 skill's `## Output path` section
7. Set `must_include` — derive from the v1 skill's `## Done criteria` or `## Quality bar`
8. Set `validation_rules.natural_language` — derive from v1 must_include + done_criteria
9. Set `blocked_by` — the artifact(s) that must exist before this event can run
10. Set `on_success.create_events` — the next template(s) in the stage graph
11. Set `on_success.update_state.current_stage` — the next stage ID

**Template file naming convention:** `EVT-TPL-NNN-<short-slug>.yaml`

**Slice 3 templates (write after Slice 2 validates):**
- EVT-TPL-003-create-business-rules.yaml
- EVT-TPL-004-create-actors-and-personas.yaml
- EVT-TPL-005-create-process-flows.yaml
- EVT-TPL-006-create-use-case-specs.yaml
- EVT-TPL-007-create-entity-model.yaml

**Slice 4 templates:**
- EVT-TPL-008-create-delivery-structure-draft.yaml
- EVT-TPL-009-review-initial-architecture.yaml
- EVT-TPL-010-create-architecture-rules.yaml
- EVT-TPL-011-confirm-delivery-structure.yaml
- EVT-TPL-012-create-traceability-matrix.yaml
- EVT-TPL-013-identify-software-modules.yaml      (Enterprise+Modular only — add condition)
- EVT-TPL-014-map-capabilities-to-modules.yaml    (Enterprise+Modular only)
- EVT-TPL-015-define-delivery-increments.yaml     (Enterprise+Modular only)

**Slice 5 templates:**
- EVT-TPL-016-check-engineering-readiness.yaml
- EVT-TPL-017-generate-initiative-context.yaml
- EVT-TPL-018-create-bdd-scenarios.yaml           (gate-conditional)
- EVT-TPL-019-create-test-plans.yaml              (gate-conditional)
- EVT-TPL-020-create-test-strategy.yaml           (gate-conditional)
- EVT-TPL-021-create-security-review.yaml         (gate-conditional)
- EVT-TPL-022-create-threat-model.yaml            (gate-conditional)
- EVT-TPL-023-create-data-contract.yaml           (gate-conditional)
- EVT-TPL-024-create-api-contract.yaml            (gate-conditional)
- EVT-TPL-025-create-event-contract.yaml          (gate-conditional)
- EVT-TPL-026-create-observability-plan.yaml      (gate-conditional)

**Slice 6 templates:**
- EVT-TPL-027-create-openspec-handoff.yaml        (OpenSpec mode only)
- EVT-TPL-028-create-standalone-handoff.yaml      (Standalone mode only)
- EVT-TPL-029-create-compact-handoff.yaml         (FastPath mode only)
- EVT-TPL-030-create-review-package.yaml
- EVT-TPL-031-create-agile-planning-view.yaml
- EVT-TPL-032-implement-one-task.yaml
- EVT-TPL-033-fix-review-comments.yaml
- EVT-TPL-034-generate-test-stubs.yaml
- EVT-TPL-035-senior-code-review.yaml
- EVT-TPL-036-architecture-review-of-implementation.yaml
- EVT-TPL-037-qa-review.yaml
- EVT-TPL-038-security-review-of-implementation.yaml
- EVT-TPL-039-spec-correction.yaml

---

## Quality bar

- Every template must be valid YAML and conform to event-schema.yaml
- `validation_rules.natural_language` entries in each template must exactly match the `done_criteria` in the corresponding skill file
- Gate-conditional templates must include the condition field — they must not be instantiated without a triggered gate
- Delivery-mode-conditional templates (OpenSpec/Standalone/FastPath) must have a `condition` field that prevents instantiation in the wrong mode
- `on_success.create_events` must chain correctly — after each template completes, the next stage's templates must appear in pending/
