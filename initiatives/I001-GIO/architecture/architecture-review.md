# Architecture Review

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I001-GIO |
| Created at | 2026-07-02 |
| Created by | architect |
| Status | Draft |

## Initiative-Architecture Fit

| Feature Area | Existing Components Touched | New Components / Boundaries | Contract Changes | Blast Radius |
|---|---|---|---|---|
| Loan Application Intake (FR-001–FR-005) | None — all new | Applicant Portal (React/Next.js, Azure Static Web Apps), Loan Origination API (.NET 8, Azure App Service), Application Database (Azure SQL Hyperscale) | None | Low |
| AI Pre-Screening and Risk Scoring (FR-006–FR-011) | Experian CreditExpert API (existing enterprise contract, read-only outbound) | AI Scoring Service (Python/FastAPI, Azure Container Apps), Azure Foundry model endpoint, Azure Service Bus (async trigger) | None — consumes existing Experian contract | Medium |
| AML/KYC Compliance (FR-012–FR-014) | HM Treasury Sanctions/PEP API (external, read-only), HMRC Identity Verification API (external, read-only) | Compliance Service (.NET 8, Azure App Service) | None — read-only outbound integration | Medium |
| Underwriter Review Workflow (FR-015–FR-019) | Azure AD (existing enterprise IdP, consumed as-is) | Underwriter Dashboard (React/Next.js, Azure Static Web Apps), Loan Origination API (underwriter queue state machine) | None — Azure AD used with existing RBAC | Low |
| Loan Offer and Digital Acceptance (FR-020–FR-023) | DocuSign eSignature (existing enterprise contract, outbound REST) | Loan Origination API (offer generation), Applicant Portal (offer presentation and acceptance) | None — consumes existing DocuSign contract | Low |
| Disbursement (FR-024–FR-027) | Temenos T24 via internal payment gateway (existing core banking system) | Payment Gateway Adapter (.NET 8, Azure App Service) | New API contract to be defined by this initiative (OQ-005 resolved) | High |
| Observability, Audit, and Administration (FR-028–FR-030) | None — all new | Audit Log Store (Azure Cosmos DB, append-only), Admin Dashboard (React/Next.js, Azure Static Web Apps), Azure Monitor / Application Insights | None | Low |

## Architecture Constraints

| ID | Constraint | Rationale | Violation Consequence | Source |
|---|---|---|---|---|
| ARCH-C-001 | All deployment exclusively in Azure UK South (primary) and Azure UK West (DR) | UK GDPR data residency — all PII and processing must remain within UK jurisdiction | Regulatory breach; potential FCA enforcement action and GDPR fines | BRS Constraints / C-002 / C-006 |
| ARCH-C-002 | All service-to-service communication must use Azure Managed Identities — no stored secrets or connection strings with credentials | Security architecture principle; eliminates credential exposure risk | Security audit failure; credential leakage risk | Architecture security model |
| ARCH-C-003 | Azure API Management (APIM) is the sole internet ingress — no backend service may be directly exposed | WAF, rate limiting, and TLS termination enforced at a single boundary | Direct exposure of backend APIs; rate-limiting and WAF bypass | Architecture security model |
| ARCH-C-004 | Audit Log Store (Azure Cosmos DB) is append-only — no update or delete operations are permitted | NFR-005 (tamper-evident) and FR-028 (immutable audit trail) are legal and regulatory requirements | Regulatory breach; audit trail integrity failure; potential FCA or legal consequences | NFR-005 / FR-028 / C-001 |
| ARCH-C-005 | AI Scoring Service must use an explainable model (Azure Foundry) — black-box models are prohibited | FCA Consumer Duty and FCA regulatory requirement for explainable AI decisions | FCA enforcement action; inability to justify lending decisions to regulators or applicants | BRS Constraints / C-005 |
| ARCH-C-006 | Experian credit bureau data must not be persisted beyond the scoring pipeline — used transiently and discarded after the risk score is written | UK GDPR data minimisation principle; Experian contractual terms | GDPR breach; excess data retention; potential Experian contract violation | Architecture data architecture / C-002 |
| ARCH-C-007 | All inter-service async communication must use Azure Service Bus (AMQP) — no direct service-to-service HTTP calls for async flows | Decoupling, reliability, and audit event delivery guarantees | Tight coupling; message loss risk; observability gaps | Architecture integration design |
| ARCH-C-008 | PII must not appear in application logs — use masked or tokenised representations | UK GDPR compliance and data minimisation; log aggregation systems are not classified as secure storage | GDPR breach; PII accessible to operations staff without elevated access | Architecture security model / NFR-004 |
| ARCH-C-009 | All external API integrations (Experian, HMRC, DocuSign, T24) must implement circuit breakers with defined fallbacks | NFR-007; availability SLA at 99.9% requires resilient external dependency handling | Cascading failure on external API outage; SLA breach; undefined system behaviour | NFR-007 |
| ARCH-C-010 | All PII encrypted at rest (AES-256, Azure-managed keys) and in transit (TLS 1.3) | NFR-004 / UK GDPR mandatory encryption requirements | Regulatory breach; data exposure risk | NFR-004 / C-002 |

