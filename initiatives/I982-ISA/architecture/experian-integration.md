# Experian CreditExpert API — Integration Contract

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I982-ISA |
| Integration ID | INT-001 |
| External system | Experian CreditExpert API (UK) |
| Direction | Consumed (outbound) |
| Enterprise contract | Yes — existing. Credentials managed by IT Architecture team |
| Created at | 2026-07-02 |
| Status | Draft |

## Purpose

The AI Scoring Service calls the Experian CreditExpert API once per submitted application to retrieve a consumer credit report. The credit data is used as input to the AI risk scoring model (FR-008). The integration must complete within 30 seconds (FR-009). If Experian is unavailable, the application is routed to `REFER_TO_UNDERWRITER` (FR-009 fallback).

The raw credit report is **not persisted**. Only the Experian report reference ID (`experian_report_ref`) and the computed risk score (`ai_risk_score`) are written to the Application entity.

## Traceability

| Source | Reference | Description |
|---|---|---|
| BRS | FR-009 | Mandatory Experian integration; 30s SLA; unavailability fallback |
| BRS | FR-008 | Credit bureau data is one of the scoring model inputs |
| BRS | NFR-007 | Circuit breakers required on all API integrations |
| Architecture | architecture.md | Experian: outbound REST/HTTPS; existing enterprise contract; circuit breaker required |
| Domain model | architecture/domain-model.md | ENT-001.experian_report_ref, ENT-001.ai_risk_score, ENT-001.ai_recommendation, state transitions T-003/T-004/T-005 |

---

## Connection Details

| Field | Value |
|---|---|
| Protocol | HTTPS (TLS 1.3 minimum — NFR-004) |
| Base URL env var | `EXPERIAN_API_BASE_URL` |
| Base URL value | `https://api.experian.com` |
| Report endpoint | `POST /consumerservices/credit-profile/v2/reports` |
| Token endpoint | `POST /oauth2/v1/token` |
| Auth mechanism | OAuth 2.0 — client credentials grant |
| Credential storage | Azure Key Vault secrets: `experian-client-id`, `experian-client-secret` |
| Key Vault access | AI Scoring Service managed identity (no stored secrets) |
| TLS | 1.3 minimum |
| Data residency | Requests routed via Azure UK South network only — GDPR data residency constraint |

---

## Authentication — OAuth 2.0 Client Credentials

### Token request

```http
POST https://api.experian.com/oauth2/v1/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id={experian-client-id from Key Vault}
&client_secret={experian-client-secret from Key Vault}
&scope=consumer-reports
```

### Token response

```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "consumer-reports"
}
```

### Token caching rules

| Rule | Value |
|---|---|
| Cache duration | `expires_in - 60` seconds (60-second safety buffer) |
| Cache scope | In-process, per AI Scoring Service instance |
| Refresh trigger | When cached token has < 60 seconds remaining |
| On 401 Unauthorized | Discard cached token, fetch new token once, retry request once. If still 401 → alert ops, fallback `REFER_TO_UNDERWRITER` |
| Cache storage | In-memory only — never persist access tokens to disk or database |

---

## Credit Report Request

### Endpoint

```
POST {EXPERIAN_API_BASE_URL}/consumerservices/credit-profile/v2/reports
```

### Request headers

| Header | Value | Notes |
|---|---|---|
| `Authorization` | `Bearer {access_token}` | Required |
| `Content-Type` | `application/json` | Required |
| `X-Request-ID` | `{UUID v4}` | Unique per request; used by Experian for idempotency and tracing. Same value on retry |
| `X-Correlation-ID` | `{application_id}` | End-to-end trace ID linking to the Application entity |
| `X-Consumer-Domain` | `loan-origination` | Required by Experian enterprise contract — identifies consumer product |

### Request body schema

```json
{
  "applicant": {
    "firstName": "string",
    "lastName": "string",
    "dateOfBirth": "YYYY-MM-DD",
    "nationalInsuranceNumber": "AB123456C"
  },
  "reportOptions": {
    "reportType": "CREDIT_PROFILE",
    "includeScore": true,
    "includeAccountDetails": true,
    "includeSearchHistory": true,
    "includeAdverseInformation": true
  }
}
```

### Field mapping from Application entity (ENT-001)

| Request field | Source field | Transformation |
|---|---|---|
| `applicant.firstName` | `Application.full_name` | Extract substring before first space |
| `applicant.lastName` | `Application.full_name` | Extract substring from first space to end |
| `applicant.dateOfBirth` | `Application.date_of_birth` | ISO 8601 date string (YYYY-MM-DD) |
| `applicant.nationalInsuranceNumber` | `Application.national_insurance_number` | As-is (format: `[A-Z]{2}[0-9]{6}[A-D]`) |

