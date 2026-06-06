# ADR-001 — Use explicit onboarding status workflow

## Status
Proposed

## Context

The BRS requires onboarding requests to be created, approved, rejected, and audited. The architecture draft does not fully define the state model.

## Decision

Use an explicit onboarding status workflow with controlled transitions.

## Consequences

- Backend validation must enforce valid transitions.
- Tests must cover valid and invalid transitions.
- Audit events must be generated for status changes.
