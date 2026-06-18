# Actors and Personas

## Metadata

| Field | Value |
|---|---|
| Initiative | I010-NEXT1 |
| Version | 1.0 |
| Status | Draft |
| Created at | 2026-06-16 |
| Created by | product-owner |

## Actor Catalog

| ID | Name | Type | Primary Goal | Permissions/Restrictions | Source |
|---|---|---|---|---|---|
| ACT-001 | Applicant | Human | Submit loan application and view status | Can submit; cannot view others' data | FR-001, FR-005 |
| ACT-002 | Underwriter | Human | Review refer-to-underwriter cases and make decisions | Can approve/decline/request-info | FR-015, FR-016, FR-017 |
| ACT-003 | Compliance Analyst | Human | Review AML/KYC holds and resolve compliance issues | Access to AML/KYC details | FR-012, FR-014 |

## System Actors

| ID | Name | Description | Source |
|---|---|---|---|
| SYS-001 | AI Scoring Service | Produces RiskScore and recommendation | FR-006, FR-007 |
| SYS-002 | Experian Credit Service | Provides credit reports | FR-009 |
| SYS-003 | T24 / Core Banking | Receives disbursement instructions | FR-024 |

---

*Status: Draft — ready for validation.*