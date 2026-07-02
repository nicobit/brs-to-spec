# CP-001 — AI Scoring Service

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I982-ISA |
| Package ID | CP-001 |
| Service | AI Scoring Service |
| Technology | Python 3.12 / FastAPI — Azure Container Apps |
| BRS References | FR-006, FR-007, FR-008, FR-009, NFR-002, NFR-007, FCA constraint (explainable AI) |
| Depends on | architecture/domain-model.md (ENT-001), architecture/experian-integration.md (INT-001) |
| Created at | 2026-07-02 |
| Status | Draft |

---

## Purpose

The AI Scoring Service receives an application intake event from the Loan Origination API, calls the Experian CreditExpert API to retrieve credit bureau data, computes a 14-feature vector, calls an Azure AI Foundry online endpoint to produce a repayment probability, maps that probability to a risk score (0–1000) and a recommendation (`AUTO_APPROVE`, `REFER_TO_UNDERWRITER`, `AUTO_DECLINE`), generates a SHAP-based explainability artefact (FCA regulatory requirement — black-box models not permitted), and publishes the result event back to the Loan Origination API.

The entire pipeline must complete in ≤ 90 seconds end-to-end (NFR-002). If any external dependency (Experian or Azure Foundry) is unavailable, the application is routed to `REFER_TO_UNDERWRITER` — never silently dropped.

---

## BRS Traceability

| FR | Requirement | Implementation |
|---|---|---|
| FR-006 | AI pre-screening triggered within 60s of submission | Service Bus consumer processes `AIScreeningRequested`; acknowledged within 60s |
| FR-007 | Produce risk score (0–1000) and recommendation | `ai_risk_score`, `ai_recommendation` computed from Azure Foundry output |
| FR-008 | Scoring inputs: applicant data, credit bureau, DTI, LTI, employment stability, credit history | 14-feature vector defined below |
| FR-009 | Experian integration ≤30s; unavailable → REFER_TO_UNDERWRITER | See INT-001; 25s timeout; circuit breaker fallback |
| NFR-002 | AI scoring pipeline ≤90s end-to-end | Total SLA budget enforced at Service Bus message level |
| NFR-007 | Circuit breakers on all external calls | Experian breaker (INT-001) + Azure Foundry breaker (below) |
| FCA | Explainable AI — black-box models not permitted | SHAP values computed and stored per inference; `ai_explanation_ref` mandatory |

---

## Architecture

```
Loan Origination API
        │  publishes AIScreeningRequested
        ▼
  Service Bus Topic: ai-screening-requested
        │
        ▼
  AI Scoring Service  ──────────────────────────────────────────────────────────
  │                                                                              │
  │  1. Decrypt PII fields (Key Vault managed identity)                          │
  │  2. Call Experian CreditExpert API (INT-001, 25s timeout, circuit breaker)   │
  │  3. Build 14-feature vector                                                  │
  │  4. Call Azure Foundry online endpoint (10s timeout, circuit breaker)        │
  │  5. Map repayment_probability → ai_risk_score + ai_recommendation            │
  │  6. Compute SHAP values                                                      │
  │  7. Write explainability JSON → Azure Blob Storage                           │
  │  8. Publish AIScoringCompleted event                                         │
  ────────────────────────────────────────────────────────────────────────────────
        │  publishes AIScoringCompleted
        ▼
  Service Bus Topic: ai-scoring-completed
        │
        ▼
  Loan Origination API (consumes, drives state machine transition T-003/T-004/T-005)
```

---

## Service Bus Event Schemas

### Inbound: `AIScreeningRequested`

**Topic:** `ai-screening-requested`
**Subscription:** `ai-scoring-service`
**Dead-letter queue:** `ai-screening-requested/$DeadLetterQueue`
**Max delivery count:** 3 (after 3 failures → dead-letter; do NOT re-route to REFER automatically from dead-letter — alert ops)
**Session:** disabled
**Duplicate detection window:** 1 hour (Service Bus native deduplication on `MessageId = applicationId`)

