# API Spec — {{F-XXX.X}}: {{User Story Name}}

> Distilled from `quality-gates/api-contract.md` for this user story only.
> Only endpoints created or modified by this story appear here.
> Full contract (sandbox credentials, SLA, rate limits) is in `quality-gates/api-contract.md`.
> Delete this file if this story has no API changes.

## {{METHOD}} {{/path}}

**Purpose:** <!-- what this endpoint does for this story specifically -->
**Auth:** <!-- API key / OAuth / mTLS -->
**Consumer:** <!-- who calls this -->

Request:
```json
{
}
```

Response — success:
```json
{
}
```

Response — errors:

| HTTP status | Code | Meaning | Retry? |
|---|---|---|---|

**Idempotency:** <!-- how duplicate calls are handled, or "not required" -->
**PII transmitted:** <!-- fields and classification, or "none" -->
**Audit:** <!-- what gets written to audit_logs, or "none" -->

---

## Integration contracts (if this story makes outbound calls)

| Integration | Protocol | Auth | Sandbox endpoint | Contract artifact |
|---|---|---|---|---|

<!-- Do not paste credentials. Reference the contract artifact path. -->
