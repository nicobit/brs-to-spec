## Metadata

- Initiative: I013-NEXT13
- Artifact: Software Modules
- Author: b2s-agent
- Status: Draft

## Purpose

Identify the candidate software modules, their responsibilities, primary interfaces, and key dependencies to support implementation planning and team assignment.

## Module Inventory

| Module ID | Name | Responsibility | Primary Interfaces | Notes |
|---:|---|---|---|---|
| MO-001 | Customer Service | Customer profile, registration, KYC orchestration | REST: /customers, Events: customer.created | Integrates with KYC provider
| MO-002 | Account Service | Account provisioning and lifecycle | REST: /accounts | Bounded by tenancy rules
| MO-003 | Loan Origination | Intake, validations, status | REST: /loans, Rules engine integration | Orchestrates decisioning
| MO-004 | Decision Engine | Business rules, scoring, approvals | API: rule.evaluate | Externalized rules (Drools/T24 connector)
| MO-005 | Payments Gateway | Disbursement, settlements | API: payments.process | External provider integration (pending contract)
| MO-006 | Audit & Compliance | Immutable audit records, explainability | Events/API | Must satisfy UK data residency

## Module Interfaces

- Event bus: Publish/subscribe for domain events (customer.created, loan.submitted, payment.settled).
- Service APIs: RESTful JSON over HTTPS with bearer token auth.
- Rules: Decision Engine exposes `evaluate` endpoint and receives rule updates via secure CI/CD pipeline.

## Non-functional Mapping

- Scalability: `Loan Origination` and `Decision Engine` must support horizontal scaling.
- Security: `Payments Gateway` and `Audit & Compliance` require hardened controls and encryption at rest.
- Data residency: `Audit & Compliance` must store UK-only audit records.

## Dependencies and Risks

- External KYC provider contract unknown — may delay work on `Customer Service` integration.
- Payments provider contract required for end-to-end `Payments Gateway` stories.

## Catalog

- MO-001 (module:service) — Customer Service: profile, registration, KYC orchestration.
- MO-002 (module:service) — Account Service: account provisioning and lifecycle.
- MO-003 (module:service) — Loan Origination: intake, validations, orchestration.
- MO-004 (module:service) — Decision Engine: business rules and scoring.
- MO-005 (module:service) — Payments Gateway: disbursement and settlement.
- MO-006 (module:service) — Audit & Compliance: immutable auditing and explainability.