```json
{
  "type": "AIScreeningRequested",
  "schemaVersion": "1.0",
  "applicationId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "annualIncomeGbp": 45000.00,
  "loanAmountRequestedGbp": 8000.00,
  "repaymentTermMonths": 36,
  "employmentStatus": "EMPLOYED_FULL_TIME",
  "loanPurpose": "Home improvement",
  "fullName_encrypted": "<AES-256 base64 ciphertext>",
  "dateOfBirth_encrypted": "<AES-256 base64 ciphertext>",
  "nationalInsuranceNumber_encrypted": "<AES-256 base64 ciphertext>",
  "correlationId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "timestamp": "2026-07-02T09:15:00Z"
}
```

**PII handling:**
- `fullName_encrypted`, `dateOfBirth_encrypted`, `nationalInsuranceNumber_encrypted` are AES-256 ciphertexts
- Decryption key retrieved from Azure Key Vault (secret: `ai-scoring-pii-key`) via managed identity
- Decrypted values used **only in-memory** for Experian call (INT-001); never logged, never stored, discarded after Experian response
- Service Bus messages are retained for 1 day (default TTL) then purged

### Outbound: `AIScoringCompleted`

**Topic:** `ai-scoring-completed`

**On success:**

```json
{
  "type": "AIScoringCompleted",
  "schemaVersion": "1.0",
  "applicationId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "aiRiskScore": 812,
  "aiRecommendation": "AUTO_APPROVE",
  "aiExplanationRef": "https://loanplatformsa.blob.core.windows.net/ai-explainability/3fa85f64-5717-4562-b3fc-2c963f66afa6/a1b2c3d4-e5f6-7890-abcd-ef1234567890.json",
  "experianReportRef": "EXP-7c3f2e1a-bb9d-4d12-8a3f-1c2d3e4f5a6b",
  "debtToIncomeRatio": 0.278,
  "loanToIncomeRatio": 0.178,
  "modelVersion": "v1.2.3",
  "failureReason": null,
  "correlationId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "timestamp": "2026-07-02T09:15:42Z"
}
```

**On failure/fallback (any external dependency failure):**

```json
{
  "type": "AIScoringCompleted",
  "schemaVersion": "1.0",
  "applicationId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "aiRiskScore": null,
  "aiRecommendation": "REFER_TO_UNDERWRITER",
  "aiExplanationRef": null,
  "experianReportRef": null,
  "debtToIncomeRatio": null,
  "loanToIncomeRatio": null,
  "modelVersion": null,
  "failureReason": "EXPERIAN_UNAVAILABLE | FOUNDRY_UNAVAILABLE | EXPERIAN_NO_MATCH | SCORING_ERROR",
  "correlationId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "timestamp": "2026-07-02T09:15:38Z"
}
```

**Loan Origination API consumes `AIScoringCompleted` and drives state machine:**

| `aiRecommendation` | `failureReason` | State transition |
|---|---|---|
| `AUTO_DECLINE` | null | T-003 → `AUTO_DECLINED` |
| Any value | Non-null | T-004 → `UNDERWRITER_QUEUE` |
| `AUTO_APPROVE` or `REFER_TO_UNDERWRITER` | null | T-005 → `COMPLIANCE_CHECK` |

---

## Internal Pipeline — Step-by-Step

### Step 1 — Idempotency check

Before processing, check whether this `applicationId` has already been scored:

```python
async def is_already_scored(application_id: str) -> bool:
    # Call Loan Origination API health endpoint
    # GET /internal/applications/{application_id}/scoring-status
    # Returns: { "scored": true/false }
    # If scored=true → ack message, return early (no re-processing)
    ...
```

If already scored: acknowledge message, emit `scoring.deduplicated` counter metric, return.

### Step 2 — Decrypt PII fields

```python
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
import base64, json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

async def decrypt_pii(encrypted_b64: str, key_secret_name: str) -> str:
    # Fetch AES-256 key from Key Vault (cached per instance lifecycle, rotated on 401)
    # key = base64-decoded 32-byte AES key
    # encrypted_b64 = base64(IV[16 bytes] + ciphertext)
    # Return plaintext string
    ...
```

**Key Vault secret names:**
- `ai-scoring-pii-key` — AES-256 symmetric key for PII decryption (managed by Loan Origination API team; rotated every 90 days)

### Step 3 — Call Experian CreditExpert API

