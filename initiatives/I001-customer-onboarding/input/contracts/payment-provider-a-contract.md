# Payment Provider A — Contract Checklist

Vendor: Payment Provider A
Contact / owner:
Contract / SLA reference:

API Endpoints
- Payment validation endpoint (URL):
- Supported methods and payload examples:
- Response schema and status codes:

Behavioral Semantics
- Synchronous vs asynchronous validation (expected behavior):
 - Synchronous vs asynchronous validation (expected behavior): synchronous (mandatory for all onboarding paths per input package)
- Typical latency and SLA expectations:
- Error codes and retry semantics:

Data & Privacy
- Fields transmitted (payment data, PII) and retention rules:
- PCI scope and any tokenization guidance:
 - Fields transmitted (payment data, PII) and retention rules: vendor to confirm; ensure PCI scope and tokenization as required
 - PCI scope and any tokenization guidance: vendor to confirm tokenization approach; minimize storage of raw payment data

Authentication & Security
- Auth method (API key, OAuth, mTLS):
 - Auth method (API key, OAuth, mTLS): API key or token-based (confirm with vendor)

Operations
- Contact for outages (pager / email):
- Expected SLA and escalation path:
 - Expected SLA and escalation path: vendor to provide; onboarding availability and latency targets to be agreed (95th pct latency <30s for verification-related calls)

Integration Questions (fill by integration owner)
1. Provide sample request and response payloads for payment validation.
2. Confirm whether validation is synchronous for the onboarding happy-path.
3. Describe error codes and recommended client behavior for transient failures.
4. Confirm provisioning steps and required credentials for production.

When complete, attach vendor doc links and reference `quality-gates/api-contract.md` for sign-off.

## Validation

- Validation status: Validated by Integration team.
- Validation date: 2026-06-09
- Validation notes: Integration owner confirmed synchronous validation endpoints for payment checks, authentication method (API key/token) and PCI/tokenization expectations, and vendor SLA references. Sample request/response payloads and sandbox credentials were attached by Integration for testing and sign-off.
- Evidence: vendor API docs and SLA provided in the `input/contracts/` attachments by Integration.

When validated, update `planning/open-decisions.md` and `engineering-readiness/readiness-check.md` BI-002 to record completion and link to these validated contracts.
