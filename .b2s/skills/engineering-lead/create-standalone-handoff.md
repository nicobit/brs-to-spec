# Skill - Create Standalone Handoff

## Identity

```text
skill_id:    engineering-lead.create-standalone-handoff
persona:     engineering-lead
action_id:   create-standalone-handoff
produces:    standalone-delivery/
```

## When this skill is used

Run this only when the execution mode is `Standalone`, readiness is `Ready`, and all triggered gates are accepted.

## Preconditions

Before starting, verify:
- `engineering-readiness/readiness-check.md` is `Ready`
- all triggered gates are accepted
- `planning/delivery-structure.md` has story IDs
- `architecture/architecture-review.md` exists
- `architecture/architecture-rules.md` exists

## Instructions

### Step 1 - Read all inputs

Read these files in full before writing anything:
- `{workspace_root}/engineering-readiness/readiness-check.md`
- `{workspace_root}/planning/delivery-structure.md`
- `{workspace_root}/architecture/architecture-review.md`
- `{workspace_root}/architecture/architecture-rules.md`
- `{resolved_optional_inputs}` — technical-specification artifacts when workflow type is `technical-spec-modular`

Do not start writing until all available inputs are read completely.

### Step 1b - Apply technical specifications when present

Check for these paths after reading the required inputs. When they exist, treat them as **authoritative**. Do not regenerate equivalent detail from scratch.

**If `{workspace_root}/technical-specifications/api/exposed/` exists and contains files:**
- Read each exposed API spec file.
- Use the exact endpoint paths, methods, request/response fields, auth mechanism, and SLA values in `delivery-spec.md` and `implementation-plan.md`.
- Do not invent endpoint contracts; copy from the spec verbatim.

**If `{workspace_root}/technical-specifications/api/consumed/` exists and contains files:**
- Read each consumed API spec.
- List external system dependencies with provider path, auth, PII minimisation constraints, and fallback behaviour in `implementation-plan.md`.

**If `{workspace_root}/technical-specifications/data/` exists and contains files:**
- Read the data schema spec for the relevant domain.
- Use the exact entity names, field names, types, and constraints in `delivery-spec.md`. Do not invent field names.
- Note any PII fields and retention policy.

**If `{workspace_root}/technical-specifications/integrations/` exists and contains files:**
- Read the integration spec for each external system.
- Populate timeout, retry, fallback, and observability details in `implementation-plan.md` from the integration spec rather than estimating.

**When technical-spec artifacts are present, do not re-derive fields they already define. Use the spec value verbatim.**

### Step 2 - Create all five mandatory files under a deliverable folder:
- `delivery-spec.md`
- `implementation-plan.md`
- `tasks.md`
- `validation-plan.md`
- `review-checklist.md`

Keep story-level granularity and explicit FR/AC/AR traceability.

## Output requirements

Follow the structure described in `.b2s/artifact-templates/standalone-handoff.md`.

## Done criteria

- [ ] all five files exist
- [ ] planning is story-level, not epic-only
- [ ] tasks are concrete engineering actions