See `architecture/experian-integration.md` (INT-001) for full contract.

**Outcome mapping:**

| Experian outcome | Effect on pipeline |
|---|---|
| `SUCCESS`, `matchStatus = FULL_MATCH` | Extract credit fields → proceed to Step 4 |
| `SUCCESS`, `matchStatus = PARTIAL_MATCH`, `matchConfidence >= 0.80` | Extract credit fields → proceed to Step 4 |
| `SUCCESS`, `matchStatus = NO_MATCH` or `matchConfidence < 0.80` | Set `has_experian_match = 0`, `credit_score_raw = 500` (neutral), all other Experian fields = 0, `adverse_flag = 0` → proceed to Step 4 with degraded features |
| `UNAVAILABLE / RATE_LIMITED / AUTH_ERROR` | Circuit breaker triggered → publish `AIScoringCompleted` with `failureReason=EXPERIAN_UNAVAILABLE`, skip Steps 4–8 |

**Note on NO_MATCH degraded scoring:** When `has_experian_match = 0`, the model will produce a lower-confidence score. The resulting `aiRecommendation` will almost always be `REFER_TO_UNDERWRITER` due to the neutral/zero feature values — this is intentional. The underwriter reviews with full context.

### Step 4 — Build feature vector

All 14 features must be present. Default values apply when Experian is unavailable for a partial-match degraded run.

| # | Feature name | Type | Source | Default (no Experian match) |
|---|---|---|---|---|
| 1 | `annual_income_gbp` | float | `AIScreeningRequested.annualIncomeGbp` | — (always available) |
| 2 | `loan_amount_requested_gbp` | float | `AIScreeningRequested.loanAmountRequestedGbp` | — |
| 3 | `repayment_term_months` | int | `AIScreeningRequested.repaymentTermMonths` | — |
| 4 | `employment_status_encoded` | int | `AIScreeningRequested.employmentStatus` | — |
| 5 | `credit_score_raw` | int | `Experian.creditScore.score` | 500 |
| 6 | `credit_history_months` | int | `Experian.creditHistory.oldestAccountOpenedMonths` | 0 |
| 7 | `missed_payments_12m` | int | `Experian.creditHistory.missedPaymentsLast12Months` | 0 |
| 8 | `missed_payments_24m` | int | `Experian.creditHistory.missedPaymentsLast24Months` | 0 |
| 9 | `hard_searches_6m` | int | `Experian.creditHistory.hardSearchesLast6Months` | 0 |
| 10 | `total_outstanding_debt_gbp` | float | `Experian.creditHistory.totalOutstandingDebtGbp` | 0.0 |
| 11 | `debt_to_income_ratio` | float | `total_outstanding_debt_gbp / annual_income_gbp` | 0.0 |
| 12 | `loan_to_income_ratio` | float | `loan_amount_requested_gbp / annual_income_gbp` | computed |
| 13 | `adverse_flag` | int (0/1) | Any `adverseInformation.*` field is `true` or `> 0` → 1, else 0 | 0 |
| 14 | `has_experian_match` | int (0/1) | 1 if Experian returned FULL_MATCH or PARTIAL_MATCH with confidence ≥ 0.80; 0 otherwise | 0 |

**`employment_status_encoded` mapping:**

| BRS value | Encoded int |
|---|---|
| `UNEMPLOYED` | 0 |
| `EMPLOYED_PART_TIME` | 1 |
| `SELF_EMPLOYED` | 2 |
| `OTHER` | 3 |
| `RETIRED` | 4 |
| `EMPLOYED_FULL_TIME` | 5 |

**Edge cases:**
- `annual_income_gbp = 0` is not possible (BR-003 enforces > 0 at submission). If received, treat as scoring error → `REFER_TO_UNDERWRITER` with `failureReason = SCORING_ERROR`.
- `total_outstanding_debt_gbp > annual_income_gbp * 10`: debt-to-income > 10 is capped at 10.0 (model was trained with this cap; values above are winsorized).

### Step 5 — Call Azure Foundry online endpoint

**Environment variables required:**
- `AZURE_FOUNDRY_ENDPOINT_URL` — e.g. `https://loanplatform-scoring.uksouth.inference.ml.azure.com/score`
- `AZURE_FOUNDRY_ENDPOINT_KEY_SECRET_NAME` — Key Vault secret name containing the endpoint API key

