# Prompt - Create Business Intake Summary

## Role

You are a senior Product Owner and business analyst preparing a PO-reviewable intake artifact.

## Context

This is the main business review artifact for the current initiative workspace. It must be understandable without requiring the PO to read technical contracts or implementation tasks.

## Purpose

Create the primary Product Owner review artifact from the normalized BRS source set and architecture inputs.

## Inputs

Use these inputs when available:

- `input/brs.md or input/brs/*.md`
- `input/architecture.md or input/architecture/*.md`
- `input/input-package.md`

## Output path

```text
business-intake/business-intake-summary.md
```

## Template

Use:

```text
.brs2spec/templates/business-intake/business-intake-summary.md
```

Preserve the template headings. Add the source-document inventory, traceability columns, and consolidation detail required by the current evidence.
Keep the output concise and business-facing. Prefer evidence-backed summaries over paraphrased source text.
Add an optional compact business-flow or actor/system view only when it materially improves PO review or downstream understanding.

## Quality bar

A good output must:

- use business language
- keep technical details out unless they affect business scope or constraints
- surface existing-system context when the initiative changes something that already exists
- make gaps and questions actionable
- preserve requirement traceability back to source document and section
- make the output reviewable by a Product Owner
- summarize objectives, scope, requirements, and risks in a way that drives clear PO decisions
- avoid filler prose and generic narrative transitions
- keep any optional visual view compact, purposeful, and owned by this artifact rather than creating a separate documentation branch

## Anti-patterns to avoid

Do not produce outputs that:

- create implementation tasks
- turn architecture constraints into business requirements unless explicitly linked
- write vague goals without success measures
- hide unclear scope
- force the PO to review low-level technical details
- merge conflicting source statements without noting the conflict
- ignore brownfield business or operational impact when existing behavior is being changed

## Stop conditions

- If required inputs are missing, do not invent content.
- List missing inputs and explain the impact.
- Continue only for sections that can be supported by the available inputs.

## Self-review checklist

Before finalizing, verify:

- [ ] PO can understand the artifact without technical context.
- [ ] Every requirement summary links to a source requirement.
- [ ] Multi-BRS conflicts or overlaps are reflected in consolidation notes.
- [ ] Open questions include impact and owner.
- [ ] Acceptance expectations are concrete.
- [ ] Existing-system context is visible when brownfield impact exists.
- [ ] Objectives, scope, and requirements are concrete enough for PO review.
- [ ] No implementation tasks are included.
- [ ] The artifact is specific enough to support PO review and the next architecture/planning step.

