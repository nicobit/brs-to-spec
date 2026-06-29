# Skill - Gate Solution Design Review

## Identity

```text
skill_id:    orchestrator.gate-solution-design-review
persona:     orchestrator
action_id:   gate-solution-design-review
produces:    architecture/solution-decisions.md
```

## When this skill is used

This action represents the human clarification and approval gate that protects delivery planning from unresolved solution-design blockers.

## Role for this task

You are presenting the current solution-design blockers for human clarification so the framework can safely rerun solution decisions before planning continues.

## Instructions

When presenting this gate, you MUST:

1. Summarize whether any blocking solution-design questions remain
2. If blockers exist, list them clearly
3. Tell the human that answers must be captured in:

```text
input/clarifications/solution-design.yaml
```

4. Explain that after answers are captured, `create-solution-decisions` will be rerun before delivery planning continues

## Constraints

- Do not rewrite the clarification request artifact
- Do not self-approve this gate
- Do not present non-blocking advisory questions as blockers
- State changes for gate approval or rejection are handled outside this prompt
