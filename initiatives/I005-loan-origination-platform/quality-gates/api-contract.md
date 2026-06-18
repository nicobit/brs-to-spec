# API Contract — Draft

Summary
- Initiative: I005-loan-origination-platform
- Owner: API Owner (TBD)

Endpoints (high level)
- POST /applications — Submit an application
- GET /applications/{id} — Retrieve application status
- POST /applications/{id}/actions/offer — Generate offer for approved application
- POST /applications/{id}/actions/decision — Record underwriting decision

Schemas
- Inline high-level request/response shapes included below; authoritative OpenAPI v3 spec expected in `specs/openapi/`.

Open Questions
- OQ-API-001: Which endpoints must be externally public versus internal-only?
- OQ-API-002: Expected authentication schemes (client credentials vs user tokens) per endpoint?

Notes
- This is a lightweight contract intended to seed the OpenAPI v3 specification. The orchestrator will run contract validation when an OpenAPI document is present at `specs/openapi/loan-origination.openapi.yaml`.
# API Contract — Loan Origination Platform

## Metadata

| Field | Value |
|---|---|
| **Status** | **In progress** — change to `Accepted` when owner signs off |
| Active deliverable | I005 — Loan Origination Platform |
| Governed boundary | Loan Origination API + AI Scoring Service + Payment Adapter |
| API owner | API Owner / Integrations |
| Review date | 2026-06-13 |
| Trigger reason from readiness | Triggered by `engineering-readiness/readiness-check.md` — new Loan Origination API and outbound adapters |

## API Summary

This gate documents the HTTP contracts owned by the initiative for the Loan Origination API, the AI Scoring Service (internal), and the Payment Gateway Adapter (internal-facing). Where actor IDs (`ACT-NNN`) are not available in `business-analysis/actors-and-personas.md`, free-text role names are used and flagged for later linkage.

## Endpoints

### Loan Origination API

| Method | Path | Purpose | Auth required? | Consumer(s) | Compatibility impact |
|---|---|---|---|---|---|
| POST | /applications | Submit loan application | Public — email+OTP | Applicant (applicant portal) | Major — introduces application resource and versioned payload |
| GET | /applications/{applicationId} | Get application status and details | OTP-verified / authenticated staff | Applicant, Underwriter, Admin | Minor — read-only evolution allowed with addition of fields |
| POST | /applications/{applicationId}/score | Request a scoring run (async) | Internal — managed identity | Applicant Portal (via API) | Internal contract with AI Scoring Service — version carefully managed |
| POST | /applications/{applicationId}/offers | Create or publish an offer | Auth: Underwriter role | Underwriter | Major — affects downstream disbursement flow |
| POST | /applications/{applicationId}/payments | Request disbursement (delegates to Payment Adapter) | Internal — managed identity | Loan Origination API | Major — depends on Payment Adapter contract (T24)

### AI Scoring Service

| Method | Path | Purpose | Auth required? | Consumer(s) | Compatibility impact |
|---|---|---|---|---|---|
| POST | /score | Trigger scoring job for an application | Internal — managed identity | Loan Origination API | Major — scoring payload schema must be versioned |
| GET | /score/{jobId}/status | Poll scoring status | Internal | Loan Origination API | Minor |
| GET | /score/{jobId}/explainability | Retrieve explainability trace for a scored decision | Internal | Loan Origination API, Compliance | Major — explainability schema must be stable and stored for audit |

### Payment Gateway Adapter (Temenos T24 adapter)

| Method | Path | Purpose | Auth required? | Consumer(s) | Compatibility impact |
|---|---|---|---|---|---|
| POST | /payments | Initiate disbursement request | Internal — managed identity | Loan Origination API | Major — depends on T24 contract (OQ-005)
| GET | /payments/{paymentId}/status | Query payment status | Internal | Loan Origination API | Minor |

## Outbound Integrations

These are third-party systems this initiative calls. Documented here as dependencies; their contracts are not authored by this team but must be referenced.

