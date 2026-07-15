# Atomic Requirements Catalogue

## Source Inventory

- Source: `input/brs.md` — Internal Digital Transfer Agent Architecture

### C-001 - Data residency and offchain authority
**Source:** input/brs.md | **Actor:** System | **Deps:** None
> **Derivation:** Direct

WHEN investor personal or KYC data is stored,
THE SYSTEM SHALL store that data offchain and expose only hashes or attestations to onchain components.

### FR-001 - Maintain internal golden record
**Source:** input/brs.md (Section 2.3) | **Actor:** Internal DTA | **Deps:** None
> **Derivation:** Direct

WHEN investor positions change,
THE SYSTEM SHALL update the internal golden record as the authoritative ledger of ownership and emit reconciliation events for onchain synchronization.

### FR-002 - Use Chainlink infrastructure for onchain actions
**Source:** input/brs.md (Sections 1, 5.1, 5.2) | **Actor:** Integration Layer | **Deps:** FR-001
> **Derivation:** Direct

WHEN an approved onchain transaction is required (mint, burn, settlement),
THE SYSTEM SHALL invoke Chainlink DTA standard contracts via the Chainlink Runtime Environment (CRE) and record the onchain transaction reference in the internal ledger.

### FR-003 - Eligibility and compliance decisioning
**Source:** input/brs.md (Section 4.2.3) | **Actor:** Eligibility Service | **Deps:** None
> **Derivation:** Direct

WHEN a subscription, redemption, or transfer request is submitted,
THE SYSTEM SHALL run eligibility and compliance checks (KYC, AML, sanctions, product eligibility) and block or allow the request based on policy outcomes.

### FR-004 - Reconciliation between internal ledger and onchain state
**Source:** input/brs.md (Section 4.2.6) | **Actor:** Reconciliation Engine | **Deps:** FR-001, FR-002
> **Derivation:** Direct

WHEN periodic reconciliation runs execute,
THE SYSTEM SHALL compare internal DTA positions, fund administrator records, custody records, and onchain token balances and mark reconciliation status as Matched, Pending, Mismatch, or Requires Investigation.

### FR-005 - Workflow state transitions for orders
**Source:** input/brs.md (Section 4.2.1) | **Actor:** Workflow Engine | **Deps:** None
> **Derivation:** Direct

WHEN an order (subscription, redemption, transfer) is processed,
THE SYSTEM SHALL progress the order through defined states (Draft → Submitted → Validated → Pending Compliance → Approved for Onchain Execution → Onchain Execution Pending → Settled → Reconciled) and record timestamps for state transitions.

### FR-006 - Audit and reporting evidence
**Source:** input/brs.md (Section 4.2.7) | **Actor:** Reporting Service | **Deps:** FR-001, FR-004
> **Derivation:** Direct

WHEN reporting or audit evidence is requested,
THE SYSTEM SHALL produce investor statements, transfer agency reports, reconciliation evidence, and immutable logs linking internal and onchain events.

### NFR-001 - Controlled rollout
**Source:** input/brs.md (Section 2.5) | **Actor:** Delivery Team | **Deps:** None
> **Derivation:** Direct

WHERE initial deployment occurs,
THE SYSTEM SHALL restrict the first rollout to one controlled fund and one controlled chain, requiring an ADR to enable multi-chain or public-chain expansion.

## Source ID Mapping

- `input/brs.md` sections mapped to extracted IDs: FR-001..FR-006, NFR-001, C-001.

## Open Questions

- Q-001: Legal authority of onchain registry — is there any scenario where onchain becomes the legal source? (Assumed: offchain remains authoritative unless ADR overrides)
- Q-002: Required SLA and reconciliation frequency — business to confirm expected intervals.

## Summary

- Extracted requirements: 7 (6 FR/NFR + 1 Constraint)
- Ambiguities flagged: 2

## Requirement Catalogue

| ID | Short title | Source |
|---|---|---|
| FR-001 | Maintain internal golden record | input/brs.md#L1-L200 |
| FR-002 | Invoke Chainlink for onchain actions | input/brs.md#L1-L200 |
| FR-003 | Eligibility and compliance decisioning | input/brs.md#L1-L200 |
| FR-004 | Reconciliation engine outcomes | input/brs.md#L1-L200 |
| FR-005 | Workflow order state transitions | input/brs.md#L1-L200 |
| FR-006 | Audit and reporting evidence | input/brs.md#L1-L200 |
| NFR-001 | Controlled rollout | input/brs.md#L1-L200 |
| C-001 | Data residency and offchain authority | input/brs.md#L1-L200 |

## Assumptions

- A-001: Offchain systems can provide attestations/hashes suitable for onchain evidence.
- A-002: Chainlink CRE workspaces and contracts will be provisioned by an integration team.

