# Initial Architecture — Example

## Technology Stack

- Frontend: React
- Backend: .NET API
- Database: Azure SQL
- Authentication: Entra ID
- Audit: existing audit service

## Constraints

- Use existing .NET API layer.
- Store onboarding data in Azure SQL.
- Emit audit event for every status change.
- Use Entra ID for authorization.
