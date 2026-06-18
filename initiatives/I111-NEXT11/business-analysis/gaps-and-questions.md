# Gaps and Questions

## Summary

This artifact captures gaps in the current specification and clarifying questions that should be answered by the product owner, compliance, or architecture teams.

## Gaps

| ID | Gap | Notes |
|---|---|---|
| GAP-001 | Initiative ID mismatch between `input/brs.md` and workspace | BRS shows `I005` while workspace is `I111-NEXT11` — fix traceability |
| GAP-002 | Experian integration SLA and error codes not enumerated | Need retry/backoff and circuit-breaker thresholds |
| GAP-003 | AML provider endpoints and response schemas missing | Compliance to provide API contracts |
| GAP-004 | DocuSign webhook and signature proof retention unspecified | Need callback contracts and retention policy |
| GAP-005 | Temenos T24 disbursement API contract missing | Architecture to supply API and reconciliation expectations |
| GAP-006 | AI explainability schema not defined | Define allowed explanation fields and disclosure policy |

## Questions

| ID | Question | Owner | Priority |
|---|---|---|---|
| Q-001 | Confirm Initiative ID to use in all artifacts (I005 vs I111-NEXT11) | Head of Retail Lending | High |
| Q-002 | Exact SLA and fallback behaviour for Experian failures | Integrations | High |
| Q-003 | Which AML/KYC providers are approved and their API constraints? | Compliance | High |
| Q-004 | Should underwriter decisions be shared with customers or only internal codes? | Legal/Product | Medium |
| Q-005 | Additional business rules for auto-approve under £10k (LTV/DTI)? | Risk | High |
| Q-006 | Retention and tamper-evidence approach for AuditLog | Security | High |

## Suggested Next Steps

1. Fix Initiative ID in `input/brs.md` or add mapping metadata in the workspace to preserve auditability.
2. Provide API contracts for Experian, HMRC KYC, DocuSign, and Temenos T24 to allow engineering to design connectors.
3. Legal and Compliance to confirm what explanation granularity is permitted to be shown to customers for AI decisions.
