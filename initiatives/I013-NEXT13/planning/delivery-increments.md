## Metadata

- Initiative: I013-NEXT13
- Artifact: Delivery Increments
- Author: b2s-agent
- Status: Draft

## Purpose

Define delivery increments and map stories to increments for incremental delivery and planning.

## Delivery Increments

- **D1** — Minimum Viable Delivery: covers core intake, KYC screening, initial scoring, underwriter queue, observability events. (Must stories: 8)
- **D2** — Integration & Automation: Experian integrations, offer generation, disbursement orchestration, retries and alerts. (Should stories: 3)
- **D3** — Nice-to-have and scaling: extended observability, performance tuning, reconciliation flows. (Could stories: 1)

## Story Mapping

| Increment | Stories (examples) |
|---|---|
| D1 | F-001.1, F-001.2, F-001.3, F-002.1, F-002.2, F-003.1, F-003.2, F-004.1 |
| D2 | F-002.3, F-005.1, F-005.2 |
| D3 | F-006.1 |

## Planning Notes

- D1 must ensure audit and explainability traces for scoring decisions to satisfy compliance.
- D2 requires external contracts (Experian, payments provider) to be in place before end-to-end E2E verification stories are accepted.
