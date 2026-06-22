# Step 9 — Validate the Redesigned Flow End to End

## Purpose

Run the redesigned business-analysis flow on a representative initiative to verify the full artifact chain works without manual patching. This step confirms the improvement is complete and usable.

## Prerequisite

All previous steps (0–8) must be complete.

Choose a representative initiative — one with real BRS content, not a skeleton. An initiative with meaningful domain data will surface entity model edge cases; one with multiple use cases will stress-test the per-file UC output.

## Run this prompt

```text
Validate the redesigned .brs2spec2 business-analysis flow end to end on a representative initiative.

Choose a suitable existing initiative workspace under initiatives/ — preferably one with a complete
input/brs.md and an existing business-intake-summary.md so the first stage does not need to rerun.

Read the updated framework to understand the new artifact chain:
- .brs2spec2/workflow/workflow-definition.yaml
- .brs2spec2/workflow/artifact-ownership.md
- The updated event templates for EVT-TPL-003, 004, 005, 006, 007, 030, and the new templates from Steps 1–2.

Run the following validation checks (do not produce actual initiative artifacts — only verify the framework
is correctly configured to produce them):

1. Event chain check
   Trace the dependency chain from CREATE_BUSINESS_INTAKE_SUMMARY through to CREATE_PROCESS_FLOWS.
   Confirm:
   - CREATE_REQUIREMENTS_CATALOG is blocked by CREATE_BUSINESS_INTAKE_SUMMARY only.
   - CREATE_ENTITY_MODEL, CREATE_USE_CASE_DIAGRAM, CREATE_BUSINESS_RULES, FIND_GAPS_AND_QUESTIONS
     are all blocked by CREATE_REQUIREMENTS_CATALOG.
   - REVIEW_INITIAL_ARCHITECTURE is blocked by CREATE_REQUIREMENTS_CATALOG and FIND_GAPS_AND_QUESTIONS only
     (not by the full analysis set).
   - CREATE_ACTORS_AND_PERSONAS is blocked by CREATE_USE_CASE_DIAGRAM.
   - CREATE_USE_CASE_SPECS is blocked by CREATE_USE_CASE_DIAGRAM.
   - CREATE_PROCESS_FLOWS is blocked by CREATE_USE_CASE_SPECS and CREATE_ACTORS_AND_PERSONAS.
   - Delivery structure and planning are blocked by CREATE_USE_CASE_SPECS and REVIEW_INITIAL_ARCHITECTURE.

2. Artifact path check
   Confirm all new and updated event templates reference valid artifact paths using hyphen naming:
   - business-analysis/requirements.md
   - business-analysis/use-cases.puml
   - business-analysis/use-cases.md
   - business-analysis/use-cases/UC-NNN.md (folder output)
   - business-analysis/entity-model.md
   No references to underscore-named variants should remain anywhere in .brs2spec2/.

   Additional check for the dual use-case diagram outputs:
   - Confirm EVT-TPL for CREATE_USE_CASE_DIAGRAM lists both use-cases.puml and use-cases.md as outputs.
   - Confirm the validation rule checks UC-NNN IDs are consistent between both files.
   - Confirm artifact-ownership.md lists both files.

3. Input completeness check
   For each event template in the business-analysis phase, confirm that all required inputs
   are produced by an upstream event in the dependency chain.
   Flag any required input that has no upstream producer — these are framework gaps.

4. Downstream reference check
   Confirm no downstream event template (planning, quality gates, handoff, review-package)
   still references business-analysis/use-case-spec.md.
   If any remain, list them as remediation items.

5. Produce a validation report at:
   framework_enhancement/business-analysis-improvement/plan2/09-validation-report.md

   Structure:
   - Event chain: pass / issues found
   - Artifact path naming: pass / issues found
   - Input completeness: pass / gaps found
   - Downstream references: pass / remaining references found
   - Overall status: ready to use / needs remediation
   - Remediation items (if any): list with file and issue
```

## Done when

- `09-validation-report.md` exists with all five check results
- Overall status is either "ready to use" or "needs remediation" with a clear list
- If remediation items exist, they are small and scoped — major issues indicate a prior step was incomplete and should be re-run before closing this plan