**Authentication:** API key from Key Vault (managed identity access). Bearer token auth is not available for Azure Foundry online endpoints — use API key header.

**Request:**

```http
POST {AZURE_FOUNDRY_ENDPOINT_URL}
Authorization: Bearer {endpoint_api_key}
Content-Type: application/json

{
  "input_data": {
    "columns": [
      "annual_income_gbp", "loan_amount_requested_gbp", "repayment_term_months",
      "employment_status_encoded", "credit_score_raw", "credit_history_months",
      "missed_payments_12m", "missed_payments_24m", "hard_searches_6m",
      "total_outstanding_debt_gbp", "debt_to_income_ratio", "loan_to_income_ratio",
      "adverse_flag", "has_experian_match"
    ],
    "data": [
      [45000.0, 8000.0, 36, 5, 780, 84, 0, 1, 2, 5000.0, 0.278, 0.178, 0, 1]
    ],
    "request_shap_values": true
  }
}
```

**Response:**

```json
{
  "predictions": [0.812],
  "shap_values": [
    {
      "annual_income_gbp": 0.038,
      "loan_amount_requested_gbp": -0.015,
      "repayment_term_months": 0.008,
      "employment_status_encoded": 0.045,
      "credit_score_raw": 0.142,
      "credit_history_months": 0.067,
      "missed_payments_12m": -0.021,
      "missed_payments_24m": -0.031,
      "hard_searches_6m": -0.012,
      "total_outstanding_debt_gbp": -0.029,
      "debt_to_income_ratio": -0.089,
      "loan_to_income_ratio": -0.034,
      "adverse_flag": 0.0,
      "has_experian_match": 0.0
    }
  ],
  "model_version": "v1.2.3"
}
```

**Azure Foundry circuit breaker:**

```python
from aiobreaker import CircuitBreaker

foundry_breaker = CircuitBreaker(
    fail_max=3,           # 3 consecutive failures → OPEN
    timeout_duration=60,  # 60s in OPEN state
)
```

**Azure Foundry timeout:**
- Connect: 3,000 ms
- Read: 10,000 ms (total: 13s — inference must be fast for 90s total SLA)

**Azure Foundry error handling:**

| HTTP Status | Action |
|---|---|
| 200 OK | Parse `predictions[0]` and `shap_values[0]` |
| 400 Bad Request | Log feature vector (without PII); `REFER_TO_UNDERWRITER` with `failureReason=SCORING_ERROR`; no circuit breaker increment |
| 401 / 403 | Refresh API key from Key Vault once; retry once; if still failing → P1 alert + `REFER_TO_UNDERWRITER` |
| 429 | Wait `Retry-After` header (default 5s); retry once; if still failing → `REFER_TO_UNDERWRITER` + circuit breaker increment |
| 5xx | Retry once after 2s; circuit breaker increment; `REFER_TO_UNDERWRITER` |
| Timeout | Circuit breaker increment; `REFER_TO_UNDERWRITER` with `failureReason=FOUNDRY_UNAVAILABLE` |
| Circuit OPEN | Immediate `REFER_TO_UNDERWRITER` with `failureReason=FOUNDRY_UNAVAILABLE` |

### Step 6 — Map model output to risk score and recommendation

```python
def map_to_risk_score(repayment_probability: float) -> int:
    """Maps 0.0-1.0 probability to 0-1000 risk score."""
    return round(repayment_probability * 1000)

def derive_recommendation(
    ai_risk_score: int,
    adverse_flag: int,
    has_experian_match: int
) -> str:
    """
    Business rule thresholds — MUST be confirmed by Head of Retail Lending before production.
    See open question AIQ-001 below.
    """
    if adverse_flag == 1:
        # Any active bankruptcy, CCJ, default, or IVA → always AUTO_DECLINE
        return "AUTO_DECLINE"
    if has_experian_match == 0:
        # No Experian match → always REFER; underwriter reviews with no credit data
        return "REFER_TO_UNDERWRITER"
    if ai_risk_score >= 700:
        return "AUTO_APPROVE"
    elif 400 <= ai_risk_score < 700:
        return "REFER_TO_UNDERWRITER"
    else:  # ai_risk_score < 400
        return "AUTO_DECLINE"
```

