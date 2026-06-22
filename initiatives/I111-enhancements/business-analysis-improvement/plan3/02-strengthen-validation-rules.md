# Step 2 — Strengthen Validation Rules for Canonical Artifacts

## Purpose

Add semantic adequacy checks to the four canonical artifact event templates. Current validation rules check structural presence (file exists, tables present, Status: Draft). This step adds cross-artifact coverage checks that enforce the spine is strong enough before downstream phases proceed.

## Prerequisites

Step 1 complete. `.brs2spec2/spec-anchoring.md` exists.

## Run this prompt

```text
Read the design anchor first:
- framework_enhancement/business-analysis-improvement/plan3/00-spec-anchoring-principles.md
  Focus on Principle 3 (semantic adequacy criteria for each canonical artifact).

Read the current event templates:
- .brs2spec2/workflow/event-templates/EVT-TPL-043-create-requirements.yaml
- .brs2spec2/workflow/event-templates/EVT-TPL-044-create-use-case-diagram.yaml
- .brs2spec2/workflow/event-templates/EVT-TPL-007-create-use-case-specs.yaml
- .brs2spec2/workflow/event-templates/EVT-TPL-005-find-gaps-and-questions.yaml

Make the following targeted changes to validation_rules.natural_language in each template.
Do not change inputs, outputs, must_include, or on_success.

--- EVT-TPL-043 CREATE_REQUIREMENTS_CATALOG ---

Extend validation_rules.natural_language to add after the current checks:
  (6) the count of FR-NNN rows is plausible given the scope described in business-intake-summary.md
      — flag if fewer than 3 FR-NNN rows exist for a non-trivial initiative;
  (7) every FR-NNN row has a Priority value (Must / Should / Could) and a non-blank Source;
  (8) no FR-NNN row has "TBD" or blank in the Acceptance Criteria column — if acceptance criteria
      are unknown, that must be surfaced as a GAP-NNN in gaps-and-questions.md, not left blank here.

--- EVT-TPL-044 CREATE_USE_CASE_DIAGRAM ---

Extend validation_rules.natural_language to add after the current checks:
  (8) every major user goal implied by FR-NNN rows in requirements.md has at least one UC-NNN —
      if a functional requirement describes a user action with no corresponding use case, flag it;
  (9) every actor named in FR-NNN rows or use-story format (As a [role]) appears as an actor node
      in use-cases.puml — no actor named in requirements can be absent from the diagram;
  (10) no UC-NNN was invented without a traceable FR-NNN source — every UC in the catalog table
       must cite at least one FR-NNN.

--- EVT-TPL-007 CREATE_USE_CASE_SPECS ---

Extend validation_rules.natural_language to add after the current checks:
  (8) for every UC-NNN in use-cases.puml, verify the corresponding UC file exists in use-cases/
      — this is a count check: UC count in .puml must equal file count in use-cases/;
  (9) every UC file's Primary Actor matches an ACT-NNN entry in actors-and-personas.md
      if that file exists — flag any actor name used in a UC file that has no ACT-NNN;
  (10) every UC file cites at least one BR-NNN rule in the Business Rules Referenced section,
       or explicitly states "No business rules apply to this use case" — blank is not acceptable;
  (11) no UC file has a Main Success Scenario step that names a technology, database, or
       implementation component — all steps must be in business language only.

--- EVT-TPL-005 FIND_GAPS_AND_QUESTIONS ---

Extend validation_rules.natural_language to add after the current checks:
  (5) every FR-NNN row in requirements.md has been reviewed — the gap catalog must contain
      either a GAP-NNN referencing that FR, or an explicit note that no gap was found for it;
  (6) every blocking gap (Severity: Blocking) has an Owner assigned — blank owner on a
      blocking gap is a validation failure;
  (7) if any blocking gap has neither a stated assumption nor a resolution, the artifact's
      Status must remain Draft and the on_failure path must be triggered — blocking gaps
      without assumptions or resolutions must not allow downstream planning to proceed.
```

## Done when

- EVT-TPL-043 validation checks FR count plausibility, Priority completeness, and AC-NNN non-blank
- EVT-TPL-044 validation checks UC coverage of FR-NNN rows, actor completeness, and no invented UCs
- EVT-TPL-007 validation checks UC count match, actor ID alignment, BR-NNN citation, and no tech language
- EVT-TPL-005 validation checks FR-level gap coverage, blocking gap ownership, and assumption completeness
