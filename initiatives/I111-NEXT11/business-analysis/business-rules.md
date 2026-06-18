# Business Rules

## Summary

This document lists concrete business rules derived from the BRS. Each rule is actionable and traceable to its source.

## Rules

| ID | Rule | Priority | Source |
|---|---|---|---|
| BR-001 | Applications above £10,000 require underwriter review regardless of AI recommendation | High | input/brs.md FR-010 |
| BR-002 | If Experian API is unavailable, route to `REFER_TO_UNDERWRITER` | High | input/brs.md FR-009 |
| BR-003 | AML/KYC failures result in `COMPLIANCE_HOLD` and no offer generation | High | input/brs.md FR-014 |
| BR-004 | Auto-decline notifications are sent within 5 minutes and enforce 30-day cooling-off | Medium | input/brs.md FR-011 |
| BR-005 | Underwriter decisions must be recorded immutably with actor and timestamp | High | input/brs.md FR-018 |
| BR-006 | Retry disbursement once after 2 minutes before alerting operations | Medium | input/brs.md FR-026 |

