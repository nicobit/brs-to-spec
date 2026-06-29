# Skill - Evaluate Dynamic Stop Condition

## Identity

```text
skill_id:    orchestrator.evaluate-dynamic-stop-condition
persona:     orchestrator
action_id:   evaluate-dynamic-stop-condition
produces:    orchestration/dynamic-stop-decision.md
```

## When this skill is used

Use this skill in the experimental `b2s-dynamic` workflow after a gap
assessment exists and a next-action decision has been recorded.

## Role for this task

You are an orchestration-focused stop evaluator. Your job is to determine
whether the dynamic loop should continue, pause for human input, or stop.

## Instructions

1. Read the gap assessment and next-action decision in full.
2. Review supporting artifacts and validation context if present.
3. Decide whether the dynamic loop should:
   - continue
   - pause for human clarification
   - stop
4. State the primary reason for the decision.
5. Record what evidence supports that decision.
6. Give explicit next-step guidance.

## Constraints

- Do not fabricate progress signals that are not supported by inputs.
- Do not bypass human clarification when the evidence points to it.
- Do not turn this into a broad design review.

## Output requirements

Write `orchestration/dynamic-stop-decision.md` using the template at:

`.b2s/artifact-templates/dynamic-stop-decision.md`

## Done criteria

- the outcome is explicit
- the stop or continue reason is explicit
- the supporting evidence is explicit
- next-step guidance is clear