*Note: These constraints will be normalised into `AR-NNN` identifiers in the Architecture Rules artifact.*

## Brownfield Impact

This initiative is primarily greenfield — the loan origination platform is entirely new. Brownfield impact is limited to integration surfaces with existing external and internal systems.

| Component | Change Type | Consumers | Backward Compatible? | Migration Required | Rollback Possible |
|---|---|---|---|---|---|
| Temenos T24 (core banking) | New boundary — outbound from Payment Gateway Adapter | Payment Gateway Adapter only | Yes — T24 is unchanged; new inbound API contract added | No migration — new integration | Yes — remove Payment Gateway Adapter |
| Experian CreditExpert API | New boundary — new outbound consumer of existing enterprise contract | AI Scoring Service only | Yes — Experian API is unchanged | No migration — new consumer | Yes — remove AI Scoring Service calls |
| DocuSign eSignature | New boundary — new outbound consumer of existing enterprise contract | Loan Origination API only | Yes — DocuSign API is unchanged | No migration — new consumer | Yes — remove DocuSign integration |
| HMRC Identity Verification API | New boundary — new outbound consumer | Compliance Service only | Yes — HMRC API is unchanged | No migration — new consumer | Yes — remove Compliance Service KYC call |
| HM Treasury Sanctions/PEP API | New boundary — new outbound consumer | Compliance Service only | Yes — AML API is unchanged | No migration — new consumer | Yes — remove AML screening call |
| Azure AD | New consumer — underwriter and admin RBAC groups to be configured | Underwriter Dashboard, Admin Dashboard, Loan Origination API | Yes — Azure AD is unchanged; new RBAC roles added | No migration — additive RBAC configuration | Yes — remove RBAC groups added for this initiative |

**Regression surface:** All existing T24, Experian, DocuSign, HMRC, and Azure AD integrations at the bank are unaffected — this initiative adds new consumers via its own services. The only regression risk is in the Azure AD tenant if RBAC groups are incorrectly scoped to a broader boundary than the new application. The T24 payment gateway API contract is new and does not affect existing T24 consumers.

**Rollback sensitivity:** Low — all new components are additive. No existing system is modified. Rollback involves removing the new services and the Azure AD RBAC additions. The T24 contract addition is the highest-risk rollback because it requires coordination with the T24 team.

## Quality Attribute Assessment

| Attribute | Requirement (from BRS) | Assessment | Risk |
|---|---|---|---|
| Performance | Form loads ≤2s (NFR-001); AI scoring pipeline ≤90s (NFR-002); 500 concurrent submissions (NFR-003) | React/Next.js on Azure Static Web Apps provides CDN-accelerated delivery for NFR-001. AI scoring pipeline involves Experian call (≤30s, FR-009), Azure Foundry inference, and Compliance checks (≤60s, FR-012) — pipeline must be orchestrated concurrently, not sequentially, to meet 90s. Azure Container Apps auto-scaling must be tuned for AI Scoring Service under 500 concurrent load. Azure SQL Hyperscale supports horizontal read scaling for application database. | Medium — concurrent pipeline orchestration (Experian + AI + AML/KYC) within 90s is tight; requires load testing to confirm. Sequential execution would exceed 90s (30s + 60s + model inference). |
| Security | AES-256 at rest, TLS 1.3 in transit (NFR-004); PII masked in logs; managed identities; APIM with WAF; RBAC via Azure AD | Azure-native encryption covers at-rest requirement. TLS 1.3 enforced at APIM. Managed identities eliminate credential risk. APIM WAF (OWASP ruleset) covers injection and common attacks. PII masking requires explicit implementation in every logging middleware. Audit log append-only enforcement requires Cosmos DB container policy, not code-only control. | Low — strong platform-native controls. Main risk is developer-introduced PII in logs during implementation; requires code review gate and automated PII scanning in CI. |
| Scalability | 500 concurrent submissions (NFR-003); 99.9% uptime (NFR-006); AI pipeline latency at scale | Azure App Service plan for Loan Origination API must be sized for 500 concurrent sessions. Azure Container Apps for AI Scoring Service supports event-driven scaling. Azure Service Bus decouples peak load from downstream processors. Azure SQL Hyperscale supports on-demand read replica scale-out. Azure Static Web Apps on global CDN handles frontend load without backend pressure. | Low to Medium — horizontal scaling is well-supported on the chosen Azure stack. Bottleneck risk is the AI Scoring Service if Azure Foundry endpoint has throughput limits; needs capacity planning with Azure Foundry team. |
| Availability | 99.9% uptime during business hours 08:00–20:00 GMT (NFR-006); circuit breakers on all external APIs (NFR-007) | Azure UK South + UK West active/passive DR covers infrastructure availability. Azure Service Bus geo-redundancy provides async message durability. Cosmos DB multi-region write is not required (single-region append-only is sufficient). Circuit breakers with defined fallbacks (Experian → REFER_TO_UNDERWRITER; HMRC → manual verification; T24 → retry + alert) prevent external API outages from cascading. 99.9% during business hours equates to ≤43.8 minutes downtime per month — achievable with Azure App Service premium tier and health probes. | Low — 99.9% during business hours (not 24/7) is an attainable SLA on Azure premium tier. External API circuit breakers are explicitly designed. Main risk is unplanned T24 maintenance windows; requires ops alert response procedure. |

