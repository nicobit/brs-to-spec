# Delivery Increments — I004 IT Portal

Purpose
-------
Define delivery increments (slices of work) for the MVP and follow-up iterations, with suggested sprint boundaries, scope, and owners to enable planning and handoff.

Guidelines
----------
- Sprint length: 2 weeks (suggested). Adjust to team cadence.
- Increment: group of 2–4 sprints delivering a coherent milestone.
- Owners: Delivery Lead owns increments; Product Owner validates; Platform/DevOps owns infra spikes.

Increment 1 — MVP (4 sprints)
--------------------------------
Goal
- Deliver a minimal, production-safe portal that demonstrates request intake, approvals, RBAC, audit, CMDB read sync and CI/CD linking for one provider.

Scope (by sprint)
- Sprint 1 (Spike & SSO PoC): Azure AD SSO PoC, group-to-role mapping, basic auth plumbing.
- Sprint 2 (Request CRUD + Approval): Minimal request UI, API, approval state machine, audit logging.
- Sprint 3 (CMDB Sync & Asset Views): Read-only ServiceNow connector, reconciliation surface in UI.
- Sprint 4 (CI/CD Linking & Dashboards): Hook one pipeline provider, show build/deploy status in change requests, basic dashboard.

Acceptance criteria (end of increment)
- SSO configured and role mapping validated for test users.
- Request intake end-to-end with approvals and auditable trails.
- CMDB read sync visible in UI and reconciled.
- CI/CD link surfaces build status for one provider.

Owners
- Delivery Lead: overall increment owner and acceptance sign-off.
- Product Owner: validates scope and acceptance criteria.
- Platform/DevOps: SSO, connector spikes, infra IaC.

Increment 2 — Operations & Automation (3 sprints)
-------------------------------------------------
Goal
- Add runbook attachments, automation hooks, richer notifications, and improved dashboards.

Scope
- Runbook service + execution hooks.
- Notifications (Teams/Slack/email) and escalation rules.
- Dashboard improvements and caching for performance.

Increment 3 — Two-way CMDB & Policy (3–4 sprints)
--------------------------------------------------
Goal
- Implement controlled two-way CMDB flows where approved, enforce approval policies, and add advanced reporting.

Scope
- Controlled CMDB writes (guarded flows) and reconciliation rules.
- Policy integration for approval decisions (if required).
- Audit export and compliance workflows.

Cross-cutting increments
------------------------
- Security & Threat Modeling: run in parallel; sign-off required before production deployment.
- Observability & SLOs: implement telemetry and dashboards across increments.

Suggested timeline and checkpoints
---------------------------------
- Sprint cadence: 2-week sprints.
- Increment checkpoints: increment demo and acceptance review with stakeholders at the end of each increment.

Next actions
------------
1. Assign named owners for Increment 1 (Delivery Lead, Product Owner, Platform/DevOps contacts).
2. Confirm sprint cadence and exact dates; record them in `planning/workflow-state.json`.
3. Create tickets/epics in the planning tool and map to the stories in `planning/delivery-structure.md`.
