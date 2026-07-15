# Architecture Review

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I944-DINA |
| Created at | 2026-07-02 |
| Created by | architect |
| Status | Draft |

## Initiative-Architecture Fit

| Feature Area | Existing Components Touched | New Components / Boundaries | Contract Changes | Blast Radius |
|---|---|---|---|---|
| Investor onboarding & orders | Fund admin systems, KYC/KYB services, payment gateway | Internal DTA workflow engine, CRE adapter | Smart contract gateway contract and CRE connectors | Medium |
| Reconciliation & reporting | Fund admin, custody, accounting | Reconciliation engine, audit log storage | Reconciliation event contract mapping | Medium |
| Onchain execution | Smart contract gateway, Chainlink CRE | Chainlink DTA contracts, CCIP integration | Onchain event reference fields in ledger | High |

## Architecture Constraints

| ID | Constraint | Rationale | Violation Consequence | Source |
|---|---|---|---|---|
| ARCH-C-001 | Personal and KYC data must remain offchain; only hashes/attestations onchain | Regulatory and privacy requirements | Block deployment; security review required | input/brs.md |
| ARCH-C-002 | Internal golden record is authoritative unless ADR changes legal model | Auditability and legal ownership | Reconciliation disputes; legal exposure | input/brs.md |
| ARCH-C-003 | Initial rollout restricted to one fund and one controlled chain | Reduce blast radius and risk for first release | Require ADR to expand; rollback if violated | input/brs.md |

## Brownfield Impact

| Component | Change Type | Consumers | Backward Compatible? | Migration Required | Rollback Possible |
|---|---|---|---|---|---|
| Fund Administration API | Integration / Modified | Reporting, Accounting, Ops | Yes | Yes | Yes |
| Investor Registry (offchain) | New component / sync | Transfer agent operations | Yes | Yes | Yes |

**Regression surface:** Reconciliation flows and reporting are highest risk due to differences between fund admin and internal ledger formats.

**Rollback sensitivity:** Medium - rollback requires restoring previous reconciliation snapshots and re-running forensic reconciliation.

## Quality Attribute Assessment

| Attribute | Requirement (from BRS) | Assessment | Risk |
|---|---|---|---|
| Performance | Timely reconciliation and onchain sync | Medium — design CRE workflows for async processing; use batching | Medium |
| Security | Sensitive data offchain; allowlists for wallets | High — explicit controls and audits required | High |
| Scalability | Multi-fund, multi-chain future support | Medium — architecture supports modular adapters; needs capacity planning | Medium |
| Availability | Order processing and reconciliation SLAs | Medium — design for retries and idempotency in CRE workflows | Medium |

## Open Decisions

| DEC-NNN | Question | Owner | Default Assumption | Required Before |
|---|---|---|---|---|
| DEC-001 | Does the onchain registry ever become the legal source-of-truth? | Legal / Product | No — offchain remains authoritative | Production launch |
| DEC-002 | Reconciliation frequency and SLA (near real-time vs batch) | Product / Ops | Daily batch with near-real-time alerts for exceptions | Implementation of reconciliation engine |

## Active Assumptions

| Assumption | Source | If False, Then |
|---|---|---|
| A-001: CRE will provide reliable delivery semantics for onchain calls | input/brs.md | Implement compensating workflows and extend retry/backoff; increase monitoring |
| A-002: Fund admin can provide machine-readable position exports | input/brs.md | Additional adapter work and manual reconciliation steps required |

## Known Unknowns

| Unknown | Impact | Discovery Path |
|---|---|---|
| Onchain legal model edge cases | Legal exposure if onchain treated as source | Legal review and ADR process; sample transactions and legal sign-off |

---
*Status: Draft — architect review required.*
