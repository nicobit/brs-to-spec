# .b2s Framework Improvement Prompts

This ZIP contains an ordered set of prompts to improve the `.b2s` / `brs-to-spec` framework.

The goal is not to add more artifacts. The goal is to make the core delivery output stronger:

```text
BRS
  -> Requirements
  -> Business Rules
  -> Architecture Impact
  -> Epics
  -> Features
  -> Story Packages
  -> Acceptance Criteria
  -> BDD Scenarios
  -> Implementation Tasks
  -> Coding-Agent Prompts
```

## Recommended usage order

1. `01-strategic-refactoring.md`
2. `02-canonical-output-structure.md`
3. `03-story-package-template.md`
4. `04-epic-feature-packages.md`
5. `05-delivery-modes.md`
6. `06-bdd-rules.md`
7. `07-shallow-output-validators.md`
8. `08-golden-example.md`
9. `09-readme-positioning.md`

## Most important prompt

If you use only one prompt, start with:

```text
03-story-package-template.md
```

That prompt addresses the missing heart of the framework: high-quality AI-ready story packages.

## Core design decision

`.b2s` should not be positioned as a BMAD competitor.

It should be positioned as:

> An enterprise BRS intake and delivery-readiness layer before BMAD, OpenSpec, GitHub Copilot, Codex, Claude Code, Cursor, Devin, or other AI coding agents.

## Desired final output

The framework should make this the central generated output:

```text
delivery/
  epics/
  features/
  stories/
    F-001.1-story-slug/
      story.md
      acceptance-criteria.md
      bdd-scenarios.md
      implementation-context.md
      tasks.md
      coding-prompt.md
      validation-checklist.md
```

Everything else in `.b2s` should support these delivery packages.
