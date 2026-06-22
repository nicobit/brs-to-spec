# Skill - Validate FR Coverage

## Identity

```text
skill_id:    delivery-lead.validate-fr-coverage
persona:     delivery-lead
action_id:   validate-fr-coverage
produces:    planning/fr-coverage.md
```

## When this skill is used

Run after epic story files are generated. This skill validates that every canonical requirement from `atomic-requirements.md` is covered by at least one story and that downstream traceability is semantically consistent.

## Role for this task

You are a delivery lead performing a strict traceability review. You do not invent coverage. You report real coverage, real gaps, and real open questions.

## Preconditions

Before starting, verify:

- `requirements/atomic-requirements.md` exists and is readable
- `planning/delivery-skeleton.md` exists and is readable
- `epics/` exists with at least one story file

If a required input is missing, stop and report the blocker.

## Hard constraints

- Every requirement from `atomic-requirements.md` must appear in the coverage matrix
- Do not mark a requirement as Covered unless the referenced story file exists and describes the same business behavior
- Use canonical requirement titles from `atomic-requirements.md`
- Flag unknown or invented requirement IDs
- Surface unresolved questions and ambiguities instead of hiding them
- Coverage metrics must be mathematically correct

## Instructions

### Step 1 — Read the computed coverage data

The engine has pre-computed the coverage mapping in `.b2s/tmp/computed-coverage.json`.
This file is listed in `{computed_inputs}` in `current-inputs.json`.

**Read this file first.** It contains:
- `canonical_requirements` — every requirement ID and canonical title from atomic-requirements.md
- `stories` — every story file on disk with its linked requirement IDs, epic, and feature
- `coverage_matrix` — the pre-built mapping of requirements to stories with status
- `summary` — total, covered, not_covered, coverage_pct (pre-computed)

This data was derived deterministically from the actual files. Use it as the
authoritative source for the coverage report. Do NOT re-derive, guess, or
invent coverage data.

### Step 2 — Read additional inputs

Read every file listed in `{resolved_required_inputs}` in full.
Use these only for context (e.g., delivery-skeleton for capability mapping).
Do not use them to override the computed coverage data.

### Step 3 — Format the coverage matrix

Transcribe `coverage_matrix` from the computed data into the markdown table
defined by the artifact template. For each row use:
- `req_id` and `title` exactly as provided (do NOT rename or paraphrase)
- `epic`, `feature`, `story` exactly as provided
- `open_questions_propagated` exactly as provided
- `evidence` exactly as provided
- `status` exactly as provided

### Step 4 — Format the summary

Transcribe `summary` from the computed data into the Coverage Summary table.
The numbers MUST match exactly — do not recount or adjust.

### Step 5 — Document gaps and risks

For each row where `status` is `Not Covered`:
- Explain why (missing story, deferred, out of scope)
- Recommend an action (create story, defer to next wave, accept risk)

For rows where `open_questions_propagated` is `No`:
- Flag that unresolved questions need to be added to the story's Open Questions section

## Output requirements

Write `planning/fr-coverage.md` using `.b2s/artifact-templates/fr-coverage.md`.

## Done criteria

- [ ] Every canonical requirement appears in the matrix
- [ ] Covered rows point to real story files
- [ ] Requirement titles use canonical titles
- [ ] Unresolved questions are surfaced where relevant
- [ ] Summary counts and percentage are accurate
- [ ] No placeholder text remains

## Stop conditions

- If `requirements/atomic-requirements.md` is missing, stop and report the blocker
- If no story files exist under `epics/`, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes only the artifact
- Validation and state updates are handled by the `.b2s` engine
