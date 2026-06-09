# API Spec — {{Deliverable ID}}: {{Deliverable Name}}

> Distilled from `quality-gates/api-contract.md` for this increment only.
> Full contract (auth details, sandbox credentials, SLA, rate limits) is in the source gate artifact.

## Endpoints

### {{METHOD}} {{/path}}

**Purpose:** <!-- what this endpoint does -->
**Auth:** <!-- API key / OAuth / mTLS / none -->
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

**Idempotency:** <!-- how duplicate calls are handled -->
**PII transmitted:** <!-- fields and classification -->

---

## Webhook / callback endpoints

### {{METHOD}} {{/webhook/path}}

**Purpose:**
**Auth / signature verification:** <!-- HMAC-SHA256 / none -->
**Idempotency key:** <!-- field name -->
**Replay protection:** <!-- how implemented -->

Expected payload:
```json
{
}
```

Error handling:
<!-- What happens on signature failure, duplicate delivery, timeout -->

---

## Integration contracts (external)

| Integration | Protocol | Sandbox endpoint | Auth | Contract artifact |
|---|---|---|---|---|

<!-- Do not paste credentials here. Reference the contract artifact path. -->