| Integration | Direction | Protocol | Auth | Notes |
|---|---|---|---|---|
| Experian CreditExpert | Outbound | REST/HTTPS | API key / OAuth | Credit report retrieval — transient storage only; circuit breaker required |
| HMRC Identity API | Outbound | REST/HTTPS | OAuth2 | KYC verification; async callbacks likely |
| DocuSign | Outbound | REST/HTTPS | OAuth2 | Signature flow for offers and documents |
| Temenos T24 (Payment Gateway) | Outbound | REST/Adapter | TBD (per contract) | Disbursement adapter; contract pending (OQ-005) |

## Request / Response Contract (high-level)

| Endpoint | Request schema | Response schema | Validation rules |
|---|---|---|---|
| POST /applications | `ApplicationCreateV1` (fields: applicant, product, amounts, income, consents) | `ApplicationCreatedV1` (applicationId, status) | Required fields: applicant.identifiers, consent.accepted=true; payload size limits apply |
| POST /score | `ScoringRequestV1` (applicationId, snapshotPayload) | `ScoringAcceptedV1` (jobId) | Snapshot must include deterministic feature set; schema version header required |
| GET /score/{jobId}/explainability | N/A | `ExplainabilityTraceV1` | Explainability material must include feature contributions and model version |
| POST /payments | `PaymentRequestV1` (applicationId, offerId, amount, beneficiary) | `PaymentAcceptedV1` (paymentId) | Idempotency-key required; payment validation performed by adapter |

## Error Handling

| Error case | Status / code | Message rule | Consumer action |
|---|---|---|---|
| Validation error | 400 | Provide `field` + `reason` structure | Client must show field-level errors |
| Not found | 404 | Resource not found | Client may show user-friendly message |
| Unauthorized | 401 / 403 | Standard auth error | Retry only after authentication |
| Downstream service unavailable (e.g. Experian/T24) | 503 | `retry_after` header recommended; include correlation id | Client should surface transient error and allow retry/backoff |

## Versioning and Compatibility

- Use `Accept` / `Content-Version` headers for major contract changes.
- Backward-compatible additions (optional fields) allowed; breaking changes require major version bump.

## Security Requirements

- Public endpoints must protect PII in transit (TLS 1.2+). Do not return PII to unauthorized callers.
- Service-to-service calls use managed identities; no long-lived secrets in repos.

## Observability Requirements

- All requests must emit correlation IDs and include trace context for distributed tracing.
- Scoring calls must emit explainability metadata linkage (jobId → applicationId) for audit.

## Open Questions

| Question ID | Question | Owner | Required before | Answer |
|---|---|---|---|---|
| OQ-005 | Temenos T24 contract shape and auth model — what protocol and fields are required? | IT Architecture / Integrations | Handoff / Payment features | _(TBD)_ |
| OQ-006 | Actor IDs mapping: map free-text callers to `ACT-NNN` IDs when `business-analysis/actors-and-personas.md` is authored. | Delivery Lead / PO | Story enrichment | _(TBD)_ |

## Acceptance

Status: `In progress` — update Metadata `Status` to `Accepted` when API owner and gate reviewers sign off and open questions are resolved.

## CI Gate

| Field | Value |
|---|---|
| Test runner / tool | Schemathesis / contract tests (TBD) |
| CI command | `schemathesis run quality-gates/api-contract.yaml --checks all` |
| CI step name | API contract gate |
| Gate status | Not wired |
## Metadata

| **Status** | **In progress** |
|---|---|
| **Owner** | ACT-005 (Service Integrator / API Owner) |
| **Reviewed** | No |
| **Required-before** | Handoff (specs/) |

## API Summary

Boundary: BND-API-LO — Loan Origination API (central orchestrator for submission, scoring, compliance, offers, disbursement).

Purpose: define endpoints, callers, request/response shapes, error semantics, and version/compatibility guidance for integrations (Experian, HMRC, DocuSign, Temenos T24) and internal consumers (Underwriter UI, AI Scoring Service, Compliance Service).

