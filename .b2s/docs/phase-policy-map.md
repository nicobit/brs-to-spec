# Phase Policy Map

This note is the human-readable companion to the staged action registry. It
shows the typical relationship between phase inputs, policy context, and target
artifacts.

| Phase | Typical Inputs | Typical Policies | Target Artifact |
|---|---|---|---|
| `2-business-intake` | `input/brs.md`, routing decision, optional supporting notes | business writing guidelines, business glossary guidance | `business-intake/business-intake-summary.md` |
| `2b-business-analysis` requirements | intake summary, BRS | requirement writing standard, definition of ready | `business-analysis/requirements.md` |
| `3-planning` architecture review | requirements, gaps, intake summary, routing, BRS, optional architecture input | architecture principles, technology standards | `architecture/architecture-review.md` |
| `4-engineering-readiness` | delivery structure, architecture review, architecture rules, intake summary, routing, BRS | definition of ready, architecture principles, technology standards | `engineering-readiness/readiness-check.md` |
| `4b-quality-gates` NFR assessment | readiness check, requirements, architecture review, architecture rules, optional quality-gate signals | security policy, availability standard, performance standard, regulatory standard | `quality-gates/nfr-assessment.md` |
| `4b-quality-gates` observability | readiness check, architecture review, architecture rules, BRS | security policy, availability standard, performance standard, testing expectations | `quality-gates/observability-plan.md` |
| `4b-quality-gates` data contract | readiness check, architecture review, business rules, entity model | security policy, regulatory standard | `quality-gates/data-contract.md` |
| `5-handoff` | readiness outputs, delivery structure, architecture rules, NFR assessment, optional traceability and contracts | coding constraints, testing expectations, AI handoff constraints | `specs/`, `standalone-delivery/`, or compact handoff outputs |

Guidance:

- Keep policies action-local rather than loading a global policy bundle.
- Prefer short policy files over large narrative governance documents.
- Add `policy_refs` only where the policy meaningfully changes the artifact.
