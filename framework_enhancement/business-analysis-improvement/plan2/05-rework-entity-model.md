# Step 5 — Rework Entity Model as a First-Class Artifact

## Purpose

Promote `business-analysis/entity-model.md` from an optional side-path artifact to a first-class business-analysis output that derives primarily from `requirements.md`. The path and filename are unchanged — only the inputs, classification, and workflow position change.

## Prerequisite

Step 1 must be complete. `requirements.md` must exist in the workflow before the entity model can depend on it.

## Run this prompt

```text
Rework .brs2spec2 entity-model support so business-analysis/entity-model.md derives from requirements.md
and is treated as a first-class artifact for data-relevant initiatives.

Read the decision record first:
- framework_enhancement/business-analysis-improvement/plan2/00-decisions.md

Read the design references:
- framework_enhancement/business-analysis-improvement/artifact-map.md
- framework_enhancement/business-analysis-improvement/prompts/02-create-entity-model.md
- framework_enhancement/business-analysis-improvement/proposed-stage-design.md

Read the current framework files that will change:
- .brs2spec2/workflow/event-templates/EVT-TPL-030-create-entity-model.yaml
- .brs2spec2/artifact-templates/entity-model.md
- .brs2spec2/skills/product-owner/create-entity-model.md (if it exists)
- .brs2spec2/workflow/workflow-definition.yaml
- .brs2spec2/workflow/artifact-ownership.md

Make the following changes:

1. Update the skill prompt:
   .brs2spec2/skills/product-owner/create-entity-model.md
   - Change primary input from input/brs.md to business-analysis/requirements.md.
   - Base updated content on framework_enhancement/business-analysis-improvement/prompts/02-create-entity-model.md.
   - Retain ENT-NNN identifier scheme, Mermaid erDiagram, and PII flag — these are already in the framework.
   - Remove dependency on business-analysis/business-rules.md as a required input
     (it becomes optional — business rules may not exist yet when entity model runs in parallel).

2. Update EVT-TPL-030:
   - Change inputs.required to:
     - business-analysis/requirements.md
   - Change inputs.optional to:
     - business-analysis/business-rules.md
     - architecture/architecture-review.md (optional architecture feedback)
     - business-intake/business-intake-summary.md (fallback context)
   - Keep outputs.primary as business-analysis/entity-model.md (path is unchanged).
   - Update blocked_by: CREATE_REQUIREMENTS_CATALOG (set in Step 1 — confirm it is already there).
   - Add a conditional_blocking note: entity-model.md blocks data-contract generation when the initiative
     has data-relevant scope; it does not block architecture review or planning for non-data initiatives.

3. Update artifact-ownership.md:
   - entity-model.md is currently owned by architect — confirm whether this should change to product-owner.
   - Per the artifact-map.md design, entity model is business-level (not database schema).
   - If ownership changes to product-owner, update the entry.
   - If it stays with architect, add a note that it is produced during business-analysis phase.

4. Update workflow-definition.yaml:
   - Confirm CREATE_ENTITY_MODEL is blocked_by CREATE_REQUIREMENTS_CATALOG.
   - Confirm it is NOT blocking REVIEW_INITIAL_ARCHITECTURE — architecture can start before entity model is done.
   - Confirm it IS blocking CREATE_DATA_CONTRACT (conditional, data-heavy initiatives).

5. Do not change:
   - The artifact path (entity-model.md stays as-is — no renaming).
   - The ENT-NNN identifier scheme.
   - The Mermaid erDiagram requirement.
```

## Done when

- `EVT-TPL-030` inputs are `requirements.md` (required) and `business-rules.md` (optional)
- Entity model skill prompt derives from `requirements.md` as primary source
- `workflow-definition.yaml` shows entity model blocked by `CREATE_REQUIREMENTS_CATALOG`, not blocking architecture
- Artifact path remains `business-analysis/entity-model.md` (unchanged)
- Ownership decision recorded in `artifact-ownership.md`
