# Proposal — F-002.1 Tenant mapping API (backend)

User story (verbatim):

As an IT Operator, I want a tenant selector and stage selector, so I can scope my view to a tenant/stage.

Requirement: FR-002

What changes:
- Implement tenant→subscription mapping service and `GET /tenants/{tenantId}/subscriptions` sample endpoint.

Dependencies:
- depends-on: none
- blocks: F-002.2, F-004.1

Acceptance Criteria (verbatim from BRS):

- AC-002: IT Operator can filter by tenant and stage and perform start/stop operations when authorized; audit log contains the action and user.

BDD scenarios: not triggered

Constraints:
- Must validate tenant mapping with sample subscription IDs (see `engineering-readiness/initiative-context.md`).
