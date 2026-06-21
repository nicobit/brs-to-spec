# Skill - Create Feature Stories

## Identity

```text
skill_id:    delivery-lead.create-feature-stories
persona:     delivery-lead
action_id:   create-feature-stories
produces:    planning/stories/
```

## When this skill is used

Run after the delivery skeleton and epic packages exist. This skill generates one story file per feature, containing full story detail for all stories within that feature.

## Role for this task

You are an Agile Story Slicing Specialist. You create implementation-ready stories for each feature, with full business context, acceptance criteria, traceability, architecture impact, and readiness status.

## Preconditions

Before starting, verify:

- `planning/delivery-skeleton.md` exists and is readable
- `planning/epics/` directory exists with at least one epic file
- `requirements/atomic-requirements.md` exists and is readable
- `domain/capability-map.md` exists and is readable
- `architecture/architecture-impact-map.md` exists and is readable
- `governance/delivery-constitution.md` exists and is readable

Optional context:

- `domain/business-rules.md`
- `domain/domain-model.md`
- `architecture/architecture-review.md`
- `architecture/architecture-rules.md`
- `input/brs.md`

If a required input is missing, stop and report the blocker.

## Hard constraints

- Generate ONE file per feature, not one file per story
- File naming: `planning/stories/F-NNN-<slug>.md` where slug is derived from the feature title
- Every story must trace to at least one requirement (REQ/FR)
- Every story must have testable acceptance criteria in Given/When/Then format
- Stories must be independently implementable and sized for one focused session
- Do not cross architecture boundaries unless explicitly justified
- Respect the delivery constitution

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
Do not start writing until all inputs are read completely.

### Step 2 - Extract feature list from skeleton

From `delivery-skeleton.md`, extract every feature ID and its stories. Count features — the number of files you create must equal this count exactly.

### Step 3 - Generate stories per feature

For each feature, create `planning/stories/F-NNN-<slug>.md` using `.b2s/artifact-templates/feature-stories.md`.

For each story within the feature:

1. **User Story** — As a [specific actor], I want [action], so that [outcome]
2. **Business Context** — 2–3 sentences on why this story matters
3. **Linked Requirements** — REQ-NNN / FR-NNN from atomic-requirements
4. **Linked Business Rules** — BR-NNN from business-rules (if applicable)
5. **Linked Capability** — CAP-NNN from capability-map
6. **Actor** — specific role name, not "user"
7. **Primary Component** — from architecture review or impact map
8. **Impacted API / Data / Integration** — from architecture impact map
9. **Architecture Constraints** — AR-NNN that apply
10. **Priority and Increment** — from delivery skeleton
11. **Out of Scope** — what a developer might assume is included but is not
12. **Dependencies** — story or external dependencies
13. **Open Questions** — questions specific to this story
14. **Readiness** — Ready or Not Ready, with reason
15. **Acceptance Criteria** — at least 2 testable Given/When/Then criteria per story

### Step 4 - Build story traceability table

At the bottom of each file, populate the Story Traceability table and flag any Not Ready stories.

## Output requirements

Write one file per feature to `planning/stories/F-NNN-<slug>.md` using `.b2s/artifact-templates/feature-stories.md`.

## Done criteria

- [ ] One file per feature in the delivery skeleton
- [ ] Every story has a complete user story statement with a named actor
- [ ] Every story links to at least one REQ/FR
- [ ] Every story has at least 2 acceptance criteria in Given/When/Then format
- [ ] Every story has an explicit out-of-scope statement
- [ ] Every story has a readiness assessment
- [ ] Traceability table is populated in every file
- [ ] No placeholder text remains

## Stop conditions

- If `planning/delivery-skeleton.md` is missing, stop and report the blocker
- If `requirements/atomic-requirements.md` is missing, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes one file per feature
- Validation and state updates are handled by the `.b2s` engine
