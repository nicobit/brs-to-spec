# API Contract Quality Gate

> Gate owner: Integration
> Triggered: Yes — governed external boundaries (IDP B, Payment Provider A, Onboarding API)

## Scope

- Onboarding API surface (`POST /onboarding`, status endpoints)
- Identity Provider B integration (async webhook/callback)
- Payment Provider A integration (synchronous validation)

## Checklist

- [ ] Contract documents present in `input/contracts/` with endpoints, schemas, and example payloads
- [ ] Authentication method documented for each integration (API key, OAuth, mTLS)
- [ ] IDP webhook: signature verification, replay protection, and error semantics documented
- [ ] Error codes and retry/backoff strategy documented for each integration
- [ ] SLA and rate limits documented or vendor doc referenced
- [ ] PII fields transmitted and residency controls noted per integration
- [ ] Staging sandbox credentials and test endpoints available
- [ ] Acceptance tests defined covering happy path, failure modes, and rate limit handling

## Contract artifacts

- `input/contracts/identity-provider-b-contract.md` — async verification, HMAC-SHA256 confirmed, Italy residency noted
- `input/contracts/identity-provider-b-api.md` — request/response schemas and example payloads
- `input/contracts/payment-provider-a-contract.md` — synchronous validation endpoints, PCI/tokenization guidance
- `input/contracts/payment-provider-a-api.md` — request/response schemas and example payloads

## Acceptance

Status: `Accepted`
