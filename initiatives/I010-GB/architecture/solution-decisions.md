# Solution Decisions

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I010-GB |
| Created at | 2026-06-28 |
| Created by | architect |
| Status | Draft |

---

## Decision Summary

| Metric | Value |
|---|---|
| Total decisions | 16 |
| Create new | 11 |
| Modify existing | 3 |
| Extend existing | 1 |
| Reuse as-is | 1 |
| New repositories | 11 |
| Flagged conflicts | 0 |

---

## Service Decisions

| ID | Component | Decision | Target Repository | Technology | Rationale | AR Constraints |
|---|---|---|---|---|---|---|
| SD-001 | Web frontend (applicant portal) | modify-existing | needs-clarification (web-frontend) | ui | Extend form flow, add status & offer pages; integrate with Intake API and DocuSign callback | AR-001 (PII) |
| SD-002 | Email subsystem | modify-existing | needs-clarification (email-subsystem) | messaging | Use existing email subsystem for confirmations and notifications; ensure SLA/retries | - |
| SD-003 | Intake API | create-new | repo-intake-api (proposed) / needs-clarification | api | Centralised submission intake, validation, ARN assignment, status endpoint | AR-001, AR-F01 |
| SD-004 | ARN service | create-new | repo-arn-service (proposed) / needs-clarification | service | Canonical ARN generation and registry to guarantee uniqueness and audit trail | AR-001 |
| SD-005 | Scoring pipeline | create-new | repo-scoring-pipeline (proposed) / needs-clarification | service/pipeline | Host models, generate score and recommendation, emit explainability artifacts | AR-005 |
| SD-006 | Explainability service | create-new | repo-explainability-service (proposed) / needs-clarification | service | Persist model rationale and feature contributions for FCA/regulatory review | AR-005 |
| SD-007 | AML/KYC orchestration | create-new | repo-aml-orchestration (proposed) / needs-clarification | service | Coordinate AML/KYC checks and HMRC identity verification before offers | AR-002, AR-005 |
| SD-008 | Underwriter dashboard | create-new | repo-underwriter-dashboard (proposed) / needs-clarification | ui/api | Aggregate scoring, Experian, AML, and explainability artifacts for reviewer workflows | AR-005 |
| SD-009 | Disbursement orchestration | create-new | repo-disbursement-orch (proposed) / needs-clarification | service | Orchestrate disbursement to Temenos T24 with idempotency and retry semantics | AR-004 |
| SD-010 | Immutable audit store | create-new | repo-immutable-audit (proposed) / needs-clarification | storage | Tamper-evident append-only store for audit of decisions, explainability, and underwriter actions | AR-005, AR-F01 |
| SD-011 | Experian adapter | create-new | repo-experian-adapter (proposed) / needs-clarification | integration | Implement adapter and circuit-breaker for Experian CreditExpert; fallback to underwriter | AR-002 |
| SD-012 | HMRC connector | create-new | repo-hmrc-adapter (proposed) / needs-clarification | integration | Connector for identity verification used by AML/KYC orchestration | AR-002 |
| SD-013 | DocuSign integration | reuse-as-is | external-DocuSign (partner) | external | Use existing DocuSign contract; implement callback handling in Intake/Offer flows | AR-003 |
| SD-014 | Temenos T24 adapter | create-new | repo-t24-adapter (proposed) / needs-clarification | integration/adapter | Adapter to map disbursement instructions to T24 with idempotency | AR-004 |
| SD-015 | Admin dashboard / metrics pipelines | modify-existing | needs-clarification (admin-dashboard/metrics) | ui / pipeline | Extend metric pipelines and admin views to show operational metrics and SLA dashboards | - |
| SD-016 | Event bus / logging (observability) | extend-existing | platform-event-bus (existing) / needs-clarification | stream | Extend existing event bus for structured telemetry from scoring and orchestration | - |

---

## API Decisions

| ID | API / Endpoint | Decision | Target Service | Protocol | Versioning | Rationale |
|---|---|---|---|---|---|---|
| SD-017 | /api/intake/submit (Intake API) | create-new | Intake API | REST | v1 | Central submission endpoint; validate and return ARN |
| SD-018 | /api/intake/status | create-new | Intake API | REST | v1 | Status retrieval by ARN+DOB for public portal |
| SD-019 | /api/offer/{arn} | create-new | Offer generation / Intake API | REST | v1 | Offer retrieval for portal and email delivery |
| SD-020 | /api/explainability/{arn} | create-new | Explainability service | REST | v1 | Retrieve explainability artifacts for UI and audits |

---

## UI Decisions