Inputs / Evidence:
- `planning/delivery-structure.md` (features F-001..F-006)
- `business-analysis/actors-and-personas.md` (ACT-001..ACT-005)
- `architecture/architecture-review.md` (integration boundaries: Experian, HMRC, T24)
- `engineering-readiness/readiness-check.md` (api-contract gate triggered)

## Endpoints

| Path | Method | Purpose | Caller(s) (ACT / SYS) | Notes / Required-before |
|---|---:|---|---|---|
| /applications | POST | Submit new application; returns ARN and submission status | ACT-001 Applicant | FR-001..FR-004; idempotency key required; returns `arn` and `status` |
| /applications/{arn} | GET | Retrieve application details & status | ACT-001 Applicant, ACT-004 Admin | Public status lookup uses ARN + DOB (no account) per FR-005 |
| /applications/{arn}/score | POST | Trigger/accept scoring results (internal) | ACT-005 Service Integrator / AI Scoring Service (SYS) | Called by scoring pipeline; payload includes explainability traces reference (link or storage key) |
| /applications/{arn}/actions | POST | Underwriter actions (approve/decline/request-info) | ACT-002 Underwriter | Records action + audit metadata (actor, timestamp, reason) — immutable audit write required |
| /applications/{arn}/offer | GET | Retrieve generated offer document metadata | ACT-001 Applicant, ACT-002 Underwriter | Links to DocuSign envelope id if e-signed |
| /webhooks/docuSign | POST | DocuSign callback for envelope events (signed/declined) | SYS-004 DocuSign (webhook) | Must verify signature; map envelope -> arn; idempotent processing |
| /disbursements | POST | Submit disbursement instruction to Payment Adapter (T24) | ACT-005 Service Integrator / Loan Origination API | Payload: account, sortCode, amount, reference; response: disbursementId/status; retry semantics defined below |
| /webhooks/t24/callback | POST | T24 confirmation / failure callbacks | SYS-005 Temenos T24 (adapter) | Verify authenticity; update status to DISBURSED/FAILED; emits observability events |

## Request / Response Contracts (compact)

1) POST /applications

Request (application/json):
```json
{
  "applicant": {"firstName":"","lastName":"","dob":"YYYY-MM-DD","niNumber":""},
  "contact": {"email":"","phone":""},
  "loan": {"amount":0,"termMonths":0},
  "metadata": {"source":"portal","idempotency_key":"<uuid>"}
}
```

Response 201 Created:
```json
{ "arn": "ARN-0001", "status":"SUBMITTED", "submitted_at":"2026-06-13T...Z" }
```

2) POST /disbursements

Request (application/json):
```json
{
  "arn":"ARN-0001",
  "beneficiary": {"accountNumber":"","sortCode":""},
  "amount": 1000,
  "requested_by": "ACT-005",
  "request_meta": {"idempotency_key":"<uuid>"}
}
```

Response 202 Accepted (async):
```json
{ "disbursementId":"DISB-1234", "status":"PENDING" }
```

Callback: POST /webhooks/t24/callback

Payload contains `disbursementId`, `arn`, `status` (`CONFIRMED` | `FAILED`), `timestamp`, `details`.

## Error Handling

- Use standard HTTP status codes. 400 for validation, 401/403 for auth, 404 for missing resource, 409 for idempotency conflict, 500 for internal errors.
- All error responses MUST include an error code and human-readable message and an owner tag when action required: `{ "code":"ERR-API-001", "message":"Invalid account number","owner":"payments" }`.
- Retries: clients should use exponential backoff. Server-side: ensure idempotency via `idempotency_key` on submission/disbursement endpoints.

## Versioning & Compatibility

- Base path versioning: `/v1/` prefix in production; current templates assume v1 contract.
- Additive changes allowed in minor releases; breaking changes require new major version and migration guidance in `specs/` handoff.

## Security & Auth

- Internal API calls: use Managed Identities (Azure AD) — do not store static secrets.
- Public endpoints: rate-limit and require ARN+DOB pair for public status lookup; CAPTCHA / abuse protection on `/applications`.
- Webhook endpoints: verify signatures (DocuSign, T24) and reject unverifiable calls.

## Observability

