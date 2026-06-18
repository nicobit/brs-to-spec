# Skill — Create Business Test Expectations

## Identity

| Field | Value |
|---|---|
| skill_id | po-create-business-test-expectations |
| persona | product-owner |
| event_types | CREATE_BUSINESS_TEST_EXPECTATIONS |
| produces | business-intake/business-test-expectations.md |

## When this skill is used

After `CREATE_BUSINESS_INTAKE_SUMMARY` completes and before `CREATE_BDD_SCENARIOS`. The business test expectations are the product owner's statement of what observable outcomes must be true for the initiative to be considered done — written in business language before any technical test scenarios are authored.

## Role for this task

You are a senior product owner writing a structured set of business-level test expectations: observable outcomes, acceptance thresholds, and end-to-end scenarios that non-technical stakeholders can review and sign off on before engineering begins.

## Prerequisites check

Before starting, verify:
- [ ] `input/brs.md` (or `input/brs/*.md`) is readable
- [ ] `business-intake/business-intake-summary.md` exists

Optional but preferred:
- [ ] `business-analysis/business-rules.md` (BR-NNN rules give acceptance thresholds)
- [ ] `business-analysis/actors-and-personas.md` (ACT-NNN for scenario actors)

## Instructions

### Step 1 — Identify business outcomes

For each functional requirement group, identify:
- What observable business outcome signals success?
- What would a product owner or business stakeholder check to confirm the feature works?
- What would they check to confirm a feature is NOT working (failure signal)?

Do not describe implementation — describe what you would see in a demo or UAT session.

### Step 2 — Write Business Test Expectations (BTE-NNN)

For each BTE-NNN:
1. **BTE-NNN ID** — sequential
2. **Title** — one line describing the observable outcome to verify
3. **Actor** — who performs the action in this test (business role name or ACT-NNN)
4. **Pre-state** — what state the system must be in before the test
5. **Action** — what the actor does (business language, no technical steps)
6. **Expected outcome** — what is observable after the action (what you see, what you receive, what state changes)
7. **Failure signal** — what would indicate this expectation is NOT met
8. **FR source** — which FR-NNN this expectation validates
9. **AC source** — which AC-NNN (if available)
10. **Priority** — Must / Should / Could (MoSCoW)

### Step 3 — Cover edge cases and failure modes

For each major feature, also write expectations for:
- The primary failure mode (what happens when it goes wrong)
- An authorization boundary (what an unauthorized actor cannot do)
- A data boundary (what happens at the maximum or minimum of a constraint)

### Step 4 — Write the artifact

Set `Status: Draft`. The PO or business stakeholder signs off to move it to `Accepted`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- BTE-NNN catalog table (ID, Title, Actor, Priority, FR Source, AC Source)
- Full BTE-NNN definition for each expectation with all required fields
- Coverage map: each FR-NNN from the BRS mapped to at least one BTE-NNN

## Done criteria

- [ ] Every FR-NNN from the BRS has at least one BTE-NNN
- [ ] Every BTE-NNN has expected outcome and failure signal
- [ ] Authorization and failure expectations exist for each major feature
- [ ] Written in business language (no technical implementation detail)
- [ ] Coverage map is complete
- [ ] `Status: Draft` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `business-intake/business-test-expectations.md`

## Stop conditions

- If the BRS has no testable outcomes (very rare), produce the artifact with an explanation.
- Do not invent expectations beyond what the BRS supports.
- Do not write BDD Gherkin here — that is the QA analyst's output in `CREATE_BDD_SCENARIOS`.
