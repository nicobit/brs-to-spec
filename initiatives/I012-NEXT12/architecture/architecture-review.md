# Architecture Review — Initial Draft

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I012-NEXT12 |
| Reviewed at | 2026-06-16 |
| Reviewed by | product-owner, architect (draft) |
| Status | Review Draft |

## Summary

The proposed cloud-native architecture targets Azure UK South (primary) with UK West for DR. Core components include Applicant Portal, Underwriter Dashboard, Loan Origination API, AI Scoring Service, Compliance Service, Notification Service, Audit Log Store, Application Database, and Payment Gateway Adapter. Integration points include Experian, DocuSign, HMRC, HM Treasury, and Temenos T24.

## Key Decisions & Rationale

- Deploy within UK regions to meet data residency and GDPR constraints (input/architecture.md).  
- Use Azure-managed services where possible (App Service, Container Apps, Service Bus, Cosmos DB) to reduce operational overhead.  
- Use Azure API Management as ingress to centralize rate-limiting, WAF, and authentication.

## Risks and Mitigations

- Experian integration: rate limits and field mappings are incomplete (GAP-001). Mitigation: confirm contract and implement circuit breaker with fallback to `REFER_TO_UNDERWRITER` (NFR-007).  
- PII handling across third-party services: verify data residency for DocuSign and Experian (GAP-002). Mitigation: configure regional accounts or implement redaction and transient ingestion patterns.  
- AI scoring performance: scoring SLA needs load profile validation (GAP-003). Mitigation: performance testing and autoscaling for AI service; consider cached inference or warm pools.

## Architecture Notes

- Audit log must be append-only and stored in Cosmos DB as specified. Consider retention policies and export to immutable blob storage for long-term retention.  
- Use Service Bus for decoupled async flows (submission -> scoring -> decision -> notifications).  
- Store minimal credit bureau data transiently and only persist score and derived summary fields.

## Recommended Next Steps

1. Confirm Experian field mapping and contractual limits (owner: product-owner / architect).  
2. Validate DocuSign regional compliance and sign-off (owner: security / legal).  
3. Define AI scoring load profile and run performance tests (owner: ops / AI team).  
4. Produce a preliminary infra diagram (C4 container) and cost estimate for Azure UK deployment (owner: architect).

## Proposed Acceptance Criteria for Review

- All blocking gaps (GAP-001, GAP-002) have either remediation plans or accepted assumptions.  
- Deployment topology documented with region-specific services and resource groups.  
- Security model validated against enterprise IdP and managed identity pattern.

---

*Set Status: Accepted only by workflow or human approval when applicable.*