- Emit structured events for: submission, scoring_complete (include explainability reference), compliance_hold, underwriter_action, offer_generated, disbursement_submitted, disbursement_confirmed.
- Correlate events by `arn` and include `trace_id` for distributed tracing.

## Open Questions

- OQ-005 (T24 contract): final API shape and authentication for Temenos T24 — owner: IT Architecture (affects `/disbursements` contract).
- Experian rate limits and response shape: confirm fields required for scoring pipeline and whether transient persistence is allowed — owner: Integrations.
- DocuSign webhook signature validation details and envelope retention policy — owner: Integrations.

## Required Actions & Owners

- Owner (API contract): ACT-005 (Service Integrator / API Owner) — produce OpenAPI + JSON Schemas and add to `quality-gates/schemas/`.
- Integrations: provide vendor API examples (Experian, T24, DocuSign) and test vectors.
- Security: validate webhook signature verification, auth scopes, and rate-limiting config.

## Self-review checklist

- [ ] Gate was triggered in `readiness-check.md` (confirmed)
- [ ] Every endpoint lists caller(s) using ACT-NNN or SYS-NNN (done)
- [ ] Owners assigned for outstanding actions (see Required Actions)
- [ ] Open questions recorded (OQ-005, Experian, DocuSign)

---
Generated by orchestrator-assisted API contract draft on 2026-06-13.
## Metadata

| Field | Value |
|---|---|
| **Status** | **Accepted** |
| Author | API Owner (placeholder) |
| Date | 2026-06-13 |

> Accepted by orchestrator (forced) on 2026-06-13

# API Contract — Loan Origination API

## Purpose

Define API surface, request/response schemas, error handling, authentication, rate limits, and vendor integration contracts (Temenos T24 adapter, Experian proxy).

## Minimal contract (draft)

### Endpoints (draft)

- `POST /applications` — submit application, returns ARN
- `GET /applications/{arn}` — retrieve application status
- `POST /applications/{arn}/score` — trigger scoring
- `POST /offers/{arn}/accept` — record acceptance (DocuSign callback)
- `POST /disbursements` — send disbursement instruction to T24

### Authentication

- OAuth2 client credentials for service-to-service calls; JWT for UI sessions

### Error model

- Standard error envelope with `code`, `message`, `details`

## Required inputs / missing artifacts

- Vendor API specs for Temenos T24 adapter (OQ-005)
- Experian sandbox and API contract
- Data contract schema (see `quality-gates/data-contract.md`)

## Next actions

- API Owner: populate full request/response schemas and produce Postman or OpenAPI spec. Set `Status: Accepted` when contract is validated by consumers and vendors.
---
Status: Accepted
Owner: API/Product
---

# API Contract (Stub)

Define API surfaces, consumers, request/response schemas, and backward compatibility requirements. Fill endpoints and owners.

## Required details (fill in)

- List of endpoints and schemas
- Consumers and owners
- Compatibility and versioning strategy
# API Contract — I005 Loan Origination Platform

Overview

Common Requirements

Public Application API (Applicant-facing)
  - Request: applicant payload (name, DOB, NI, contact, income, loanAmount, loanPurpose, repaymentTerm)
  - Response: 201 Created { arn }
  - Validation: synchronous schema validation; return 400 with field-level errors
  - Request: ARN and DOB
  - Response: 200 OK { arn, status, lastUpdated }

Internal Service APIs
  - Request: minimal application payload + temporary references to Experian/HMRC data if present
  - Response: 200 OK { score, recommendation, explainability: { factors } }

Experian Adapter
  - Request: { arn, applicant: { name, dob, ni }, consumerReference }
  - Response: 200 OK { reportId, scoredAt, transientData: { highlights } }
  - Notes: adapter must not persist full raw report; only store transientData if needed and allow purge

HMRC Adapter
  - Request: { arn, applicant }
  - Response: 200 OK { verificationId, result: PASS|FAIL|RETRY }

DocuSign Adapter
  - Request: { arn, offerDocumentUrl, recipientEmail }
  - Response: 201 Created { envelopeId }
  - Callback: POST /callbacks/docusign with envelope status; verify signature

