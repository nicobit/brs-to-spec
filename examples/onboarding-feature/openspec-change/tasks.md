# Tasks — Onboarding Approval

## Task 001 — Implement backend domain model and validation

Status: Not Started

### Parent Epic

- EPIC-001 — Client Onboarding Workflow

### Parent Feature / Capability

- FEAT-001 — Onboarding Request Creation

### Goal

Create or update the backend domain model for onboarding requests.

### Requirements Covered

- FR-001
- DATA-001

### User Stories / Acceptance Criteria Covered

- US-001
- AC-001
- AC-002

### Context Files to Read First

- `business-intake/requirements.md`
- `business-intake/epics-and-features.md`
- `business-intake/user-stories.md`
- `engineering-contracts/technical-spec.md`
- `openspec-change/design.md`

### Existing Code Areas to Inspect

- Existing domain models
- Existing validation approach
- Existing tests

### Implementation Instructions

- Follow existing domain patterns.
- Add mandatory field validation.
- Add unit tests.

### Do Not Do

- Do not create frontend code.
- Do not create approval workflow.
- Do not introduce new frameworks.

### Expected Changes

- Domain entity or model update.
- Validation logic.
- Unit tests.

### Tests Required

- Valid request creation.
- Missing mandatory fields.

### Definition of Done

- Code compiles.
- Unit tests pass.
- No unrelated refactoring.

## Task 002 — Implement create onboarding API endpoint

Status: Not Started

### Parent Epic

- EPIC-001 — Client Onboarding Workflow

### Parent Feature / Capability

- FEAT-001 — Onboarding Request Creation

### Goal

Expose backend API for creating onboarding requests.

### Requirements Covered

- FR-001
- SEC-001
- AUD-001

### User Stories / Acceptance Criteria Covered

- US-001
- AC-001
- AC-003

### Implementation Instructions

- Reuse existing API patterns.
- Enforce Relationship Manager authorization.
- Create audit event.
- Add API tests.

### Do Not Do

- Do not implement frontend.
- Do not implement approval/rejection.

### Definition of Done

- Endpoint works.
- Authorization is enforced.
- Audit event is created.
- Tests pass.
