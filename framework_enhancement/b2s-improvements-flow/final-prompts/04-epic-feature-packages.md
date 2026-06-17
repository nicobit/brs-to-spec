# Prompt 4 — Epic and Feature Package Templates

## Context

You are working on the `.b2s` framework at the root of this repository.

Currently the framework generates `planning/delivery-structure.md` which contains the Epic → Feature → Story hierarchy in a single flat document. Epics and Features are not standalone artifacts — they have no business context, no impacted system list, no risk section, and no success metrics. This makes them unsuitable as standalone review or planning artifacts.

Your task is to create two new artifact templates and two new skills so that Epics and Features become first-class reviewable artifacts generated from the existing business analysis inputs.

## Step 1 — Create epic-package.md artifact template

Create `.b2s/artifact-templates/epic-package.md`.

The template must contain these sections:

```markdown
# {{Epic ID}} — {{Epic Title}}

## Metadata

| Field | Value |
|---|---|
| Epic ID | {{epic_id}} |
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Status | Draft |

## Business Objective

{{2–4 sentences: what business capability does this epic deliver and why does it matter?}}

## Business Capabilities Delivered

- {{capability}}

## Scope

**In scope:**
- {{item}}

**Out of scope:**
- {{item}}

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| BRS | BRS-§N | |
| Requirement | FR-NNN | |
| Business Rule | BR-NNN | |

## Impacted Business Processes

| Process | Change Type | Notes |
|---|---|---|
| {{process name}} | New / Changed / Retired | |

## Impacted Systems and Modules

| System / Module | Change Type | Notes |
|---|---|---|
| {{system name}} | New integration / API change / Data change / UI change | |

## Features

| Feature ID | Feature Name | Priority | Increment | Notes |
|---|---|---|---|---|
| F-NNN | | Must / Should / Could | D1 / D2 | |

## Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| | Epic / External / Architecture | Yes / No | |

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| | Low / Medium / High | Low / Medium / High | |

## Success Metrics

| Metric | Target | Measurement Method |
|---|---|---|
| | | |

## Readiness Status

{{Draft / Ready for review / Accepted}}
```

## Step 2 — Create feature-package.md artifact template

Create `.b2s/artifact-templates/feature-package.md`.

The template must contain these sections:

```markdown
# {{Feature ID}} — {{Feature Title}}

## Metadata

| Field | Value |
|---|---|
| Feature ID | {{feature_id}} |
| Parent Epic | {{epic_id}} — {{epic_name}} |
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Status | Draft |

## Feature Goal

{{2–3 sentences: what coherent business capability does this feature deliver?}}

## Business Value

{{Why does this feature matter to the business? What is the cost of not having it?}}

## Scope

**In scope:**
- {{item}}

**Out of scope:**
- {{item}}

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| BRS | BRS-§N | |
| Requirement | FR-NNN | |
| Business Rule | BR-NNN | |

## Business Rules

| Rule ID | Rule | Impact on Feature |
|---|---|---|
| BR-NNN | {{rule}} | {{impact}} |

## Impacted Components

| Component | Type | Expected Change |
|---|---|---|
| {{component}} | API / UI / Service / Database / Event / Integration | |

## Stories

| Story ID | Story Title | Priority | Increment | Status |
|---|---|---|---|---|
| F-NNN.N | | Must / Should / Could | D1 / D2 | Draft |

## Acceptance Criteria Summary

{{High-level statement of what "done" looks like for this feature as a whole.}}

## BDD Coverage Expectations

{{Which scenario types are expected: happy path, negative, authorization, state transition, audit. List by story.}}

## Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| | Feature / Story / External | Yes / No | |

## Implementation Notes

{{Key technical or architectural decisions the implementing team must know before starting.}}

## Test Strategy Summary

{{What test types are required, what the coverage target is, and who owns sign-off.}}
```

## Step 3 — Create the create-epic-packages skill

Create `.b2s/skills/delivery-lead/create-epic-packages.md`.

The skill must:

1. Read in full before writing:
   - `{workspace_root}/planning/delivery-structure.md`
   - `{workspace_root}/business-intake/business-intake-summary.md`
   - `{workspace_root}/business-analysis/requirements.md`
   - `{workspace_root}/architecture/architecture-review.md`
   - If present: `{workspace_root}/business-analysis/business-rules.md`

2. Create one file per epic: `planning/epics/E-NNN-<slug>.md`

3. Populate every section from the inputs. Do not leave placeholder text.

4. Done criteria:
   - [ ] one file per epic in delivery-structure.md
   - [ ] every epic file has business objective, impacted systems, features list, risks, success metrics
   - [ ] source traceability links to real FR-NNN references
   - [ ] Status is Draft

