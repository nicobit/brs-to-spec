# Prompt 02 — Artifact Templates for Technical Specifications

## Context

You are working on the `.b2s` framework at the root of this repository.

The `technical-specifications/` folder was introduced in prompt 01.
This prompt creates four artifact templates — one per specification type.
Templates define the output shape contract that skills must produce.

Read `.b2s/artifact-templates/api-contract.md` and `.b2s/artifact-templates/story-package.md`
to understand the existing template style before writing these.

---

## Template 1 — Exposed API Specification

Create `.b2s/artifact-templates/exposed-api-spec.md`:

```markdown
# {{API Name}} — Exposed API Specification

## Metadata

| Field | Value |
|---|---|
| API ID | {{api_id}} |
| Initiative ID | {{initiative_id}} |
| Contract mode | {{product / internal / coordinated}} |
| Version | {{semver}} |
| Owner | {{team or role}} |
| Status | Draft |
| Created at | {{date}} |

## Purpose

{{One paragraph: what this API does, who consumes it, and why it exists.}}

## Consumer Context

| Consumer | Type | Dependency level |
|---|---|---|
| {{consumer name}} | {{internal / external}} | {{blocking / non-blocking}} |

## Endpoint Catalog

| Method | Path | Purpose | Story ref |
|---|---|---|---|
| {{METHOD}} | {{/v1/path}} | {{one line}} | {{F-NNN.N}} |

## Endpoint Definitions

For each endpoint in the catalog:

### {{METHOD}} {{/v1/path}}

**Request**

| Field | Type | Required | Validation |
|---|---|---|---|
| {{field}} | {{type}} | {{yes/no}} | {{rule}} |

**Response — {{HTTP status}}**

| Field | Type | Description |
|---|---|---|
| {{field}} | {{type}} | {{description}} |

**Error responses**

| Status | Code | Condition |
|---|---|---|
| 422 | VALIDATION_ERROR | {{when}} |
| 404 | NOT_FOUND | {{when}} |

## Authentication and Authorisation

- Auth mechanism: {{OAuth2 / API key / mTLS}}
- Required scope: {{scope name}}
- Role restrictions: {{which roles may call this endpoint}}

## Versioning Policy

- Strategy: {{semver / date-based}}
- Breaking change process: {{describe}}
- Deprecation notice period: {{N weeks/months}}

## SLAs

| Endpoint | P50 | P99 | Timeout |
|---|---|---|---|
| {{path}} | {{ms}} | {{ms}} | {{ms}} |

## Contract Tests

- Test framework: {{Pact / other}}
- CI enforcement: {{yes/no}}
- Provider verification: {{how}}

## Open Questions

| # | Question | Owner | Status |
|---|---|---|---|
| 1 | {{question}} | {{owner}} | Open |

---
*Status: Draft — set to Accepted only after architecture review sign-off.*
```

---

## Template 2 — Consumed API Specification

Create `.b2s/artifact-templates/consumed-api-spec.md`:

```markdown
# {{External System Name}} — Consumed API Specification

## Metadata

| Field | Value |
|---|---|
| External system | {{system name}} |
| Initiative ID | {{initiative_id}} |
| Provider | {{company / team}} |
| Contract source | {{URL or document reference}} |
| Status | Draft |
| Created at | {{date}} |

## Purpose

{{Why this initiative consumes this API. What data or capability it provides.}}

## Endpoints Used

| Method | Path | Purpose | Story ref |
|---|---|---|---|
| {{METHOD}} | {{/path}} | {{one line}} | {{F-NNN.N}} |

## Authentication

- Auth mechanism: {{OAuth2 client credentials / API key / mTLS}}
- Credential storage: {{where credentials are stored — secret manager, env var}}
- Token refresh: {{how tokens are refreshed}}

## Data Received

| Field | Type | Used for | PII? |
|---|---|---|---|
| {{field}} | {{type}} | {{purpose}} | {{yes/no}} |

## PII and Data Residency

- PII fields received: {{list}}
- Storage location: {{UK Azure / not stored}}
- Masking/pseudonymisation: {{required / not required}}

## Integration Behaviour

- Timeout per request: {{ms}}
- Retry policy: {{N retries, backoff strategy}}
- Fallback on failure: {{refer-to-underwriter / degrade gracefully / hard fail}}
- Circuit breaker: {{yes/no}}

## SLAs (Provider Commitments)

| Metric | Value | Source |
|---|---|---|
| Availability | {{%}} | {{SLA document}} |
| P99 response time | {{ms}} | {{SLA document}} |
| Rate limit | {{requests/second}} | {{SLA document}} |

## Known Risks

| Risk | Impact | Mitigation |
|---|---|---|
| {{risk}} | {{impact}} | {{mitigation}} |

---
*Status: Draft — validate against provider documentation before handoff.*
```

