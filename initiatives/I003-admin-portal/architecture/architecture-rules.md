 # Architecture Rules

 ## Principles

 - Follow least-privilege and least-blast-radius principles for operational actions.
 - Preserve auditability for every action and user-facing change; all actions must emit auditable records.
 - Do not assume tenancy/subscription mapping without explicit sample data and Product confirmation.

 ## API Rules

 - Authentication: All UI and API traffic MUST use Azure AD (OIDC/OAuth) for authentication. Roles MUST be mapped to Azure AD groups or app roles; no local user stores for production.
 - Gateway: All public API endpoints MUST be fronted by the platform API gateway with rate-limiting and auth enforcement.
 - Idempotency: Any action that mutates cloud resources MUST be idempotent or provide an idempotency key to prevent duplicate side effects.
 - Dry-run / Preview: Any action that affects >N resources or carries high blast radius MUST offer a dry-run/preview mode and explicit user confirmation.

 ## Data Rules

 - Inventory store: The inventory backing store is read-optimized; writes must be controlled by a single ingestion/orchestration flow and follow pagination and TTL guidelines defined in delivery.
 - Audit store: Audit records MUST be append-only and tamper-evident where supported; retention and export requirements must be captured in readiness gate.
 - Residency & PII: If the BRS or input package specifies residency or PII handling, enforce region-scoped storage and encryption-at-rest policies per legal guidance.

 ## Security Rules

 - Service principals: Provision a scoped service principal per subscription (or per tenancy pattern as agreed). Role assignments MUST follow least-privilege and be documented in delivery notes.
 - Secrets & keys: Secrets MUST be stored in the approved secret store and never baked into images or client code.
 - Encryption: All data in transit MUST use TLS; sensitive data at rest MUST be encrypted using platform-managed keys unless otherwise approved.

 ## Deployment Rules

 - Target platform: Initial deployments target Azure only. Representative subscription IDs MUST be provided to validate scale and role assignments before handoff.
 - Autoscaling: API backend MUST be autoscalable behind the API gateway; sizing targets to be defined in readiness with performance evidence.
 - Operational actions: Long-running or multi-resource operations SHOULD be executed asynchronously or be gated with rate limits and dry-run; synchronous-only is acceptable for short, bounded operations with documented timeout and retry behavior.

 ## Rule ownership and traceability

 - Each rule above requires an Owner and a short implementation note in `engineering-readiness/initiative-context.md` before handoff.
 - If a rule cannot be met as-written, that deviation MUST be recorded as an open decision in `planning/open-decisions.md` with an owner and required-before stage.