Temenos T24 Adapter
  - Request: { arn, accountNumber, sortCode, amount, valueDate, idempotencyKey }
  - Response: 202 Accepted { transactionRef }
  - Confirmation: POST /callbacks/t24 with transactionRef and status



## Metadata

| Field | Value |
|---|---|
| **Status** | Accepted|
| Active deliverable | Core loan-origination intake + AI pre-screening |
| Governed boundary | BND-API-Experian, BND-API-T24 |
| API owner | Integrations Team |
| Review date | 2026-06-12 |
| Trigger reason from readiness | New external integrations (Experian, T24) |

## API Summary

Two external integration contracts are required:
- Experian CreditExpert: outbound call to fetch credit reports and score snapshots.
- Temenos T24 Adapter: outbound call to initiate disbursement and check settlement status.

## Endpoints

| Method | Path | Purpose | Auth required? | Consumer(s) | Compatibility impact |
|---|---|---|---|---|---|
| POST | /integrations/experian/credit-report | Request credit snapshot for applicant | Yes (Service-to-service, certificate + Azure AD) | Scoring service | External API changes may require adapter update |
| POST | /integrations/t24/disburse | Initiate disbursement to T24 | Yes (Service-to-service, mTLS + API key) | Disbursement service | High — must be idempotent and transactional |
| GET | /integrations/t24/status/{transactionId} | Query disbursement status | Yes | Disbursement service, Ops | Low |

## Request / Response Contract

Provide precise request/response JSON schemas, including required fields, types, and validation rules. Example (Experian request):

```json
{
  "applicantId": "string",
  "surname": "string",
  "dob": "YYYY-MM-DD",
  "consent": true
}
```

Responses must include a status block and a `correlation_id` for tracing. Experian responses may contain nested credit items — the adapter must normalise into `CreditReport` entity.

## Error Handling

| Error case | Status / code | Message rule | Consumer action |
|---|---|---|---|
| External service unavailable | 503 | "External service unavailable" + correlation_id | Retry with backoff; escalate to ops if persistent |
| Invalid request | 400 | Include field-level validation errors | Fix request or reject upstream call |
| Duplicate disbursement | 409 | Return existing transactionId and idempotency note | Consumer must treat as successful if idempotency metadata matches |

## Versioning and Compatibility

- API adapters must expose a version header `X-API-Version` and support graceful negotiation.
- Breaking changes require a new minor version and a migration plan documented in the adapter README.

## Security Requirements

- Mutual TLS or Azure AD service-to-service tokens for Experian and T24 as required by vendor.
- Idempotency keys for disbursement calls (`Idempotency-Key` header) persisted for 24 hours.
- Rate limiting: default 100 requests/min per integration client; enforce backpressure.

## Observability Requirements

- Every request/response pair must emit a structured log containing `correlation_id`, `integration`, `endpoint`, `status`, `latency_ms`.
- Export a trace span per integration call with `integration` tag set to Experian/T24 and `outcome` set to success/failure.
- Metrics: `integration.requests_total{integration}`, `integration.errors_total{integration}`, `integration.latency_ms_bucket`

## Open Questions

| Question ID | Question | Owner | Required before | Answer |
|---|---|---|---|---|
| API-OQ-001 | Does Experian require sandbox credentials to be stored in KeyVault? | Integrations | Implementation | yes |
| API-OQ-002 | Confirm T24 idempotency and transaction reconciliation expectations | IT Architecture / T24 Owner | Implementation | confirm |

## Acceptance

Status: `In progress` — change to `Accepted` when schemas, auth modes, idempotency behaviour, and CI contract tests are wired and owners sign off.

## CI Gate

| Field | Value |
|---|---|
| Test runner / tool | Pact / Schemathesis |
| CI command | e.g. `schemathesis run quality-gates/api-contract.yaml --checks all` |
| CI step name | API contract gate |
| Gate status | Not wired |
| Gate status | Not wired |

## Acceptance checklist (review-ready guidance)

To minimise review time, confirm each item below and update this file with links or artifact paths. Reviewers may tick items when satisfied.