**PII note:** `firstName`, `lastName`, `dateOfBirth`, and `nationalInsuranceNumber` are transmitted to Experian over TLS 1.3. They MUST NOT be logged at any verbosity level in AI Scoring Service logs.

---

## Credit Report Response

### Success response — HTTP 200

```json
{
  "reportId": "EXP-{UUID}",
  "reportGeneratedAt": "2026-07-02T09:15:00Z",
  "applicantMatch": {
    "matchStatus": "FULL_MATCH | PARTIAL_MATCH | NO_MATCH",
    "matchConfidence": 0.97
  },
  "creditScore": {
    "score": 750,
    "scoreBand": "A | B | C | D | E",
    "scoreModel": "EXPERIAN_DELPHI_V7"
  },
  "creditHistory": {
    "oldestAccountOpenedMonths": 84,
    "totalAccountCount": 5,
    "activeAccountCount": 3,
    "closedAccountCount": 2,
    "missedPaymentsLast12Months": 0,
    "missedPaymentsLast24Months": 1,
    "hardSearchesLast6Months": 2,
    "totalOutstandingDebtGbp": 12500.00,
    "highestCreditLimitGbp": 8000.00,
    "currentPaymentStatus": "UP_TO_DATE | LATE | DEFAULTED"
  },
  "adverseInformation": {
    "bankruptcyActive": false,
    "bankruptcyLast6Years": false,
    "ccjsLast6Years": 0,
    "ivaActive": false,
    "defaultsLast6Years": 0,
    "debtManagementPlanActive": false
  }
}
```

### Field mapping from response to AI Scoring Service inputs (FR-008)

| AI Scoring input | Source field(s) | Computation |
|---|---|---|
| Credit bureau score | `creditScore.score` | Direct (0–999 Experian Delphi scale) |
| Credit score band | `creditScore.scoreBand` | Direct (A = best, E = worst) |
| Credit history length (months) | `creditHistory.oldestAccountOpenedMonths` | Direct |
| Missed payments (recent) | `creditHistory.missedPaymentsLast12Months` | Direct |
| Missed payments (extended) | `creditHistory.missedPaymentsLast24Months` | Direct |
| Recent credit searches | `creditHistory.hardSearchesLast6Months` | Direct — high count signals credit stress |
| Total outstanding debt (GBP) | `creditHistory.totalOutstandingDebtGbp` | Used for DTI computation (see below) |
| Adverse indicator | `adverseInformation.*` | Any `true` or `> 0` field → adverse flag = true |
| Match confidence | `applicantMatch.matchConfidence` | If `< 0.80` → treat as NO_MATCH → route REFER_TO_UNDERWRITER |

### Derived metrics (computed by AI Scoring Service, not Experian)

| Metric | Formula | Written to |
|---|---|---|
| `debt_to_income_ratio` | `creditHistory.totalOutstandingDebtGbp / Application.annual_income_gbp` | `Application.debt_to_income_ratio` |
| `loan_to_income_ratio` | `Application.loan_amount_requested_gbp / Application.annual_income_gbp` | `Application.loan_to_income_ratio` |

### Fields stored from response

| Field stored | Entity field | Notes |
|---|---|---|
| `reportId` | `Application.experian_report_ref` | Reference only — raw report discarded after scoring |

**All other Experian response fields are used in-memory for scoring and then discarded.** They MUST NOT be persisted to any database or log stream.

---

## Error Catalogue and Fallback Behaviour

| HTTP Status | Condition | Retry? | Fallback | Alert? | Circuit Breaker |
|---|---|---|---|---|---|
| 200 OK | Success — parse response | No | — | No | Reset failure counter |
| 400 Bad Request | Invalid request payload | No | `REFER_TO_UNDERWRITER` with reason `CREDIT_BUREAU_VALIDATION_ERROR` | Yes — log request details (without PII) at ERROR level | No increment |
| 401 Unauthorized | Token expired or invalid | Yes — refresh token once, retry once | If still 401: `REFER_TO_UNDERWRITER` + ops alert | Yes (if persists after refresh) | No increment (auth issue, not availability) |
| 403 Forbidden | Insufficient scope | No | `REFER_TO_UNDERWRITER` + immediate ops P1 alert | Yes — P1 | No increment |
| 404 Not Found | Applicant not found in Experian | No | `REFER_TO_UNDERWRITER` with reason `CREDIT_BUREAU_NO_MATCH` | No | No increment |
| 422 Unprocessable Entity | NI format rejected by Experian | No | `REFER_TO_UNDERWRITER` with reason `CREDIT_BUREAU_VALIDATION_ERROR` | Yes — log (without PII) | No increment |
| 429 Too Many Requests | Rate limited | Yes — once, after `Retry-After` header value (default 5s if header absent) | If still 429: `REFER_TO_UNDERWRITER` | Yes — WARNING | **Increment** |
| 500 Internal Server Error | Experian server error | Yes — once, after 2s delay | If still 5xx: `REFER_TO_UNDERWRITER` | Yes — WARNING | **Increment** |
| 502 Bad Gateway | Upstream Experian error | Yes — once, after 2s delay | `REFER_TO_UNDERWRITER` | Yes | **Increment** |
| 503 Service Unavailable | Experian down | No | `REFER_TO_UNDERWRITER` | Yes | **Increment** |
| Timeout (`> 25s`) | Connect or read timeout | No | `REFER_TO_UNDERWRITER` | Yes — WARNING | **Increment** |
| Connection refused | Network error | No | `REFER_TO_UNDERWRITER` | Yes | **Increment** |

