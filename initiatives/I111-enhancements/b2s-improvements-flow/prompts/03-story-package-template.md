# Prompt 3 — Create the Story Package Template

Create a new first-class `.b2s` artifact template called `story-package.md`.

This template must become the core delivery unit for AI-assisted implementation.

The story package must not be a simple user story table. It must be detailed enough for a coding agent to implement safely without guessing business rules, architecture constraints, or validation expectations.

Create the template with the following structure:

```markdown
# {{Story ID}} {{Story Title}}

## 1. Story Summary

### User Story

As a {{actor}},
I want to {{capability}},
so that {{business outcome}}.

### Business Goal

Explain the business purpose of this story in 2–5 sentences.

### Scope

In scope:
- ...

Out of scope:
- ...

## 2. Source Traceability

| Source Type | Reference | Description |
|---|---|---|
| BRS | BRS-XXX | ... |
| Requirement | FR-XXX | ... |
| Business Rule | BR-XXX | ... |
| Architecture Rule | AR-XXX | ... |
| NFR | NFR-XXX | ... |

## 3. Business Rules Applied

| Rule ID | Rule | Impact on this Story |
|---|---|---|
| BR-XXX | ... | ... |

## 4. Acceptance Criteria

Each acceptance criterion must be specific, testable, and traceable.

### AC-001: {{Name}}

Given ...
When ...
Then ...

Traceability:
- Requirement: FR-XXX
- Business Rule: BR-XXX
- BDD Scenario: SCN-XXX

## 5. BDD Scenarios

Include at least:
- happy path
- negative path
- validation scenario
- permission scenario where relevant
- integration failure scenario where relevant
- audit/compliance scenario where relevant

```gherkin
Scenario: {{Scenario name}}
  Given ...
  When ...
  Then ...
```

## 6. Implementation Context

### Impacted Components

| Component | Type | Expected Change |
|---|---|---|
| ... | API/UI/Service/Database/Event/Integration | ... |

### Data Impact

Describe new or changed data fields, entities, status values, audit events, or retention implications.

### API Impact

Describe endpoint, request, response, error handling, idempotency, and compatibility implications.

### UI Impact

Describe changed screens, user actions, validation messages, and accessibility expectations.

### Integration Impact

Describe upstream/downstream systems, failure modes, retries, timeouts, and fallbacks.

## 7. Constraints

The coding agent must respect these constraints:
- ...
- ...
- ...

## 8. Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| ... | Business/Technical/Architecture/Data/External | Yes/No | ... |

## 9. Implementation Tasks

Tasks must be concrete and executable.

| Task ID | Task | Area | Depends On | Validation |
|---|---|---|---|---|
| T-001 | ... | API/UI/DB/Test/Docs | ... | ... |

## 10. Test Expectations

Required tests:
- unit tests
- integration tests
- API tests
- UI tests where relevant
- regression tests
- negative tests
- permission tests
- audit/compliance tests where relevant

## 11. Definition of Done

The story is done only when:
- all acceptance criteria are implemented
- all BDD scenarios are covered by automated or documented manual tests
- traceability is updated
- architecture constraints are respected
- no blocking questions remain
- regression risks are addressed
- coding prompt has been executed and validated

## 12. Coding-Agent Prompt

Write a precise prompt that can be given to GitHub Copilot Agent, Claude Code, Codex, Cursor, Devin, or another coding agent.

The prompt must include:
- story goal
- files/components likely impacted
- constraints
- expected implementation steps
- tests to add/update
- validation checklist
- what not to change
```

Also create validation rules for this artifact:

1. Story must have an ID.
2. Story must have an actor, capability, and business outcome.
3. At least one source requirement must be linked.
4. At least one acceptance criterion must be present.
5. Every acceptance criterion must be testable.
6. BDD scenarios are mandatory in Standard and Full Governance mode.
7. Implementation tasks must not be generic.
8. Coding prompt must include constraints and tests.
9. The story must declare out-of-scope items.
10. The story must link to the traceability matrix.

Update the workflow so that story packages are generated after business rules, architecture review, and delivery structure are available.
