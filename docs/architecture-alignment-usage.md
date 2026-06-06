# How `brs-architecture-alignment.md` Is Used

The alignment artifact must not be created and forgotten.

It is an input/control artifact that connects:

```text
Business intent
+ Extracted requirements
+ Architecture constraints
  ↓
Better delivery structure
Better user stories
Better gaps/questions
Better technical spec
Better OpenSpec design/tasks
```

## Source artifact

```text
features/<feature-name>/business-intake/brs-architecture-alignment.md
```

## It is produced by

```text
prompts/01-business-intake/03-review-brs-and-requirements-against-architecture.md
```

## It should be consumed by

```text
prompts/01-business-intake/04-create-delivery-structure.md
prompts/01-business-intake/05-create-user-stories.md
prompts/01-business-intake/06-find-gaps-and-questions.md
prompts/02-engineering-contracts/01-create-technical-spec.md
prompts/03-openspec-handoff/01-create-openspec-proposal.md
prompts/03-openspec-handoff/02-create-openspec-design.md
prompts/03-openspec-handoff/03-create-openspec-tasks.md
prompts/08-enablement/01-identify-enablement-scope.md
```

## 1. Usage in delivery structure

The delivery structure prompt should use alignment findings to:

```text
identify feature boundaries
identify blocked features
identify architecture-dependent features
improve delivery slicing
avoid grouping requirements that belong to different architecture areas
```

Example:

```text
Alignment finding:
BRS expects real-time approval, but architecture shows batch processing.

Delivery structure response:
Create a separate feature for Approval Processing and mark architecture decision as blocking.
```

## 2. Usage in user stories

The user-story prompt should use alignment findings to:

```text
avoid inventing unsupported behavior
add open questions to stories
mark acceptance criteria that depend on unresolved architecture decisions
include architecture constraints where relevant
```

Example:

```text
Alignment finding:
Audit event payload is not defined.

User story response:
Do not invent audit fields. Add an open question under the relevant story.
```

## 3. Usage in gaps and questions

The gaps prompt should consolidate:

```text
business gaps
requirement gaps
architecture gaps
security gaps
data/integration gaps
audit/logging gaps
deployment/environment gaps
```

into:

```text
business-intake/gaps-and-questions.md
```

## 4. Usage in technical spec

The technical spec should explicitly address each relevant alignment finding.

Example:

```text
Alignment finding:
Architecture does not define approval state model.

Technical spec response:
Section 7 defines the state model, or carries it as an open architecture decision.
```

## 5. Usage in OpenSpec proposal

The proposal should include major constraints, risks, and unresolved decisions.

Example:

```text
Risk:
Current architecture draft does not define approval workflow state management.
```

## 6. Usage in OpenSpec design

The design must resolve or defer alignment findings.

Example:

```text
Decision:
Use existing workflow service for approval state transitions.

Deferred:
Audit event schema to be confirmed before Task 004.
```

## 7. Usage in OpenSpec tasks

If an alignment finding implies work, it should become a task.

Example:

```text
Missing architecture decision:
Audit event payload

OpenSpec task:
Task 004 — Define and implement audit event payload
```

## 8. Usage in Enablement Track

If alignment findings mention infrastructure, CI/CD, environment, observability, release, or operations, they should feed the Enablement Track.

Example:

```text
Alignment finding:
New event topic required but not defined in architecture.

Enablement response:
Create enablement scope item for messaging infrastructure and IaC task.
```

## Dependency chain

```text
brs-original.md
requirements.md
architecture-draft.md
  ↓
brs-architecture-alignment.md
  ↓
delivery structure
user stories
gaps and questions
technical spec
OpenSpec proposal
OpenSpec design
OpenSpec tasks
enablement scope
```

# Corrected Business Intake Sequence

For the full business intake sequence, use:

```text
00a-extract-brs-from-word.md
00b-extract-architecture-from-word.md
01-summarize-brs.md
02-extract-requirements.md
03-review-brs-and-requirements-against-architecture.md
04-create-delivery-structure.md
05-create-user-stories.md
06-find-gaps-and-questions.md
07-create-business-test-expectations.md
```

The mandatory alignment position is:

```text
02-extract-requirements.md
  ↓
03-review-brs-and-requirements-against-architecture.md
  ↓
04-create-delivery-structure.md
  ↓
05-create-user-stories.md
```

`brs-architecture-alignment.md` is created after requirements extraction and before delivery structure.

Reason:
The delivery structure must be informed by both the structured requirements and the architecture alignment findings.

# Relationship with Architecture & Contract Extensions

Architecture alignment findings may trigger optional architecture-contract artifacts.

| Alignment finding | Possible artifact |
|---|---|
| Missing architecture decision | ADR |
| API behavior unclear | API contract / OpenAPI |
| Business rules unclear | Domain model |
| Audit event payload unclear | Event contract |
| Database persistence unclear | Data model |
| Vague NFR | Quality attribute scenario |
| Security/authorization gap | Threat model |
