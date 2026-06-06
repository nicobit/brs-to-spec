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