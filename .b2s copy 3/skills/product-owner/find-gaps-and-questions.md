# Skill - Find Gaps and Questions

## Identity

```text
skill_id:    product-owner.find-gaps-and-questions
persona:     product-owner
action_id:   find-gaps-and-questions
produces:    business-analysis/gaps-and-questions.md
```

## When this skill is used

Run this after the requirements catalog exists. It identifies ambiguities, missing specification, conflicts, and unanswered questions that could block architecture, planning, readiness, or handoff.

## Role for this task

You are a senior business analyst and product owner performing structured gap analysis across the intake summary, requirements, and any available business-analysis artifacts.

## Preconditions

Before starting, verify:
- `business-intake/business-intake-summary.md` exists
- `business-analysis/requirements.md` exists and has `FR-NNN` rows

Optional context:
- `business-analysis/entity-model.md`
- `business-analysis/use-cases.md`
- `business-analysis/business-rules.md`
- `architecture/architecture-review.md`

If a required input is missing, stop and report the blocker.

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/business-intake/business-intake-summary.md`
- `{workspace_root}/business-analysis/requirements.md`

If optional files exist, read them too:
- `{workspace_root}/business-analysis/entity-model.md`
- `{workspace_root}/business-analysis/use-cases.md`
- `{workspace_root}/business-analysis/business-rules.md`
- `{workspace_root}/architecture/architecture-review.md`

Do not start writing until all available inputs are read completely.

### Step 2 - Scan for gap categories

Review the source systematically for:
- ambiguity gaps
- missing specification gaps
- conflict gaps
- scope boundary gaps
- acceptance-criteria gaps
- integration or external-system gaps
- data ownership or lifecycle gaps

Review the source in sequence rather than relying on intuition. Ensure all major requirement clusters are covered.

### Step 3 - Cross-check optional artifacts

If optional artifacts exist:
- compare entities to owning requirements
- inspect use-case breadth for omitted behaviors
- inspect business-rule coverage for unresolved rules
- inspect architecture review findings for unresolved business questions

### Step 4 - Assign severity and ownership

For each gap, record:
- `GAP-NNN`
- category
- description
- impact
- severity: `Blocking`, `High`, or `Low`
- suggested resolution
- owner
- source

### Step 5 - Identify critical path

Separate:
- blocking gaps that must be resolved before planning or architecture progression
- high-severity gaps that should be resolved before handoff
- low-severity gaps that can proceed with explicit assumptions

## Output requirements

Write `business-analysis/gaps-and-questions.md` using `.b2s/artifact-templates/gaps-and-questions.md`.

The artifact must contain:
- metadata with `Status: Draft`
- gap catalog
- critical path sections
- coverage summary

## Done criteria

- [ ] Every major source area has been reviewed for each gap category
- [ ] Every `GAP-NNN` has severity, owner, and source reference
- [ ] Blocking gaps are explicitly listed
- [ ] Non-blocking gaps have explicit assumptions where progression is possible
- [ ] Open questions from the BRS are either represented as gaps or clearly already answered
- [ ] The artifact is not biased toward only the first few requirements
- [ ] No invented gaps remain
- [ ] Status is `Draft`

## Notes for the staged engine

- Do not mention orchestrator event queues or result files
- This prompt writes only the artifact
