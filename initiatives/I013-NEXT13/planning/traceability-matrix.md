## Metadata

- Initiative: I013-NEXT13
- Artifact: Traceability Matrix
- Author: b2s-agent
- Status: Draft

## Purpose

Map functional requirements (FRs) to delivery epics, features, and stories to ensure end-to-end traceability and test coverage.

## Story Count Assertion

- Total epics: 6
- Total features: 18
- Total stories: 72

## FR Coverage

| FR ID | Description (summary) | Epic | Feature(s) | Story refs | Coverage Status |
|---|---|---:|---|---|---|
| FR-001 | Customer registration | E-001 | F-001 | F-001.1, F-001.2 | covered |
| FR-002 | Identity verification (KYC) | E-001 | F-002 | F-002.1, F-002.2 | covered |
| FR-003 | Account provisioning | E-002 | F-003 | F-003.1, F-003.2 | covered |
| FR-004 | Loan application intake | E-003 | F-004 | F-004.1..F-004.4 | covered |
| FR-005 | Decisioning / rules engine | E-003 | F-005 | F-005.1..F-005.3 | covered |
| FR-006 | Payment / disbursement | E-004 | F-006 | F-006.1..F-006.5 | partial (integration dependent) |

## Mapping Notes

- Epics reference: see planning/delivery-structure.md for full epic/feature/story definitions.
- Stories are grouped by feature; story ids use the convention `F-<n>.<m>` where `<m>` is the story index.
- Coverage status key: `covered`, `partial`, `missing`.

## FR -> Story Matrix

| FR ID | Mapped Story IDs |
|---|---|
| FR-001 | F-001.1, F-001.2 |
| FR-002 | F-002.1, F-002.2 |
| FR-003 | F-003.1, F-003.2 |
| FR-004 | F-004.1, F-004.2, F-004.3, F-004.4 |
| FR-005 | F-005.1, F-005.2, F-005.3 |
| FR-006 | F-006.1, F-006.2, F-006.3 |

## Story -> Requirements Matrix

| Story ID | Satisfies FRs |
|---|---|
| F-001.1 | FR-001 |
| F-001.2 | FR-001 |
| F-002.1 | FR-002 |
| F-002.2 | FR-002 |
| F-004.1 | FR-004 |
| F-006.1 | FR-006 |

## Coverage Summary

- Covered FRs: 5/6 fully covered.
- Partial coverage: FR-006 requires external gateway integration stories (see gaps).

## Gaps

- FR-006 (Payment / disbursement): integration stories for payment gateway and settlement reconciliation are pending external contract and therefore marked `partial`.
- Integration test scenarios for third-party KYC providers are noted but not yet fleshed out.
## Traceability Table (summary)

- Requirements mapped: 6 key FRs (critical path).
- Downstream consumers: QA, Security, Ops, Integration.

## Validation

This artifact asserts minimum story counts and coverage for critical FRs. Reviewers should verify integration stories for `FR-006` (payments) remain dependent on external gateway contracts.