### Fallback message sent on REFER_TO_UNDERWRITER

When Experian call fails and application is routed to `REFER_TO_UNDERWRITER` (state machine transition T-004), publish this Service Bus event:

```json
{
  "type": "CreditBureauCheckFailed",
  "applicationId": "{uuid}",
  "requestId": "{X-Request-ID used}",
  "outcome": "UNAVAILABLE | RATE_LIMITED | NO_MATCH | VALIDATION_ERROR | AUTH_ERROR",
  "fallbackAction": "REFER_TO_UNDERWRITER",
  "timestamp": "ISO 8601 UTC"
}
```

---

## Timeout and Circuit Breaker Configuration

### Timeout

| Timeout type | Value | Rationale |
|---|---|---|
| Connect timeout | 5,000 ms | Network connection establishment |
| Read timeout | 20,000 ms | Response receipt after connection |
| Total budget | 25,000 ms | Leaves 5s for AI scoring overhead within FR-009's 30s end-to-end SLA |

### Circuit breaker — `aiobreaker` (Python, AI Scoring Service)

```python
from aiobreaker import CircuitBreaker
import asyncio

experian_breaker = CircuitBreaker(
    fail_max=3,            # 3 consecutive failures → OPEN
    timeout_duration=60,   # 60s in OPEN state before half-open probe
    exclude=[              # Do not trip breaker for these — they are not availability signals
        # HTTP 400, 401, 403, 404, 422 are handled inline (see error catalogue)
    ]
)
```

| Parameter | Value | Notes |
|---|---|---|
| `fail_max` | 3 | 3 consecutive circuit-breaker-eligible failures → OPEN state |
| `timeout_duration` | 60s | Duration in OPEN state before allowing 1 probe request (half-open) |
| Half-open probe | 1 request | On success → CLOSED; on failure → OPEN for another 60s |
| Eligible failures | 429, 500, 502, 503, Timeout, ConnectionError | See error catalogue above |
| Excluded from breaker | 400, 401, 403, 404, 422 | These are request/auth issues, not availability issues |

**When circuit is OPEN:** Do not attempt Experian call. Immediately publish `CreditBureauCheckFailed` event with `outcome: UNAVAILABLE` and trigger state machine transition T-004 (→ `UNDERWRITER_QUEUE`).

---

## Service Bus Event Contract

### Trigger — Loan Origination API → AI Scoring Service

The Loan Origination API publishes this event to Service Bus topic `credit-bureau-check-requested` when application reaches `AI_SCREENING` state:

```json
{
  "type": "CreditBureauCheckRequested",
  "applicationId": "{uuid}",
  "fullName": "{encrypted — decrypted by AI Scoring Service using managed identity}",
  "dateOfBirth": "{encrypted}",
  "nationalInsuranceNumber": "{encrypted}",
  "annualIncomeGbp": 45000.00,
  "loanAmountRequestedGbp": 8000.00,
  "correlationId": "{uuid}",
  "timestamp": "ISO 8601 UTC"
}
```

**Note:** PII fields in Service Bus messages are encrypted at the field level using the AI Scoring Service's managed identity key. The AI Scoring Service decrypts them in-memory, uses them for the Experian call, and never re-emits them in any downstream event.

### Result — AI Scoring Service → Loan Origination API

Published to Service Bus topic `credit-bureau-check-completed`:

**On success:**
```json
{
  "type": "CreditBureauCheckCompleted",
  "applicationId": "{uuid}",
  "reportRef": "EXP-{UUID}",
  "outcome": "SUCCESS",
  "creditScoreRaw": 750,
  "creditScoreBand": "A",
  "creditHistoryMonths": 84,
  "missedPayments12Months": 0,
  "missedPayments24Months": 1,
  "hardSearches6Months": 2,
  "totalOutstandingDebtGbp": 12500.00,
  "adverseFlag": false,
  "correlationId": "{uuid}",
  "timestamp": "ISO 8601 UTC"
}
```

