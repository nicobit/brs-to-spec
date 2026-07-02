# Skill — Orchestrate Dynamic Iteration

## Identity

```text
skill_id:    orchestrator.orchestrate-dynamic-iteration
persona:     orchestrator
action_id:   orchestrate-dynamic-iteration
produces:    orchestration/iteration-log.md
             + one artifact per iteration (path decided by the orchestrator)
```

## North star

An AI coding assistant can implement every capability in this initiative
without asking a single clarifying question.

Every iteration closes one gap toward that bar. Nothing else matters.

## Inputs — read all that exist before starting

**Always read:**
- `input/brs.md` — the primary source of truth. Read it in full, every iteration.
- `orchestration/iteration-log.md` — orientation from prior iterations (if exists)

**Read if they exist:**
- `input/architecture.md` — technology stack, deployment topology, integration points
- `input/loop-steer.md` — human steering notes written between iterations
- Every file under `coding-packages/` — what has already been produced
- Every file under `requirements/`, `architecture/`, `planning/`, `quality-gates/`

Do not start until all existing files are read completely.

## Step 1 — Orient

### If this is iteration 1 (no iteration-log.md exists yet):

Derive the **goal state** from the input files. Do not use a template —
derive it from what this BRS actually describes.

Answer these questions from the inputs:

1. What are the concrete implementable capabilities? List them in the order
   a developer would need to build them (domain model before business rules,
   business rules before integrations, integrations before UI, UI before CI).

2. For each capability: what does a developer need to implement it correctly?
   Think like a senior engineer reviewing a junior's work before they start:
   - Entity definitions and state machines?
   - API contracts (request/response/errors)?
   - Integration contracts (auth, timeout, circuit breaker, fallback)?
   - Business rules and edge cases?
   - Acceptance criteria (Gherkin, traceable to BRS IDs)?
   - Test expectations (unit / integration / API / e2e)?
   - CI pipeline gate?
   - Security, compliance, or regulatory constraints specific to this capability?

3. What are the non-negotiable best practices for this initiative type?
   Apply these automatically — do not wait to be asked:
   - **Regulated / fintech:** idempotency keys on all state transitions,
     immutable audit log (append-only, tamper-evident), explainable AI
     (no black-box models — FCA requirement), circuit breakers on every
     external call, GDPR right-to-erasure compatible data model, PII
     minimisation in logs, cooling-off enforcement at state machine level.
   - **Event-driven:** at-least-once delivery, dead-letter queue handling,
     ordering guarantees where required, idempotent consumers.
   - **Multi-tenant:** data isolation, per-tenant RBAC, no cross-tenant
     data leakage in queries or events.
   - **Public API:** versioning strategy, rate limiting, contract stability,
     deprecation policy.
   - Apply whichever set fits. A single initiative may trigger multiple sets.

4. What open questions in the inputs would block a developer?
   A blocking question is one where a developer would have to guess or
   ask before writing code. List them specifically — name the FR, name
   the missing fact, name what breaks if it stays unresolved.

Record the goal state as the `## Goal State` section of `orchestration/iteration-log.md`.

### If this is iteration N (iteration-log.md exists):

Read the last `## Iteration N` block. What was produced? What gap was closed?
What is the declared next gap? Check whether prior artifacts actually closed
their declared gaps by reading the produced files. Adjust if needed.

Read `input/loop-steer.md`. If it contains new human input since the last
iteration, incorporate it before selecting the next gap.

## Step 2 — Gap

Identify the **single highest-value gap** toward the north star.

A gap is not a coverage dimension. A gap is a specific, concrete missing fact:

> "An AI coder cannot implement FR-009 without knowing the Experian API
>  error response schema for rate-limiting (HTTP 429) and the circuit
>  breaker threshold."

> "The loan application state machine has 6 states but only 3 transitions
>  are defined — the AUTO_DECLINE → 30-day cooling-off enforcement path
>  has no implementation contract."

> "FR-022 requires DocuSign e-signature but no webhook callback contract
>  exists for offer acceptance confirmation — the coder would have to
>  guess the event payload schema."

Rank gaps by: **blocks the most downstream work first**.
Domain model gaps block everything. Integration contract gaps block
the capability that uses them. UI gaps block only UI.

### Stop conditions

**Pause for human:** the gap requires a fact that cannot be derived from
the inputs. Write a specific developer question — not "objectives missing"
but exactly what a developer would ask before writing the code.

**Stop (complete):** every capability in the goal state has a coding package
where a developer can implement it without asking a question. Set
`continue: false, reason: complete`.

**Stop (budget):** iteration count exceeds 20 and critical gaps remain.
Set `continue: false, reason: budget`. List remaining gaps explicitly.

## Step 3 — Synthesize

Decide what artifact to produce to close this gap.

Do not default to a fixed artifact type. Produce what closes this specific gap.
The artifact can be:

- A **coding package** (or a section of one) — the primary deliverable
- A **domain model** — entity definitions, field constraints, state machine,
  business rules, with Mermaid diagrams where they aid implementability
