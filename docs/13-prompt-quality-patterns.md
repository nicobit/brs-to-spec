# Prompt Quality Patterns

## Recommended prompt pattern

Each prompt should follow this structure:

```text
Role
Context
Purpose
Inputs
Output path
Required output structure
Quality bar
Anti-patterns
Stop conditions
Self-review checklist
```

## Why this matters

Weak prompts produce plausible but shallow artifacts.

Strong prompts force the model to:

```text
show evidence
preserve traceability
make decisions explicit
identify risks
assign owners
state what blocks implementation, merge, or release
```

## Self-review questions

Every generated artifact should be checked against:

```text
Is the decision explicit?
Is evidence provided?
Are risks visible?
Are actions assigned?
Are required-before stages clear?
Is traceability preserved?
Are assumptions separated from facts?
```
