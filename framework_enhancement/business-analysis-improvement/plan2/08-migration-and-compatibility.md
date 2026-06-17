# Step 8 — Migration and Compatibility

## Purpose

Define and implement the compatibility strategy for initiatives that already exist in the workspace. These initiatives were created before this improvement and may have `use-case-spec.md` instead of `use-cases/UC-*.md`, or `business-intake-summary.md` but no `requirements.md`.

## Prerequisite

Steps 1–7 must be complete. The full new framework must be in place before migration notes are written against it.

## Run this prompt

```text
Design and implement a compatibility strategy for existing initiatives after the business-analysis
artifact transition in .brs2spec2.

Read the decision record first:
- framework_enhancement/business-analysis-improvement/plan2/00-decisions.md
  Focus on the "Compatibility strategy" decision recorded in that file.

Read the updated framework for reference:
- .brs2spec2/workflow/workflow-definition.yaml
- .brs2spec2/workflow/artifact-ownership.md
- .brs2spec2/workflow/event-templates/EVT-TPL-007-create-use-case-specs.yaml (updated in Step 4)

Scan the initiatives/ folder for all existing initiative workspaces.
For each workspace found:
- Check whether business-analysis/use-case-spec.md exists.
- Check whether business-analysis/requirements.md exists.
- Check whether business-analysis/use-cases/ folder exists.
- Check whether business-analysis/use-cases.puml exists.

Produce the following:

1. A migration state table
   File: framework_enhancement/business-analysis-improvement/plan2/08-migration-state.md
   One row per initiative. Columns:
   - Initiative ID and slug
   - Has use-case-spec.md (yes/no)
   - Has requirements.md (yes/no)
   - Has use-cases.puml (yes/no)
   - Has use-cases/ folder (yes/no)
   - Recommended action (see below)

2. Recommended action per initiative state:
   - requirements.md missing + use-case-spec.md exists:
     Add a note in the initiative's .flow/decisions/ or state folder saying
     "requirements.md not yet generated — run CREATE_REQUIREMENTS_CATALOG before continuing."
     Do not generate requirements.md automatically.
   - use-case-spec.md exists + use-cases/ folder missing:
     Add a note that use-case-spec.md is deprecated.
     Do not split it automatically — that is a manual or initiative-level step.
   - use-cases.puml missing + use-cases/ folder missing:
     Note that the initiative has no UC diagram yet.
     If the initiative is still active, it should run CREATE_USE_CASE_DIAGRAM before CREATE_USE_CASE_SPECS.
   - All new artifacts present:
     Mark the initiative as fully migrated.

3. Framework-level compatibility guard
   If the compatibility decision in 00-decisions.md is "dual-read":
   - Identify every skill prompt and event template where the input reads use-case-spec.md.
   - For each, add a fallback note: "If use-cases/ folder does not exist, fall back to use-case-spec.md."
   - This is a temporary measure — set a removal condition in the note.
   If the decision is "cutover":
   - Confirm that Steps 4 and 7 have removed all use-case-spec.md references.
   - No additional framework changes needed.

4. Filename consistency check
   Search .brs2spec2/ for any remaining reference to entity_model.md (underscore).
   If found, replace with entity-model.md (hyphen).
   Search for any remaining reference to use_cases.puml or use_cases/ (underscore).
   If found, replace with use-cases.puml and use-cases/ (hyphen).
   These are naming errors from the AIUP reference design that must not appear in the framework.
```

## Done when

- `08-migration-state.md` exists with one row per initiative workspace found
- All existing initiatives have a recommended action recorded
- Framework-level compatibility guard is implemented per the decision in `00-decisions.md`
- No underscore-form artifact names remain in any `.brs2spec2` file
