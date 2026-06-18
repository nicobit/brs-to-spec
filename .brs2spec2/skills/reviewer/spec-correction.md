# Skill — Spec Correction

## Identity

| Field | Value |
|---|---|
| skill_id | rev-spec-correction |
| persona | reviewer |
| event_types | SPEC_CORRECTION |
| produces | Updated source artifact (varies by target) |

## When this skill is used

When a review finding or human feedback identifies an error in a framework artifact (delivery structure, use case spec, BDD scenario, architecture review, etc.) that must be corrected before the artifact can be used downstream.

This skill corrects existing artifacts — it does not create new ones.

## Role for this task

You are a senior reviewer applying a targeted, minimal correction to a specific artifact — fixing the identified error without expanding the correction scope or reopening decisions that were already made.

## Hard constraints

- Correct only the specific identified error — do not refactor surrounding content
- Do not change IDs (FR-NNN, AC-NNN, AR-NNN, SCN-NNN, etc.) without an explicit reason
- Do not change the artifact's scope or add content not in the approved source
- Do not mark an artifact as Accepted after correction — human sign-off is still required
- If the correction would require changes to multiple dependent artifacts: flag the impact chain before making any change

## Prerequisites check

Before starting, verify:
- The target artifact and the specific error to correct are clearly identified
- The correction is grounded in the BRS or another upstream artifact (not invented)

## Instructions

### Step 1 — Identify the exact correction

State explicitly:
- Target artifact path
- What is wrong (the error)
- What the correct content is (and its BRS or upstream source)
- Which other artifacts depend on the target (impact chain)

### Step 2 — Assess impact chain

For each dependent artifact:
- Does the correction change any ID that downstream artifacts reference?
- Does the correction change any scope that downstream artifacts depend on?

If the impact chain affects accepted quality gate artifacts: flag this to the human before making any change. Do not cascade corrections silently.

### Step 3 — Apply the minimal correction

Change only what is needed to fix the identified error. Do not improve, refactor, or add adjacent content.

### Step 4 — Document the correction

After correcting:
- What was changed and why
- Which artifacts in the impact chain need to be reviewed for consistency
- Whether any dependent artifact must be regenerated

## Output requirements

- The corrected artifact at its original path
- A brief correction note (can be in the result file) listing: what changed, source of truth, impact chain

## Done criteria

- [ ] The specific error is corrected
- [ ] No scope expansion beyond the correction
- [ ] Impact chain is explicitly listed
- [ ] Artifact status remains as-was (do not self-accept after correction)
- [ ] Result file written with `status: pass` and `artifacts_written` listing the corrected artifact path

## Stop conditions

- If the correction would require cascading changes to accepted gate artifacts: stop and surface this to the human.
- If the correct content cannot be derived from the BRS or an upstream artifact: stop and request clarification.
- Do not correct an artifact by inventing content not grounded in approved sources.
