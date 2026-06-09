 # Architecture Review

 > Primary consumer: Architect, tech lead, delivery lead
 > Purpose of this artifact: confirm architecture constraints, alignment, conflicts, and decisions that shape delivery
 > Downstream use: architecture rules, delivery structure, readiness, governed contract decisions

 ## Metadata

 | Field | Value |
 |---|---|
 | Active deliverable | I003-admin-portal |
| Reviewer | Nico (Architect) |
| Review date | 2026-06-09 |
 | Initial architecture source | input/architecture.md |

 ## Review Decision

 | Decision | Value |
 |---|---|
| Status | Approved  |


 ## Constraints Identified

 - **Azure-only deployment target**: the draft targets Azure only; region/residency and service availability are constrained to Azure services and must be validated with subscription samples.
 - **Azure AD authentication required**: UI and API rely on Azure AD (OAuth/OIDC) and role/group mappings — integration contract and group mappings must be confirmed.
 - **Synchronous Action Orchestrator (MVP)**: the draft configures operational actions to run synchronously; long-running operations may time out and require an async/job-queue design for robustness.
 - **Tenant → Subscription mapping assumption**: the draft assumes a one-to-one tenant→subscription mapping; if shared subscriptions exist the data model and RBAC scoping will change materially.

 ## Existing-System Impact Summary

 - **Azure Subscriptions / Resource Groups**: inventory is derived from live subscriptions — placeholder subscription IDs exist; provide representative subscription IDs to validate scale, naming and RBAC surface.
 - **Identity & Access**: using Azure AD groups/app-roles affects existing identity mappings and may impact downstream consumers expecting different role semantics.
 - **Operational actions surface**: synchronous operations executed against live resources increase blast radius; confirm rollback, dry-run and rate-limiting plans with Platform/Ops.

 ## Optional Visual View

 The draft `input/architecture.md` contains a high-level component list and operational flows. No additional visual was added here; include a compact container or context diagram only if it materially improves decision clarity.

 ## BRS Alignment

 - The draft architecture aligns with the stated goals: secure/scoped UI, API surface, inventory/cache, audit store, and telemetry.
 - Key non-functional concerns (scalability, observability, least-privilege) are addressed at a conceptual level but need concrete evidence (subscription samples, performance targets, retention rules).

 ## Conflicts / Risks

 - Risk: synchronous action model may time out for reprovision/restart operations — classified as high risk for operations that touch many resources.
 - Risk: tenant→subscription mapping variance may force a different data model and RBAC strategy — medium-high risk until validated.
 - Gap: placeholder subscription IDs and tenancy mapping are required to validate scale, costs, and role assignments.

 ## Architecture Findings

 | Finding ID | Severity | Evidence | Risk | Recommendation | Owner | Required before |
 |---|---|---|---|---|---|---|
 | F-001 | High | `input/architecture.md`: synchronous orchestrator | Long-running ops may fail | Evaluate async job queue fallback and add dry-run gating | Architecture / Platform | Delivery structure & readiness
 | F-002 | Medium | `input/architecture.md`: tenant→subscription mapping assumption | Incorrect assumption causes RBAC/data model issues | Provide representative subscription mapping and validate model | Architecture / Product | Readiness

 ## Open Architecture Decisions

- None. All architecture decisions are resolved and recorded in [planning/open-decisions.md](planning/open-decisions.md).
## Architecture Decisions

The following decisions have been resolved and are recorded in the planning open-decisions register: [planning/open-decisions.md](planning/open-decisions.md#L1-L200).

| Decision ID | Question | Final decision | Owner | Required before |
|---|---|---|---|---|
| OD-001 | Validate tenant → subscription mapping for target customers | Resolved: One-to-one mapping (2026-06-09) — reduces complexity and blast radius. | Architect / Product | Delivery structure
| OD-002 | Action Orchestrator execution model for long-running operations | Resolved: Hybrid model (sync for short ops; async job queue for long ops) (2026-06-09). | Architect / Platform | Readiness
| OD-003 | Service principal role set and provisioning guidance | Resolved: Custom `AdminPortalActionRunner` role + per-subscription service principal (MVP) (2026-06-09). | Architecture / Ops | Readiness

 ## Recommended Next Actions (short)

 - Architect: validate and replace placeholder tenant/subscription mappings in `input/architecture.md` with representative sample IDs.
 - Architect / Platform: evaluate async fallback for the Action Orchestrator and document required changes to delivery slices.
 - Ops: provide guidance on service principal provisioning and required role assignments for the MVP.
 - Product: confirm target tenancy pattern and acceptance criteria for operations (timeouts, dry-run requirements).

 ---

 Generated from `input/architecture.md` on 2026-06-09.
