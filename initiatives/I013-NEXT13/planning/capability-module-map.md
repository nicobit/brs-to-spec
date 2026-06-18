## Metadata

- Initiative: I013-NEXT13
- Artifact: Capability → Module Map
- Author: b2s-agent
- Status: Draft

## Purpose

Map high-level capabilities to the candidate software modules identified earlier to guide component ownership and implementation slices.

## Capability → Module Mapping

| Capability | Description | Mapped Module(s) |
|---|---|---|
| User registration | Capture and verify user identity | MO-001 |
| KYC screening | AML/KYC checks and decision flags | MO-001, MO-003 |
| Application intake | Intake and persist loan applications | MO-003 |
| Scoring & Decisioning | Produce explainable risk scores | MO-004, MO-003 |
| Offer generation | Create and present loan offers | MO-005, MO-003 |
| Disbursement | Orchestrate payment to core banking | MO-005, MO-002 |
| Audit & Observability | Emit events and store immutable audit | MO-006 |

## Notes and Risks

- MO-005 (Payments) remains conditional on provider contract and early integration spikes are recommended.
- Capability ownership assumes API contracts between `MO-003` and `MO-004` for decision payloads.

## Catalog

| Catalog ID | Entry | Mapped Modules |
|---|---|---|
| CM-001 | User registration | MO-001 |
| CM-002 | KYC screening | MO-001, MO-003 |
| CM-003 | Application intake | MO-003 |
| CM-004 | Scoring & Decisioning | MO-004, MO-003 |
| CM-005 | Offer generation | MO-005, MO-003 |
| CM-006 | Disbursement | MO-005, MO-002 |
| CM-007 | Audit & Observability | MO-006 |