**Threshold summary (pending business confirmation — AIQ-001):**

| Condition | Recommendation |
|---|---|
| `adverse_flag = 1` (any adverse — bankruptcies, CCJs, defaults, IVA) | `AUTO_DECLINE` |
| `has_experian_match = 0` | `REFER_TO_UNDERWRITER` |
| `ai_risk_score ≥ 700` | `AUTO_APPROVE` |
| `400 ≤ ai_risk_score < 700` | `REFER_TO_UNDERWRITER` |
| `ai_risk_score < 400` | `AUTO_DECLINE` |

**Note on loan amount:** FR-010 states that `AUTO_APPROVE` with loan > £10,000 still requires underwriter review. This filter is applied by the **Loan Origination API state machine** (guard T-006/T-007), not by this service. The AI Scoring Service always returns `AUTO_APPROVE` based purely on the score — the Loan Origination API enforces the £10,000 threshold.

### Step 7 — Generate and store explainability artefact

**Explainability JSON schema:**

```json
{
  "schemaVersion": "1.0",
  "applicationId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "correlationId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "modelVersion": "v1.2.3",
  "scoredAt": "2026-07-02T09:15:42Z",
  "repaymentProbability": 0.812,
  "aiRiskScore": 812,
  "recommendation": "AUTO_APPROVE",
  "featureVector": {
    "annual_income_gbp": 45000.0,
    "loan_amount_requested_gbp": 8000.0,
    "repayment_term_months": 36,
    "employment_status_encoded": 5,
    "credit_score_raw": 780,
    "credit_history_months": 84,
    "missed_payments_12m": 0,
    "missed_payments_24m": 1,
    "hard_searches_6m": 2,
    "total_outstanding_debt_gbp": 5000.0,
    "debt_to_income_ratio": 0.278,
    "loan_to_income_ratio": 0.178,
    "adverse_flag": 0,
    "has_experian_match": 1
  },
  "featureContributions": {
    "annual_income_gbp": 0.038,
    "loan_amount_requested_gbp": -0.015,
    "repayment_term_months": 0.008,
    "employment_status_encoded": 0.045,
    "credit_score_raw": 0.142,
    "credit_history_months": 0.067,
    "missed_payments_12m": -0.021,
    "missed_payments_24m": -0.031,
    "hard_searches_6m": -0.012,
    "total_outstanding_debt_gbp": -0.029,
    "debt_to_income_ratio": -0.089,
    "loan_to_income_ratio": -0.034,
    "adverse_flag": 0.0,
    "has_experian_match": 0.0
  },
  "topPositiveFactors": ["credit_score_raw", "credit_history_months", "employment_status_encoded"],
  "topNegativeFactors": ["debt_to_income_ratio", "loan_to_income_ratio", "missed_payments_24m"],
  "declineReasonCategory": null
}
```

**`declineReasonCategory` values (used for applicant-facing decline notification per FR-011):**

| Reason code | When set |
|---|---|
| `"ADVERSE_CREDIT_HISTORY"` | `adverse_flag = 1` |
| `"HIGH_DEBT_TO_INCOME"` | `debt_to_income_ratio` is top negative SHAP contributor AND `ai_risk_score < 400` |
| `"INSUFFICIENT_CREDIT_HISTORY"` | `credit_history_months` is top negative contributor AND `ai_risk_score < 400` |
| `"POOR_PAYMENT_HISTORY"` | `missed_payments_24m` is top negative contributor AND `ai_risk_score < 400` |
| `"LOAN_TO_INCOME_RATIO"` | `loan_to_income_ratio` is top negative contributor AND `ai_risk_score < 400` |
| `"CREDIT_SCORE"` | `credit_score_raw` is top negative contributor AND `ai_risk_score < 400` |
| `null` | Recommendation is `AUTO_APPROVE` or `REFER_TO_UNDERWRITER` |

**Note:** `declineReasonCategory` must be a category code — never reveal the raw score or SHAP values to applicants (FR-011 mandates "decline reason category, not the score").

**Azure Blob Storage — write explainability JSON:**

