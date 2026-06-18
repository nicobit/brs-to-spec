# Prompt — Create API Contract

## Role

You are a senior API architect performing a Conditional Quality Gate review.

## Context

This gate is only run when `engineering-readiness/readiness-check.md` marks it as Triggered = Yes and Required = Yes.

## Purpose

Define API endpoint, request/response, errors, consumers, compatibility, security and observability requirements.

## Inputs

Use these inputs when available:

- `engineering-readiness/readiness-check.md`
- `input/brs.md or input/brs/*.md`
- `input/architecture.md or input/architecture/*.md`
- `architecture/architecture-rules.md`
- `planning/traceability-matrix.md`
- `business-intake/business-intake-summary.md`
- `business-analysis/actors-and-personas.md` — **if exists**: ACT-NNN IDs and authorization profiles; every endpoint caller must be identified using ACT-NNN, not a free-text role name

## Output path

```text
quality-gates/api-contract.md
```

> **Path note:** Do not write OpenAPI documents, JSON schemas, or contract examples to `specs/`. The `specs/` directory is reserved for OpenSpec handoff story folders (`F-XXX.X-slug/`) and `dependency-graph.md`. API schemas produced as part of this gate belong inline in `quality-gates/api-contract.md` (as fenced code blocks) or as links to files in `quality-gates/schemas/`. Writing gate artifacts to `specs/` collides with handoff output and makes the gate invisible to the stage gate chain.

## Generation steps

**Follow these steps in order. Do not skip or reorder.**

1. Read `.brs2spec/templates/quality-gates/api-contract.md` — this is the required output structure
2. Read all inputs listed above. Then immediately apply the service identification rule:

   ### Service identification rule — mandatory before writing any endpoint content

   Read `architecture/architecture-review.md`. Find the `## Impacted Components` table.

   Filter rows where **both** of the following are true:
   - `Type` = `Service`
   - `Exposes HTTP API?` = `Yes`

   These are the **API-owning services**. Produce one `### <Component Name>` endpoint subsection in the Endpoints section for each matching row — even if endpoints are not yet fully known (use a stub row, see below).

   Also collect rows where `Type` = `External` — these go in a `## Outbound Integrations` section, not in the Endpoints table.

   **Stub rule:** if a service appears in the table but its endpoints cannot yet be determined from BRS or architecture inputs, add the subsection with:

   | Method | Path | Purpose | Auth | Caller (ACT-NNN) |
   |---|---|---|---|---|
   | _(TBD)_ | _(TBD)_ | Endpoints not yet defined — raise open decision | — | — |

   Do not silently omit a service. A stub is better than a gap.

   **Fallback — if `## Impacted Components` table does not exist in `architecture-review.md`:**
   Add a note at the top of the Endpoints section:
   > `Impacted Components table not found in architecture-review.md. Endpoints derived from BRS prose and architecture narrative. Re-run after the architecture review is updated with the Impacted Components table for accurate service segmentation.`
   Then proceed deriving from BRS prose. Do not stop.

3. Write `quality-gates/api-contract.md` starting with the `## Metadata` table exactly as it appears in the template — `| **Status** | **In progress** |` must be the first table in the file
4. Complete every section from the template in order: Metadata, API Summary, Endpoints, Outbound Integrations, Request/Response Contract, Error Handling, Versioning and Compatibility, Open Questions.

   **Endpoints section structure when multiple API-owning services exist:**

   ```markdown
   ## Endpoints

   ### Loan Origination API

   | Method | Path | Purpose | Auth | Caller (ACT-NNN) |
   |---|---|---|---|---|
   | POST | /applications | Submit loan application | Public — OTP | ACT-001 Applicant |
   | GET | /applications/{arn} | Get application status | OTP-verified | ACT-001, ACT-002 |

   ### AI Scoring Service

   | Method | Path | Purpose | Auth | Caller (ACT-NNN or SYS-NNN) |
   |---|---|---|---|---|
   | POST | /score | Trigger scoring job | Internal — managed identity | SYS-001 Loan Origination API |
   | GET | /score/{job-id}/status | Poll job status | Internal | SYS-001 |
   | GET | /score/{job-id}/explainability | Get explainability trace | Internal | SYS-001 |

   ### <Next service> ...
   ```

   **Outbound Integrations section — always present when External rows exist:**

   ```markdown
   ## Outbound Integrations

   These are APIs owned by third parties that this initiative calls. They are not contracts
   this team defines — they are dependencies on third-party contracts.

   | Integration | Direction | Protocol | Auth | Notes |
   |---|---|---|---|---|
   | Experian CreditExpert | Outbound | REST/HTTPS | API key | Circuit breaker required |
   | HMRC Identity Verification | Outbound | REST/HTTPS | OAuth2 | Fallback TBD |
   ```

   When only one API-owning service exists: use a flat Endpoints table — no `###` subsections needed.