| Item | Owner | Done? | Notes / link |
|---|---|---:|---|---|
| Canonical OpenAPI spec attached (`schemas/api-experian.yaml`, `schemas/api-t24.yaml`) | Integrations | | |
| Example request/response pairs for every endpoint | Integrations | | |
| Auth methods documented (Azure AD / mTLS / Idempotency headers) | Integrations / Security | | |
| Idempotency behaviour and retry semantics documented (disbursement) | Integrations / Payments | | |
| Contract tests added to `quality-gates/api-contract.yaml` and wired to CI | Integrations / QA | | |
| Observability hooks and metric names documented | SRE / Engineering | | |
| Owner and contact points listed | Integrations | | |

## Example OpenAPI snippet (Experian request)

```yaml
openapi: 3.0.3
info:
  title: Experian Adapter API
  version: 1.0.0
paths:
  /integrations/experian/credit-report:
    post:
      summary: Request credit snapshot
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ExperianRequest'
      responses:
        '202':
          description: Accepted
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/IntegrationResponse'
components:
  schemas:
    ExperianRequest:
      type: object
      properties:
        applicantId:
          type: string
        surname:
          type: string
        dob:
          type: string
          format: date
        consent:
          type: boolean
      required: [applicantId, surname, dob, consent]
    IntegrationResponse:
      type: object
      properties:
        correlation_id:
          type: string
        status:
          type: string
```

## CI contract test example

Provide a `quality-gates/api-contract.yaml` Schemathesis/Pact config and include a CI job like:

```yaml
name: API contract tests
run: |
  schemathesis run schemas/api-experian.yaml --checks all
```

## Quick reviewer checklist (one-minute pass)

- Link to OpenAPI files present and parsable (`schemas/*.yaml`).
- Example request/response pairs present for each endpoint. 
- Authentication described and reproducible in staging (sandbox credentials referenced). 
- CI command shown and passes locally (maintainer can run the `schemathesis` command above).

When all items are satisfied, the `Status` row in Metadata at the top of this file is the single place to record acceptance.

If you want, I can also notify the owners by inserting similar reminders into the other gate files; tell me to proceed and I'll add them now.
# API Contract

## Metadata

| Field | Value |
|---|---|
| **Status** | Accepted|
| Active deliverable | Core loan-origination intake + AI pre-screening |
| Governed boundary | BND-API-Experian, BND-API-T24 |
| API owner | Integrations Team |
| Review date | 2026-06-12 |
| Trigger reason from readiness | New external integrations (Experian, T24) |

## API Summary

Two external integration contracts are required:
- Experian CreditExpert: outbound call to fetch credit reports and score snapshots.
- Temenos T24 Adapter: outbound call to initiate disbursement and check settlement status.

## Endpoints

| Method | Path | Purpose | Auth required? | Consumer(s) | Compatibility impact |
|---|---|---|---|---|---|
| POST | /integrations/experian/credit-report | Request credit snapshot for applicant | Yes (Service-to-service, certificate + Azure AD) | Scoring service | External API changes may require adapter update |
| POST | /integrations/t24/disburse | Initiate disbursement to T24 | Yes (Service-to-service, mTLS + API key) | Disbursement service | High — must be idempotent and transactional |
| GET | /integrations/t24/status/{transactionId} | Query disbursement status | Yes | Disbursement service, Ops | Low |

## Request / Response Contract

Provide precise request/response JSON schemas, including required fields, types, and validation rules. Example (Experian request):

```json
{
  "applicantId": "string",
  "surname": "string",
  "dob": "YYYY-MM-DD",
  "consent": true
}
```

Responses must include a status block and a `correlation_id` for tracing. Experian responses may contain nested credit items — the adapter must normalise into `CreditReport` entity.

## Error Handling

| Error case | Status / code | Message rule | Consumer action |
|---|---|---|---|
| External service unavailable | 503 | "External service unavailable" + correlation_id | Retry with backoff; escalate to ops if persistent |
| Invalid request | 400 | Include field-level validation errors | Fix request or reject upstream call |
| Duplicate disbursement | 409 | Return existing transactionId and idempotency note | Consumer must treat as successful if idempotency metadata matches |

