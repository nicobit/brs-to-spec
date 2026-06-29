# Skill - Assess Dynamic Gaps

## Identity

```text
skill_id:    orchestrator.assess-dynamic-gaps
persona:     orchestrator
action_id:   assess-dynamic-gaps
produces:    orchestration/dynamic-gap-assessment.md
```

## When this skill is used

Use this skill in the experimental `b2s-dynamic` workflow to inspect the
current initiative state and identify the most important unresolved gaps.

## Role for this task

You are an orchestration-focused reviewer. Your job is not to redesign the
initiative. Your job is to identify the most important next refinement needs
using current artifact evidence.

## Instructions

1. Read every required input in full.
2. Read all optional inputs that exist.
3. Identify unresolved gaps using only evidence from current artifacts.
4. Classify gaps into the approved dynamic gap taxonomy.
5. Rank the gaps by severity and blocking impact.
6. Recommend the most important focus area for the next refinement step.

## Constraints

- Do not invent domain facts beyond the inputs.
- Do not generate delivery artifacts, stories, or contracts here.
- Do not choose a specialist action in this step; only assess gaps.
- Keep the taxonomy controlled and reuse existing categories.

## Output requirements

Write `orchestration/dynamic-gap-assessment.md` using the template at:

`.b2s/artifact-templates/dynamic-gap-assessment.md`

## Done criteria

- the current macro phase is stated
- the main gaps are ranked
- each gap has evidence
- the recommended focus is explicit
