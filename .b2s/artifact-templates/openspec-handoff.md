# OpenSpec Handoff

This template defines the required structure and content contract of the `specs/`
handoff package.

## Required folder structure

```text
specs/
  dependency-graph.md
  F-XXX.X-<slug>/
    story.md
    design.md
    tasks.md
    coding-prompt.md
```

One folder per story. Folder name must include the story ID and a slug derived
from the story title.

## dependency-graph.md

Must contain:
- full list of story IDs with titles
- dependency links
- external system dependencies per story
- major impacted areas per story
- recommended implementation order

## story.md - content contract

Must follow `.b2s/artifact-templates/story-package.md` exactly. All 12 sections
must be populated with specific content. No placeholder text is acceptable.

| Section | Required content |
|---|---|
| 1. User Story | As a / I want / so that with named actor; business goal in 2 to 5 sentences; explicit in and out of scope |
| 2. Source Traceability | FR-NNN, BR-NNN, AR-NNN, NFR-NNN, BRS section references |
| 3. Business Rules Applied | Every BR that constrains this story, with concrete impact statement |
| 4. Acceptance Criteria | Testable Given/When/Then, linked to FR-NNN and SCN-NNN, minimum: happy path and negative |
| 5. BDD Scenarios | Valid Gherkin, observable behavior only, minimum: happy path and validation or negative |
| 6. Implementation Context | Named components, data fields, API endpoints, UI screens, integration failure modes |
| 7. Constraints | Architecture rules plus security, compliance, supportability, resilience, and SLA constraints from NFR assessment |
| 8. Dependencies | Story and external dependencies, blocking flag |
| 9. Implementation Tasks | 3 to 8 concrete tasks, each with area and validation expectation |
| 10. Test Expectations | Specific unit, integration, API, UI, negative, permission, regression, and NFR verification tests |
| 11. Definition of Done | Confirmed checkboxes relevant to this story |
| 12. Coding-Agent Prompt | Self-contained prompt: business context, technical context, acceptance criteria, impacted files or areas, constraints, steps, tests, what not to change |

## design.md - content contract

Must contain:
- component list with layer and responsibility
- sequence flow for the main scenario
- data model changes
- API surface
- integration touchpoints and failure handling
- observability and audit expectations
- brownfield impact

## tasks.md - content contract

Must contain:
- all implementation tasks in execution order
- grouped by area: API, Service, Database, UI, Tests, Docs
- each task with what to build, acceptance expectation, and validation reference

## coding-prompt.md - content contract

Must be fully self-contained. A coding agent must be able to execute it without
reading any other file.

Must include:
- story goal
- business context
- technical context
- acceptance criteria summary
- impacted files or areas
- full component list
- full task list
- all constraints
- explicit do-not-touch rules
- tests to add or update
- validation checklist

## Quality bar

The handoff is complete only when:
- story count matches folder count exactly
- every story.md has all 12 sections with specific content
- every story links to at least one FR-NNN
- every story links to every relevant NFR-NNN
- every story has at least two valid BDD scenarios
- every coding-prompt.md is self-contained
- no folder covers more than one story
- no generic or placeholder content remains in any file

---
*This is a structural and content contract, not a fill-in artifact.*
