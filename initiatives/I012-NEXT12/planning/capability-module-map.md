# Capability → Module Map

Map of high-level capabilities to the software modules that will implement them.

| Capability | Modules |
|---|---|
| Applicant onboarding | portal-app, application-service |
| Document upload & verification | portal-app, integration-adapters |
| AI scoring | ai-scoring, data-platform |
| Underwriting & offer | application-service, integration-adapters, api-gateway |
| Audit & compliance | data-platform, audit-store |

Notes: Use this mapping to inform module ownership and backlog slicing.
