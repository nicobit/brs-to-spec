# Step 3 — Demote Intake Summary to Support Role

## Purpose

`business-intake-summary.md` is currently listed as a required input in several downstream event templates where `requirements.md` now exists and is the authoritative source. This step demotes it to optional in those templates, consistent with Principle 2 of the spec-anchoring design.

## Prerequisites

Step 1 complete. `spec-anchoring.md` exists and defines the enforcement rule:
> "Any event template where a canonical artifact exists must demote `business-intake-summary.md` to `inputs.optional`."

## Scope

Search `.brs2spec2/workflow/event-templates/` for all files that list `business-intake/business-intake-summary.md` as a **required** input AND also list `business-analysis/requirements.md` as a required input.

These are contradictory: if `requirements.md` is required, then `business-intake-summary.md` is background context, not a requirements source.

## Run this prompt

```text
Read the design anchor first:
- framework_enhancement/business-analysis-improvement/plan3/00-spec-anchoring-principles.md
  Focus on Principle 2 (summary vs. canonical distinction) and the encoding rule at the end.

Search .brs2spec2/workflow/event-templates/ for all YAML files that have BOTH:
  - business-intake/business-intake-summary.md under inputs.required
  - business-analysis/requirements.md under inputs.required

For each file found:
  Move business-intake/business-intake-summary.md from inputs.required to inputs.optional.
  Do not change any other field.
  Add a comment on the moved line: "# support context — requirements.md is the canonical source"

Also check event templates that list business-intake-summary.md as required but do NOT list
requirements.md — leave those unchanged. They may be early-stage events (e.g. EVT-TPL-043 itself)
where the intake summary is still the primary source.

Then check the following skill prompts for references to business-intake-summary.md as a primary
requirements source (phrases like "scan the intake summary for requirements", "derive FRs from the
intake summary"):
- .brs2spec2/skills/product-owner/create-entity-model.md
- .brs2spec2/skills/product-owner/create-business-rules.md
- .brs2spec2/skills/product-owner/find-gaps-and-questions.md
- .brs2spec2/skills/product-owner/create-actors-and-personas.md
- .brs2spec2/skills/product-owner/create-use-case-specs.md

For each skill prompt:
  If the Prerequisites check section still lists business-intake-summary.md as required,
  change it to optional with a note: "background context — requirements.md is the primary source."
  If the Instructions section says to scan intake-summary for requirements or actors,
  change it to say "read requirements.md first; intake-summary is fallback context only."
  Do not change any other section.

After all changes, produce a list of every file modified.
```

## Done when

- No event template lists `business-intake-summary.md` as required when `requirements.md` is also required
- Skill prompts treat `business-intake-summary.md` as fallback context, not as a primary source, when `requirements.md` is available
- No other fields changed in any template or skill
