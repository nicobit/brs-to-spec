# Delivery Increments

## D1 - Guided onboarding submission

| Field | Value |
|---|---|
| Objective | capture identity and document evidence in a controlled submission flow |
| Related stories | US-01, US-02 |
| Why first | reduces incomplete submissions while establishing auditable behavior |
| Main risks | retention detail, security controls, audit-event dependencies |

- capture customer identity inputs
- upload required onboarding documents
- submit onboarding request for review
- emit auditable submission event

## D2 - Approval and audit visibility

| Field | Value |
|---|---|
| Objective | improve reviewer decision flow and expose approval traceability |
| Related stories | follow-on approval and audit stories |
| Why later | depends on the stable D1 submission baseline |
| Main risks | reviewer workflow complexity and downstream visibility expectations |

- route approvals
- display onboarding state and review notes
- expose auditable status history
