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

## Execution artifact guidelines

Prompts fed to LLMs (`.github/prompts/`, `.brs2spec/skills/8-copilot-implementation/`) are
execution artifacts — they are sensitive to model upgrades. A new model version is a
change of interpreter. Apply these rules to keep execution artifacts durable:

**Constraints first.** Hard rules and the quality bar must appear before any narrative
description. The model reads top-down — what it reads first shapes everything after.
A prompt that buries its constraints in section 5 will produce inconsistent output as
models change.

**Short over long.** Prefer constraint lists over narrative paragraphs. Every sentence
of narrative is an additional interpretation surface. If a rule can be expressed as a
bullet, express it as a bullet.

**Anchor to IDs, not prose.** Done criteria and traceability references must use
machine-verifiable IDs (SCN-NNN, FR-NNN, REQ-NNN), not prose descriptions. A prompt
that says "implement the login feature" is less stable than one that says "implement
the behavior covered by SCN-004 and SCN-005".

**Treat a model upgrade as a regression trigger.** After upgrading the model, run a
smoke test on the 2–3 most-used execution prompts and compare output structure to a
known-good previous run. If sections are missing or reordered, tighten the prompt.

See [Artifact Durability](23-artifact-durability.md) for the full classification of
human vs execution artifacts and the upgrade strategy for each.
