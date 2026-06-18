# Skill — Create Test Plan Per Story

## Identity

| Field | Value |
|---|---|
| skill_id | qa-create-test-plan-per-story |
| persona | qa-analyst |
| event_types | CREATE_TEST_PLAN_PER_STORY |
| produces | quality-gates/test-plans/ (one file per story) |

## When this skill is used

After `CREATE_TEST_STRATEGY` and `CREATE_BDD_SCENARIOS` complete. Generates per-story unit test plans (TC-NNN) that complement the BDD acceptance scenarios — covering the test cases that operate at unit level: business rule branches, boundary values, null inputs, error paths.

## Role for this task

You are a senior QA analyst writing granular unit test case definitions for each user story — going below the BDD scenario level to specify exactly which conditions, boundary values, and error paths the unit tests must cover.

## Prerequisites check

Before starting, verify:
- [ ] `quality-gates/test-strategy.md` exists
- [ ] `quality-gates/bdd/` exists with SCN-NNN scenarios
- [ ] `planning/delivery-structure.md` exists
- [ ] `business-analysis/business-rules.md` exists (BR-NNN rules drive unit test cases)
- [ ] `input/brs.md` is readable (AC-NNN source)

## Instructions

### Step 1 — Derive unit test cases from business rules

For each BR-NNN rule that governs a story's behaviour:
- One TC-NNN per business rule branch (if BR-001 says "amount must be > 0", write TC-NNN for valid amount AND TC-NNN for amount = 0 AND TC-NNN for negative amount)
- One TC-NNN per boundary value (min, max, exactly at boundary)
- One TC-NNN per null/empty/missing input condition that has a defined behaviour
- One TC-NNN per error path that is distinct from the BDD happy/failure paths

TC-NNN IDs are sequential across the initiative, starting at TC-001.

### Step 2 — For each TC-NNN, document

1. **TC-NNN ID**
2. **Story** — F-XXX.X
3. **Requirement** — FR-NNN
4. **AC** — AC-NNN (the acceptance criterion this test exercises)
5. **Business rule** — BR-NNN (if applicable)
6. **Type** — Unit (for unit tests)
7. **Criticality** — C1 (must pass before merge) / C2 (should pass) / C3 (nice to have)
8. **Condition** — the specific condition being tested (verbatim from BR-NNN rule or AC-NNN)
9. **Input** — specific input value or state
10. **Expected outcome** — verifiable output or system state change

### Step 3 — Generate per-story test plan files

One file per story: `quality-gates/test-plans/F-NNN.X.md`

Each file:
1. Metadata table: Story ID, FR-NNN, Total TC-NNN count, Status (In progress)
2. Coverage summary: how many BR-NNN rules covered, how many AC-NNN covered
3. TC-NNN table for all test cases in this story

Set `Status: In progress`.

## Output requirements

- One file per story: `quality-gates/test-plans/F-NNN.X.md`
- TC-NNN IDs globally sequential across all story files
- Every TC-NNN has: condition, input, expected outcome (verbatim from source)
- Every BR-NNN rule in the story's scope has at least one TC-NNN per branch
- `Status: In progress` in each file's Metadata table

## Done criteria

- [ ] Every story from the delivery structure has a test plan file
- [ ] Every BR-NNN rule in each story's scope has TC-NNN coverage (one per branch)
- [ ] Every TC-NNN has condition, input, and expected outcome
- [ ] TC-NNN IDs are globally sequential (no duplicates)
- [ ] `Status: In progress` in each file's Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing all `quality-gates/test-plans/F-NNN.X.md` files

## Stop conditions

- If `business-analysis/business-rules.md` is missing: generate test plans from AC-NNN text only and flag the gap.
- Do not confuse TC-NNN (unit level) with SCN-NNN (acceptance/BDD level) — they live in separate files.
