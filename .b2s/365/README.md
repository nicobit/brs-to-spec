# Office 365 Copilot Prompt Pack

This folder contains an ordered prompt set for using Office 365 Copilot to
follow the `.b2s` framework from BRS input through planning, readiness, quality
gates, and handoff artifacts.

## Scope

This pack covers:

- the minimum path to reach `planning/delivery-structure.md`
- the richer downstream path that produces BDD, test planning, quality-gate
  artifacts, and handoff outputs

`planning/delivery-structure.md` contains:

- epics
- features
- user stories
- FR coverage

## Ordered sequence

1. `01-route-initiative.md`
2. `02-create-business-intake-summary.md`
3. `03-business-intake-review-gate.md`
4. `04-create-requirements.md`
5. `05-create-use-case-diagram.md`
6. `06-create-use-case-specs.md`
7. `07-find-gaps-and-questions.md`
8. `08-review-initial-architecture.md`
9. `09-architecture-review-gate.md`
10. `10-create-delivery-structure.md`
11. `11-create-architecture-rules.md`
12. `12-check-engineering-readiness.md`
13. `13-engineering-readiness-review-gate.md`
14. `14-generate-initiative-context.md`
15. `15-create-bdd-scenarios.md`
16. `16-create-test-strategy.md`
17. `17-create-security-review.md`
18. `18-create-threat-model.md`
19. `19-create-api-contract.md`
20. `20-create-data-contract.md`
21. `21-create-event-contract.md`
22. `22-create-observability-plan.md`
23. `23-create-test-plan-per-story.md`
24. `24-create-openspec-handoff.md`
25. `25-create-standalone-handoff.md`
26. `26-create-compact-handoff.md`
27. `27-create-agile-planning-view.md`
28. `28-create-review-package.md`

## How to use each prompt

For each step:

1. Open the corresponding prompt file in this folder.
2. Give Office 365 Copilot every markdown input listed in the `Inputs to give
   Copilot` section.
3. Also give Copilot the referenced artifact template so it can preserve the
   required output structure.
4. Save the resulting output into the `Output file to create` path.
5. Do not continue to the next prompt until the current artifact is complete.

## Important framework stops

- After step 2, stop for the business intake review gate in step 3.
- After step 8, stop for the architecture review gate in step 9.
- After step 12, stop for the engineering readiness review gate in step 13.
- Do not skip those review points if you want to stay aligned with `.b2s`.

## Inputs Office 365 Copilot should receive

At minimum, give Copilot:

- the prompt text from this folder
- the listed markdown source inputs for that step
- the listed `.b2s/artifact-templates/...` file for that step

When a prompt lists `optional` inputs, include them if they already exist.

## Output target

The first major planning target is:

- `planning/delivery-structure.md`

That artifact is the framework planning hierarchy used for epics, features, and
user stories.

The richer downstream outputs can include:

- `engineering-readiness/readiness-check.md`
- `engineering-readiness/initiative-context.md`
- `quality-gates/bdd/`
- `quality-gates/test-strategy.md`
- `quality-gates/test-plans/`
- `quality-gates/security-review.md`
- `quality-gates/threat-model.md`
- `quality-gates/api-contract.md`
- `quality-gates/data-contract.md`
- `quality-gates/event-contract.md`
- `quality-gates/observability-plan.md`
- `specs/` for OpenSpec handoff
- `standalone-delivery/` for Standalone handoff