5. Fill each service's endpoint table with every endpoint derivable from the BRS and architecture for that service — do not leave any service's table empty unless using the stub rule above
6. Add an optional compact interaction or request/response sequence only when it materially improves contract clarity
7. Set `Status: In progress` — the reviewer changes it to `Accepted` after sign-off

**The output file must start with `## Metadata` and the Status row. Free-form prose without a Metadata table is wrong — the workflow cannot detect gate acceptance without it.**

## Quality bar

A good output must:

- include evidence for each assessment
- link findings to requirements, constraints or deliverables
- assign owners and required-before stages
- distinguish blockers from accepted risks
- produce actionable findings, not generic advice
- keep any optional visual tightly focused on the governed API boundary
- read `architecture/architecture-review.md` Impacted Components table before writing any endpoint content — never derive service count from prose alone when the table exists
- produce one `### <Service Name>` endpoint subsection per row where Type=Service and Exposes HTTP API?=Yes — never merge endpoints from different services into a single flat table when multiple services exist
- document outbound integrations (Type=External rows) in `## Outbound Integrations`, not in the Endpoints table
- include a stub row for any service whose endpoints are not yet determinable — never silently omit a service identified in the Impacted Components table

## Anti-patterns to avoid

Do not produce outputs that:

- say 'looks good' without evidence
- list risks without owners
- ignore triggered gate reason from readiness check
- approve with unresolved critical findings
- create implementation code
- produce a single flat Endpoints table when the Impacted Components table identifies multiple HTTP-exposing services — each service must have its own `###` subsection
- include outbound calls to external systems (Type=External) in the Endpoints table — those are third-party dependencies documented in Outbound Integrations
- silently omit a service from the Endpoints section because its endpoints are not yet defined — use a stub row and reference an open decision
- read `input/architecture.md` to identify services when `architecture-review.md` has an Impacted Components table — always read the review, not the raw input

## Stop conditions

- If this gate was not triggered in the readiness check, stop and state that it should not be run.
- If inputs are missing, list missing inputs and produce only the parts supported by evidence.
- Do not invent evidence.

## Actor-endpoint traceability rule

For every endpoint defined in this contract:
- The "Consumers" or "Callers" field must reference the `ACT-NNN` ID(s) from `business-analysis/actors-and-personas.md`, not a free-text role name
- The authorization level must be consistent with the authorization boundary defined for that ACT-NNN in actors-and-personas.md
- Example: `Caller: ACT-001 Applicant (unauthenticated — public endpoint)`; `Caller: ACT-003 Underwriter (requires role: underwriter-role)`
- If `business-analysis/actors-and-personas.md` does not exist: use free-text role names but add a note per endpoint: `<!-- ACT-NNN reference to be added when actors-and-personas.md is authored -->`

## Self-review checklist

Before finalizing, verify:

- [ ] The gate was triggered in the readiness check.
- [ ] Every finding has evidence.
- [ ] Every required action has owner and required-before stage.
- [ ] Residual risks are explicit.
- [ ] The final decision is clear.
- [ ] Every endpoint names its caller(s) using ACT-NNN IDs from actors-and-personas.md — or notes the gap with the standard comment.
- [ ] Authorization level per endpoint is consistent with the actor's permission profile in actors-and-personas.md.
- [ ] `architecture/architecture-review.md` Impacted Components table was read before writing the Endpoints section (or fallback noted if table absent).
- [ ] Every row where Type=Service and Exposes HTTP API?=Yes has its own `###` subsection in the Endpoints section.
- [ ] No endpoint from one service appears in another service's subsection.
- [ ] All Type=External rows appear in `## Outbound Integrations`, not in Endpoints.
- [ ] Any service with unknown endpoints has a stub row and an open decision reference — not silently omitted.