**On failure/fallback:**
```json
{
  "type": "CreditBureauCheckCompleted",
  "applicationId": "{uuid}",
  "reportRef": null,
  "outcome": "UNAVAILABLE | RATE_LIMITED | NO_MATCH | VALIDATION_ERROR | AUTH_ERROR",
  "creditScoreRaw": null,
  "correlationId": "{uuid}",
  "timestamp": "ISO 8601 UTC"
}
```

The Loan Origination API state machine consumes this event:
- `outcome: SUCCESS` → evaluate `ai_recommendation` → proceed to T-003 or T-005
- `outcome: *` (any failure) → T-004 (→ `UNDERWRITER_QUEUE`)

---

## Observability Signals

| Signal type | Name | Labels | Condition |
|---|---|---|---|
| Histogram | `experian_request_duration_ms` | `outcome: success/no_match/unavailable/rate_limited/error/timeout` | Every call attempt |
| Counter | `experian_request_total` | `outcome: ...`, `http_status: NNN` | Every call attempt |
| Gauge | `experian_circuit_breaker_state` | `state: closed/open/half_open` | On state change |
| Counter | `experian_circuit_breaker_trips_total` | — | On every trip to OPEN |
| Counter | `experian_fallback_total` | `reason: ...` | Every fallback to REFER_TO_UNDERWRITER |

### Alert thresholds

| Alert | Condition | Severity | Response |
|---|---|---|---|
| Circuit breaker open | `experian_circuit_breaker_state = open` for > 120s | P1 | Page on-call; Experian enterprise support contact |
| High fallback rate | `experian_fallback_total` rate > 5% of total calls over 5 min | P2 | Investigate; check Experian status page |
| Auth failure | `experian_request_total{http_status="401"}` > 0 after token refresh | P1 | Rotate credentials in Key Vault immediately |
| Elevated latency | P95 `experian_request_duration_ms` > 20,000 ms over 5 min | P2 | Risk of SLA breach on FR-009 |

---

## Data Residency and Compliance

| Constraint | Implementation |
|---|---|
| UK data residency | All API calls made from Azure UK South only. No Experian responses leave the UK region. |
| PII in transit | Encrypted via TLS 1.3. PII fields (`firstName`, `lastName`, `dateOfBirth`, `nationalInsuranceNumber`) never logged |
| Raw credit report retention | Zero. All Experian response fields except `reportId` are discarded after scoring |
| Stored data | Only `Application.experian_report_ref` (Experian `reportId`) and `Application.ai_risk_score` are persisted |
| Audit trail | Every Experian call outcome is captured in the AuditEvent for the `AI_SCREENING → {next_state}` transition (see ENT-004 data_snapshot schema) |
| Enterprise contract | Credentials provisioned and rotated by IT Architecture team. Rotation schedule: 90 days. Key Vault secret versioning enabled |

---

## Known Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Experian outage during peak | All non-Experian-available applications routed to underwriter queue; underwriter load spikes | Circuit breaker limits queue storm; escalation timer (FR-019) handles backlog; operations dashboard (FR-029) shows AML/KYC hold rate |
| Applicant not found (404) | Cannot compute AI score; routes to underwriter | Underwriter reviews manually; no auto-decline without a score |
| Rate limit breach | Requests throttled during bulk processing | Service Bus queue absorbs burst; retry with `Retry-After`; alert at > 5% fallback rate |
| Token expiry at high concurrency | Multiple threads refresh token simultaneously | Implement mutex/lock on token refresh to prevent thundering herd |
| Credit report response schema change | Field mapping breaks; scoring fails | Monthly contract review; schema validation on response (`422 Unprocessable Experian Response` → fallback + alert) |

---

## Open Questions

| # | Question | Owner | Needed before | Status |
|---|---|---|---|---|
| IQ-001 | What is the exact Experian enterprise API version in the existing contract — v1 or v2 of `/consumerservices/credit-profile`? | IT Architecture | AI Scoring Service implementation | Open |
| IQ-002 | What is the contracted rate limit (requests/minute) for the Experian CreditExpert enterprise account? | IT Architecture | Circuit breaker and queue sizing | Open |
| IQ-003 | Does the existing Experian contract include the `nationalInsuranceNumber` matching field or is address-based matching required? | IT Architecture | AI Scoring Service implementation | Open |
| IQ-004 | What is the Experian enterprise SLA for P99 response time? | IT Architecture | Timeout calibration and alert thresholds | Open |

**Note:** These open questions do not block the coding package skeleton but MUST be resolved before the AI Scoring Service is production-ready. If NIN-based matching is not available (IQ-003), the Application entity (ENT-001) requires two additional fields: `address_line_1` and `postcode`, and FR-001 must be updated to collect them.
