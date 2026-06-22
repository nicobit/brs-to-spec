# E-002 — AI Pre-Screening & Scoring

## Summary

Epic E-002 runs the automated AI pre-screening and scoring pipeline that produces a numeric risk score and recommendation labels for each submitted application. This epic enables downstream routing (auto-approve, refer, auto-decline) and supplies data for observability and audit.

## Business Objective

Provide an automated pre-screening capability to speed decisions and reduce manual work while preserving traceability, auditability, and safe fallbacks to underwriter review.

## In Scope

- AI scoring pipeline invocation and orchestration
- Experian credit retrieval integration and fallback behavior
- Recording scoring results and recommendation labels in the audit log
- Exposing scoring outputs to downstream flows (underwriter queue, offer generation)

## Out of Scope

- Offer generation, acceptance and disbursement (E-004)
- Implementation contracts and coding handoffs

## High-level Acceptance Criteria

- AI scoring pipeline completes within 90s under normal load (REQ-012)
- Experian credit report retrieved within 30s or application routes to `REFER_TO_UNDERWRITER` (REQ-006)
- Risk score (0–1000) and recommendation labels produced for every submission (REQ-004)
- Scoring events and state transitions written to immutable audit log (REQ-011)

## Traceability (requirements)

- REQ-004 — AI Pre-Screening Trigger and Output
- REQ-006 — Experian Integration for Credit Reports
- REQ-011 — Immutable Audit Log
- REQ-012 — Performance and Scalability NFRs
- REQ-013 — Encryption and Data Residency

## Impacted Systems

- Applicant Portal (frontend)
- Loan Origination API (backend)
- AI Scoring Service (containerized service)
- Experian integration gateway
- Audit store (Cosmos DB)

## Dependencies

- Completion of E-001 (application intake) so ARN and submission events exist
- Experian enterprise contract and credentials (ASM-001)
- Key management configuration for encryption in UK region (REQ-013)

## Risks

- Experian outages causing frequent referrals to underwriters (mitigate via circuit breaker) (NFR-007)
- Model vendor decision pending (OQ-001) — affects scoring contract and telemetry

## Stories

| Story | Title | Linked Requirements |
|---|---|---|
| F-003.1 | Scoring Invocation and Orchestration | REQ-004, REQ-012 |
| F-003.2 | Experian Integration & Fallback | REQ-006, REQ-007 |
| F-003.3 | Scoring Result Handling & Audit | REQ-011, REQ-013 |

## Wave and Ordering

Wave: core scoring capability implemented early (wave 1) with Experian integration and audit plumbing completed alongside the scoring service.

## Foundation / Setup Needs

- AI model service endpoint and contract (vendor TBD)
- Experian API credentials and sandbox access
- Audit append-only container configured in Cosmos DB in UK region

---
