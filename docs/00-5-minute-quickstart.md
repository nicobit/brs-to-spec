# 5-Minute Quickstart

You have a BRS document (or notes from a business conversation). You want a governed, story-scoped engineering handoff. This guide gets you there.

---

## Step 1 — Create your initiative workspace

```bash
python .brs2spec/tools/scripts/new_initiative.py customer-onboarding --initiative-id I002
```

This creates:

```text
initiatives/I002-customer-onboarding/
  input/
  planning/
  routing/
```

---

## Step 2 — Add your BRS

Copy your BRS into:

```text
initiatives/I002-customer-onboarding/input/brs.md
```

If your BRS is a Word document or raw notes, the framework can convert it:

```text
.brs2spec/skills/0-input-preparation/01-convert-brs-word-to-markdown.md
```

Optionally, add architecture context at:

```text
initiatives/I002-customer-onboarding/input/architecture.md
```

If you have no architecture input, the framework will draft one from the BRS.

---

## Step 3 — Run the workflow

In your AI assistant (Copilot, Codex, Claude Code, Cursor), load this file:

```text
.brs2spec/brs-to-spec-run-workflow.md
```

Say: **"Run the workflow for I002-customer-onboarding"**

The orchestrator will:

1. Detect which artifacts are missing
2. Create the business intake summary
3. Draft or review the architecture
4. Build the delivery structure (epics, features, user stories)
5. Check engineering readiness
6. Run required quality gates (security, API contract, data contract — only when triggered)
7. Generate the story-scoped OpenSpec handoff

---

## Step 4 — Review the business intake

Open:

```text
initiatives/I002-customer-onboarding/business-intake/business-intake-summary.md
```

Check that:
- Business objectives have measurable success criteria
- Gaps and open questions are listed with owners
- Scope boundaries are explicit

If something is wrong, correct it before proceeding.

---

## Step 5 — Say "continue"

The workflow advances automatically after each artifact passes its quality bar. If it stops, it will tell you exactly what human input is needed. Provide it, then say "continue".

---

## Step 6 — Inspect the handoff

The final output is in:

```text
initiatives/I002-customer-onboarding/openspec/changes/
```

One folder per user story, for example:

```text
openspec/changes/
  dependency-graph.md            ← wave-ordered execution plan
  F-001.1-onboarding-submission/ ← one self-contained story folder
    proposal.md
    design.md
    tasks.md
    specs/
```

Copy the story folder into your code repository and implement one task at a time.

---

## What success looks like

When the workflow completes you will have a folder per user story in `openspec/changes/` and a `workflow-state.json` showing the workflow is complete. Open `openspec/changes/F-XXX.X-<story>/` and copy it into your code repository.

For the full artifact list, see [`HOW_TO_USE.md`](../HOW_TO_USE.md).

---

## If unsure where to start

Run the workflow. It detects where you are and does the next thing.

```text
.brs2spec/brs-to-spec-run-workflow.md
```

See `initiatives/I001-customer-onboarding/` for a fully worked example.
