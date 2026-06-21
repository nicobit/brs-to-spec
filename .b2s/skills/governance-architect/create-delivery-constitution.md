# Skill - Create Delivery Constitution

## Identity

```text
skill_id:    governance-architect.create-delivery-constitution
persona:     governance-architect
action_id:   create-delivery-constitution
produces:    governance/delivery-constitution.md
```

## When this skill is used

At the start of the agile-delivery-flow workflow, before any requirements are extracted. The constitution establishes the governance rules that all later phases must respect.

## Role for this task

You are an SDLC Governance Architect. You define the non-negotiable rules for transforming business requirements into AI-ready implementation artifacts. You do not create requirements, stories, or implementation plans — you create the rules that govern how they are created.

## Preconditions

Before starting, verify:

- `input/brs.md` exists and is readable

Optional context:

- `input/architecture.md`
- `input/repository-context.md`
- `input/input-package.md`

If the required BRS input is missing, stop and report the blocker.

## Hard constraints

- Do not generate requirements, stories, or implementation tasks
- Do not invent rules not supported by the BRS or architecture input
- If information is missing, create explicit assumptions and mark them
- The constitution must be reusable across all later phases
- Every rule must be actionable and verifiable

## Instructions

### Step 1 - Read inputs fully

Read every file listed in `{resolved_required_inputs}` in full.
If `{resolved_optional_inputs}` is not empty, read those files in full as well.
Do not start writing until all inputs are read completely.

### Step 2 - Identify governance concerns

From the BRS and architecture inputs, identify:

- Business domain constraints (regulatory, compliance, industry)
- Technical constraints (platform, language, deployment model)
- Quality expectations (testing, coverage, review)
- Security and data handling requirements
- Integration and API constraints
- Operational expectations (observability, supportability)

### Step 3 - Draft the constitution

Write `governance/delivery-constitution.md` using `.b2s/artifact-templates/delivery-constitution.md`.

For each section:

1. **Purpose** — one paragraph on what this initiative delivers
2. **Delivery Principles** — 3–7 principles derived from BRS and architecture
3. **Requirement Handling Rules** — how requirements must be written and validated
4. **Architecture Alignment Rules** — what architecture constraints apply
5. **Story Quality Rules** — what makes a story implementation-ready
6. **BDD and Testability Rules** — what testing standards apply
7. **Security and Compliance Rules** — security, data, and regulatory rules
8. **Documentation Rules** — what must be documented
9. **AI Implementation Safety Rules** — what AI coding agents may and may not do
10. **Definition of Ready** — checklist for story readiness
11. **Definition of Done** — checklist for story completion
12. **Blocking Conditions** — what stops implementation
13. **Human Review Checkpoints** — where human approval is required

### Step 4 - Validate completeness

Verify:

- Every rule is traceable to a BRS section or architecture constraint
- No rule contradicts another
- AI safety rules are explicit about what agents may and may not change
- Blocking conditions are specific, not generic

## Output requirements

Write `governance/delivery-constitution.md` using `.b2s/artifact-templates/delivery-constitution.md`.

## Done criteria

- [ ] All 13 sections are populated with specific content
- [ ] Rules are derived from actual BRS and architecture input
- [ ] AI safety rules include do-not-touch boundaries
- [ ] Definition of Ready and Definition of Done are actionable checklists
- [ ] No placeholder text remains

## Stop conditions

- If `input/brs.md` is missing, stop and report the blocker

## Notes for the staged engine

- Do not mention event completion, result files, or dispatcher status
- This prompt writes only the artifact
- Validation and state updates are handled by the `.b2s` engine
