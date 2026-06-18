# Skill — Create Security Review

## Identity

| Field | Value |
|---|---|
| skill_id | sec-create-security-review |
| persona | security-reviewer |
| event_types | CREATE_SECURITY_REVIEW |
| produces | quality-gates/security-review.md |

## When this skill is used

Conditional quality gate — triggered when `engineering-readiness/readiness-check.md` marks Security Review Triggered = Yes.

Security review trigger conditions (ANY of these):
- Authentication or authorization is involved
- Sensitive or PII data is handled
- External API exposure or new service boundary is introduced
- Audit trail is required

## Role for this task

You are a senior security reviewer performing a Conditional Quality Gate review — assessing the initiative's security posture across authentication, authorization, data handling, audit, and integration security.

## Prerequisites check

Before starting, verify:
- [ ] `engineering-readiness/readiness-check.md` marks Security Review as Triggered = Yes
- [ ] `input/brs.md` is readable
- [ ] `architecture/architecture-review.md` exists
- [ ] `architecture/architecture-rules.md` exists

If this gate was NOT triggered in the readiness check: stop and state that the security review should not be run.

## Instructions

### Step 1 — Assess each security domain

**Authorization**
- What roles and permissions exist? (from actors-and-personas.md, BR-NNN)
- What data or actions are restricted by role?
- Is privilege escalation possible in any identified flow?
- Are there horizontal access control risks? (user A accessing user B's data)

**Authentication**
- What authentication mechanism is used? (OIDC, JWT, session, API key)
- Where are tokens validated?
- Are there unauthenticated endpoints? Are they intentional?
- Token expiry, rotation, and revocation strategy?

**Input validation**
- Are all external inputs validated at the boundary?
- Are there injection risks? (SQL, command, template injection, XSS)
- Are file uploads or user-generated content sanitized?

**Sensitive data handling**
- What PII data is processed? (from entity-model.md, data-contract.md)
- Is PII encrypted at rest and in transit?
- Are there data retention and deletion requirements? (from BRS)
- Is logging PII-safe? (no PII in log lines)

**Audit trail**
- What actions require an audit trail? (from BRS and BR-NNN)
- Is the audit trail tamper-evident?
- Is audit data retained for the required period?

**Integration security**
- What external systems are called? (from architecture.md)
- How are integration credentials stored and rotated?
- Is inter-service authentication in place (mTLS, signed JWTs)?
- Are integration responses validated before use?

### Step 2 — Classify findings

Each finding: ID, Domain, Severity (Critical/High/Medium/Low), Evidence, Risk, Recommendation, Owner, Required Before.

Severity definitions:
- **Critical**: exploitable without authentication or allows data breach
- **High**: exploitable with user credentials or allows unauthorized access
- **Medium**: design weakness that increases risk surface
- **Low**: best practice gap with low exploitation probability

### Step 3 — Write the artifact

The output file must start with `## Metadata` and `| **Status** | **In progress** |`. Set `Status: In progress`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- Security findings table: ID, Domain, Severity, Evidence, Risk, Recommendation, Owner, Required Before, Blocking?
- Security control coverage summary: which controls are in place vs missing
- Accepted risks section: risks explicitly accepted with justification and owner
- Decision: Approved / Request Changes / Blocked

## Done criteria

- [ ] All 6 security domains assessed (Authorization, Authentication, Input Validation, Data Handling, Audit, Integration)
- [ ] Every finding has evidence and risk
- [ ] Accepted risks have owner and justification
- [ ] No generic advice without actionable recommendation
- [ ] `Status: In progress` in the Metadata table (the gate owner sets to Accepted)
- [ ] Result file written with `status: pass` and `artifacts_written` listing `quality-gates/security-review.md`

## Stop conditions

- If this gate was not triggered: stop immediately.
- If inputs are missing: review only what is supportable and list missing inputs.
- Do not invent security requirements not grounded in source artifacts or evident risk.
