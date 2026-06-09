 # Decision Proposals — I003 Admin Portal

 This document proposes recommended options for the open architecture decisions recorded in `planning/open-decisions.md`. These are draft proposals for architect/product/platform/ops to review, accept, modify, or reject.

 ## OD-001 — Tenant → Subscription mapping

 - Question: Validate tenant → subscription mapping for target customers.
 - Options considered:
   - One-to-one mapping (one subscription per tenant) — simplifies RBAC scoping and data model.
   - Shared subscriptions (multiple tenants/share of resources) — increases RBAC complexity and data model changes.
   - Hybrid (support both patterns) — more flexible but higher implementation effort for the MVP.
 - Proposed option (recommended for MVP): One-to-one mapping.
 - Rationale: One-to-one mapping reduces initial delivery complexity, simplifies least-privilege service principal assignments, and reduces risk around cross-tenant RBAC. It enables a well-scoped MVP and faster handoff.
 - Acceptance criteria:
   - Product provides representative sample subscription IDs for 3 target customers or environment variants.
   - Architect verifies that tenant→subscription mapping in `input/architecture.md` matches samples and documents any deviations.
 - Impact of acceptance: Delivery assumes per-subscription role assignments and simpler inventory model. If a customer requires shared subscriptions later, plan a follow-up extension with migration guidance.
 - Owner: Product / Architect
 - Required before: `planning/delivery-structure.md` finalization and readiness

 ## OD-002 — Action Orchestrator execution model for long-running operations

 - Question: Decide execution model for operational actions (synchronous vs async).
 - Options considered:
   - Keep synchronous for all operations.
   - Add an async job queue for long-running operations (preferred hybrid).
   - Fully async-first model.
 - Proposed option (recommended): Hybrid model — synchronous for short, bounded operations; async (job queue) for long-running or multi-resource operations.
 - Rationale: Hybrid model preserves simple UX for quick operations while avoiding timeouts and large-scale failures for long-running work. It reduces blast radius by allowing dry-run, rate-limiting, and retry semantics to be handled via an async job system.
 - Implementation notes:
   - Define operation classification thresholds (e.g., operations expected >30s become async).
   - API response patterns: synchronous operations return `200` with result; async operations return `202 Accepted` with `job_id` and status endpoint.
   - Provide a migration path: start with sync for clearly short operations, add async paths incrementally.
 - Acceptance criteria:
   - Platform/Architecture provide an API pattern and small integration example (202+job id) in the delivery notes.
   - Delivery slices that include long-running actions document fallback and validation in user acceptance criteria.
 - Owner: Architect / Platform
 - Required before: Readiness and delivery slices that implement operational actions

 ## OD-003 — Service principal role set and provisioning guidance

 - Question: Define the role set and provisioning approach for the Action Orchestrator service principal(s).
 - Options considered:
   - Use built-in broad roles (e.g., Contributor) per subscription — faster but over-privileged.
   - Create custom least-privilege role(s) aligned to exact actions (preferred).
   - Per-environment service principals vs central service principal.
 - Proposed option (recommended): Create a custom role `AdminPortalActionRunner` with the minimal permissions required for the set of orchestration actions, and provision one service principal per subscription (MVP). Document provisioning via IaC.
 - Rationale: Custom roles minimize blast radius and are auditable; per-subscription principals align with the one-to-one tenancy mapping and simplify scoping. IaC provisioning enables repeatable, auditable assignments.
 - Example minimal permission surface (illustrative — platform to confirm exact actions):
   - `Microsoft.Compute/virtualMachines/start/action`
   - `Microsoft.Compute/virtualMachines/restart/action`
   - `Microsoft.Resources/subscriptions/resourceGroups/read`
   - `Microsoft.Resources/deployments/*` (if deployment orchestration required)
 - Acceptance criteria:
   - Ops provides a draft custom role definition for review and a sample IaC snippet to create and assign it to the service principal in a sample subscription.
   - Security reviews the custom role and signs off on least-privilege coverage.
 - Owner: Ops / Architecture
 - Required before: Readiness and handoff; service principal and role docs must be present before implementation begins.

 ## Next steps for proposals

 - Share these proposals with Product, Platform, and Ops for review.
 - When one option is accepted, update `planning/open-decisions.md` setting Status = Resolved, add a short Resolution note and date, and update the home artifact(s) where relevant.
 - After decisions are resolved, set `planning/workflow-state.json` → `state_validated: true` and continue to readiness.
