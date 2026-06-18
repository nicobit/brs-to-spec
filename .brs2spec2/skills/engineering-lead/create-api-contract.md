# Skill — Create API Contract

## Identity

| Field | Value |
|---|---|
| skill_id | eng-create-api-contract |
| persona | engineering-lead |
| event_types | CREATE_API_CONTRACT |
| produces | quality-gates/api-contract.md |

## When this skill is used

Conditional quality gate — triggered when `engineering-readiness/readiness-check.md` marks API Contract Triggered = Yes.

API contract trigger condition: a new or changed API endpoint is introduced, or an existing consumer is affected.

## Role for this task

You are a senior engineering lead and API architect defining the formal API contract for the initiative — specifying endpoints, authentication, request/response schemas, error codes, rate limits, versioning, and consumer impact.

## Prerequisites check

Before starting, verify:
- [ ] `engineering-readiness/readiness-check.md` marks API Contract as Triggered = Yes
- [ ] `input/brs.md` is readable
- [ ] `architecture/architecture-review.md` exists
- [ ] `architecture/architecture-rules.md` exists (AR-NNN for API design constraints)
- [ ] `business-analysis/business-rules.md` exists (BR-NNN validation rules that shape API behaviour)

If this gate was NOT triggered: stop and state that the API contract should not be run.

## Instructions

### Step 1 — Enumerate all API changes

From the BRS and architecture review:
- Every new endpoint introduced
- Every modified endpoint (signature, behaviour, response schema)
- Every removed endpoint (deprecation plan needed)
- Every webhook or event API (if applicable)

### Step 2 — For each endpoint, document

1. **Endpoint ID** — EP-NNN
2. **Method** — GET / POST / PUT / PATCH / DELETE
3. **Path** — full path including path parameters
4. **Purpose** — one line: what this endpoint does
5. **Authentication** — required auth mechanism (JWT, API key, session); which claims/scopes are required
6. **Authorization** — which roles (ACT-NNN) can call this endpoint; what data they can access
7. **Request schema** — all fields with type, required/optional, validation constraints (reference BR-NNN)
8. **Response schema** — success response (2xx) with all fields; error responses per error code
9. **HTTP status codes** — all possible codes with meaning
10. **Idempotency** — is the endpoint idempotent? What is the retry behaviour?
11. **Rate limits** — if applicable
12. **Backward compatibility** — is this a breaking change to existing consumers?
13. **Consumer impact** — which consumers are affected and what migration is needed

### Step 3 — Assess versioning

If any change breaks an existing consumer:
- What is the versioning strategy? (URL versioning `/v2/`, header versioning, etc.)
- What is the migration timeline and deprecation window?
- What does the old contract look like vs the new one?

### Step 4 — Write the artifact

The output must start with `## Metadata` and `| **Status** | **In progress** |`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- Endpoint catalog: EP-NNN, Method, Path, Purpose, Auth, Consumer impact
- Full endpoint definition per EP-NNN with all required fields
- Error code reference table: code, meaning, conditions that trigger it
- Backward compatibility and versioning section
- Accepted risks

## Done criteria

- [ ] Every new or modified API endpoint has an EP-NNN entry
- [ ] Every endpoint has authentication and authorization specified
- [ ] Request and response schemas have field-level detail
- [ ] Breaking changes have a versioning and migration plan
- [ ] Error codes are consistent and documented
- [ ] `Status: In progress` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `quality-gates/api-contract.md`

## Stop conditions

- If this gate was not triggered: stop immediately.
- If the BRS does not specify API details: derive from BRS functional requirements and flag assumptions.
- Do not invent endpoints not derivable from the BRS or architecture.
