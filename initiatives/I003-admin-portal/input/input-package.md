# Input Package

## Initiative Workspace

| Field | Value |
|---|---|
| Initiative ID | I003 |
| Initiative slug | admin-portal |
| Workspace path | `initiatives/I003-admin-portal/` |

## Owners

| Role | Name |
|---|---|
| Product | Nico |
| Engineering | Engineering |
| Security | TBD |

## Key Decisions (recorded)

| Decision ID | Question / open decision | Answer received | Source (who / when) | Confidence | Impact on workflow |
|---|---|---|---|---|---|
| D-001 | Tenant mapping: how tenants map to Azure? | One subscription per tenant | Product / Engineering (2026-06-09) | High | Simplifies inventory and RBAC scoping |
| D-PO | Confirm Product Owner | Product Owner set to Nico | Product (Nico) (2026-06-09) | High | Enables intake ownership and approvals |
| D-TENANT | Tenant mapping placeholder | Placeholder mapping entry created — real subscription IDs required | Product (Nico) (2026-06-09) | Low | Requires sample subscription IDs to validate architecture |
| D-ALERT | Alerting channels for MVP | Microsoft Teams (channel/webhook) | Product (Nico) (2026-06-09) | Medium | Affects integrations and notification design |
| D-OPS | Operational actions execution model | Synchronous for MVP (Sync) | Product (Nico) (2026-06-09) | Medium | Affects UI behaviour and job handling |

## MVP Prioritization

Recommended MVP (prioritized):

1. Environment Inventory (FR-001)
2. Tenant & Stage Explorer (FR-002)
3. RBAC Management via Azure AD (FR-003)
4. Audit & Change History (FR-006)
5. Basic Operational Actions: view status, start/stop (FR-004)
6. Diagnostics links to Azure Monitor (FR-005)

## Next Steps

1. Confirm Security owner name and contact (PO provided: Nico).
2. Validate subscription mapping for a sample tenant (provide subscription IDs; replace placeholder).
3. Create `planning/delivery-structure.md` with MVP slices and acceptance criteria.

## Tenant → Subscription Mapping (test samples)

| Tenant identifier | Subscription ID | Resource Group pattern | Environment stage | Notes |
|---|---|---|---|---|
| tenant-test-1 | 11111111-1111-1111-1111-111111111111 | rg-tenantname-{stage} | DEV/AIT/UAT/PROD | Sample test subscription (TEST ONLY)
| tenant-test-2 | 22222222-2222-2222-2222-222222222222 | rg-tenantname-{stage} | DEV/AIT/UAT/PROD | Sample test subscription (TEST ONLY)
| tenant-test-3 | 33333333-3333-3333-3333-333333333333 | rg-tenantname-{stage} | DEV/AIT/UAT/PROD | Sample test subscription (TEST ONLY)

## Test Service Principal (TEST ONLY)

Do not use these credentials in production. These are invented examples for local testing and documentation purposes only.

| Field | Example value |
|---|---|
| clientId (appId) | a1111111-aaaa-4aaa-8aaa-aaaaaaaaaaaa |
| objectId (service principal) | b2222222-bbbb-4bbb-8bbb-bbbbbbbbbbbb |
| tenantId | t3333333-cccc-4ccc-8ccc-cccccccccccc |
| clientSecret | <TEST_SECRET_DO_NOT_USE> |


