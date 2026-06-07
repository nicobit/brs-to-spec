# Initial Architecture — Client Onboarding

## Constraints

| Constraint ID | Area | Constraint | Mandatory? |
|---|---|---|---|
| ARC-001 | Identity | Use Entra ID for authentication. | Yes |
| ARC-002 | Authorization | Access must be role-based. | Yes |
| ARC-003 | Data | Store onboarding requests in Azure SQL. | Yes |
| ARC-004 | Audit | Use the existing audit service for status changes. | Yes |
| ARC-005 | Observability | Emit structured logs without sensitive client data. | Yes |
