# Use Case Specifications

> **Consumer:** Business analysts, QA, product owner, architects
> **Purpose:** Structured UC-XXX specs mapping business goals to system behaviour — richer than user stories, narrower than full test cases
> **Generated from:** `planning/delivery-structure.md`, `input/brs.md`, `business-intake/business-rules.md`, `review-package/01-business-analysis/actors-and-personas.md`

## Metadata

| Field | Value |
|---|---|
| Initiative |  |
| Version |  |
| Last updated |  |

---

<!-- One section per use case. A use case is a complete user goal, not a single screen action. -->
<!-- Map each use case to one or more F-XXX.X user stories. Multiple stories may implement one use case. -->
<!-- Derive use cases from: BRS functional requirements groups; epic-level goals in delivery-structure.md. -->

## UC-001 — {{Use Case Name}}

| Field | Value |
|---|---|
| ID | UC-001 |
| Name | {{Goal-oriented name — "Verb + Object", e.g. "Submit Loan Application"}} |
| Primary actor | {{ACT-NNN from actors-and-personas.md}} |
| Supporting actors | {{ACT-NNN, SYS-NNN — or "none"}} |
| Goal | {{One sentence: what the primary actor achieves}} |
| Scope | {{Which system boundary this use case lives in}} |
| Related requirements | {{FR-NNN, FR-NNN}} |
| Related stories | {{F-NNN.N, F-NNN.N}} |
| Priority | Must / Should / Could |
| Status | Draft / Reviewed / Accepted |

### Preconditions

<!-- What must be true before the actor can start this use case. -->

1. 

### Main success scenario

<!-- Numbered steps. Each step is one observable action by actor or system. -->
<!-- No implementation detail — describe WHAT happens, not HOW. -->
<!-- Keep each step to one action. If a step has a condition, break it into an alternative flow. -->

| Step | Actor / System | Action |
|---|---|---|
| 1 | {{Actor}} | |
| 2 | System | |
| 3 | {{Actor}} | |

### Postconditions

<!-- What is true when the use case completes successfully. Observable outcomes only. -->

1. 

### Alternative flows

#### AF-001.1 — {{Alternative name}} (triggered at step N if {{condition}})

| Step | Actor / System | Action |
|---|---|---|
| 1 | System | |

**Outcome:** {{Where this alternative flow ends — back to main flow at step N, or terminates with error.}}

### Exception flows

#### EX-001.1 — {{Exception name}} (triggered at step N if {{error condition}})

| Step | Actor / System | Action |
|---|---|---|
| 1 | System | Display error: "{{message}}" |
| 2 | {{Actor}} | Correct input and retry from step N |

### Business rules applied

<!-- Only BR-NNN rules that directly govern behaviour in this use case. -->

| Rule ID | Rule | Applied at step |
|---|---|---|
| BR-NNN | | |

### Acceptance criteria covered

<!-- AC-NNN IDs from story.md that this use case's scenarios verify. -->

| AC ID | Criterion | Covered by |
|---|---|---|
| AC-NNN | | Main flow step N / AF-001.1 / EX-001.1 |

---

## UC-002 — {{Use Case Name}}

<!-- Copy section above -->
