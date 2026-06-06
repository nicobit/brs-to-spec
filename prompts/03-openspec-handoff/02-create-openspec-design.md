# Prompt — Create OpenSpec Design

Recommended environment:
- VS Code Copilot Chat

Owner:
- Architect / Tech Lead / Senior Developer

Repository access is strongly recommended.

You are a senior engineer creating an OpenSpec-style design document.

Input files:
- `features/<feature-name>/openspec-change/proposal.md`
- `features/<feature-name>/engineering-contracts/technical-spec.md`
- `features/<feature-name>/engineering-contracts/bdd-scenarios.md`
- `features/<feature-name>/engineering-contracts/test-strategy.md`

Task:
Create the design document that engineers and Copilot will use during implementation.

Rules:
- Follow existing architecture.
- Do not invent new components unless explicitly justified.
- Include API, data, security, audit, testing, observability, and compatibility details.
- Include diagrams where helpful.
- Mark open decisions clearly.

Output:
Create `features/<feature-name>/openspec-change/design.md`.

Structure:

```markdown
# Design — <feature name>

## Overview
## Architecture Context
## Component Changes
## Data Changes
## API / Event Changes
## UI Changes
## Security and Authorization
## Audit and Logging
## Error Handling
## Observability
## Configuration
## Backward Compatibility
## Test Approach
## Open Decisions
## Diagrams
```

Also read if available:

```text
features/<feature-name>/business-intake/brs-architecture-alignment.md
```

The design should explicitly address or defer the alignment findings.

## Mandatory use of architecture alignment

If this file exists, read it:

```text
features/<feature-name>/business-intake/brs-architecture-alignment.md
```

The design must explicitly address or defer the alignment findings.
Do not let unresolved alignment issues disappear.

## Architecture & Contract Extensions

Resolve or reference relevant architecture-contract artifacts: ADRs, API/OpenAPI, domain model, data model, event contracts, quality scenarios, and threat model mitigations.

## Boundary note

This prompt can be used in two ways:

```text
1. Standalone mode
   This project remains the source of truth for engineering execution.

2. Adapter mode
   Use this only to create OpenSpec-native or OpenSpec-like artifacts from the handoff package.
```

If an external downstream framework is used, avoid maintaining a second competing task plan in this repository.
