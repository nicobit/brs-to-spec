# Prompt 9 — README Positioning Update

Update the README and documentation of `brs-to-spec`.

The new positioning is:

`brs-to-spec` is an enterprise BRS intake and delivery-readiness framework that transforms raw business requirement documents into AI-ready story packages.

It is not a competitor to BMAD. It sits before BMAD, OpenSpec, GitHub Copilot, Codex, Claude Code, Cursor, Devin, or other coding agents.

The main value is:

```text
Raw enterprise BRS
→ clarified requirements
→ business rules
→ architecture impact
→ epics/features/stories
→ acceptance criteria
→ BDD scenarios
→ traceability
→ AI-ready coding handoff
```

Update the README to make the central output very clear:

The main output is not a collection of generic documents.
The main output is a delivery package containing:

- Epic packages
- Feature packages
- Story packages
- Acceptance Criteria
- BDD Scenarios
- Implementation Tasks
- Coding-Agent Prompts
- Traceability Matrix
- Readiness Report

Add a section called:

## What does brs-to-spec produce?

Show this structure:

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

Add a section called:

## How is this different from BMAD?

Explain:

- BMAD is a broad AI agile delivery method.
- brs-to-spec is focused on enterprise BRS normalization and AI-ready delivery package creation.
- brs-to-spec can feed BMAD, OpenSpec, Copilot, Codex, Claude Code, Cursor, or Devin.
- brs-to-spec is especially useful for regulated, brownfield, multi-team, architecture-constrained environments.

Add a section called:

## Delivery Modes

Explain:

- Compact
- Standard
- Full Governance

Add a section called:

## Golden Example

Link to the golden example and show snippets of:

- one Epic
- one Feature
- one Story Package
- one BDD scenario
- one Coding Prompt
- traceability matrix
