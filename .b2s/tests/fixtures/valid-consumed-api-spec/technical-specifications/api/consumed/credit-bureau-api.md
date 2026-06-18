# Credit Bureau API — Consumed API Specification

## Metadata

| **Field** | **Value** |
|---|---|
| Status | In progress |
| Provider | CreditBureau Inc. |
| Initiative ID | I001-loan-origination |
| Created at | 2026-06-17 |
| Created by | engineering-lead |

## Purpose

Called during loan application assessment to retrieve credit score and derogatory
history. Used in the underwriting decision step.

## Endpoint Catalog

| ID | Method | Path | Purpose | Story ref |
|---|---|---|---|---|
| EP-001 | POST | /v2/credit-check | Retrieve credit score and history | F-002.1 |

## Endpoint Definitions

### EP-001: POST /v2/credit-check

**Purpose:** Retrieve applicant credit score and derogatory history
**Authentication:** OAuth2 client credentials (our system as client)
**Authorization:** scope: credit.read
**Story ref:** F-002.1

**Request:**

| Field | Type | Required | Notes |
|---|---|---|---|
| applicant_nid | string | Yes | 11 digits |
| consent_ref | string | Yes | Proof of applicant consent |

**Response:**

| Field | Type | Description |
|---|---|---|
| score | integer | Credit score 300–850 |
| risk_band | string | Credit risk classification: LOW, MEDIUM, or HIGH |
| derogatory_count | integer | Number of derogatory marks |

**Error responses:**

| HTTP Status | Code | Condition |
|---|---|---|
| 400 | VALIDATION_ERROR | Missing field |
| 503 | SERVICE_UNAVAILABLE | Bureau unreachable |

## Authentication and Authorisation

| Field | Value |
|---|---|
| Auth mechanism | OAuth2 client credentials |
| Required scope | credit.read |
| Token endpoint | https://auth.creditbureau.example.com/oauth/token |
| Token lifetime | 3600 |

## Reliability

| Field | Value |
|---|---|
| Timeout per request | 8000 ms |
| Max retries | 2 |
| Retry strategy | exponential backoff |
| Fallback behaviour | refer-to-underwriter |
| Circuit breaker | Yes — trip after 5 failures in 60 s |

## PII and Data Residency

| Field | Classification | Retention | Notes |
|---|---|---|---|
| applicant_nid | PII | Not stored — pass-through only | Must not be logged |
| score | Sensitive | 7 years | Stored encrypted |

All fields must remain within EU jurisdiction. Bureau is EU-based.

## Open Questions

| # | Question | Owner | Status |
|---|---|---|---|

---
*Status: In progress — set to Accepted only after integration test in staging. Never self-accept.*
