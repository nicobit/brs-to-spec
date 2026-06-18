# Prompt — Extract Business Rules

## Role

You are a senior business analyst extracting and formalising business rules from the initiative BRS.

## Purpose

Produce `business-intake/business-rules.md` — a standalone, traceable list of every business rule in the BRS. Business rules are the logic, invariants, and constraints that govern how the system must behave, independent of implementation. They are the safety boundaries for the AI coding agent: a rule violated in code is a business defect, not just a bug.

## What is a business rule (vs a functional requirement)

| | Business rule | Functional requirement |
|---|---|---|
| What it expresses | An invariant or constraint that must always hold | A capability the system must provide |
| Example | "A subscription above CHF 1M requires dual approval" | "The system shall support subscription submission" |
| ID format | BR-NNN | FR-NNN |
| Source | Business policy, compliance, regulation | Stakeholder need |

Rules are often embedded inside FR descriptions, AC, or prose sections of the BRS. Extract them explicitly.

## Inputs

Read all of the following:

- `input/brs.md` or `input/brs/*.md` — primary source; read every section for embedded rules
- `business-intake/business-intake-summary.md` — actors, scope, objectives that help classify rules
- `input/architecture.md` — integration boundaries that impose technical rules

## Output path

```text
business-intake/business-rules.md
```

Use template: `.brs2spec/templates/business-intake/business-rules.md`

## Extraction rules

### What to extract as a BR-NNN rule

Extract a rule when you find:

- A threshold, limit, or numeric boundary (e.g. "above £10,000 requires manual review")
- A mandatory precondition before a state transition (e.g. "eligibility must pass before submission")
- An invariant that must hold regardless of user action (e.g. "every approval decision must be auditable")
- A role or permission boundary (e.g. "only Compliance role may override sanctions flags")
- A data retention or residency constraint (e.g. "PII must be stored in UK regions")
- An integration ordering rule (e.g. "KYC must complete before disbursement")
- A prohibition (e.g. "duplicate disbursement with same idempotency key must be rejected")

### What NOT to extract as a BR-NNN rule

Do not extract:

- UI layout or wording preferences
- Implementation choices (e.g. "use PostgreSQL")
- Performance targets (those belong in NFR-NNN)
- Generic good practices not specific to this initiative

### Rule quality bar

Each rule must be:
- **Verifiable** — a test can confirm whether the rule holds
- **Specific** — names actors, thresholds, or states; not "the system must be secure"
- **Traceable** — has a BRS section reference

## Output rules

- Assign BR-NNN IDs sequentially starting at BR-001
- Write the rule in plain business language — no technical jargon
- Map each rule to the features and stories it constrains (derive from delivery-structure.md)
- Group rules by category (eligibility, approval, data/audit, security, integration) when there are more than 5 rules
- Record open questions for any rule where the BRS is ambiguous

## Quality bar

A good output:
- covers every rule embedded in the BRS — none silently omitted
- uses verifiable, specific language — not "system must be compliant"
- traces every rule to a BRS section
- maps every rule to the feature(s) and story(ies) it constrains
- flags ambiguous rules as open questions rather than inventing an interpretation
- is reviewable by a non-technical PO in 15 minutes

## Anti-patterns

- Extracting functional requirements (FR-NNN) as business rules — they are different; do not duplicate
- Writing vague rules ("system must be secure", "data must be protected") with no testable threshold
- Omitting the BRS section reference — every rule must trace to a source
- Inventing rules not in the BRS — record as an open question if you suspect a rule exists but is not stated
- Omitting the impacted features/stories columns — these are mandatory for AI coding agent consumption

## Self-review checklist

Before finalising, verify:

- [ ] Every section of the BRS has been read and rules extracted where present
- [ ] Each rule is verifiable and specific — not generic compliance language
- [ ] Each rule has a BRS section reference
- [ ] Each rule maps to at least one feature or story ID
- [ ] Open questions are recorded for ambiguous rules
- [ ] No functional requirements (FR-NNN) appear as business rules
- [ ] Status is `In progress` — PO review required before marking Accepted
