# 01 — Extract Capabilities from BRS

You are a senior business analyst and product architect.

## Input

Read:

- `/input/brs.md`
- `/input/architecture.md` if available
- `.github/instructions/brs-traceability.instructions.md`
- `.github/instructions/output-format.instructions.md`

## Goal

Extract business capabilities from the BRS.

## Important Rules

- Do not create epics yet.
- Do not create user stories yet.
- Do not follow the BRS section structure blindly.
- Group requirements by business capability and business outcome.
- Preserve traceability to the BRS.
- Separate facts, assumptions, risks, and open questions.

## Output

Create:

```text
/output/01-extracted-capabilities.md
```

Use this structure:

# Extracted Capabilities

## 1. Business Goals

For each goal include:

- Goal ID
- Goal
- Business value
- Source reference
- Confidence: High / Medium / Low

## 2. Personas / User Groups

For each persona include:

- Persona ID
- Name
- Description
- Responsibilities
- Main needs
- Related BRS references
- Confidence

## 3. Business Processes

For each process include:

- Process ID
- Process name
- Trigger
- Main steps
- Actors
- Systems involved
- Data used/created
- Source reference

## 4. Business Capabilities

For each capability include:

- Capability ID, for example CAP-001
- Capability name
- Business outcome
- Users involved
- Main process supported
- Related business rules
- Related data entities
- Related systems
- Related NFRs
- Source references from the BRS
- Open questions
- Confidence: High / Medium / Low

## 5. Cross-Cutting Concerns

Identify requirements related to:

- Security
- Authorization
- Audit
- Reporting
- Notifications
- Integration
- Data migration
- Compliance
- Monitoring
- Operations
- Performance
- Availability

For each concern include:

- Concern ID
- Description
- Affected capabilities
- Source reference
- Confidence

## 6. Data Entities

For each entity include:

- Entity name
- Description
- Key attributes if known
- Lifecycle/state if known
- Used by capabilities
- Source reference

## 7. External Systems / Integrations

For each system include:

- System name
- Purpose
- Data exchanged
- Direction: inbound/outbound/bidirectional
- Related capabilities
- Source reference

## 8. Open Questions

List ambiguities, contradictions, missing information, and assumptions.

For each question include:

- Question ID
- Question
- Affected capability/process/story area
- Severity: High / Medium / Low
- Why it matters

## 9. Initial Delivery Risks

For each risk include:

- Risk ID
- Description
- Impact
- Mitigation suggestion
- Source or reason

## Quality Bar

The output must be precise enough to generate epics later.