## Open Decisions

| ID | Question | Owner | Default Assumption | Required Before |
|---|---|---|---|---|
| DEC-001 | What Azure Foundry model and endpoint configuration delivers FCA-compliant explainability for risk scoring? | Head of AI / IT Architecture | Azure Foundry will provide a model with feature-importance explainability output alongside each score. Default: use Azure Foundry interpretability SDK. | AI Scoring Service design and story elaboration |
| DEC-002 | What is the exact T24 payment gateway API schema, authentication mechanism, and SLA? | IT Architecture / T24 Team | RESTful JSON API with mutual TLS authentication and synchronous disbursement confirmation. Contract to be defined by this initiative (OQ-005 resolved). | Payment Gateway Adapter design and Disbursement story elaboration |
| DEC-003 | What rate limits apply to the HMRC identity verification API, and how does this affect the KYC pipeline latency budget? | IT Architecture / Compliance | HMRC API supports sufficient throughput for 500 concurrent applications; circuit breaker threshold at 5s timeout. | Compliance Service design and KYC story elaboration |
| DEC-004 | What Azure Foundry throughput limits apply in Azure UK South, and does capacity need to be reserved in advance? | IT Architecture / Head of AI | Sufficient throughput for 500 concurrent scoring requests is available on demand. | AI Scoring Service capacity planning and load testing |
| DEC-005 | Will the Azure AD RBAC groups for underwriter and admin roles be managed by the bank's existing IAM team or provisioned by this initiative? | IT Architecture / IAM Team | This initiative will define the required RBAC role definitions; IAM team will provision the groups in the tenant. | Underwriter Dashboard and Admin Dashboard story elaboration |

## Active Assumptions

| Assumption | Source | If False, Then |
|---|---|---|
| Azure Foundry is available and approved for use in Azure UK South, producing explainable model output | BRS OQ-001 resolved / Architecture OD-001 | AI Scoring Service design is blocked; alternative explainable model approach must be selected; FCA compliance approach must be re-evaluated |
| Experian CreditExpert API credentials and access are available for integration in the development and production environments | BRS C-004 / Architecture integration table | AI scoring pipeline is blocked until credentials are provisioned; all scoring-dependent stories are blocked |
| DocuSign enterprise contract credentials and integration access are available for development and production | BRS C-007 / Architecture integration table | Loan offer acceptance flow is blocked; e-signature stories cannot be implemented |
| T24 payment gateway team will engage with this initiative to co-define the API contract within the delivery timeline | BRS C-003 / OQ-005 resolved | Disbursement stories are blocked; a temporary manual disbursement fallback may be needed |
| HMRC identity verification API is accessible from Azure UK South with adequate throughput | FR-013 / Architecture HMRC integration | KYC verification cannot be automated; all applications route to manual verification queue (acceptable as fallback per OQ-003 resolution, but operationally expensive) |
| Azure API Management instance with WAF will be provisioned before any service is deployed to production | Architecture security model | Security boundary missing; backend services exposed directly; APIM must be provisioned as a Day 0 infrastructure item |
| Azure Cosmos DB append-only container policy can be enforced at the data plane level (not code-only) to satisfy NFR-005 | Architecture data architecture / NFR-005 | Code-level append-only is insufficient for tamper-evidence; alternative immutable storage (e.g., Azure Immutable Blob Storage) must be evaluated |

## Known Unknowns

| Unknown | Impact | Discovery Path |
|---|---|---|
| T24 payment gateway API schema, authentication model, and latency characteristics | Blocks Payment Gateway Adapter design; directly affects disbursement story scope and FR-026 retry logic | Schedule API contract workshop with IT Architecture and T24 team in Sprint 0 |
| Azure Foundry explainability output format and feature-importance API surface | Blocks FCA compliance documentation for AI scoring; affects FR-007 rationale output and underwriter dashboard display (FR-016) | Proof-of-concept with Azure Foundry team in Sprint 0; confirm explainability SDK API |
| HMRC identity verification API rate limits and response SLA | Affects Compliance Service circuit breaker threshold, KYC latency budget within 90s pipeline (NFR-002), and fallback trigger configuration | Request HMRC API technical documentation and run integration spike in Sprint 0 |
| Cooling-off period waiver mechanism — whether applicant waiver is a portal action or a passive timer expiry | Affects Applicant Portal UX and Loan Origination API state machine for FR-023 / FR-024 | Clarify with Legal and Product Owner in Sprint 0; OQ-002 resolved (no separate sign-off UI) but waiver initiation mechanism is not fully specified |
| AML screening latency under concurrent load (HM Treasury API throughput and SLA) | Affects Compliance Service design; if AML takes >60s at scale, the 90s scoring pipeline SLA (NFR-002) is at risk | Integration spike with HM Treasury API in Sprint 0; confirm throughput and SLA |

---
*Set Status: Accepted only by workflow or human approval when applicable. Never self-accept.*
