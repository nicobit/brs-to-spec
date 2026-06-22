# Prompt 15 - Deepen `.b2s` Artifact Validation

## Goal

Make the staged validator reject skeleton artifacts mechanically instead of
accepting them based on headings plus one sample row.

## Files to modify

- `.b2s/scripts/b2s_engine/validation.py`
- `.b2s/tests/test_engine_fixtures.py`
- add or extend fixtures under `.b2s/tests/fixtures/` as needed

## Required work

### Phase 1 validation baseline rule

Use deterministic, local source baselines only.

For this prompt, the validator should prefer these references:

- `business-intake-summary.md` validation may inspect:
  - `input/brs.md`
  - `input/brs/*.md`
- `requirements.md` validation may inspect:
  - `input/brs.md`
  - `input/brs/*.md`
  - `business-intake/business-intake-summary.md`
- `use-cases.md` and `use-cases.puml` validation may inspect:
  - `business-analysis/requirements.md`
- `readiness-check.md` validation may inspect:
  - the readiness artifact itself
  - directly required upstream artifacts only when needed for simple deterministic checks

Do not introduce semantic LLM-like reasoning into validation.

Phase 1 heuristics should use row counts, marker detection, placeholder
rejection, and simple source-pattern counts rather than trying to prove perfect
semantic completeness.

### `business-intake/business-intake-summary.md`

Strengthen `_validate_business_intake_summary()` so it checks more than basic
structure.

Add checks such as:

- Objectives section has real populated rows when objectives exist in source
- Requirements table is not suspiciously tiny for the source size
- Scope table is not left placeholder-only
- Capabilities table is not left placeholder-only
- Gaps and Questions table is populated when source contains unresolved items,
  TBDs, or explicit questions
- Consolidation Notes section exists and was not removed
- Existing-System Context is populated when source suggests brownfield or
  integration impact
- obvious placeholder/template-only outputs fail

Minimum Phase 1 rule:

- if the BRS contains multiple atomic requirement markers and the summary emits
  only one requirement row, fail
- if the BRS contains unresolved-question markers such as `?`, `TBD`, `open
  question`, or similar patterns and the summary has no GAP rows, fail
- if every populated table row still matches untouched template language, fail

### `business-analysis/requirements.md`

Strengthen `_validate_requirements_catalog()` to reject:

- untouched template rows
- blank titles or blank sources in all real rows
- generic user-story filler across the whole artifact
- empty NFR and Constraints sections that only preserve headings

Minimum Phase 1 rule:

- if the BRS contains multiple apparent functional requirement markers and the
  catalog contains only one FR row, fail
- if all FR rows still use the exact template user-story wording, fail
- if NFR or Constraints sections have headings only and no real populated rows,
  fail

### `business-analysis/use-cases.md` and `use-cases.puml`

Strengthen the use-case validators to check:

- actors exist, not only UC ids
- markdown UC catalog has non-placeholder rows
- plausible consistency between markdown and PUML outputs
- suspiciously tiny UC coverage fails when the requirements catalog is broad

Minimum Phase 1 rule:

- count FR rows in `business-analysis/requirements.md`
- if FR breadth is above a simple threshold such as 6+ FR rows and the use-case
  set has only 1 or 2 UCs, fail with a shallow-coverage reason
- require at least one actor declaration in both markdown and PUML outputs

### `engineering-readiness/readiness-check.md`

Strengthen readiness validation to check:

- real pass/fail values in the core checklist
- explicit Yes/No values in gate trigger decisions
- every "No" has non-empty justification text
- readiness score is a real numeric value
- decision row is populated

Minimum Phase 1 rule:

- fail if any gate row uses `No` without non-empty justification text
- fail if the readiness score is still template text such as `NN / 100`
- fail if the decision cell is blank

## Constraints

- prefer deterministic heuristics over semantic overreach
- phase 1 should reject obviously shallow artifacts without requiring perfect
  source-to-output semantic equivalence
- do not make the validator so strict that all thin-slice fixtures fail
- when choosing thresholds, document them clearly in code comments near the
  relevant checks

## Verification

Verify:

1. skeleton business-intake output fails validation
2. untouched or template-like requirements output fails validation
3. suspiciously shallow use-case output fails when requirements breadth is high
4. readiness output without gate justifications fails validation
5. existing good fixtures still pass after validator strengthening
