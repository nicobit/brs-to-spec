# Step 4 — Replace Monolithic Use-Case Spec With Per-UC Files

## Purpose

Replace `business-analysis/use-case-spec.md` (one monolithic file) with `business-analysis/use-cases/UC-NNN.md` (one file per use case). This is the highest-risk step because the old path is referenced by several downstream event templates.

## Prerequisite

Steps 1–3 must be complete. The use-case diagram (`use-cases.puml`) must be wired into the workflow before per-UC specs can depend on it.

## Run this prompt

```text
Refactor .brs2spec2 so detailed use-case specs are written to business-analysis/use-cases/UC-NNN.md
instead of business-analysis/use-case-spec.md.

Read the decision record first:
- framework_enhancement/business-analysis-improvement/plan2/00-decisions.md

Read the design references:
- framework_enhancement/business-analysis-improvement/artifact-map.md
- framework_enhancement/business-analysis-improvement/prompts/04-create-use-case-spec.md
- framework_enhancement/business-analysis-improvement/proposed-stage-design.md

Read the current framework files that will change:
- .brs2spec2/workflow/event-templates/EVT-TPL-007-create-use-case-specs.yaml
- .brs2spec2/artifact-templates/use-case-spec.md
- .brs2spec2/skills/product-owner/create-use-case-specs.md (if it exists)
- .brs2spec2/workflow/artifact-ownership.md

Also search for all references to business-analysis/use-case-spec.md across .brs2spec2/:
- Check every event template for inputs or outputs referencing this path.
- Check every skill prompt for references to this path.
- Check every artifact template for references to this path.
List all files found before making changes.

Make the following changes:

1. Update the skill prompt:
   .brs2spec2/skills/product-owner/create-use-case-specs.md
   - Change output target from use-case-spec.md to use-cases/UC-NNN.md (one file per UC).
   - Base new content on framework_enhancement/business-analysis-improvement/prompts/04-create-use-case-spec.md.
   - The skill must produce one markdown file per UC-NNN identified in use-cases.puml.
   - No multiple UCs in one file.

2. Update the event template EVT-TPL-007:
   - Change outputs.primary from business-analysis/use-case-spec.md
     to business-analysis/use-cases/ (folder output).
   - Change inputs.required to:
     - business-analysis/requirements.md
     - business-analysis/use-cases.puml
   - Change inputs.optional to:
     - business-analysis/business-rules.md
     - business-analysis/actors-and-personas.md
     - architecture/architecture-review.md (optional architecture feedback)
   - Update validation_rules: check that use-cases/ folder exists and contains at least one UC-NNN.md.
   - Update blocked_by: CREATE_USE_CASE_DIAGRAM (already set in Step 2).

3. Create an artifact template for per-UC files:
   .brs2spec2/artifact-templates/use-case-detail.md
   Include: metadata, UC ID, title, primary actor, preconditions, main success scenario,
   alternative flows, exception paths, postconditions, business rules referenced, AC coverage.

4. Update artifact-ownership.md:
   - Change business-analysis/use-case-spec.md entry to business-analysis/use-cases/* owned by product-owner.
   - Add a deprecation note for the old path.

5. For every other file that references business-analysis/use-case-spec.md:
   - Replace the reference with business-analysis/use-cases/UC-*.md or business-analysis/use-cases/ as appropriate.
   - Do NOT update downstream event templates for planning, handoff, quality gates, or review-package —
     those are updated in Step 7.
   - Only update the business-analysis-phase files identified in the search above.

Note on naming:
- Folder: business-analysis/use-cases/ (hyphen, plural)
- Files: UC-001.md, UC-002.md … UC-NNN.md
- No underscores anywhere in the path.
```

## Done when

- `EVT-TPL-007` outputs to `business-analysis/use-cases/` not `use-case-spec.md`
- `EVT-TPL-007` inputs are `requirements.md` and `use-cases.puml`
- A new artifact template `use-case-detail.md` exists
- `artifact-ownership.md` reflects the new folder path
- All in-phase references to `use-case-spec.md` in business-analysis event templates and skills are updated
- Downstream consumers (planning, handoff, quality gates) are NOT yet changed — that is Step 7
- A list of all remaining downstream references to `use-case-spec.md` is noted for Step 7
