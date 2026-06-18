# Data Contract

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I021-NEXT21 |
| Created at | 2026-06-17T19:20:00+00:00 |
| Created by | data-governance |
| Status | Draft |

## Data Entities

- Application: application_id, applicant_id, amount, term_months, status
- Decision: decision_id, application_id, score, recommendation, timestamp

## Storage and Retention

- PII retention: 7 years; personal identifiers encrypted at rest using managed keys.

## Data Ownership and Access

- Owners: Product and Data teams; access via RBAC and service principals.

## Accepted Risks

- Limited anonymization tooling for analytics; mitigate with pseudonymization in ETL.

## Data Asset Catalog

| Asset | Owner | Purpose |
|---|---|---|
| applications | Product | Store application records |
| decisions | Risk | Store decision outcomes |

## Schema Definitions

- Application schema: (application_id: uuid, applicant_id: uuid, amount: decimal, term_months: int, status: string)
- Decision schema: (decision_id: uuid, application_id: uuid, score: float, recommendation: string, timestamp: datetime)

## PII Mapping

| Field | PII Type | Storage |
|---|---|---|
| applicant_id | Identifier | Encrypted at rest |

## Data Flow

- Intake -> Staging -> Scoring Service -> Decision Store -> Reporting

## Access Control

- Service principals for adapters; RBAC for humans with least privilege.

## Migration Plan

- Consume existing T24 extracts, map fields, run parallel processing for 2 weeks prior to cutover.

## Decision

- Decision: Data contract approved for draft; final approval after integration tests and ETL verification.