```python
from azure.storage.blob.aio import BlobServiceClient
from azure.identity.aio import ManagedIdentityCredential

async def store_explainability(
    application_id: str,
    correlation_id: str,
    payload: dict
) -> str:
    """Returns the blob URL as ai_explanation_ref."""
    credential = ManagedIdentityCredential()
    client = BlobServiceClient(
        account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
        credential=credential
    )
    blob_name = f"{application_id}/{correlation_id}.json"
    blob_client = client.get_blob_client(
        container=AI_EXPLAINABILITY_CONTAINER,
        blob=blob_name
    )
    await blob_client.upload_blob(
        json.dumps(payload),
        content_type="application/json",
        overwrite=False  # Never overwrite — scoring is idempotent but write-once
    )
    return blob_client.url
```

**Blob write failure handling:** If blob write fails (storage unavailable), do NOT publish `AIScoringCompleted` with a null `aiExplanationRef`. Instead: retry once after 2s; if still failing → publish with `failureReason=SCORING_ERROR` and `aiRecommendation=REFER_TO_UNDERWRITER`. The FCA requires `ai_explanation_ref` to be non-null for every scored application — a missing explainability artefact is a scoring failure, not a recoverable gap.

---

## Environment Variables

| Variable | Description | Example value |
|---|---|---|
| `AZURE_SERVICE_BUS_NAMESPACE` | Service Bus namespace FQDN | `loanplatform-sb.servicebus.windows.net` |
| `AI_SCREENING_TOPIC` | Inbound topic name | `ai-screening-requested` |
| `AI_SCREENING_SUBSCRIPTION` | Subscription name | `ai-scoring-service` |
| `AI_SCORING_COMPLETED_TOPIC` | Outbound topic name | `ai-scoring-completed` |
| `EXPERIAN_API_BASE_URL` | Experian base URL | `https://api.experian.com` |
| `KEY_VAULT_URL` | Azure Key Vault URI | `https://loanplatform-kv.vault.azure.net/` |
| `AZURE_FOUNDRY_ENDPOINT_URL` | Azure Foundry scoring endpoint | `https://loanplatform-scoring.uksouth.inference.ml.azure.com/score` |
| `AZURE_FOUNDRY_ENDPOINT_KEY_SECRET_NAME` | Key Vault secret for Foundry API key | `foundry-scoring-endpoint-key` |
| `AI_EXPLAINABILITY_STORAGE_ACCOUNT` | Blob storage account name | `loanplatformsa` |
| `AI_EXPLAINABILITY_CONTAINER` | Blob container name | `ai-explainability` |
| `LOAN_ORIGINATION_API_BASE_URL` | Internal base URL for idempotency check | `https://loan-api.internal.loanplatform.co.uk` |
| `LOG_LEVEL` | Logging level | `INFO` (never DEBUG in production — risk of PII leak) |
| `MAX_DTI_RATIO_CAP` | DTI winsorization cap | `10.0` |
| `SCORE_THRESHOLD_AUTO_APPROVE` | Recommendation threshold | `700` |
| `SCORE_THRESHOLD_AUTO_DECLINE` | Recommendation threshold | `400` |

**All secrets** (Experian credentials, Foundry API key, PII decryption key) are fetched from Key Vault via managed identity. No secrets in environment variables.

---

## FastAPI Endpoints

The AI Scoring Service exposes the following HTTP endpoints (not for external traffic — internal / Container Apps ingress only):

| Method | Path | Purpose | Response |
|---|---|---|---|
| `GET` | `/health` | Liveness probe — always 200 if process is alive | `{ "status": "ok" }` |
| `GET` | `/ready` | Readiness probe — checks Service Bus consumer, Key Vault, Foundry endpoint | `{ "status": "ready" | "degraded", "checks": {...} }` |
| `GET` | `/metrics` | Prometheus metrics | Prometheus text format |

**Readiness checks:**
- Service Bus consumer connected: call `peek_messages` with count=0 on the subscription
- Key Vault reachable: call `get_secret("ai-scoring-pii-key")` with 3s timeout
- Azure Foundry endpoint reachable: `GET {AZURE_FOUNDRY_ENDPOINT_URL}/` with 3s timeout (200 or 401 = reachable)

