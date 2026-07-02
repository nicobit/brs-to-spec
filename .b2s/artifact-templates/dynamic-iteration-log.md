# Iteration Log — {{initiative_id}}

## Goal State

*Derived from input/brs.md on iteration 1. Referenced on all subsequent iterations.*

**Initiative:** {{initiative title}}

**Final objective:** An AI coding assistant can implement every capability
in this initiative without asking a single clarifying question.

### Capabilities to implement (in order)

| # | Capability | Source requirements | Status |
|---|---|---|---|
| 1 | {{capability name}} | {{FR-NNN, FR-NNN}} | pending / in-progress / done |

### Technology and architecture constraints

{{Derived from input/brs.md and input/architecture.md. List concrete constraints
that apply across all coding packages: stack, cloud provider, data residency,
security model, compliance frameworks, enterprise contracts.}}

### Best practices mandatory for this initiative type

{{Domain-appropriate non-negotiables the orchestrator will enforce without being
asked. Examples:
- regulated/fintech: idempotency keys, immutable audit log, explainable AI,
  circuit breakers on all external calls, GDPR right-to-erasure compatible model
- event-driven: at-least-once delivery, dead-letter handling, ordering guarantees
- multi-tenant: data isolation, per-tenant RBAC
- public API: versioning, rate limiting, contract stability}}

### Open questions blocking implementation

| ID | Question | Blocks | Owner |
|---|---|---|---|
| OQ-NNN | {{specific question a developer would ask}} | {{capability or FR}} | {{owner}} |

---

## Iteration {{N}}

| Field | Value |
|---|---|
| Date | {{date}} |
| Gap closed | {{specific gap — name the FR, capability, or contract that was missing}} |
| Artifact produced | {{path/to/artifact}} |
| Confidence delta | {{what dimension improved and from what to what}} |
| Next gap | {{specific next gap — same format as gap closed}} |
| Continue | {{yes / no — reason if no}} |

### Reasoning

{{One short paragraph: why this gap was chosen, what the artifact resolves,
and what a developer can now do that they could not do before.}}

---

*(Repeat ## Iteration N block for each loop cycle)*
