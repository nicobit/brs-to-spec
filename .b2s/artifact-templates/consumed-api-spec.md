# {{External System Name}} — Consumed API Specification

## Metadata

| **Field** | **Value** |
|---|---|
| **Status** | **In progress** |
| External system | {{system name, e.g. Experian CreditExpert}} |
| Initiative ID | {{initiative_id}} |
| Provider | {{company / team}} |
| Contract source | {{URL or document reference — or "unknown, see OQ-001"}} |
| Created at | {{date}} |
| Created by | engineering-lead |

## Purpose

{{Why this initiative consumes this API. What capability or data it provides. Which FRs depend on it.}}

## Traceability

| Source | Reference | Description |
|---|---|---|
| BRS | FR-NNN | {{requirement that mandates this integration}} |
| Architecture | ARCH-C-NNN | {{constraint on integration pattern, SLA, or fallback}} |
| Business rule | BR-NNN | {{rule applied to data received from this system}} |

## Endpoints Used

| Method | Path | Purpose | FR ref | PII transmitted? |
|---|---|---|---|---|
| {{METHOD}} | {{/path}} | {{one line}} | FR-NNN | {{Yes / No}} |

## Authentication

| Field | Value |
|---|---|
| Auth mechanism | {{OAuth2 client credentials / API key / mTLS / SAML}} |
| Credential storage | {{Azure Key Vault / AWS Secrets Manager / env var name}} |
| Token refresh | {{how and when tokens are refreshed}} |
| Credential owner | {{who provisions and rotates credentials}} |

## Data Received

| Field | Type | Used for | PII? | PII type | Stored? |
|---|---|---|---|---|---|
| {{field}} | {{type}} | {{purpose}} | {{Yes / No}} | {{name / DOB / financial / identity}} | {{Yes / No}} |

## PII and Data Residency

| PII field | Storage location | Masking in non-prod | Retention | Deletion trigger |
|---|---|---|---|---|
| {{field}} | {{UK Azure / not stored}} | {{masked / pseudonymised / clear}} | {{period}} | {{event or policy}} |

## Integration Behaviour

| Behaviour | Specification | Source |
|---|---|---|
| Timeout per request | {{ms}} | {{BRS §N / architecture constraint / open question}} |
| Max retries | {{N}} | {{same}} |
| Retry backoff | {{exponential / fixed — intervals}} | {{same}} |
| Circuit breaker | {{Yes / No — threshold}} | {{same}} |
| Fallback on failure | {{refer-to-underwriter / degrade gracefully / hard fail}} | {{same}} |

## SLAs (Provider Commitments)

| Metric | Value | Source |
|---|---|---|
| Availability | {{%}} | {{SLA document or open question}} |
| P99 response time | {{ms}} | {{SLA document or open question}} |
| Rate limit | {{requests / second}} | {{SLA document or open question}} |

## Known Risks

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|
| {{risk}} | {{impact}} | {{mitigation}} | {{owner}} |

## Open Questions

| # | Question | Owner | Needed before | Status |
|---|---|---|---|---|
| 1 | {{question}} | {{owner}} | {{milestone}} | Open |

---
*Status: In progress — validate against provider documentation before handoff. Never self-accept.*
