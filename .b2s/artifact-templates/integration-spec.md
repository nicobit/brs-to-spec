# {{External System Name}} — Integration Specification

## Metadata

| **Field** | **Value** |
|---|---|
| **Status** | **In progress** |
| Integration ID | {{integration_id, e.g. INT-001}} |
| Initiative ID | {{initiative_id}} |
| External system | {{system name}} |
| Direction | {{consumed / exposed / bidirectional}} |
| Enterprise contract | {{Yes — ref ARCH-C-NNN / No}} |
| Created at | {{date}} |
| Created by | engineering-lead |

## Purpose

{{What this integration does, why it exists, and which stories depend on it.}}

## Traceability

| Source | Reference | Description |
|---|---|---|
| BRS | FR-NNN | {{requirement that mandates this integration}} |
| Architecture | ARCH-C-NNN | {{constraint on reliability, auth, or fallback}} |
| Consumed API spec | {{consumed-api-spec filename}} | {{link to the companion consumed-api-spec if consumed direction}} |

## Dependent Stories

| Story ref | Dependency type | Impact if unavailable |
|---|---|---|
| {{FR-NNN or S-NNN.N}} | {{blocking / optional}} | {{describe}} |

## Connection Details

| Field | Value |
|---|---|
| Protocol | {{HTTPS / AMQP / SFTP / gRPC}} |
| Base URL env var | {{VAR_NAME — never hardcode values}} |
| Auth mechanism | {{OAuth2 client credentials / API key / mTLS / SAML}} |
| Credential storage | {{Azure Key Vault / AWS Secrets Manager}} |
| TLS minimum version | {{TLS 1.2 / TLS 1.3}} |

## Reliability Contract

| Behaviour | Specification | Source |
|---|---|---|
| Timeout per call (ms) | {{ms}} | {{BRS §N / architecture constraint / recommended default}} |
| Max retries | {{N}} | {{same}} |
| Retry backoff | {{exponential / fixed — intervals}} | {{same}} |
| Circuit breaker threshold | {{N failures in M seconds}} | {{same}} |
| Fallback behaviour | {{refer-to-underwriter / degrade gracefully / hard fail / queue}} | {{same}} |

## Failure Modes

| Failure | Detection | Response | Alert? |
|---|---|---|---|
| Timeout | HTTP / socket timeout | {{retry → fallback}} | {{Yes — threshold}} |
| 5xx error | HTTP status code | {{retry → fallback}} | {{Yes — threshold}} |
| Auth failure | 401 / 403 | {{stop, alert ops}} | Yes |
| Rate limit | 429 | {{backoff, queue}} | Yes |
| Unavailable | Connection refused | {{circuit breaker → fallback}} | Yes |

## Observability

| Signal | Name | Condition |
|---|---|---|
| Success event | {{EVENT_NAME}} | {{when emitted}} |
| Failure event | {{EVENT_NAME}} | {{when emitted}} |
| Latency metric | {{metric_name}} | {{always}} |
| Alert threshold | {{condition}} | {{ops response}} |

## Compliance Notes

{{Regulatory or contractual constraints: PII minimisation, data residency, audit requirements, enterprise contract terms.
Reference architecture constraints explicitly (e.g. ARCH-C-001, ARCH-C-003).}}

## Open Questions

| # | Question | Owner | Needed before | Status |
|---|---|---|---|---|
| 1 | {{question}} | {{owner}} | {{milestone}} | Open |

---
*Status: In progress — set to Accepted only after integration test in staging. Never self-accept.*
