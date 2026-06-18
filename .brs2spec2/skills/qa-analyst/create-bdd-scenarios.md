# Skill — Create BDD Scenarios

## Identity

| Field | Value |
|---|---|
| skill_id | qa-create-bdd-scenarios |
| persona | qa-analyst |
| event_types | CREATE_BDD_SCENARIOS |
| produces | quality-gates/bdd/ (one file per feature) |

## When this skill is used

Conditional quality gate — triggered only when `engineering-readiness/readiness-check.md` marks BDD Triggered = Yes and Required = Yes.

BDD trigger conditions (ANY of these triggers the gate):
- The initiative has role-based authorization rules
- The initiative has multi-step workflows or state transitions
- The initiative has async execution paths (202 Accepted + polling)
- The initiative has dry-run, preview, or confirmation flows
- The initiative has exception paths or retry/recovery flows
- The initiative has complex validation rules derived from business rules

## Role for this task

You are a senior QA analyst writing executable BDD scenarios that specify the observable behaviour of each user story — making acceptance criteria testable, failure paths explicit, and implementation boundaries clear.

## Prerequisites check

Before starting, verify:
- [ ] `engineering-readiness/readiness-check.md` marks BDD gate as Triggered = Yes
- [ ] `planning/delivery-structure.md` exists with F-XXX.X story IDs
- [ ] `input/brs.md` (or `input/brs/*.md`) is readable (AC-NNN source)
- [ ] `business-intake/business-intake-summary.md` exists
- [ ] `business-analysis/business-rules.md` exists (BR-NNN for scenario guards)
- [ ] `business-analysis/actors-and-personas.md` exists (ACT-NNN for scenario actors)

If this gate was NOT triggered in the readiness check: stop and state that BDD scenarios should not be authored for this initiative.

## Instructions

### Step 1 — Read all inputs before writing any scenario

Read the full BRS, business-rules, actors-and-personas, and delivery-structure before writing the first scenario. Cross-file consistency of IDs (FR-NNN, BR-NNN, ACT-NNN, AC-NNN) requires reading everything first.

### Step 2 — Assign scenario IDs

Scenarios are assigned sequential SCN-NNN IDs across the full initiative (not per-feature). Start at SCN-001 and increment per scenario.

### Step 3 — Generate scenarios per feature

For each feature (F-NNN) in the delivery structure, create one file at:
`quality-gates/bdd/F-NNN.md`

For each user story (F-NNN.X) within the feature, write:
- **Minimum:** one happy-path scenario + one failure/negative scenario
- **High-risk stories** (async, RBAC, dry-run, state transitions, export): add additional scenarios per the BDD minimum counts below

BDD minimum counts:
- RBAC story: one scenario per role (authorized + unauthorized)
- Async story: happy path + polling path + timeout/failure path
- Dry-run story: dry-run execution + commit execution + abort path
- State transition story: one scenario per valid transition + one invalid transition attempt
- Complex validation story: one per significant BR-NNN validation rule

### Step 4 — For each scenario, write full Gherkin

Each scenario must have:

**Metadata block (before the Gherkin code block):**
```
| Field | Value |
|---|---|
| ID | SCN-NNN |
| Story | F-XXX.X |
| Requirement | FR-NNN |
| AC | AC-NNN (the specific AC this scenario validates) |
| Type | Happy path / Failure / Authorization / State transition / Async / Dry-run |
| Priority | Must / Should / Could |
```

**Gherkin block:**
```gherkin
Scenario: [Scenario name]
  Given [system state before the action — not "the user is on a page"]
  When [one specific action — one When per scenario]
  Then [observable outcome — what can be verified]
  And [additional observable outcome if needed]
```

Gherkin rules:
- `Given` — world state before the action; no implementation details
- `When` — exactly one action per scenario; split if two actions are needed
- `Then` — observable outcome only (what you can see, read, or verify)
- `And` — extends the nearest Given, When, or Then
- Every `Then` must be verifiable without implementation knowledge
- Each scenario's `AC` field must be the specific AC it validates — not a shared generic AC across all scenarios

### Step 5 — Write each feature file

Each `quality-gates/bdd/F-NNN.md` file:
1. Metadata table: Feature ID, Feature name, Story count, Scenario count, Status (In progress)
2. Story-to-scenario mapping table: F-NNN.X → SCN-NNN list
3. Full scenario block per SCN-NNN (metadata + Gherkin)

Set `Status: In progress` — the gate owner sets it to `Accepted` after review.

## Output requirements

- One file per feature: `quality-gates/bdd/F-NNN.md`
- Full Gherkin blocks — not scenario summaries or tables without Gherkin
- Every AC-NNN from the delivery structure covered by at least one SCN-NNN
- SCN-NNN IDs sequential across all feature files

## Done criteria

- [ ] Every F-NNN feature has a BDD file
- [ ] Every F-NNN.X story has at minimum one happy-path and one failure scenario
- [ ] High-risk stories have additional scenarios per the minimum counts
- [ ] Every SCN-NNN has a complete Gherkin block (Given/When/Then)
- [ ] Every SCN-NNN metadata block references the specific AC-NNN it validates
- [ ] SCN-NNN IDs are globally sequential (no duplicates across features)
- [ ] `Status: In progress` in each file's Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing all `quality-gates/bdd/F-NNN.md` files

## Stop conditions

- If the BDD gate was not triggered in the readiness check: stop immediately.
- If AC-NNN IDs are missing from the BRS: flag the gap and derive scenarios from FR text with noted assumptions.
- Do not write scenario summaries as BDD stubs — full Gherkin is required.
