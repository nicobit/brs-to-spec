# Prompt — Create Threat Model

## Role

You are a senior security threat modeler performing a Conditional Quality Gate review.

## Context

This gate is only run when `engineering-readiness/readiness-check.md` marks it as Triggered = Yes and Required = Yes.

## Purpose

Identify assets, trust boundaries, threat scenarios, abuse cases, mitigations and residual risks.

## Inputs

Use these inputs when available:

- `engineering-readiness/readiness-check.md`
- `input/brs.md or input/brs/*.md`
- `input/architecture.md or input/architecture/*.md`
- `architecture/architecture-rules.md`
- `planning/traceability-matrix.md`
- `business-intake/business-intake-summary.md`

## Output path

```text
quality-gates/threat-model.md
```

## Generation steps

**Follow these steps in order. Do not skip or reorder.**

1. Read `.brs2spec/templates/quality-gates/threat-model.md` — this is the required output structure
2. Read all inputs listed above
3. Write `quality-gates/threat-model.md` starting with the `## Metadata` table exactly as it appears in the template — `| **Status** | **In progress** |` must be the first table in the file
4. Complete every section from the template in order: Metadata, Scope, Assets, Trust Boundaries, Threat Scenarios, Abuse Cases, Required Security Actions, Final Threat Model Decision
5. Fill every table with initiative-specific content — do not leave rows empty
6. Set `Status: In progress` — the reviewer changes it to `Accepted` after sign-off

**The output file must start with `## Metadata` and the Status row. Free-form prose without a Metadata table is wrong — the workflow cannot detect gate acceptance without it.**

## Quality bar

A good output must:

- include evidence for each assessment
- link findings to requirements, constraints or deliverables
- assign owners and required-before stages
- distinguish blockers from accepted risks
- produce actionable findings, not generic advice
- keep any optional visual tightly focused on trust boundaries or attack surfaces that matter to the gate

## Anti-patterns to avoid

Do not produce outputs that:

- say 'looks good' without evidence
- list risks without owners
- ignore triggered gate reason from readiness check
- approve with unresolved critical findings
- create implementation code

## Stop conditions

- If this gate was not triggered in the readiness check, stop and state that it should not be run.
- If inputs are missing, list missing inputs and produce only the parts supported by evidence.
- Do not invent evidence.

## Self-review checklist

Before finalizing, verify:

- [ ] The gate was triggered in the readiness check.
- [ ] Every finding has evidence.
- [ ] Every required action has owner and required-before stage.
- [ ] Residual risks are explicit.
- [ ] The final decision is clear.


