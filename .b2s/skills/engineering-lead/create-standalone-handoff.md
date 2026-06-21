# Skill - Create Standalone Handoff

## Identity

```text
skill_id:    engineering-lead.create-standalone-handoff
persona:     engineering-lead
action_id:   create-standalone-handoff
produces:    standalone-delivery/
```

## When this skill is used

Run this only when the execution mode is `Standalone`, readiness is `Ready`,
and all triggered gates are accepted.

## Preconditions

Before starting, verify:
- `engineering-readiness/readiness-check.md` is `Ready`
- all triggered gates are accepted
- `engineering-readiness/initiative-context.md` exists
- `planning/delivery-structure.md` has story IDs
- `architecture/architecture-review.md` exists
- `architecture/architecture-rules.md` exists
- `quality-gates/nfr-assessment.md` exists

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/engineering-readiness/initiative-context.md`
- `{workspace_root}/engineering-readiness/readiness-check.md`
- `{workspace_root}/planning/delivery-structure.md`
- `{workspace_root}/architecture/architecture-review.md`
- `{workspace_root}/architecture/architecture-rules.md`
- `{workspace_root}/quality-gates/nfr-assessment.md`
- `{resolved_optional_inputs}` - technical-specification artifacts when workflow type is `technical-spec-modular`

Do not start writing until all available inputs are read completely.
Read every policy file listed in `{resolved_policy_inputs}` in full before
creating the handoff package.

### Step 1b - Apply technical specifications when present

Check for these paths after reading the required inputs. When they exist, treat
them as authoritative. Do not regenerate equivalent detail from scratch.

If `{workspace_root}/technical-specifications/api/exposed/` exists and contains files:
- Read each exposed API spec.
- Use the exact endpoint paths, methods, request and response fields, auth
  mechanism, and SLA values in `delivery-spec.md` and `implementation-plan.md`.

If `{workspace_root}/technical-specifications/api/consumed/` exists and contains files:
- Read each consumed API spec.
- List external system dependencies with provider path, auth, PII minimization
  constraints, and fallback behavior in `implementation-plan.md`.

If `{workspace_root}/technical-specifications/data/` exists and contains files:
- Read the relevant data schema spec.
- Use the exact entity names, field names, types, and constraints in
  `delivery-spec.md`.
- Note any PII fields and retention policy.

If `{workspace_root}/technical-specifications/integrations/` exists and contains files:
- Read the integration spec for each external system.
- Populate timeout, retry, fallback, and observability details in
  `implementation-plan.md` from the integration spec rather than estimating.

### Step 2 - Create the handoff package

Create all five mandatory files under each deliverable folder:
- `delivery-spec.md`
- `implementation-plan.md`
- `tasks.md`
- `validation-plan.md`
- `review-checklist.md`

Keep story-level granularity and explicit FR, AC, AR, and relevant `NFR-NNN`
traceability.

### Step 3 - Make the package explicitly AI-agent ready

Use the five files together as the AI coding handoff package.

The package must make these items explicit:
- business context and expected business outcome
- technical context and architecture boundaries
- acceptance criteria and key traceability links
- non-functional and compliance constraints
- likely impacted files, modules, services, interfaces, and data stores
- test expectations, including regression and NFR verification
- explicit do-not-touch boundaries

## Output requirements

Follow the structure described in `.b2s/artifact-templates/standalone-handoff.md`.

## Done criteria

- [ ] all five files exist
- [ ] planning is story-level, not epic-only
- [ ] tasks are concrete engineering actions
- [ ] the package is self-contained enough for a coding agent to execute
- [ ] impacted areas and do-not-touch boundaries are explicit
- [ ] NFR expectations are carried into implementation and validation