**Degraded state:** If any dependency is unreachable, `/ready` returns 503 with `{ "status": "degraded", "unhealthy": ["foundry"] }`. Container Apps will stop routing messages to this instance until it becomes ready.

---

## Acceptance Criteria

### AC-001 — End-to-end successful scoring

```gherkin
Scenario: Application scored successfully with full Experian match
  Given an AIScreeningRequested event arrives for applicationId="APP-001"
    And annualIncomeGbp=45000, loanAmountRequestedGbp=8000, repaymentTermMonths=36, employmentStatus="EMPLOYED_FULL_TIME"
    And Experian returns matchStatus="FULL_MATCH" with creditScoreRaw=780, creditHistoryMonths=84, missedPayments12m=0, missedPayments24m=1, hardSearches6m=2, totalOutstandingDebtGbp=5000, no adverse information
    And Azure Foundry returns repaymentProbability=0.812 with SHAP values for all 14 features
  When the AI Scoring Service processes the event
  Then it publishes AIScoringCompleted with aiRiskScore=812 and aiRecommendation="AUTO_APPROVE"
  And debtToIncomeRatio=0.278 and loanToIncomeRatio=0.178 are included
  And an explainability JSON is written to blob storage at path "APP-001/{correlationId}.json"
  And aiExplanationRef is a non-null URL to that blob
  And the event is acknowledged from the Service Bus subscription
```

### AC-002 — Adverse information triggers AUTO_DECLINE

```gherkin
Scenario: Active bankruptcy causes auto-decline regardless of score
  Given an AIScreeningRequested event arrives for applicationId="APP-002"
    And Experian returns matchStatus="FULL_MATCH" with creditScoreRaw=720 and adverseInformation.bankruptcyActive=true
    And Azure Foundry returns repaymentProbability=0.652
  When the AI Scoring Service processes the event
  Then it publishes AIScoringCompleted with aiRecommendation="AUTO_DECLINE"
  And the explainability JSON declineReasonCategory is "ADVERSE_CREDIT_HISTORY"
  And aiRiskScore is 652
```

### AC-003 — Experian circuit breaker open

```gherkin
Scenario: Experian unavailable routes to underwriter
  Given the Experian circuit breaker is in OPEN state (3 consecutive failures already recorded)
  When an AIScreeningRequested event arrives for applicationId="APP-003"
  Then the service does NOT attempt an Experian HTTP call
  And it publishes AIScoringCompleted with aiRecommendation="REFER_TO_UNDERWRITER" and failureReason="EXPERIAN_UNAVAILABLE"
  And aiRiskScore is null
  And aiExplanationRef is null
  And the event is acknowledged from Service Bus
```

### AC-004 — Explainability artefact is mandatory (FCA)

```gherkin
Scenario: All 14 SHAP feature contributions present in explainability artefact
  Given Experian and Azure Foundry both respond successfully
  When the AI Scoring Service produces the explainability JSON
  Then the featureContributions object contains exactly 14 keys:
    annual_income_gbp, loan_amount_requested_gbp, repayment_term_months,
    employment_status_encoded, credit_score_raw, credit_history_months,
    missed_payments_12m, missed_payments_24m, hard_searches_6m,
    total_outstanding_debt_gbp, debt_to_income_ratio, loan_to_income_ratio,
    adverse_flag, has_experian_match
  And topPositiveFactors contains the 3 features with highest positive SHAP contribution
  And topNegativeFactors contains the 3 features with highest negative SHAP contribution
  And aiExplanationRef in AIScoringCompleted is non-null
```

### AC-005 — Blob write failure escalates to REFER

```gherkin
Scenario: Blob storage unavailable prevents scoring completion
  Given Experian and Azure Foundry respond successfully
  And Azure Blob Storage is unavailable (connection timeout on upload)
  When the AI Scoring Service attempts to write the explainability JSON
  Then it retries once after 2 seconds
  And if the retry also fails it publishes AIScoringCompleted with failureReason="SCORING_ERROR" and aiRecommendation="REFER_TO_UNDERWRITER"
  And aiExplanationRef is null
```

### AC-006 — Idempotency: duplicate event is a no-op

