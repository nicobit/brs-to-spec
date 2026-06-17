# Step 3 — Update Workflow Overlap With Architecture

## Purpose

Encode the architecture overlap model in `workflow-definition.yaml` so architecture can start after the minimum business-analysis baseline, before analysis is fully elaborated.

This step is placed here — before per-UC files and entity model — because those artifacts will be wired into the workflow in Steps 4 and 5. If the overlap model is not encoded first, Steps 4 and 5 may introduce hard sequential dependencies that then need to be unwound.

## Prerequisite

Steps 1 and 2 must be complete. `requirements.md` and `use-cases.puml` must be wired into the workflow before the overlap model is encoded.

## Run this prompt

```text
Update .brs2spec2/workflow/workflow-definition.yaml to support the intended overlap between business analysis and architecture.

Read the decision record first:
- framework_enhancement/business-analysis-improvement/plan2/00-decisions.md

Read the design references:
- framework_enhancement/business-analysis-improvement/proposed-stage-design.md
  Focus on:
  - "What Must Exist Before Architecture Starts"
  - "Recommended Overlap Model"
  - "Architecture Entry Point"
  - "Recommended Dependency Graph"

Read the current framework context:
- .brs2spec2/workflow/workflow-definition.yaml
- .brs2spec2/workflow/event-templates/EVT-TPL-008-review-initial-architecture.yaml

Make the following changes to workflow-definition.yaml:

1. Architecture entry point
   Set REVIEW_INITIAL_ARCHITECTURE (EVT-TPL-008) as blocked_by:
   - CREATE_BUSINESS_INTAKE_SUMMARY
   - CREATE_REQUIREMENTS_CATALOG
   - FIND_GAPS_AND_QUESTIONS
   Remove any existing block that makes architecture wait for the full business-analysis phase.

2. Parallel analysis artifacts
   After CREATE_REQUIREMENTS_CATALOG completes, the following events must be allowed to run in parallel
   (none of them blocking each other):
   - CREATE_ENTITY_MODEL
   - CREATE_USE_CASE_DIAGRAM
   - CREATE_BUSINESS_RULES
   - FIND_GAPS_AND_QUESTIONS

3. Architecture feedback loop
   After REVIEW_INITIAL_ARCHITECTURE, architecture findings should be available to:
   - CREATE_ENTITY_MODEL (if not yet complete)
   - CREATE_USE_CASE_SPECS (as optional input)
   - CREATE_BUSINESS_RULES (as optional input)
   Encode this as optional_reads, not hard blockers.

4. Planning gate
   Confirm that delivery-structure and planning events remain blocked until both:
   - CREATE_USE_CASE_SPECS is complete
   - REVIEW_INITIAL_ARCHITECTURE is complete

5. Do not change
   - Stage numbers or stage names
   - Event template internal content (that is Step 6)
   - Any event not related to business analysis or architecture

After making changes, produce a short summary note at:
  framework_enhancement/business-analysis-improvement/plan2/03-overlap-summary.md
  describing the new dependency model in plain language (10-15 lines max).
```

## Done when

- `workflow-definition.yaml` encodes architecture entry after the minimum baseline
- `REVIEW_INITIAL_ARCHITECTURE` is no longer blocked by full business-analysis completion
- Parallel analysis artifacts are correctly unblocked after `CREATE_REQUIREMENTS_CATALOG`
- Planning gate still requires both UC specs and architecture review
- `03-overlap-summary.md` exists in this folder
