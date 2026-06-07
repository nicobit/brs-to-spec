# Prompt — Create OpenSpec Change for Active Deliverable

## Purpose

Create one OpenSpec change for the active delivery increment only.

This prevents one massive engineering task list and avoids AI context saturation.

## Output folder

```text
openspec/changes/<deliverable-id>-<deliverable-name>/
  proposal.md
  design.md
  tasks.md
```

## Tasks output

Create small, sequential engineering tasks for this deliverable only.

Each task must include:
- objective,
- files likely to change,
- implementation note,
- explicit automated validation sub-task,
- completion criteria.

## Task sizing rules

- Do not create one massive checklist.
- Do not create tasks for future deliverables.
- Each task should have one responsibility.
- Each task should be independently reviewable.
- Each task should touch a small number of files.
- Each task should include a test or validation step.
- Prefer small tasks, but do not use a hard line-of-code limit as the only sizing rule.

## Output structure for tasks.md

```markdown
# Tasks — <Deliverable ID> <Deliverable Name>

## Task 1 — <Name>

- Objective:
- Files likely to change:
- Implementation notes:
- Validation sub-task:
- Completion criteria:
```
