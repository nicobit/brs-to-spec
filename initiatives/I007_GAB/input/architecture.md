# High-Level Architecture — AI-Powered Loan Origination Platform

## Status

DRAFT — pending architect review

## Deployment topology

Cloud-native deployment on Azure UK South (primary) + Azure UK West (DR). All components must remain within UK data centres to satisfy GDPR data residency constraints.

## System components

| Component | Role | Technology (proposed) |
|---|---|---|
| Applicant Portal | Web UI for loan application submission, status tracking, offer acceptance | React / Next.js — Azure Static Web Apps |
| Underwriter Dashboard | Web UI for underwriter queue, review, and decision | React / Next.js — Azure Static Web Apps |
| Admin Dashboard | Operational metrics and compliance monitoring | React / Next.js — Azure Static Web Apps |
| Loan Origination API | Core backend orchestrating application lifecycle, state machine, business rules | .NET 8 / ASP.NET Core — Azure App Service |
| AI Scoring Service | Risk scoring model inference, recommendation engine | Python / FastAPI — Azure Container Apps |
| Compliance Service | AML/KYC checks, sanctions screening, identity verification | .NET 8 / ASP.NET Core — Azure App Service |
| Notification Service | Email and portal notifications (submission, decisions, reminders) | .NET 8 — Azure Functions |
| Audit Log Store | Immutable append-only audit trail | Azure Cosmos DB (append-only container with TTL disabled) |
| Application Database | Mutable application state, underwriter queue | Azure SQL (Hyperscale) |
| Payment Gateway Adapter | Internal adapter to Temenos T24 core banking system | .NET 8 — Azure App Service |

## Integration points

| Integration | Direction | Protocol | Notes |
|---|---|---|---|
| Experian CreditExpert API | Outbound | REST / HTTPS | Existing enterprise contract. Circuit breaker required (NFR-007). Fallback: route to REFER_TO_UNDERWRITER |
| HMRC Identity Verification API | Outbound | REST / HTTPS | KYC verification. Fallback TBD (OQ-003) |
| HM Treasury Sanctions / PEP database | Outbound | REST / HTTPS | AML screening. Additional providers TBD (OQ-004) |
| DocuSign eSignature | Outbound | REST / HTTPS | E-signature for offer acceptance. Existing enterprise contract |
| Temenos T24 via Payment Gateway | Outbound | REST / HTTPS | Internal API. Contract details TBD (OQ-005) |
| Azure Service Bus | Internal | AMQP | Async event bus between Loan Origination API, AI Scoring Service, Compliance Service, Notification Service |

## Data architecture

- All PII stored in Azure SQL and Azure Cosmos DB encrypted at rest (AES-256, Azure-managed keys)
- All in-transit communication over TLS 1.3
- Audit log in Cosmos DB is append-only — no update or delete operations permitted
- Credit bureau data (Experian) not persisted beyond scoring pipeline — used transiently and discarded after score is written
- Data residency: all storage accounts, databases, and service bus instances in Azure UK South or UK West only

## Security model (high-level)

- Applicant authentication: email + OTP (no account registration required for status check)
- Underwriter / admin authentication: Azure AD (existing enterprise IdP), RBAC enforced at API layer
- All service-to-service calls use managed identities (no stored secrets)
- API Gateway (Azure API Management) as single ingress — rate limiting, WAF, TLS termination
- PII fields masked in application logs; full PII only accessible via Audit Log Store with elevated RBAC role

## Open decisions

| ID | Decision | Status | Impact |
|---|---|---|
| OD-001 | AI scoring model vendor / approach (in-house vs. Experian PowerCurve vs. other) | Resolved | Affects AI Scoring Service design, explainability architecture, FCA compliance approach |
| OD-002 | HMRC KYC API fallback behaviour (manual verification queue vs. auto-refer) | Resolved | Affects Compliance Service state machine and underwriter queue load |
| OD-003 | AML database providers (HM Treasury only vs. HM Treasury + Dow Jones Watchlist) | Resolved | Affects Compliance Service integration count and latency budget |
| OD-004 | T24 payment gateway API contract — existing or requires negotiation | Resolved | Affects Payment Gateway Adapter design and D3 increment scope |
| OD-005 | Cooling-off period waiver legal sign-off flow — separate UI step required? | Resolved | Affects Applicant Portal and Loan Origination API state machine |
