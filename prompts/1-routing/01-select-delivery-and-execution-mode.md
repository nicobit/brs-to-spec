# Prompt â€” Select Delivery and Execution Mode

## Role

You are a delivery architect deciding the minimum safe process for an enterprise initiative.

## Context

This prompt routes the work. It must avoid both under-processing risky work and over-processing simple work.

## Purpose

Select both the delivery mode and execution mode, with clear rationale and trade-offs.

## Inputs

Use these inputs when available:

- `input/brs.md or input/brs/*.md`
- `input/architecture.md or input/architecture/*.md`
- `input/input-package.md`

## Output path

```text
routing/routing-decision.md
```

## Required output structure

```markdown
# Routing Decision

## Decision Summary

| Decision | Selected value | Reason | Confidence |
|---|---|---|---|
| Delivery mode | Fast / Standard / Enterprise / Enterprise + Modular |  |  |
| Execution mode | OpenSpec / Standalone / Business Copilot |  |  |

## Delivery Mode Assessment

| Criterion | Low / Medium / High | Evidence | Impact |
|---|---|---|---|
| Requirement ambiguity |  |  |  |
| Architecture impact |  |  |  |
| Compliance / audit relevance |  |  |  |
| Business criticality |  |  |  |
| Number of teams |  |  |  |
| Delivery size |  |  |  |
| AI context saturation risk |  |  |  |

## Execution Mode Assessment

| Criterion | OpenSpec | Standalone | Business Copilot |
|---|---|---|---|
| Available in project? |  |  |  |
| Recommended? |  |  |  |
| Reason |  |  |  |

## Required Next Prompts

| Step | Prompt | Required? | Reason |
|---|---|---|---|

## Prompts Not Needed

| Prompt | Reason not needed |
|---|---|

## Risks of Under-Processing

## Risks of Over-Processing
```

## Quality bar

A good output must:

- select the smallest safe workflow
- make OpenSpec default only when it is actually available and appropriate
- choose standalone when OpenSpec is not used
- justify Enterprise + Modular only when complexity really requires it
- include risks of both too much and too little process

## Anti-patterns to avoid

Do not produce outputs that:

- select Enterprise + Modular for every request
- force OpenSpec when the project does not use it
- give a decision without evidence
- hide uncertainty
- recommend all prompts by default

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Self-review checklist

Before finalizing, verify:

- [ ] Delivery mode and execution mode are both selected.
- [ ] Each major criterion includes evidence.
- [ ] Unnecessary prompts are explicitly excluded.
- [ ] Under-processing and over-processing risks are both described.
- [ ] The recommendation is practical for a real project.


