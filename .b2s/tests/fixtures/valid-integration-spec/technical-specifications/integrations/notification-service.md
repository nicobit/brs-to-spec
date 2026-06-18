# Notification Service — Integration Specification

## Metadata

| **Field** | **Value** |
|---|---|
| Integration ID | INT-001 |
| Initiative ID | I001-loan-origination |
| Direction | Outbound |
| Created at | 2026-06-17 |
| Created by | engineering-lead |
| Status | In progress |

## Purpose

Sends email and SMS notifications to applicants when application status changes.
Used by the origination service after each state transition.

## Connection Details

| Field | Value |
|---|---|
| Protocol | HTTPS REST |
| Base URL env var | NOTIFICATION_SERVICE_BASE_URL |
| Auth mechanism | API key (header X-API-Key) |
| Credential storage | AWS Secrets Manager — secret: notification-service/api-key |
| TLS | Required — TLS 1.2 minimum |

## Reliability Contract

| Field | Value |
|---|---|
| Timeout per request | 3000 ms |
| Max retries | 3 |
| Retry strategy | exponential backoff (base 500 ms, max 5000 ms) |
| Circuit breaker | Yes — trip after 5 failures in 30 s, half-open after 60 s |
| Fallback behaviour | degrade gracefully — queue notification for retry, do not block application state transition |

## Observability

| Field | Value |
|---|---|
| Success event | notification.sent |
| Failure event | notification.failed |
| Latency metric | notification_service.request.duration_ms |
| Alert threshold | p99 > 2000 ms for 5 consecutive minutes |

## Open Questions

| # | Question | Owner | Status |
|---|---|---|---|

---
*Status: In progress — set to Accepted only after integration test in staging. Never self-accept.*
