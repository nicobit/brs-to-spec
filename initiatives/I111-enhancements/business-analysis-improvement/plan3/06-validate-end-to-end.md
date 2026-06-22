# Step 6 — Validate End to End

## Purpose

Confirm all plan 3 changes are consistent, complete, and do not conflict with plan 2 changes. Produce a validation report.

## Prerequisites

Steps 1–5 complete.

## Run this prompt

```text
Validate all plan 3 changes to .brs2spec2/.

Read the design anchor:
- framework_enhancement/business-analysis-improvement/plan3/00-spec-anchoring-principles.md

Run the following checks:

1. Spine declaration check
   - .brs2spec2/spec-anchoring.md exists
   - It names all four canonical artifact groups with paths and EVT-TPL producers
   - It defines support artifacts and their roles
   - It states the six enforcement rules
   - It declares the traceability chain

2. Ownership table check
   - .brs2spec2/workflow/artifact-ownership.md has a Spec role column
   - All four canonical artifact groups are marked CANONICAL
   - All support artifacts are marked SUPPORT
   - A cross-reference note points to spec-anchoring.md

3. Validation rule strengthening check
   For each of EVT-TPL-043, 044, 007, 005:
   - Confirm the new adequacy checks are present in validation_rules.natural_language
   - Confirm existing checks were not removed
   - Confirm no inputs, outputs, or on_success fields were changed

4. Intake-summary demotion check
   Search .brs2spec2/workflow/event-templates/ for all YAML files.
   For each file that lists requirements.md as required:
   - Confirm business-intake-summary.md is NOT also listed as required
   - Confirm it is either optional or absent
   Report any file where both are still required.

5. Gap-to-planning gate check
   Read EVT-TPL-011-create-delivery-structure.yaml:
   - must_include contains the blocking-gap resolution check
   - validation_rules references gaps-and-questions.md
   - on_failure is blocking: true with a gap-specific question
   Read the skill prompt create-delivery-structure.md:
   - Step 0 gap gate check is present before any story decomposition step

6. Traceability enforcement check
   Read EVT-TPL-011, 012, 024, 025:
   - Each has the traceability must_include additions from Step 5
   - Each has the cross-artifact validation_rules additions from Step 5
   - No existing content was removed

7. Conflict check with plan 2
   Confirm no plan 3 change contradicts a plan 2 change:
   - blocked_by dependencies from plan 2 are unchanged
   - artifact paths from plan 2 are unchanged
   - on_success chains from plan 2 are unchanged

Produce the validation report at:
framework_enhancement/business-analysis-improvement/plan3/06-validation-report.md

Structure:
- Check 1 Spine declaration: pass / issues
- Check 2 Ownership table: pass / issues
- Check 3 Validation strengthening: pass / issues per template
- Check 4 Intake-summary demotion: pass / remaining violations
- Check 5 Gap-to-planning gate: pass / issues
- Check 6 Traceability enforcement: pass / issues per template
- Check 7 Conflict with plan 2: pass / conflicts found
- Overall status: ready to use / needs remediation
- Remediation items (if any)
```

## Done when

- `06-validation-report.md` exists with all seven check results
- Overall status is "ready to use" or has a clear remediation list
