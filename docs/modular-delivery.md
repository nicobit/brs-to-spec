# Modular Delivery Track

The Modular Delivery Track is an optional extension for large BRS-driven initiatives.

It prevents two common problems:

1. Product Owners being forced to manage too many intermediate artifacts.
2. AI coding agents receiving too much context from a flat Epic → Feature → User Story breakdown.

## Position in the framework

```text
BRS
  ↓
Business Intake Summary
  ↓
Global Architecture Rules
  ↓
Software Modules
  ↓
Capability-to-Module Map
  ↓
Delivery Increments
  ↓
OpenSpec change for active deliverable
```

## Software Module

A software module is a bounded implementation area with clear ownership, responsibilities, interfaces, and data/API contracts.

A module can be a bounded context, but it does not have to be. Avoid calling every technical layer a bounded context.

## Deliverable

A deliverable is a vertical, testable increment that can be demonstrated and validated.

A good deliverable:
- produces visible business or technical value,
- touches only the modules needed for that slice,
- has acceptance criteria,
- has automated validation criteria,
- is ideally achievable in 2-3 weeks,
- becomes one OpenSpec change.

## Traceability

```text
Requirement → Business capability → Software module(s) → Deliverable → OpenSpec change → Tasks/tests
```

## Anti-patterns

Avoid:
- replacing all business capability thinking with technical modules,
- creating one massive `tasks.md`,
- creating tasks for all deliverables at once,
- duplicating OpenSpec with a separate task system,
- forcing 20-30 line limits as an absolute rule.
