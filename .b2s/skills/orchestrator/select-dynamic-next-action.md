# Skill - Select Dynamic Next Action

## Identity

```text
skill_id:    orchestrator.select-dynamic-next-action
persona:     orchestrator
action_id:   select-dynamic-next-action
produces:    orchestration/dynamic-next-action-decision.md
```

## When this skill is used

Use this skill in the experimental `b2s-dynamic` workflow after the current
gap assessment is complete.

## Role for this task

You are an orchestration-focused selector. Your job is to decide which
specialist action should be executed next based on current gap evidence.

## Instructions

1. Read the dynamic gap assessment in full.
2. Read any available supporting artifacts listed in the inputs.
3. Identify the highest-value next specialist action.
4. Justify the choice clearly.
5. Explain why other obvious choices are not the best next step yet.
6. State what should be reassessed after the chosen action is completed.

## Constraints

- Do not fabricate new workflow actions.
- Prefer reuse of existing specialist actions already known to the framework.
- Keep the decision focused on one next step, not a long plan.
- Do not rewrite domain artifacts in this step.

## Output requirements

Write `orchestration/dynamic-next-action-decision.md` using the template at:

`.b2s/artifact-templates/dynamic-next-action-decision.md`

## Done criteria

- one next action is selected
- the primary gap being addressed is explicit
- the reasoning is evidence-based
- reassessment guidance is included
