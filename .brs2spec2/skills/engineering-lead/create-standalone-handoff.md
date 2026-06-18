# Skill — Create Standalone Handoff

## Identity

| Field | Value |
|---|---|
| skill_id | eng-create-standalone-handoff |
| persona | engineering-lead |
| event_types | CREATE_STANDALONE_HANDOFF |
| produces | standalone-delivery/D1-{deliverable-name}/ (folder) |

## When this skill is used

Only when `execution_mode` is `Standalone`. Standalone mode must not be lower quality than OpenSpec — the discipline difference is in format, not rigour.

Requires the same gate conditions as OpenSpec: readiness-check is Ready and all triggered quality gates are Accepted.

## Role for this task

You are an engineering lead preparing a disciplined standalone delivery package — deriving the handoff from the approved delivery shape plus initiative-specific architecture refinement.

## Prerequisites check

Before starting, verify:
- [ ] `engineering-readiness/readiness-check.md` is `Ready`
- [ ] All triggered quality gates are `Accepted`
- [ ] `planning/delivery-structure.md` has F-XXX.X story IDs (not just epics)
- [ ] `architecture/architecture-review.md` exists
- [ ] `architecture/architecture-rules.md` exists

If delivery-structure.md has no F-XXX.X stories (only epics or bullet points): stop and run `CREATE_DELIVERY_STRUCTURE` first. Do not invent tasks from epics.

## Instructions

### Step 1 — Read all inputs before writing

Read everything before writing any file:
- `engineering-readiness/readiness-check.md`
- `quality-gates/*.md` (all accepted gates)
- `planning/delivery-structure.md`
- `planning/traceability-matrix.md`
- `architecture/architecture-review.md`
- `architecture/architecture-rules.md`
- `business-intake/business-intake-summary.md`

### Step 2 — Generate all five mandatory output files

All five are required. Do not skip any:

```
standalone-delivery/D1-{deliverable-name}/
  delivery-spec.md
  implementation-plan.md
  tasks.md
  validation-plan.md
  review-checklist.md
```

**delivery-spec.md**: scope, FR-NNN requirements covered, AR-NNN architecture constraints, triggered quality gates with accepted status, risks, out-of-scope statement

**implementation-plan.md**: one section per F-XXX.X story — not per epic; include story statement, AC-NNN, FR-NNN, AR-NNN constraints, quality gate references

**tasks.md**: one task block per story per engineering concern (API, data, observability, security); each task must have: FR-NNN, F-XXX.X story, AC-NNN, AR-NNN (if applicable), Evidence expected; no blank fields

**validation-plan.md**: one validation task per AC-NNN; each references its SCN-NNN BDD scenario(s) or states "BDD not triggered"

**review-checklist.md**: reviewer checklist tied to gate artifacts and AR-NNN rules; one item per gate, one item per architectural constraint

### Step 3 — Quality bar

- Tasks must be engineering-ready concrete actions — not restatements of user stories
- Every task traces to a requirement, AC, and evidence expectation
- AR-NNN rule IDs cited explicitly (not generic "follow architecture rules")
- Quality gates reflected with Accepted status confirmation
- Out-of-scope explicitly stated in delivery-spec.md

## Done criteria

- [ ] All 5 output files present
- [ ] implementation-plan.md has one section per F-XXX.X story (not per epic)
- [ ] Every task in tasks.md has: FR-NNN, F-XXX.X, AC-NNN, Evidence expected (no blank fields)
- [ ] validation-plan.md has one entry per AC-NNN
- [ ] delivery-spec.md Requirements Covered table references all FR-NNN in scope
- [ ] AR-NNN rule IDs cited in tasks and checklist
- [ ] Result file written with `status: pass` and `artifacts_written` listing all 5 output files

## Stop conditions

- If delivery-structure.md has no F-XXX.X IDs: stop — run `CREATE_DELIVERY_STRUCTURE` first.
- If required inputs are missing or gates not Accepted: stop and list what is missing.
- Do not write tasks by copying user story text — every task must be a concrete engineering action.
