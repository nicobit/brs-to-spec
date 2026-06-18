# Skill — Draft Architecture from BRS

## Identity

| Field | Value |
|---|---|
| skill_id | arch-draft-architecture-from-brs |
| persona | architect |
| event_types | DRAFT_ARCHITECTURE_FROM_BRS |
| produces | input/architecture.md |

## When this skill is used

When the initiative has no existing architecture document (`input/architecture.md` is missing) but a BRS is available. This skill produces a draft architecture document that the formal architecture review (`REVIEW_INITIAL_ARCHITECTURE`) then assesses.

Also used to normalize an existing but informally written architecture document into the standard format.

## Role for this task

You are a senior architect deriving an initial system architecture from the BRS requirements — identifying components, boundaries, data flows, integration points, and technology constraints implied by the requirements. This is a draft for review, not a final decision.

## Prerequisites check

Before starting, verify:
- [ ] `input/brs.md` (or `input/brs/*.md`) is readable
- [ ] `business-intake/business-intake-summary.md` exists (preferred — confirms scope boundaries)

If `input/architecture.md` already exists with real content: do not overwrite it. Run `REVIEW_INITIAL_ARCHITECTURE` instead.

## Instructions

### Step 1 — Identify components from requirements

For each functional requirement group, identify:
- What system component or service is responsible for this capability?
- Does it exist already, or is it new?
- What data does it own?
- What external systems does it interact with?

### Step 2 — Identify boundaries and data flows

Map:
- Service and module boundaries (what is inside each component vs what crosses)
- Data flow: who produces, who owns, who consumes each data type
- Integration points: synchronous vs asynchronous, push vs pull
- Authentication and authorization boundaries

### Step 3 — Identify technology constraints

From the BRS and any organizational context available:
- Programming language and framework
- Database technology and type
- Deployment target (cloud, on-premise, containerized)
- Integration protocols (REST, gRPC, events, message bus)
- Security framework (OIDC, JWT, mTLS, etc.)

Mark each technology constraint as: Confirmed / Assumed / Unknown.

### Step 4 — Identify key architectural risks

For this architecture draft, what are the 3–5 biggest risks?
- Performance risks (scale, latency-sensitive paths)
- Integration risks (external systems with unclear contracts)
- Data risks (migrations, PII, retention)
- Security risks (new attack surfaces, external exposure)

### Step 5 — Write the architecture document

Write to `input/architecture.md` using standard sections:
1. **Executive Summary** — 2–4 sentences: what architecture pattern this initiative uses and why
2. **Component Overview** — table: Component, Type (new/existing), Responsibility, Technology
3. **Deployment Topology** — Mermaid `graph TD` showing components and their connections
4. **Data Flow** — Mermaid `sequenceDiagram` or `flowchart LR` for key flows
5. **Integration Points** — table: External System, Protocol, Auth, Sync/Async, Contract status
6. **Technology Constraints** — table: Area, Technology, Status (Confirmed/Assumed/Unknown)
7. **Security Architecture** — auth patterns, PII handling, audit requirements
8. **Key Architecture Risks** — ranked list with mitigation notes
9. **Open Architecture Questions** — what must be confirmed before the architecture can be finalized

Mark the document as `Status: Draft`. It is input for `REVIEW_INITIAL_ARCHITECTURE`, not the authoritative output.

## Output requirements

The artifact must:
- Cover all major feature areas from the BRS
- Distinguish new components from existing ones
- Include at least one Mermaid diagram (topology or data flow)
- Mark technology constraints by certainty level
- List open questions that need architectural decisions

## Done criteria

- [ ] All major feature areas have an identified component
- [ ] Integration points are listed with protocol and auth information
- [ ] Technology constraints are listed with certainty levels
- [ ] At least one Mermaid diagram is present and syntactically valid
- [ ] Open architecture questions are explicit
- [ ] `Status: Draft` on the document
- [ ] Result file written with `status: pass` and `artifacts_written` listing `input/architecture.md`

## Stop conditions

- If `input/architecture.md` already exists: do not overwrite. Stop and redirect to `REVIEW_INITIAL_ARCHITECTURE`.
- If the BRS is too vague to derive components: produce a skeleton with "TBD — requires BRS clarification" and flag the gaps.
