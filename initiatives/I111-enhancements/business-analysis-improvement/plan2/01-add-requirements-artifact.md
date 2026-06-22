# Step 1 — Add the Requirements Artifact

## Purpose

Introduce `business-analysis/requirements.md` as the canonical business-analysis entry point. This becomes the artifact that all other business-analysis artifacts derive from.

## Prerequisite

Step 0 (`00-decisions.md`) must be complete.

## Run this prompt

```text
Implement support for business-analysis/requirements.md in .brs2spec2.

Read the decision record first:
- framework_enhancement/business-analysis-improvement/plan2/00-decisions.md

Read the design references:
- framework_enhancement/business-analysis-improvement/artifact-map.md
- framework_enhancement/business-analysis-improvement/prompts/01-create-requirements.md
- framework_enhancement/business-analysis-improvement/proposed-stage-design.md

Read the current framework context:
- .brs2spec2/workflow/workflow-definition.yaml
- .brs2spec2/workflow/artifact-ownership.md
- .brs2spec2/workflow/event-templates/EVT-TPL-002-create-business-intake-summary.yaml
- .brs2spec2/skills/product-owner/ (list files)

Make the following changes:

1. Create a new skill prompt:
   .brs2spec2/skills/product-owner/create-requirements.md
   Base the content on framework_enhancement/business-analysis-improvement/prompts/01-create-requirements.md.
   Adapt it to use initiative-local paths and the framework's skill prompt conventions.

2. Create an artifact template:
   .brs2spec2/artifact-templates/requirements.md
   Model the structure after existing artifact templates (e.g., artifact-templates/business-rules.md).
   Include: metadata table, FR table, NFR table, constraints table.

3. Create a new event template:
   .brs2spec2/workflow/event-templates/EVT-TPL-043-create-requirements.yaml
   (EVT-TPL-042 is the current highest number — 043 is pre-assigned for this step.)
   Follow the YAML structure of existing event templates.
   Set:
   - type: CREATE_REQUIREMENTS_CATALOG
   - persona: product-owner
   - inputs.required: business-intake/business-intake-summary.md and input/brs.md
   - outputs.primary: business-analysis/requirements.md
   - on_success.update_state: mark artifact as ai_validated, keep stage as 2b-business-analysis

4. Update .brs2spec2/workflow/workflow-definition.yaml:
   - Add CREATE_REQUIREMENTS_CATALOG to stage 2b event list.
   - Set it as blocked_by CREATE_BUSINESS_INTAKE_SUMMARY.
   - Do not yet encode architecture overlap — that is Step 3.
   - Set CREATE_ENTITY_MODEL, CREATE_USE_CASE_DIAGRAM, CREATE_BUSINESS_RULES, and FIND_GAPS_AND_QUESTIONS as blocked_by CREATE_REQUIREMENTS_CATALOG.

5. Update .brs2spec2/workflow/artifact-ownership.md:
   - Add business-analysis/requirements.md owned by product-owner.

Verify after changes:
- No existing event template references have been broken.
- The new event template follows existing YAML conventions exactly.
- No downstream consumers have been changed yet — that is Step 7.
```

## Done when

- `.brs2spec2/skills/product-owner/create-requirements.md` exists
- `.brs2spec2/artifact-templates/requirements.md` exists
- `EVT-TPL-043-create-requirements.yaml` event template exists
- `workflow-definition.yaml` lists `CREATE_REQUIREMENTS_CATALOG` in stage 2b
- `artifact-ownership.md` includes `business-analysis/requirements.md`
- No existing event templates broken
