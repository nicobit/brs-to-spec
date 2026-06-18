## Metadata

- Initiative: I013-NEXT13
- Artifact: Data Contract
- Author: b2s-agent
- Status: Draft

## Scope and Data Subjects

- Collections: Customer (PII), Loan, Decision, Audit Logs.

## Schema Catalog

- Customer: id, name, dob, email (PII masked in outputs).
- Loan: id, amount, term, status.

## Data Asset Catalog

| Asset | Owner | Sensitivity |
|---|---|---|
| Customer | Product | PII |
| Loan | Product | Confidential |
| Decision | Product | Confidential |

## Schema Definitions

- Customer: { id: uuid, name: string, dob: date, email: string }
- Loan: { id: uuid, amount: number, term: int, status: string }

## PII Mapping

- Customer.email: PII -> Mask in non-prod, pseudonymize for analytics.

## Data Flows and Boundaries

## Data Flows and Boundaries

- Source systems, transform layers, sinks (analytics, audit store); PII never leaves UK compliance boundary.

## Ownership and Stewardship

- Data owners: Product; Data stewards: Platform team; Security: InfoSec.

## Migration Plan

- Schema changes: use backward-compatible additions; migration scripts executed in staging with verification.

## Access Control

- Role-based access controls enforced via central IAM; data access logged and audited.

## Retention and Disposal

- Audit logs: 7 years; transactional data: 3 years unless otherwise specified.

## Masking and Anonymization

- Apply deterministic pseudonymization for analytics; mask PII in non-prod environments.

## Contract Tests and CI Integration

- Schema compatibility tests in CI; data contract validations run on schema changes.

## Decision

- Data contract accepted pending enforcement of masking in staging and SRE monitoring for retention.

## Accepted Risks

- Short-term acceptance of certain analytic fields changing shape; consumers must tolerate unknown fields.
