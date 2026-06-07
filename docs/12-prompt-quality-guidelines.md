# Prompt Quality Guidelines

v1.0.3 improves prompt quality without changing the framework structure.

## Goal

Prompts should produce outputs that are:

```text
specific
evidence-based
traceable
decision-oriented
risk-aware
actionable
reviewable
```

## Prompt quality rules

Every core prompt should include:

| Prompt section | Purpose |
|---|---|
| Role | Forces the model to act from a specific expert viewpoint |
| Context | Clarifies where this prompt sits in the workflow |
| Inputs | Identifies required and optional artifacts |
| Output path | Makes the output location explicit |
| Required structure | Prevents free-form vague output |
| Quality bar | Defines what a good answer must contain |
| Anti-patterns | Prevents shallow or generic answers |
| Self-review checklist | Forces the model to validate its own output |
| Stop conditions | Prevents hallucination when inputs are missing |

## Anti-generic-output rule

Do not accept outputs like:

```text
Looks good.
No major issues.
Add tests.
Architecture is aligned.
Security should be considered.
```

Prefer outputs that include:

```text
evidence
risk
owner
required action
required-before stage
traceability to requirement or architecture constraint
```

## Stop condition rule

If the prompt lacks enough input to produce a reliable answer, it should not invent details.

It should produce:

```text
Missing input
Impact
Owner / question to resolve
Recommended next step
```

## Traceability rule

Important conclusions must refer to at least one of:

```text
requirement ID
architecture constraint ID
business objective
deliverable ID
quality gate
source section
```

## Decision rule

Every review-like prompt must produce a decision:

```text
Approved
Approved with risks
Not approved
Ready
Ready with risks
Not ready
```

## Actionability rule

Every finding should have:

```text
severity
evidence
risk
recommendation
owner
required-before stage
```