## Step 4 — Create the create-feature-packages skill

Create `.b2s/skills/delivery-lead/create-feature-packages.md`.

The skill must:

1. Read in full before writing:
   - `{workspace_root}/planning/delivery-structure.md`
   - `{workspace_root}/planning/epics/` (all epic files)
   - `{workspace_root}/business-analysis/requirements.md`
   - `{workspace_root}/business-analysis/business-rules.md` (if present)
   - `{workspace_root}/architecture/architecture-review.md`
   - `{workspace_root}/business-analysis/actors-and-personas.md` (if present)

2. Create one file per feature: `planning/features/F-NNN-<slug>.md`

3. Populate every section from the inputs. Do not leave placeholder text.
   Specifically: every feature must name real impacted components from `architecture-review.md`, not generic labels.

4. Done criteria:
   - [ ] one file per feature in delivery-structure.md
   - [ ] every feature links back to its parent epic
   - [ ] every feature lists its stories with IDs
   - [ ] impacted components are named, not generic
   - [ ] BDD coverage expectations are stated
   - [ ] Status is Draft

## Step 5 — Register the new actions in stage-actions.yaml

Add two new action entries to `.b2s/workflow/stage-actions.yaml`, inside stage `3-planning-and-modular-delivery`, after `create-delivery-structure` and before `create-traceability-matrix`.

Action 1: `create-epic-packages`
- persona: delivery-lead
- skill_ref: `.b2s/skills/delivery-lead/create-epic-packages.md`
- artifact_template_ref: `.b2s/artifact-templates/epic-package.md`
- inputs required: `planning/delivery-structure.md`, `business-intake/business-intake-summary.md`, `business-analysis/requirements.md`, `architecture/architecture-review.md`
- inputs optional: `business-analysis/business-rules.md`
- outputs primary: `planning/epics/`
- validation_profile: artifact-package
- artifact_criticality: standard
- blocked_by_action: `[create-delivery-structure]`
- conditions: `[delivery_mode in [OpenSpec, Standalone]]`
- human_gate required: false

Action 2: `create-feature-packages`
- persona: delivery-lead
- skill_ref: `.b2s/skills/delivery-lead/create-feature-packages.md`
- artifact_template_ref: `.b2s/artifact-templates/feature-package.md`
- inputs required: `planning/delivery-structure.md`, `planning/epics/`, `business-analysis/requirements.md`, `architecture/architecture-review.md`
- inputs optional: `business-analysis/business-rules.md`, `business-analysis/actors-and-personas.md`
- outputs primary: `planning/features/`
- validation_profile: artifact-package
- artifact_criticality: standard
- blocked_by_action: `[create-epic-packages]`
- conditions: `[delivery_mode in [OpenSpec, Standalone]]`
- human_gate required: false

Use existing action entries in stage-actions.yaml as the format model. Copy the full YAML structure including source_event_template, selection_mode, status_model, and on_pass fields from a nearby action such as `create-delivery-structure`.

## Step 6 — Update create-openspec-handoff inputs

Read `.b2s/workflow/stage-actions.yaml`, action `create-openspec-handoff`.

Add to the optional inputs list:
- `planning/epics/`
- `planning/features/`

Read `.b2s/skills/engineering-lead/create-openspec-handoff.md`.

In Step 1 (Read all inputs), add to the "Read if present" list:
- `{workspace_root}/planning/epics/` — epic context for story traceability
- `{workspace_root}/planning/features/` — feature context for scope and business value

In the `story.md` Section 1 instruction, add: populate the Feature and Epic metadata fields from the feature-package and epic-package files when available.

## What not to change

- Do not change or remove `create-delivery-structure`.
- Do not change the `specs/` folder structure.
- Do not modify any initiative workspace files.
- Do not change existing stage IDs or stage ordering in workflow-definition.yaml.

## Done criteria

- [ ] `.b2s/artifact-templates/epic-package.md` exists with all required sections
- [ ] `.b2s/artifact-templates/feature-package.md` exists with all required sections
- [ ] `.b2s/skills/delivery-lead/create-epic-packages.md` exists with full instructions
- [ ] `.b2s/skills/delivery-lead/create-feature-packages.md` exists with full instructions
- [ ] `create-epic-packages` and `create-feature-packages` are registered in stage-actions.yaml
- [ ] `create-openspec-handoff` optional inputs include `planning/epics/` and `planning/features/`
- [ ] All existing tests still pass: `python -m pytest .b2s/tests/ -q`
