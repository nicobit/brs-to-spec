# Prompt 02 — Create Workflow Types Library

## Context

You are working on the `.b2s` framework at the root of this repository.

With workspace.py updated in prompt 01, the framework can now read workflow
files from an initiative's local `.b2s/workflow/` folder. This prompt creates
the central library of named workflow types that initiatives can be initialised with.

Read these files in full before starting:
- `.b2s/workflow/stage-actions.yaml`
- `.b2s/workflow/workflow-definition.yaml`

---

## Step 1 — Create the workflow-types directory structure

Create the following folder structure under `.b2s/`:

```
.b2s/
  workflow-types/
    enterprise-modular/
      stage-actions.yaml
      workflow-definition.yaml
      README.md
    fast-path/
      stage-actions.yaml
      workflow-definition.yaml
      README.md
```

---

## Step 2 — enterprise-modular workflow type

Copy the current `.b2s/workflow/stage-actions.yaml` to
`.b2s/workflow-types/enterprise-modular/stage-actions.yaml` unchanged.

Copy the current `.b2s/workflow/workflow-definition.yaml` to
`.b2s/workflow-types/enterprise-modular/workflow-definition.yaml` unchanged.

Create `.b2s/workflow-types/enterprise-modular/README.md`:

```markdown
# Workflow Type: enterprise-modular

## When to use

Use this workflow for initiatives that require the full staged delivery process:
business intake, detailed business analysis, architecture review, quality gates,
and full story package handoff.

Suitable for: regulated industries, complex multi-team deliveries, initiatives
with external integrations, initiatives requiring audit trails.

## Stages

0-routing → 2-business-intake → 2b-business-analysis → 3-planning →
4-engineering-readiness → 4b-quality-gates → 5-handoff → 6-review-package

## Quality gates

All quality gates are conditional — triggered only if the engineering readiness
check determines they are needed (BDD, test strategy, security review, API contract,
data contract, event contract, observability plan).

## Delivery modes supported

- OpenSpec (full story packages)
- Standalone (standalone handoff document)
- FastPath (compact handoff)
```

---

## Step 3 — fast-path workflow type

Create `.b2s/workflow-types/fast-path/workflow-definition.yaml` — a simplified
version with fewer stages:

```yaml
version: 1
framework: b2s
description: >
  Lightweight workflow for simple, low-risk initiatives that do not require
  full business analysis, quality gates, or story package generation.

constraints:
  single_active_action: true
  max_active_actions: 1
  state_files_orchestrator_only: true

stages:
  - id: "0-routing"
    name: "Initiative routing"
    execution_mode: serial
    actions:
      - route-initiative
    next_stages:
      - id: "2-business-intake"
        condition: always

  - id: "2-business-intake"
    name: "Business intake"
    execution_mode: serial
    actions:
      - create-business-intake-summary
    next_stages:
      - id: "3-planning"
        condition: always

  - id: "3-planning"
    name: "Planning"
    execution_mode: serial
    actions:
      - review-initial-architecture
      - create-delivery-structure
    next_stages:
      - id: "5-handoff"
        condition: always

  - id: "5-handoff"
    name: "Handoff"
    execution_mode: serial
    actions:
      - create-compact-handoff
    next_stages:
      - id: "6-review-package"
        condition: always

  - id: "6-review-package"
    name: "Review package"
    execution_mode: serial
    actions:
      - create-review-package
    next_stages: []

human_triggered_actions:
  - create-brs
  - spec-correction
```

Create `.b2s/workflow-types/fast-path/stage-actions.yaml` — include only the
actions referenced in the fast-path workflow-definition.yaml above. Copy the
relevant action definitions verbatim from the central `stage-actions.yaml`.
Do not include actions that are not referenced in the fast-path workflow.

Create `.b2s/workflow-types/fast-path/README.md`:

```markdown
# Workflow Type: fast-path

## When to use

Use this workflow for simple, low-risk, or internal initiatives where full
business analysis, quality gates, and story packages are not required.

Suitable for: internal tools, spikes, proof-of-concepts, small enhancements
with well-understood scope.

## Stages

0-routing → 2-business-intake → 3-planning → 5-handoff → 6-review-package

## What is skipped

- Detailed business analysis (requirements, use cases, business rules, actors)
- Quality gates (BDD, security review, API contract, etc.)
- Engineering readiness check
- Story packages (OpenSpec handoff replaced by compact handoff)

## Delivery modes supported

- FastPath only
```

---

## Step 4 — Add a workflow-types index

Create `.b2s/workflow-types/index.yaml`:

```yaml
version: 1
description: Registry of available workflow types for initiative initialisation.

workflow_types:
  - id: enterprise-modular
    path: ".b2s/workflow-types/enterprise-modular"
    description: "Full staged workflow with business analysis, quality gates, and story packages."
    suitable_for:
      - "Regulated industries"
      - "Multi-team deliveries"
      - "External integrations"
      - "Complex initiatives"
    delivery_modes:
      - OpenSpec
      - Standalone
      - FastPath

  - id: fast-path
    path: ".b2s/workflow-types/fast-path"
    description: "Lightweight workflow for simple or internal initiatives."
    suitable_for:
      - "Internal tools"
      - "Spikes and proof-of-concepts"
      - "Small enhancements"
    delivery_modes:
      - FastPath
```

---

## Step 5 — Verify

Run the full test suite:

```
python -m pytest .b2s/tests/ -q
```

All existing tests must pass. No engine code was changed in this prompt —
only new files were added.

---

## Done criteria

- [ ] `.b2s/workflow-types/enterprise-modular/stage-actions.yaml` is an exact copy of current central
- [ ] `.b2s/workflow-types/enterprise-modular/workflow-definition.yaml` is an exact copy of current central
- [ ] `.b2s/workflow-types/enterprise-modular/README.md` created
- [ ] `.b2s/workflow-types/fast-path/workflow-definition.yaml` created with 5 stages
- [ ] `.b2s/workflow-types/fast-path/stage-actions.yaml` contains only fast-path actions
- [ ] `.b2s/workflow-types/fast-path/README.md` created
- [ ] `.b2s/workflow-types/index.yaml` created with both types registered
- [ ] All existing tests pass
