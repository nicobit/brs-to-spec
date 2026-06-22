# Prompt — Create Business Rules

## Purpose

Create or update `business-analysis/business-rules.md` as the cross-cutting rule catalog for the initiative.

This prompt is adapted from `.brs2spec2/skills/product-owner/create-business-rules.md`, refocused to consume the canonical requirements artifact and to coexist with AIUP-style use-case artifacts.

## Instructions

Create or update `business-analysis/business-rules.md`.

Treat this artifact as the shared `BR-NNN` catalog for:

- validation rules
- authorization rules
- calculation rules
- state transition rules
- data integrity rules
- notification rules
- integration rules
- configuration and policy rules

## DO NOT

- Invent rules not supported by the requirements or BRS
- Write narrative summaries instead of testable rule statements
- Merge multiple independent rules into one row
- Compete with the use-case specs by restating full scenarios here

## Inputs

Required:

- `business-analysis/requirements.md`

Optional:

- `input/brs.md`
- `business-intake/business-intake-summary.md`
- architecture feedback that exposes integration boundaries or policy constraints

## Workflow

1. Scan the requirements and source BRS for constraints, decisions, validations, thresholds, and authorizations.
2. Assign sequential `BR-NNN` IDs.
3. Classify each rule.
4. Write each rule as a single, unambiguous, implementation-testable statement.
5. Record source references and affected requirements.
6. Where architecture has exposed integration constraints that are truly business-visible, reflect them here.

## Required structure

Suggested table:

| ID | Category | Rule Statement | Source | Affected Requirements | Affected Actors | Notes |
|---|---|---|---|---|---|---|
| BR-001 | Validation |  |  |  |  |  |

Also include a coverage table:

| Requirement ID | Business rule(s) | Status |
|---|---|---|
| FR-001 | BR-001, BR-002 | Covered / No rule |

## Quality rules

- Every `BR-NNN` must be testable.
- Rules must stay singular.
- Every FR or constraint that encodes a business decision should map to at least one rule.
- If a requirement is a pure process step with no rule, note that explicitly.

## Output expectations

This artifact is a supporting analysis artifact, not the primary behavior specification.

It should later support:

- use-case specifications
- process flows
- BDD generation
- architecture rule refinement
- implementation acceptance criteria

## Error handling

- If the initiative genuinely has very few explicit business rules, produce a small catalog and explain why.
- Do not create placeholder rules to fill the document.
