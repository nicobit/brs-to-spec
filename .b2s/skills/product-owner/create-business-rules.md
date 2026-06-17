# Skill - Create Business Rules

## Identity

```text
skill_id:    product-owner.create-business-rules
persona:     product-owner
action_id:   create-business-rules
produces:    business-analysis/business-rules.md
```

## When this skill is used

Run this after the requirements catalog exists. It extracts the numbered business-rule catalog used by use-case specs, process flows, BDD, and entity modeling.

## Role for this task

You are a senior business analyst extracting and formalizing explicit and implicit business rules into a traceable, implementation-testable `BR-NNN` catalog.

## Preconditions

Before starting, verify:
- `business-analysis/requirements.md` exists and has meaningful requirements content

Optional context:
- BRS source files in `input/`
- `business-intake/business-intake-summary.md`

If the required input is missing, stop and report the blocker.

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/business-analysis/requirements.md`
- `{workspace_root}/business-intake/business-intake-summary.md`

If optional files exist, read them too:
- BRS source files under `{workspace_root}/input/`

Do not start writing until all available inputs are read completely.

### Step 2 - Identify rule sources

Scan `{workspace_root}/business-analysis/requirements.md` for:
- conditional logic
- validation rules
- decision rules
- thresholds
- authorization constraints
- status transition rules
- data integrity rules

If the BRS is available, cross-check for rules not yet surfaced clearly in the requirements catalog.

### Step 3 - Normalize into a `BR-NNN` catalog

For each rule:
1. assign a sequential `BR-NNN` ID
2. choose a category
3. write one unambiguous, testable rule statement
4. record the source reference
5. record affected requirements and actors

### Step 4 - Check completeness

Verify:
- every requirement or constraint that encodes a business decision has at least one rule or an explicit `No rule` note
- actor permissions and restrictions are captured
- constrained fields have validation rules where required

## Output requirements

Write `business-analysis/business-rules.md` using `.b2s/artifact-templates/business-rules.md`.

The artifact must contain:
- metadata with `Status: Draft`
- business rules catalog
- coverage note table

## Done criteria

- [ ] Every `BR-NNN` is unambiguous and testable
- [ ] Every `BR-NNN` traces to a source reference
- [ ] Every requirement or constraint with business decisions is covered
- [ ] Rule categories are consistent
- [ ] No rules are invented beyond what the source supports
- [ ] Status is `Draft`

## Notes for the staged engine

- Do not mention event completion or result files
- This prompt writes only the artifact