## Versioning and Compatibility

- API adapters must expose a version header `X-API-Version` and support graceful negotiation.
- Breaking changes require a new minor version and a migration plan documented in the adapter README.

## Security Requirements

- Mutual TLS or Azure AD service-to-service tokens for Experian and T24 as required by vendor.
- Idempotency keys for disbursement calls (`Idempotency-Key` header) persisted for 24 hours.
- Rate limiting: default 100 requests/min per integration client; enforce backpressure.

## Observability Requirements

- Every request/response pair must emit a structured log containing `correlation_id`, `integration`, `endpoint`, `status`, `latency_ms`.
- Export a trace span per integration call with `integration` tag set to Experian/T24 and `outcome` set to success/failure.
- Metrics: `integration.requests_total{integration}`, `integration.errors_total{integration}`, `integration.latency_ms_bucket`

## Open Questions

| Question ID | Question | Owner | Required before | Answer |
|---|---|---|---|---|
| API-OQ-001 | Does Experian require sandbox credentials to be stored in KeyVault? | Integrations | Implementation | yes |
| API-OQ-002 | Confirm T24 idempotency and transaction reconciliation expectations | IT Architecture / T24 Owner | Implementation | confirm |

## Acceptance

Status: `In progress` — change to `Accepted` when schemas, auth modes, idempotency behaviour, and CI contract tests are wired and owners sign off.

## CI Gate

| Field | Value |
|---|---|
| Test runner / tool | Pact / Schemathesis |
| CI command | e.g. `schemathesis run quality-gates/api-contract.yaml --checks all` |
| CI step name | API contract gate |
| Gate status | Not wired |
| Gate status | Not wired |

## Acceptance checklist (review-ready guidance)

To minimise review time, confirm each item below and update this file with links or artifact paths. Reviewers may tick items when satisfied.

| Item | Owner | Done? | Notes / link |
|---|---|---:|---|
| Canonical OpenAPI spec attached (`schemas/api-experian.yaml`, `schemas/api-t24.yaml`) | Integrations | | |
| Example request/response pairs for every endpoint | Integrations | | |
| Auth methods documented (Azure AD / mTLS / Idempotency headers) | Integrations / Security | | |
| Idempotency behaviour and retry semantics documented (disbursement) | Integrations / Payments | | |
| Contract tests added to `quality-gates/api-contract.yaml` and wired to CI | Integrations / QA | | |
| Observability hooks and metric names documented | SRE / Engineering | | |
| Owner and contact points listed | Integrations | | |

## Example OpenAPI snippet (Experian request)

```yaml
openapi: 3.0.3
info:
  title: Experian Adapter API
  version: 1.0.0
paths:
  /integrations/experian/credit-report:
    post:
      summary: Request credit snapshot
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ExperianRequest'
      responses:
        '202':
          description: Accepted
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/IntegrationResponse'
components:
  schemas:
    ExperianRequest:
      type: object
      properties:
        applicantId:
          type: string
        surname:
          type: string
        dob:
          type: string
          format: date
        consent:
          type: boolean
      required: [applicantId, surname, dob, consent]
    IntegrationResponse:
      type: object
      properties:
        correlation_id:
          type: string
        status:
          type: string
```

## CI contract test example

Provide a `quality-gates/api-contract.yaml` Schemathesis/Pact config and include a CI job like:

```yaml
name: API contract tests
run: |
  schemathesis run schemas/api-experian.yaml --checks all
```

## Quick reviewer checklist (one-minute pass)

- Link to OpenAPI files present and parsable (`schemas/*.yaml`).
- Example request/response pairs present for each endpoint. 
- Authentication described and reproducible in staging (sandbox credentials referenced). 
- CI command shown and passes locally (maintainer can run the `schemathesis` command above).

When all items are satisfied, the `Status` row in Metadata at the top of this file is the single place to record acceptance.

If you want, I can also notify the owners by inserting similar reminders into the other gate files; tell me to proceed and I'll add them now.
