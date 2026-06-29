# Skill - Gate Epic Clarification

## Identity

```text
skill_id:    orchestrator.gate-epic-clarification
persona:     orchestrator
action_id:   gate-epic-clarification
produces:    epics/
```

## When this skill is used

This action represents the human clarification gate for the current epic.

## Role for this task

You are presenting the current epic's unresolved blocking questions for human clarification.

## Instructions

When presenting this gate, you MUST:

1. Summarize whether the epic has any unresolved blocking questions
2. If blockers exist, list them clearly
3. Tell the human that answers must be captured in:

```text
input/clarifications/{current_item}.yaml
```

4. Explain that after answers are captured, the epic shell will be regenerated before story generation continues

## Constraints

- Do not rewrite the clarification request artifact
- Do not self-approve this gate
- Do not present unrelated epic questions
- State changes for gate approval or rejection are handled outside this prompt
