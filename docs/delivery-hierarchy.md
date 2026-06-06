# Delivery Hierarchy

This project distinguishes requirements, epics, features, user stories, and tasks.

## Hierarchy

```text
Business Objective
  ↓
Epic
  ↓
Feature / Capability
  ↓
Requirement
  ↓
User Story
  ↓
Acceptance Criteria
  ↓
BDD Scenario
  ↓
Test Case
  ↓
OpenSpec Task
  ↓
Code
```

## Definitions

### Business Objective

A business outcome or goal.

Example:

```text
Improve control, traceability, and speed of client onboarding.
```

### Epic

A large business delivery container.

Example:

```text
EPIC-001 — Client Onboarding Workflow
```

### Feature / Capability

A product capability that delivers part of an epic.

Example:

```text
FEAT-001 — Onboarding Request Creation
FEAT-002 — Compliance Approval
FEAT-003 — Status Tracking
FEAT-004 — Audit Trail
```

### Requirement

A condition, rule, or behavior that must be satisfied.

Example:

```text
FR-001 — The system shall allow Relationship Managers to create onboarding requests.
SEC-001 — Only authorized users may create onboarding requests.
AUD-001 — Every status change must be auditable.
```

### User Story

A user-centered delivery increment.

Example:

```text
As a Relationship Manager,
I want to create an onboarding request,
so that the onboarding process can start.
```

### Acceptance Criteria

Concrete conditions that make a story acceptable.

Example:

```text
Given I am a Relationship Manager
When I submit a valid onboarding request
Then the system creates the request
And an audit event is recorded.
```

### BDD Scenario

A more executable behavioral scenario.

### Test Case

A concrete validation procedure.

### OpenSpec Task

An implementation task for engineers and Copilot.

## Requirements are not epics

A requirement is not automatically an epic or a feature.

One feature can satisfy multiple requirements.

One requirement can affect multiple features.

Example:

| Requirement | Feature |
|---|---|
| FR-001 Create onboarding request | FEAT-001 Onboarding Request Creation |
| SEC-001 Role-based access | FEAT-001 and FEAT-002 |
| AUD-001 Audit status changes | FEAT-001, FEAT-002, FEAT-004 |

## Why this matters

This prevents:

```text
BRS requirements becoming hundreds of disconnected user stories
```

and creates a clearer delivery model:

```text
business outcome → delivery slice → implementation task
```
