# Stakeholder Notice — I003 Admin Portal: Action Orchestrator & RBAC

To: Product (Nico), Platform/Ops, Security, Architecture

Summary of current state:

- Architecture review and rules completed. Open decisions OD-001..OD-003 were resolved (One-to-one tenancy mapping; Hybrid action model; Custom `AdminPortalActionRunner` role + per-subscription SP).
- Readiness check scaffold created and currently marked `Not ready` pending a few artifacts.

Requested artifacts and where to add them:

- Product: provide 3 representative subscription IDs or tenancy mapping examples and add to `input/input-package.md`.
- Ops: review and harden the custom role definition in `engineering-readiness/service-principal-iac.md` and the Terraform example `engineering-readiness/service-principal-terraform.tf`; provide final role JSON and IaC PR.
- Architecture/Platform: review `planning/openapi-actions.yaml` for API contract and confirm async patterns and idempotency guidance.
- Security: perform a threat-model review for operational actions and capture mitigations in `engineering-readiness/readiness-check.md` or a linked quality gate artifact.

Links:

- Architecture review: [architecture/architecture-review.md](architecture/architecture-review.md)
- Architecture rules: [architecture/architecture-rules.md](architecture/architecture-rules.md)
- Decision proposals: [planning/decision-proposals.md](planning/decision-proposals.md)
- Open decisions (resolved): [planning/open-decisions.md](planning/open-decisions.md)
- Terraform example: [engineering-readiness/service-principal-terraform.tf](engineering-readiness/service-principal-terraform.tf)
- Role/IaC guidance: [engineering-readiness/service-principal-iac.md](engineering-readiness/service-principal-iac.md)
- API OpenAPI draft: [planning/openapi-actions.yaml](planning/openapi-actions.yaml)
- Readiness check: [engineering-readiness/readiness-check.md](engineering-readiness/readiness-check.md)

Please review the linked artifacts and update them in-repo or reply here with approvals. Once Ops and Security confirm the role and threat model, we can mark the readiness check as `Ready` and continue to delivery structure finalization.
