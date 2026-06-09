# Security Review Quality Gate

> Gate owner: Security
> Triggered: Yes — PII handling, external integrations, data residency

## Scope

- PII encryption at rest and in transit
- Data residency for Italy (GDPR)
- Webhook authentication and replay protection (IDP B)
- Secrets management and key rotation
- RBAC for support UI and internal operations
- Threat model for onboarding integration flows

## Checklist

- [ ] PII encrypted at rest (Azure Key Vault or equivalent KMS); TLS enforced in transit
- [ ] Data residency approach confirmed for Italy; Legal sign-off attached to `input/input-package.md`
- [ ] IDP webhook: HMAC-SHA256 signature verification and replay protection implemented
- [ ] Secrets stored in managed key vault; no credentials hard-coded; rotation policy defined
- [ ] RBAC for support UI reviewed; least-privilege access for operator roles confirmed
- [ ] Audit logging and retention policy defined for PII and verification records
- [ ] Vendor security documentation (DPA / SOC2 / SLA) reviewed
- [ ] Threat model summary completed for top risks (IDP outage, data leak, replay attacks)

Any item not completed must be recorded as an accepted risk with approver name and expiry date.

## Required evidence (note paths here when attached)

- Integration contracts with webhook details: `input/contracts/identity-provider-b-contract.md`
- Data model and PII field mapping: `quality-gates/data-contract.md`
- Legal residency sign-off: `input/input-package.md` — Decisions and Clarifications Received

## Acceptance

Status: `Accepted`
