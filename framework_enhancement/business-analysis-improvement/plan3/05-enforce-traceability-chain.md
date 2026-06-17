# Step 5 — Enforce Traceability Chain into Planning and Handoff

## Purpose

Add explicit traceability enforcement to the planning and handoff events. Currently these events produce artifacts that may or may not cite the canonical spec artifacts. This step encodes the traceability chain from Principle 5 into `must_include` and `validation_rules` so every story, task, and handoff item carries a spec trace.

## Prerequisites

Steps 1–4 complete.

## Changes per event template

### EVT-TPL-011 — CREATE_DELIVERY_STRUCTURE

**Add to `must_include`:**
```yaml
- "Every F-NNN.X story row must cite at least one UC-NNN source in a 'Source' column
   or inline reference — stories with no UC-NNN or FR-NNN trace are not acceptable"
- "The FR Coverage table must account for every FR-NNN in requirements.md:
   each FR-NNN either maps to at least one F-NNN.X story, or is explicitly excluded
   with a documented reason (e.g. 'Handled by NFR-NNN / out of delivery scope')"
```

**Extend `validation_rules.natural_language`:**
```
(N) Read requirements.md and count FR-NNN rows. Read delivery-structure.md and count rows
    in the FR Coverage table. They must be equal — no FR-NNN may be silently omitted.
    For each FR-NNN row in the FR Coverage table: confirm at least one F-NNN.X story ID
    is listed, or a documented exclusion reason is present.
(N+1) For every F-NNN.X story in delivery-structure.md: confirm a UC-NNN or FR-NNN source
    is cited. A story with no spec trace is a validation failure.
```

### EVT-TPL-012 — CREATE_TRACEABILITY_MATRIX

**Add to `must_include`:**
```yaml
- "## UC-NNN to Story Matrix is present: every UC-NNN from use-cases/ maps to at least
   one F-NNN.X story, or is explicitly excluded with a reason"
- "## Requirements to UC Coverage table shows which FR-NNN rows are realized by which UC-NNN"
```

**Extend `validation_rules.natural_language`:**
```
(N) Verify that a UC-NNN to Story matrix exists. For every UC-NNN declared in use-cases.puml,
    check that at least one F-NNN.X story maps to it. A UC with no story coverage is a gap
    that must be listed in the Gaps section.
(N+1) Verify that a FR-NNN to UC-NNN coverage table exists, showing the chain:
    FR-NNN → UC-NNN → F-NNN.X. Any FR-NNN not covered by this chain must be in the Gaps section.
```

### EVT-TPL-024 — CREATE_OPENSPEC_HANDOFF

**Add to `must_include`:**
```yaml
- "Every story.md contains a 'Spec Sources' section listing the UC-NNN and FR-NNN sources
   for that story — blank Spec Sources is a validation failure"
- "Every coding-prompt.md references the AC-NNN it is implementing verbatim"
```

**Extend `validation_rules.natural_language`:**
```
(N) For every story folder in specs/: open story.md and verify a 'Spec Sources' section
    exists with at least one UC-NNN and one FR-NNN cited.
    If any story folder has no Spec Sources section, fail and list the folder names.
(N+1) For every coding-prompt.md: verify the AC-NNN being implemented is quoted verbatim
    from delivery-structure.md — paraphrasing is not acceptable.
```

### EVT-TPL-025 — CREATE_STANDALONE_HANDOFF

**Add to `must_include`:**
```yaml
- "Every task in tasks.md has FR-NNN, UC-NNN (or F-NNN.X), AC-NNN, and Evidence expected
   columns all populated — no blank required fields"
- "delivery-spec.md includes a Requirements Traceability section mapping FR-NNN to
   the relevant implementation tasks"
```

**Extend `validation_rules.natural_language`:**
```
(N) Verify every task in tasks.md has FR-NNN, at least one of (UC-NNN or F-NNN.X), AC-NNN,
    and Evidence expected all populated. A task with any blank required field is a failure.
(N+1) Verify delivery-spec.md has a Requirements Traceability section. Every FR-NNN from
    requirements.md must appear in it, either mapped to a task or explicitly excluded.
```

## Run this prompt

```text
Read the design anchor first:
- framework_enhancement/business-analysis-improvement/plan3/00-spec-anchoring-principles.md
  Focus on Principle 5 (traceability chain enforcement) and the enforcement points table.

Read the current files:
- .brs2spec2/workflow/event-templates/EVT-TPL-011-create-delivery-structure.yaml
- .brs2spec2/workflow/event-templates/EVT-TPL-012-create-traceability-matrix.yaml
- .brs2spec2/workflow/event-templates/EVT-TPL-024-create-openspec-handoff.yaml
- .brs2spec2/workflow/event-templates/EVT-TPL-025-create-standalone-handoff.yaml

Make the changes described in this step prompt for each file.
Do not change inputs, outputs, blocked_by, or on_success.
Only extend must_include and validation_rules as specified.

After changes, confirm that:
- Every modified template has a traceability check in both must_include and validation_rules
- No existing must_include or validation_rules content was removed
- The traceability checks cross-reference between artifacts (not just within the artifact being produced)
```

## Done when

- EVT-TPL-011 requires every story to cite a UC-NNN or FR-NNN source; requires FR Coverage table to match requirements.md count
- EVT-TPL-012 requires a UC-NNN to Story matrix and a FR-NNN to UC-NNN coverage table
- EVT-TPL-024 requires Spec Sources sections in every story.md; requires AC-NNN verbatim in coding-prompt.md
- EVT-TPL-025 requires UC-NNN / FR-NNN / AC-NNN on every task; requires Requirements Traceability in delivery-spec.md
