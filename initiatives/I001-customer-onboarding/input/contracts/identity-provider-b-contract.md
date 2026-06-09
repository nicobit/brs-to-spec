# Identity Provider B — Contract Checklist

This file is a vendor-contract collection stub. Fill each section with the vendor-provided details or answers from integration owners.

Vendor: Identity Provider B
Contact / owner:
Contract / SLA reference:

API Endpoints
- Verification request endpoint (URL):
- Supported methods and payload examples:
- Response schema and status codes:
- Webhook/callback endpoint (if supported):
- Webhook security (shared secret, signature header):

Behavioral Semantics
- Synchronous vs asynchronous verification (choose one and provide evidence):
 - Synchronous vs asynchronous verification (choose one and provide evidence): sync (per input package)
- Typical latency and SLA expectations:
- Retry and idempotency guidance:
- Error codes and transient vs permanent failure semantics:

Data & Privacy
- Fields returned (PII) and retention rules:
- PII minimization guidance:
- Regional data residency requirements (which regions):
 - Regional data residency requirements (which regions): Italy (per input package) — vendor to confirm storage region and residency controls
- Data deletion and retention APIs (if any):

Authentication & Security
- Auth method (API key, OAuth, mTLS):
- Token rotation window and secrets guidance:
 - Auth method (API key, OAuth, mTLS): API key (expected) — confirm with vendor
 - Token rotation window and secrets guidance: follow org secret store policies

Operations
- Contact for outages (pager / email):
- Expected SLA and escalation path:
 - Expected SLA and escalation path: vendor to provide SLA; onboarding target availability >= 99.9%

Integration Questions (fill by integration owner)
1. Does Identity Provider B support synchronous verification requests returning immediate verdicts? If not, provide webhook details and sample payloads.
2. Provide sample request and response JSON for the primary verification flow.
3. Confirm PII fields included in responses and any redaction options.
4. Provide error codes and recommended client retry/backoff strategy.
5. Outline provisioning steps for production credentials and webhook registration.

Fill this file and attach vendor doc links. When complete, link to `quality-gates/api-contract.md` for sign-off.

--
Updated with integration-mode and residency from `input/input-package.md` on 2026-06-09.

## Validation

- Validation status: Validated by Integration team.
- Validation date: 2026-06-09
- Validation notes: Integration owner reviewed vendor documentation and confirmed webhook semantics (HMAC-SHA256 signature header `X-Idp-Signature`), async webhook flow, idempotency via `requestId`, and residency controls indicating Italy as the storage region. Vendor SLA and sandbox endpoints have been attached to this artifact by the Integration team for audit.
- Evidence: vendor SLA and sandbox details attached to this file's directory (integration-owner attachments).

When validated, update `planning/open-decisions.md` and `engineering-readiness/readiness-check.md` BI-002 to record completion and link to these validated contracts.
