# Architecture & Contract Artifact Decision

## 1. Summary

The onboarding feature has API, data, audit/event, authorization, and workflow aspects.

## 2. Artifact Decision Matrix

| Artifact | Needed? | Reason | Owner | Mandatory before implementation? |
|---|---|---|---|---|
| Architecture decisions / ADRs | Yes | Need to decide status workflow approach | Architect | Yes |
| API contract | Yes | Backend endpoints are required | Backend Lead | Yes |
| OpenAPI contract | Partial | Useful for frontend/backend contract-first work | Backend Lead | No |
| Domain model / DDD | Yes, lightweight | Status transitions and approval decisions need clarity | Tech Lead | Yes |
| Data model | Yes | New onboarding request persistence is needed | DB Lead | Yes |
| Event contracts | Yes | Audit event payload must be clarified | Tech Lead | Yes |
| Quality attribute scenarios | No | No special NFR beyond standard platform NFRs | Architect | No |
| Threat model | Yes, lightweight | Authorization and audit are involved | Security Expert | Yes |
