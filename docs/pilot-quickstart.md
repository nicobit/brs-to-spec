# Pilot Quickstart

Use this on one real feature before rolling out broadly.

## Step 1 — Create the feature package

```bash
python tools/scripts/new_feature.py <feature-name>
```

Example:

```bash
python tools/scripts/new_feature.py onboarding-client-approval
```

This creates:

```text
features/<feature-name>/
  input/
  business-intake/
  engineering-contracts/
  openspec-change/
  quality-gates/
  reviews/
```

## Step 2 — Add inputs

Put the converted BRS here:

```text
features/<feature-name>/input/brs-original.md
```

Put the draft architecture here:

```text
features/<feature-name>/input/architecture-draft.md
```

## Step 3 — Business intake

Run these prompts:

```text
prompts/01-business-intake/02-extract-requirements.md
prompts/01-business-intake/05-create-user-stories.md
prompts/01-business-intake/06-find-gaps-and-questions.md
```

Review with the Business PO.

Gate:

```text
features/<feature-name>/quality-gates/business-ready-checklist.md
```

## Step 4 — Engineering contract

Run:

```text
prompts/02-engineering-contracts/01-create-technical-spec.md
prompts/02-engineering-contracts/02-create-bdd-scenarios.md
prompts/02-engineering-contracts/03-create-test-strategy.md
```

Review with Architect / Tech Lead / QA.

Gate:

```text
features/<feature-name>/quality-gates/engineering-ready-checklist.md
```

## Step 5 — OpenSpec handoff

Run:

```text
prompts/03-openspec-handoff/01-create-openspec-proposal.md
prompts/03-openspec-handoff/02-create-openspec-design.md
prompts/03-openspec-handoff/03-create-openspec-tasks.md
```

OpenSpec becomes the implementation source of truth.

## Step 6 — Copilot implementation

Use:

```text
prompts/04-copilot-implementation/01-implement-one-task.md
```

Implement one task at a time. Review each task before continuing.

## Step 7 — Review

Use:

```text
prompts/05-reviewers/01-senior-code-review.md
prompts/05-reviewers/02-qa-review.md
prompts/05-reviewers/03-architecture-review.md
prompts/05-reviewers/04-security-review.md
```

## Pilot success criteria

The pilot is successful if:

- Business PO agrees the stories and acceptance criteria reflect the BRS.
- Engineering can create small implementation tasks.
- Copilot implements one task without inventing architecture.
- Review effort decreases or quality improves.
- Tests are traceable to acceptance criteria.

## Updated pilot flow with epics and features

For the first pilot, run the business prompts in this order:

```text
01-summarize-brs.md
02-extract-requirements.md
03-review-brs-and-requirements-against-architecture.md
04-create-delivery-structure.md
05-create-user-stories.md
06-find-gaps-and-questions.md
07-create-business-test-expectations.md
```

The minimum business intake package is now:

```text
brs-summary.md
requirements.md
epics-and-features.md
user-stories.md
gaps-and-questions.md
```

# Pilot with Change Size Modes

For the first pilot, do not force the full framework.

Pick one of each if possible:

```text
one small change
one medium feature
one large/risky feature
```

## Pilot 1 — Small change

Goal:
Prove the minimal flow works without bureaucracy.

Use:

```text
requirements.md
epics-and-features.md
user-stories.md
gaps-and-questions.md
technical-spec.md
proposal.md
design.md
tasks.md
```

## Pilot 2 — Medium feature

Goal:
Prove BDD and test strategy improve quality.

Add:

```text
bdd-scenarios.md
test-strategy.md
```

## Pilot 3 — Large/risky feature

Goal:
Prove full governance helps with risk.

Add:

```text
business-test-expectations.md
test-plan.md
traceability-matrix.md
full quality gates
review prompts
```

## Pilot evaluation

After each pilot, ask:

```text
Which artifacts helped?
Which artifacts were unnecessary?
Did Copilot implement more safely?
Did reviewers find fewer issues?
Did QA have clearer acceptance criteria?
```

## If the input is a Word BRS

Start with:

```text
prompts/01-business-intake/00a-extract-brs-from-word.md
```

Then continue with:

```text
01-summarize-brs.md
02-extract-requirements.md
03-review-brs-and-requirements-against-architecture.md
04-create-delivery-structure.md
05-create-user-stories.md
```

## If an architecture draft exists

Run:

```text
prompts/01-business-intake/00b-extract-architecture-from-word.md
prompts/01-business-intake/03-review-brs-and-requirements-against-architecture.md
```

For small changes, the alignment review can be lightweight.

For medium and large/risky changes, it is strongly recommended.
