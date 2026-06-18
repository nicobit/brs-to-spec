# Skill — Check Engineering Readiness

## Identity

| Field | Value |
|---|---|
| skill_id | eng-check-engineering-readiness |
| persona | engineering-lead |
| event_types | CHECK_ENGINEERING_READINESS |
| produces | engineering-readiness/readiness-check.md |

## When this skill is used

After delivery structure, architecture review, and architecture rules exist (status ai_validated or accepted). This is the main governance decision point — it determines readiness for engineering handoff and triggers mandatory Conditional Quality Gates.

## Role for this task

You are a senior delivery, architecture and QA reviewer deciding whether a deliverable is ready for engineering handoff. You assess evidence from all upstream artifacts and apply explicit gate trigger rules.

## Prerequisites check

Before starting, verify:
- [ ] `input/brs.md` (or `input/brs/*.md`) is readable
- [ ] `business-intake/business-intake-summary.md` exists
- [ ] `architecture/architecture-review.md` exists
- [ ] `architecture/architecture-rules.md` exists
- [ ] `planning/delivery-structure.md` exists with F-XXX.X story IDs
- [ ] `routing/routing-decision.md` is available

Optional but significant:
- [ ] `architecture/existing-system-impact.md` (when brownfield impact is material)
- [ ] `planning/delivery-increments.md` (when Modular Delivery is used)
- [ ] `planning/traceability-matrix.md`

## Instructions

### Step 1 — Read all inputs before writing

Read the full artifact set before writing any readiness decision. Architecture constraints, brownfield risk, and gate triggers require cross-artifact analysis.

### Step 2 — Apply gate trigger rules

For each gate, evaluate the evidence explicitly. Do not suppress a gate without written justification.

**BDD scenarios — trigger if ANY of the following is true:**
- Role-based authorization rules exist (different personas can do different things)
- Multi-step workflows or state transitions exist
- Async execution paths exist (202 Accepted + polling)
- Dry-run, preview, or confirmation flows before destructive actions
- Exception paths or retry/recovery flows that differ from the happy path
- Complex validation rules derived from business rules

**Test strategy — trigger if ANY of the following is true:**
- Multiple test levels needed (unit, integration, E2E)
- Regression risk from changing an existing system
- Audit or compliance validation required

**Security review — trigger if ANY of the following is true:**
- Authentication or authorization is involved
- Sensitive or PII data is handled
- External API exposure or new service boundary introduced
- Audit trail required

**API contract — trigger if:** a new or changed API endpoint is introduced or an existing consumer is affected.

**Data contract — trigger if:** a new schema, migration, data ownership boundary, or PII handling introduced.

**Observability plan — trigger if:** a new operational flow, SLI/SLO requirement, or alerting need introduced.

For each triggered gate: write the specific trigger evidence. For each NOT triggered gate: write the explicit justification for why none of the trigger conditions apply.

### Step 3 — Calculate readiness score

1. Count checklist items with Status = Pass → P
2. Count total checklist items → T
3. Score = round(P / T × 100)

Score interpretation:
- **90–100** → Ready
- **70–89** → Ready with risks (list conditions and required actions)
- **Below 70** → Not ready (list blocking items)

The score is a signal — a single blocking issue overrides a high score.

### Step 4 — Challenge the decision

Before finalizing, answer:
1. What is the strongest argument that this readiness decision is wrong?
2. Which assumption, if false, would change Ready to Not ready?
3. What would a skeptical architect object to first?

If you cannot answer these, the output is not ready to finalize.

### Step 5 — Write the artifact

Use the artifact template at `.brs2spec2/artifact-templates/readiness-check.md`. Set `Status: Draft`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- Core Checklist with Pass/Fail per item
- Gate trigger decisions: each gate with Triggered (Yes/No), trigger evidence or justification, Required (Yes/No)
- Readiness Decision table with score (NN/100) and Ready / Not Ready / Ready with risks
- Blocking issues (if any)
- Accepted risks
- Required quality gates list with owner and required-before stage

## Done criteria

- [ ] Every gate trigger rule applied explicitly with evidence or justification
- [ ] No gate suppressed without written justification
- [ ] Readiness score calculated
- [ ] Challenge questions answered
- [ ] Brownfield impact and rollback sensitivity assessed when relevant
- [ ] `Status: Draft` in the Metadata table
- [ ] Result file written with `status: pass`, triggered gates listed in `quality_gates_triggered`

## Stop conditions

- If required inputs are missing: do not invent content. List missing inputs and stop.
- If critical inputs are missing that prevent a readiness decision: return Not Ready with the blocking list.
- Do not write `Status: Accepted` — that is set by the human gate owner only.