```gherkin
Scenario: Duplicate message for already-scored application is deduplicated
  Given applicationId="APP-001" has already been scored and the Loan Origination API returns scored=true
  When a duplicate AIScreeningRequested event arrives for applicationId="APP-001"
  Then the service acknowledges the message without calling Experian or Azure Foundry
  And no new AIScoringCompleted event is published
  And the scoring.deduplicated counter metric is incremented
```

### AC-007 — SLA compliance (NFR-002)

```gherkin
Scenario: Full scoring pipeline completes within 90 seconds
  Given a valid AIScreeningRequested event arrives at T=0
  And Experian responds within 20 seconds
  And Azure Foundry responds within 10 seconds
  And blob storage write completes within 5 seconds
  When the AI Scoring Service processes the event
  Then AIScoringCompleted is published before T + 90 seconds
```

---

## Test Plan

| Test | Scope | What to assert |
|---|---|---|
| Unit: `map_to_risk_score` | Function | `repaymentProbability=0.812` → `aiRiskScore=812`; `0.0` → `0`; `1.0` → `1000` |
| Unit: `derive_recommendation` | Function | All 5 threshold conditions including `adverse_flag=1` override; `has_experian_match=0` override |
| Unit: `build_feature_vector` | Function | All 14 features populated correctly; DTI and LTI computed from inputs; employment_status_encoded mapping |
| Unit: `declineReasonCategory` derivation | Function | Each reason code selected for correct adverse/SHAP condition |
| Unit: PII decryption | Function (with mock Key Vault) | Ciphertext correctly decrypted; plaintext not logged |
| Integration: Experian call | Service + mock Experian | All INT-001 error cases (401, 404, 429, 503, timeout) produce correct `failureReason` |
| Integration: Azure Foundry call | Service + mock endpoint | All error cases produce `REFER_TO_UNDERWRITER`; circuit breaker opens after 3 failures |
| Integration: Blob write | Service + Azure Storage emulator (Azurite) | JSON written to correct path; `overwrite=False` raises on duplicate |
| Integration: Idempotency check | Service + mock Loan Origination API | Already-scored application → early return; Experian and Foundry NOT called |
| Integration: Service Bus consumer | Service + Service Bus emulator | Message acknowledged on success; dead-lettered after 3 processing failures |
| API: `/health` | FastAPI test client | Always 200; no external calls |
| API: `/ready` | FastAPI test client + mock dependencies | 200 when all healthy; 503 with `unhealthy` list when any dependency down |
| E2E: Full pipeline | Staging environment | `AIScreeningRequested` published → `AIScoringCompleted` received within 90s; blob exists; Loan Origination API state transitions correctly |
| E2E: Experian unavailable | Staging with Experian mocked as 503 | `AIScoringCompleted.aiRecommendation = REFER_TO_UNDERWRITER`; circuit breaker opens; subsequent calls skip Experian |

**CI gate requirements:**
- Unit test coverage ≥ 80% of service module
- Integration tests run against Azure Service Bus (Standard tier) and Azurite emulator
- E2E tests run in staging environment only (not in PR CI)
- PII scan: no test fixture or log file may contain real NI numbers, names, or DOBs — use synthetic data (`AB123456C`, `John Test`, `1990-01-01`)

---

## Open Questions

| ID | Question | Owner | Needed before | Status |
|---|---|---|---|---|
| AIQ-001 | What are the approved recommendation thresholds (ai_risk_score ≥ 700 = AUTO_APPROVE, < 400 = AUTO_DECLINE)? These are provisional — Head of Retail Lending must confirm before production deployment | Head of Retail Lending | Production go-live | Open |
| AIQ-002 | Which specific Azure AI Foundry model type is approved? (LightGBM / XGBoost / other?) Model must support SHAP value computation | Head of AI | Model training sprint | Open |
| AIQ-003 | Is NIN-based matching confirmed available in the Experian enterprise contract (see IQ-003 in experian-integration.md)? If not, FR-001 must be extended to collect applicant address | IT Architecture | Sprint 1 | Open |
| AIQ-004 | What is the approved AES-256 key rotation procedure for the `ai-scoring-pii-key` shared between Loan Origination API and AI Scoring Service? | IT Architecture / Security | Sprint 1 | Open |
