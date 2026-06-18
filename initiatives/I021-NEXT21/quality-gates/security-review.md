# Security Review

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I021-NEXT21 |
| Created at | 2026-06-17T19:12:00+00:00 |
| Created by | security-reviewer |
| Status | Draft |

## Summary

- PII handling required for applicant data; ensure encryption at rest and in transit.
- External integrations (Experian, T24) require credential rotation and least-privilege access.

## Required Actions

- Threat model review for disbursement paths.
- SAST on scoring service and adapters.

## Security Findings

- PII in transit and at rest requires clear encryption and key management controls.
- Adapter credentials currently unspecified; rotation and secret management needed.

## Security Control Coverage

- Encryption: planned (Azure managed keys) — implementation owner: infra
- Identity: RBAC for services; service principals for adapters
- Logging: audit trails enabled for decision and disbursement events

## Accepted Risks

- Limited T24 sandbox parity — will mitigate by feature flags and staged rollout.

## Decision

- Decision: Security review required and SAST/SCA scans to be integrated into CI before production deployment.

## Analysis

- The highest-risk area is disbursement integration; review must prioritize threat modelling and sandbox testing to reduce deployment risk.