---

## Template 3 — Database Schema Specification

Create `.b2s/artifact-templates/database-schema-spec.md`:

```markdown
# {{Schema / Domain Name}} — Database Schema Specification

## Metadata

| Field | Value |
|---|---|
| Schema ID | {{schema_id}} |
| Initiative ID | {{initiative_id}} |
| Database | {{PostgreSQL / other}} |
| Owner | {{team or role}} |
| Shared across teams | {{yes/no}} |
| Status | Draft |
| Created at | {{date}} |

## Purpose

{{What domain this schema covers and which stories produce or consume it.}}

## Tables

For each table:

### {{table_name}}

{{One line: what this table stores.}}

| Column | Type | Nullable | Default | Constraints | Description |
|---|---|---|---|---|---|
| id | uuid | no | gen_random_uuid() | PK | Primary key |
| {{column}} | {{type}} | {{yes/no}} | {{default}} | {{UK, FK, CHECK}} | {{description}} |

**Indexes**

| Name | Columns | Type | Rationale |
|---|---|---|---|
| {{idx_name}} | {{columns}} | {{btree/hash}} | {{why}} |

**Foreign keys**

| Column | References | On delete |
|---|---|---|
| {{column}} | {{table.column}} | {{CASCADE/RESTRICT}} |

## Enumerations

| Enum name | Values | Used in |
|---|---|---|
| {{enum}} | {{value1, value2}} | {{table.column}} |

## Migration Strategy

- Approach: {{additive only / blue-green / feature flag}}
- Rollback plan: {{describe}}
- Staging verification: {{how migrations are verified before prod}}

## Data Residency and PII

| Column | PII? | Masking in non-prod | Retention |
|---|---|---|---|
| {{column}} | {{yes/no}} | {{masked/pseudonymised/clear}} | {{period}} |

## Shared Schema Notes

{{If shared across teams: who else reads/writes this table, coordination process for schema changes.}}

---
*Status: Draft — set to Accepted only after data architecture review.*
```

---

## Template 4 — Integration Specification

Create `.b2s/artifact-templates/integration-spec.md`:

```markdown
# {{External System Name}} — Integration Specification

## Metadata

| Field | Value |
|---|---|
| Integration ID | {{integration_id}} |
| Initiative ID | {{initiative_id}} |
| External system | {{system name}} |
| Integration direction | {{consumed / exposed / bidirectional}} |
| Enterprise contract | {{yes/no — ref ARCH-C-NNN if applicable}} |
| Status | Draft |
| Created at | {{date}} |

## Overview

{{What this integration does, why it exists, and which stories depend on it.}}

## Dependent Stories

| Story ID | Dependency type |
|---|---|
| {{F-NNN.N}} | {{blocking / optional}} |

## Connection Details

- Protocol: {{HTTPS / AMQP / SFTP}}
- Base URL: {{env-var name — never hardcode}}
- Auth: {{OAuth2 client credentials / API key / mTLS / SAML}}
- Credential storage: {{Azure Key Vault / AWS Secrets Manager}}

## Reliability Contract

| Behaviour | Specification |
|---|---|
| Timeout per call | {{ms}} |
| Max retries | {{N}} |
| Retry backoff | {{exponential / fixed — intervals}} |
| Circuit breaker threshold | {{N failures in M seconds}} |
| Fallback behaviour | {{refer-to-underwriter / degrade / hard fail}} |

## Failure Modes and Responses

| Failure | Detection | Response | Alert? |
|---|---|---|---|
| Timeout | HTTP timeout | Retry → fallback | Yes if > threshold |
| 5xx error | HTTP status | Retry → fallback | Yes if > threshold |
| Auth failure | 401/403 | Stop, alert ops | Yes |
| Rate limit | 429 | Backoff, queue | Yes |

## Observability

- Success event: {{event name emitted on success}}
- Failure event: {{event name emitted on failure}}
- Latency metric: {{metric name}}
- Alert threshold: {{condition}}

## Compliance Notes

{{Any regulatory or contractual constraints on this integration — PII minimisation, data residency, audit requirements.}}

---
*Status: Draft — set to Accepted only after integration test in staging.*
```

---

## Done criteria

- [ ] `.b2s/artifact-templates/exposed-api-spec.md` created with all sections
- [ ] `.b2s/artifact-templates/consumed-api-spec.md` created with all sections
- [ ] `.b2s/artifact-templates/database-schema-spec.md` created with all sections
- [ ] `.b2s/artifact-templates/integration-spec.md` created with all sections
- [ ] All four templates follow the placeholder convention `{{field}}` consistently
- [ ] All existing tests pass
