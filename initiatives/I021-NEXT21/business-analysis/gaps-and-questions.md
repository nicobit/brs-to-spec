# Gaps and Questions

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I021-NEXT21 |
| Created at | 2026-06-17T17:55:00+00:00 |
| Created by | product-owner |
| Status | Draft |

## Summary

This document captures gaps identified during business analysis and questions for stakeholders.

## Gap Catalog

| GAP-NNN | Category | Description | Impact | Severity | Suggested Resolution | Owner | BRS Source |
|---|---|---|---|---|---|---|---|
| GAP-001 | Integration / Missing Spec | Experian API SLA and error modes not specified | High | Blocking | Define SLA and error handling policy with vendor | product-owner / architect | FR-009 |
| GAP-002 | Integration / Missing Spec | KYC provider and integration pattern not chosen | High | High | Select KYC provider and define integration contract | product-owner | FR-013 |

## Critical Path

### Blocking Gaps

| GAP-NNN | Description | Impact | Owner |
|---|---|---|---|
| GAP-001 | Experian SLA & error handling undefined | Blocks credit checks integration | product-owner / vendor |

### High-Severity Gaps

| GAP-NNN | Description | Default Assumption (if proceeding) | Owner |
|---|---|---|---|
| GAP-002 | KYC provider selection missing | Assume provider X with standard API | product-owner |

### Low-Severity Gaps

| GAP-NNN | Description | Assumption | Risk if assumption is wrong |
|---|---|---|---|
| GAP-003 | Minor UI acceptance text | Assume default copy | Low |

## Questions for Stakeholders

1. Which KYC provider should we use for identity verification? (Q-001)
2. Are there limits on auto-approval amounts beyond the £10,000 rule? (Q-002)

## Coverage Summary

| Category | Count |
|---|---|
| Blocking gaps | 1 |
| High-severity gaps | 1 |
| Low-severity gaps | 1 |
| Total gaps | 3 |

## Questions for Stakeholders

1. Which KYC provider should we use for identity verification?
2. Are there limits on auto-approval amounts beyond the £10,000 rule?