| ID | Page / Module | Decision | Target Application | Routing | Rationale |
|---|---|---|---|---|---|
| SD-021 | Application Form | modify-existing | Web frontend (applicant portal) | /applications/new | Keep single-page flow; integrate with Intake API and client-side validation |
| SD-022 | Status Lookup | modify-existing | Web frontend | /applications/status | Simple lookup UI calling Intake API status endpoint |
| SD-023 | Offer Detail & Acceptance | create-new | Web frontend | /applications/{arn}/offer /accept | New acceptance flow integrating DocuSign callback and audit recording |
| SD-024 | Underwriter Queue & Case Detail | create-new | Underwriter dashboard | /underwriter/* | New UI aggregating scoring, explainability, Experian, AML status |

---

## Data Decisions

| ID | Schema / Table | Decision | Target Data Store | Migration Strategy | Rationale |
|---|---|---|---|---|---|
| SD-025 | Application submission schema | create-new | Intake API datastore | additive | Define canonical submission payload for downstream services |
| SD-026 | Scoring result schema | create-new | Scoring pipeline store / audit store | additive | Store score, recommendation, and feature contributions for explainability |
| SD-027 | Immutable audit entry schema | create-new | Immutable audit store | additive | Append-only schema for regulatory audit and tamper evidence |

---

## Integration Decisions

| ID | Integration | Decision | Contract Approach | Test Strategy | Rationale |
|---|---|---|---|---|---|
| SD-028 | Experian CreditExpert | create-new (adapter) | adapter / circuit-breaker | contract tests + staging integration | Controlled access, mapping to internal model inputs |
| SD-029 | HMRC identity verification | create-new (adapter) | adapter / new-contract | contract tests + staging | Required for KYC flows and regulatory compliance |
| SD-030 | DocuSign | reuse-as-is | existing-contract | callback integration tests | Use existing contract; ensure callback and signing flows recorded in audit store |
| SD-031 | Temenos T24 | create-new (adapter) | adapter / partner integration | integration tests with idempotency verification | Map disbursement instructions, ensure idempotency and retries |

---

## Infrastructure Decisions

| ID | Component | Decision | Target | CI/CD | Rationale |
|---|---|---|---|---|---|
| SD-032 | CI/CD pipelines for new services | create-new | per-repo pipelines (proposed) | new-pipeline | Each new repo requires a pipeline with infra-as-code and deployment controls |
| SD-033 | Monitoring / APM integration | extend-existing | existing monitoring platform | existing-pipeline | Integrate scoring telemetry and explainability metrics into platform APM |

---

## Repository Summary

| Repository | Status | Technology | Deployment Target | Decisions |
|---|---|---|---|---|
| repo-intake-api (proposed) | new | needs-clarification | needs-clarification | SD-003, SD-017, SD-018 |
| repo-arn-service (proposed) | new | needs-clarification | needs-clarification | SD-004 |
| repo-scoring-pipeline (proposed) | new | needs-clarification | needs-clarification | SD-005, SD-026 |
| repo-explainability-service (proposed) | new | needs-clarification | needs-clarification | SD-006, SD-020 |
| repo-experian-adapter (proposed) | new | needs-clarification | needs-clarification | SD-011, SD-028 |
| repo-underwriter-dashboard (proposed) | new | needs-clarification | needs-clarification | SD-008, SD-024 |
| repo-disbursement-orch (proposed) | new | needs-clarification | needs-clarification | SD-009, SD-031 |
| repo-immutable-audit (proposed) | new | needs-clarification | needs-clarification | SD-010, SD-027 |
| platform-event-bus (existing) | existing | needs-clarification | needs-clarification | SD-016 |
| email-subsystem (existing) | existing | needs-clarification | needs-clarification | SD-002 |
| admin-dashboard (existing) | existing | needs-clarification | needs-clarification | SD-015 |

---

## Architecture Rule Compliance

| Decision | AR Rule | Status | Notes |
|---|---|---|---|
| SD-003 (Intake API) | AR-001 | compliant | Must ensure UK-only datacenters and PII encryption |
| SD-005 / SD-006 (Scoring / Explainability) | AR-005 | compliant | Explainability artifacts persisted in audit store per AR-005 |
| SD-009 / SD-014 (Disbursement / T24) | AR-004 | compliant | Adapter must implement idempotency and retry semantics |
| SD-011 / SD-028 (Experian) | AR-002 | compliant | Adapter with circuit-breaker and fallback to manual / underwriter |

---

## Open Solution Design Questions

| ID | Question | Affects Decision(s) | Blocking? | Required Before | Status |
|---|---|---|---|---|---|
| SDQ-001 | Are Experian and DocuSign contracts available in test environments? | SD-011, SD-030 | Yes | integration testing / staging | open |
| SDQ-002 | Will repository-level mapping be provided (`input/repository-context.md`)? | multiple (repo assignments) | Yes | delivery-planning / epic-elaboration | open |
| SDQ-003 | Which teams own the proposed new services (scoring, audit store)? | SD-005, SD-010 | Yes | delivery-planning | open |

---

## Carried-Forward Open Questions

| ID | Question | From | Impact | Owner |
|---|---|---|---|---|
| Q-001 | Are the Experian and DocuSign contracts already provisioned for test environments? | impacted-systems.md | Affects integration timeline and testing | Procurement / IT |
| Q-002 | Will repository-level mapping be provided (`input/repository-context.md`)? | impacted-systems.md | Affects where code changes will be implemented | Engineering Lead |
| Q-003 | Which teams own the proposed new services (scoring, audit store)? | impacted-systems.md | Affects delivery planning and SLAs | Delivery Lead |

---

*Set Status: Draft — decision artifact to be reviewed and approved by architecture lead.*
