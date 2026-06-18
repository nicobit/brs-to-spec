# Business Rules

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I021-NEXT21 |
| Created at | 2026-06-17T17:50:00+00:00 |
| Created by | product-owner |
| Status | Draft |

## Rules

| ID | Rule | Trigger | Priority | Source |
|---|---|---|---|---|
| BR-001 | Auto-approve if score >= 800 and amount <= 10000 and AML/KYC passed | Decision creation | High | FR-010, FR-006 |
| BR-002 | Refer to underwriter if Experian API unavailable | External integration failure | High | FR-009 |
| BR-003 | Auto-decline if score <= 200 | Decision creation | High | FR-011 |
| BR-004 | Escalate if underwriter action not taken within 4 business hours | Underwriter queue | Medium | FR-016 |
| BR-005 | Retry disbursement once on failure then alert ops | Disbursement failure | Medium | FR-026 |

---

*Set Status: Accepted only by human approval when required by the workflow. Never self-accept.*