- An **integration contract** — API schema (OpenAPI), auth mechanism,
  timeout, retry, circuit breaker, fallback behaviour, error response
  catalogue, observability signals, compliance notes
- **Acceptance criteria** — Gherkin scenarios traceable to FR-NNN IDs,
  one scenario per testable behaviour, including error paths and edge cases
- A **test plan** — what to test (unit / integration / API / e2e),
  what to assert, criticality, automation tag, CI gate mapping
- A **CI pipeline definition** — stages, gates, what must pass before merge,
  environment-specific behaviour (staging vs. production)
- A **best-practice analysis** — for this initiative type: what a senior
  engineer adds that the BRS doesn't mention (e.g. idempotency, GDPR
  erasure, cooling-off state enforcement, audit trail immutability strategy)
- A **traceability map** — FR-NNN → artifact → AC-NNN → test → CI gate

You may combine types within one artifact if that is what closes the gap.

**Structure guidance:** reference `.b2s/artifact-templates/` for structure
patterns appropriate to the artifact type you are producing. Use them as
advisory — adapt to what this gap actually needs. Available templates include:
`integration-spec.md`, `epic-coding-handoff.md`, `coding-prompt.md`,
`entity-model.md`, `business-rules.md`, `bdd-scenarios.md`,
`test-plan-per-story.md`, `consumed-api-spec.md`, `api-contract.md`,
`data-contract.md`, `event-contract.md`, `observability-plan.md`.

**Output path:** decide the path based on what you are producing:
- Coding packages → `coding-packages/CP-NNN-<slug>/`
- Architecture artifacts → `architecture/<name>.md`
- Requirements artifacts → `requirements/<name>.md`
- Quality artifacts → `quality-gates/<name>.md`

## Step 4 — Produce

Write the artifact. Rules:

- Ground every statement in the BRS or input/architecture.md.
  Do not invent requirements.
- Preserve all BRS requirement IDs (FR-NNN, NFR-NNN, OBJ-NNN) for
  traceability. Every artifact must trace to at least one BRS ID.
- Apply mandatory best practices from Step 1 automatically — do not
  wait to be asked. If the BRS says "circuit breakers required (NFR-007)"
  and you are writing an integration contract, include the circuit breaker
  specification without prompting.
- Be specific enough that an AI coding assistant produces production-quality
  code, not a scaffold. Concrete field names, concrete error codes, concrete
  timeout values, concrete Gherkin scenarios — not "define appropriate
  error handling".
- State explicit boundaries: what NOT to implement in this artifact's scope.
  A coding agent that does not know what to exclude will over-build.
- For acceptance criteria: every scenario must have a Given/When/Then with
  concrete values, not placeholders. The coding agent implements exactly
  what is specified.
- For integration contracts: always include the failure mode catalogue —
  timeout, 5xx, auth failure, rate limit, unavailable — with the specific
  fallback behaviour for each. "Refer to underwriter" is not enough —
  name the state the application transitions to.

## Step 5 — Log

Append one `## Iteration N` block to `orchestration/iteration-log.md`.

Include:
- Date
- Gap closed (specific — same format as the gap you identified in Step 2)
- Artifact produced (full path)
- Confidence delta (what a developer can now do that they could not before)
- Next gap (the specific next gap, already identified while producing this artifact)
- Continue decision: `yes` or `no — <reason>`
- One short reasoning paragraph: why this gap, what it resolves, what
  a developer can now implement

If this is iteration 1, write the `## Goal State` section first, then
the first `## Iteration 1` block.

## Constraints

- One artifact per iteration. No batching.
- Never modify `input/brs.md` or any file under `input/`.
- Never invent requirements not present in the inputs.
- Pause with a specific developer question. Generic pauses ("objectives missing",
  "requirements unclear") are not acceptable — name the FR, name the missing
  fact, name what breaks.
- Every produced artifact must be self-contained: a developer reads that one
  file and knows exactly what to build, in what order, and how to verify it.
- Traceability is mandatory: every artifact section must reference the BRS
  requirement IDs it addresses.
- Do not produce orchestration meta-artifacts (gap backlogs, coverage ledgers,
  spec anchors). The iteration log is the only orchestration artifact.
  Everything else is a developer-facing deliverable.

## Done criteria for this iteration

- [ ] All input files read in full
- [ ] Goal state recorded (iteration 1) or referenced (iteration N)
- [ ] One specific gap identified with developer-level precision
- [ ] One artifact produced that closes that gap
- [ ] Artifact is self-contained and traceable to BRS IDs
- [ ] Best practices for this initiative type are applied inline
- [ ] Iteration log updated with gap, artifact, delta, next gap, continue
- [ ] Continue decision is explicit with a reason

## Notes for the staged engine

- Do not mention dispatcher status, result files, or validation mechanics
- Validation and state updates are handled by the .b2s engine after this skill runs
- The dispatcher will re-invoke this skill on the next dispatch-next call
  if continue: yes is set in the iteration log
- If continue: false is set, the dispatcher will transition to finalize-dynamic-initiative
