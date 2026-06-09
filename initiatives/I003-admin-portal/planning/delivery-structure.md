 # Delivery Structure — I003 Admin Portal

 ## Metadata

 | Field | Value |
 |---|---|
 | Initiative | I003-admin-portal |
 | Created by | Copilot (draft) |
 | Date | 2026-06-09 |

 ## Purpose

 Define the feature-level delivery shape and acceptance criteria for the MVP slices. Each feature is split into at least two user stories to preserve separable implementation and review boundaries.

 ## Traceability

 Source: `input/brs.md`, `input/architecture.md`

 ## Features and User Stories (MVP)

 1) Environment Inventory
    - Story 1: Backend: implement inventory ingestion from Azure subscriptions and resource groups, provide paginated API. Acceptance: API returns consolidated inventory for sample subscription IDs; performance within agreed target for sample dataset.
    - Story 2: Frontend: present inventory list with filters and pagination. Acceptance: UI displays inventory, supports filters, and links to diagnostics.
    - Trace: FR-001, Architecture: Inventory Store

 2) Tenant & Stage Explorer
    - Story 1: Backend: implement tenant→subscription mapping and sample data endpoints. Acceptance: supports sample tenant-test-1..3 and returns correct resource groups.
    - Story 2: Frontend: provide tenant/stage selector and environment explorer view. Acceptance: UX allows switching tenants and stages with correct inventory context.
    - Trace: FR-002

 3) RBAC Management via Azure AD
    - Story 1: Backend: expose APIs to read and map Azure AD groups to roles and perform RBAC checks. Acceptance: APIs validate group membership and resolve roles for sample users.
    - Story 2: Frontend: manage role mappings and show effective permissions per tenant. Acceptance: UI allows role mapping edits and shows validation results.
    - Trace: FR-003, Security rules

 4) Audit & Change History
    - Story 1: Backend: implement append-only audit store and write events for actions (user, timestamp, resource). Acceptance: audit entries written for sample actions and exportable.
    - Story 2: Frontend: display audit timeline and allow filtering by resource/user/date. Acceptance: UI displays audit records and supports export.
    - Trace: FR-006, Architecture: Audit Store

 5) Basic Operational Actions (start/stop)
    - Story 1: Backend: implement action endpoints with sync/async pattern (use OpenAPI `actions/{actionId}/run`). Acceptance: short ops return `200`; long ops return `202` + `job_id`.
    - Story 2: Frontend: action confirmations, dry-run preview, and job status polling. Acceptance: UI shows progress and final result for async jobs.
    - Trace: FR-004, Architecture: Action Orchestrator

 6) Diagnostics Links to Azure Monitor
    - Story 1: Backend: resolve diagnostic links per resource to Log Analytics queries. Acceptance: links generated for sample subscriptions.
    - Story 2: Frontend: link from resource to diagnostics and support opening in new tab. Acceptance: link correctly opens Log Analytics with pre-populated query.
    - Trace: FR-005, Observability

 ## Cross-cutting Acceptance Criteria

 - Security: all authentication uses Azure AD; service principal usage documented and secrets stored in Key Vault.
 - Observability: Application Insights traces emitted for actions and job processing; diagnostic links validated.
 - Testing: BDD scenarios for critical flows must be added before handoff to QA.

 ## Implementation Notes

 - Each feature must have at least two stories (backend + frontend) as above. If a feature cannot be split, define technical sub-stories (API, data model, validation) to meet the rule.
 - Use `planning/open-decisions.md` and `architecture/architecture-rules.md` for constrained choices and non-negotiable rules.

 ---

 Drafted from `input/brs.md` and `input/architecture.md` on 2026-06-09.
---
Title: Delivery Structure (MVP)
Status: Confirmed
Generated: 2026-06-09
Source: `input/brs.md`, `business-intake/business-intake-summary.md`
---

## Overview

This delivery structure breaks the MVP into features and user stories suitable for early planning and traceability. Each feature below includes at least two user stories.

### Feature: Environment Inventory (FR-001)
- Story E-001.1: As an IT Operator, I want to see a paginated list of environments by tenant and stage, so that I can find an environment quickly.
  - Acceptance: list renders within 2s for 1000 items; filters by tenant/stage work.
- Story E-001.2: As a Platform Engineer, I want exportable inventory CSV for selected tenant/stage, so that I can analyze inventory offline.
  - Acceptance: exported CSV contains identifier, resource type, last-updated timestamp.

### Feature: Tenant & Stage Explorer (FR-002)
- Story T-002.1: As an IT Operator, I want a tenant selector and stage selector, so I can scope my view to a tenant/stage.
  - Acceptance: selector persists selection across navigation.
- Story T-002.2: As a Support Engineer, I want free-text search and tag filters, so I can find environments by tags and names.
  - Acceptance: search returns matching results within 2s.

### Feature: RBAC Management (FR-003)
- Story R-003.1: As a Platform Engineer, I want to assign `Operator` role to a user scoped to a tenant/stage, so they can perform allowed actions.
  - Acceptance: role assignment reflected in Azure AD and enforced by API.
- Story R-003.2: As an Auditor, I want to view role assignment history, so I can see who changed roles and when.
  - Acceptance: audit view lists assignments with timestamp and actor.

### Feature: Operational Actions (FR-004)
- Story O-004.1: As an IT Operator, I want to start/stop an environment and receive immediate status, so I know the action succeeded or failed.
  - Acceptance: action completes synchronously for quick ops; UI shows success/failure within 30s.
- Story O-004.2: As a Platform Engineer, I want to trigger reprovision and see job status, so I can monitor progress (MVP: synchronous trigger + status link).
  - Acceptance: reprovision returns a status and job link; audit log created.

### Feature: Diagnostics & Links (FR-005)
- Story D-005.1: As an IT Operator, I want a diagnostics probe that returns health and a quick link to Log Analytics, so I can investigate issues.
  - Acceptance: diagnostics probe returns health status and a link to Log Analytics for the resource.
- Story D-005.2: As a Support Engineer, I want to view recent errors and traces for an environment, so I can triage incidents faster.
  - Acceptance: recent error list shows last 50 events and links to full telemetry.

### Feature: Audit & Change History (FR-006)
- Story A-006.1: As an Auditor, I want an append-only audit view of admin actions, so I can generate compliance reports.
  - Acceptance: audit entries are immutable and exportable.
- Story A-006.2: As an IT Operator, I want to see the last actor and timestamp for environment actions, so I can understand recent changes.
  - Acceptance: UI shows actor and timestamp for last action.

## MVP Slice and Priorities (short)
- Slice 1 (Sprint 1): Inventory listing, tenant/stage explorer, basic start/stop operations, Teams alert integration.
- Slice 2 (Sprint 2): RBAC assignment UI and enforcement, diagnostics probes, audit logging.
- Slice 3 (Sprint 3): Export, reprovision status, performance tuning and observability.

## Traceability
- Source BRS FR identifiers: FR-001..FR-006
- Acceptance criteria map to AC-001..AC-004 in the business intake.
