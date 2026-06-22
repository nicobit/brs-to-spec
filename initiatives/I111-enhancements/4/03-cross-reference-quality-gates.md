# Enhancement 3 — Cross-Reference Quality Gates to Business Analysis

## Problem

Quality gate skills each read their own inputs in isolation. None of them cross-references the business analysis layer:

- `create-bdd-scenarios.md` reads delivery-structure and BRS but not process flows (`business-analysis/process-flows.md`) or business rules (`business-intake/business-rules.md`). Scenarios are authored without knowing which process flow they exercise or which BR creates the decision branch being tested.

- `create-api-contract.md` does not reference `business-analysis/actors-and-personas.md`. API endpoints list consumers as free text ("applicant", "underwriter") without tying them to ACT-NNN IDs and their authorization profiles.

- `create-data-contract.md` does not reference `business-analysis/entity-model.md` when it exists. Schema tables in the contract are authored independently from the entity model, creating divergence.

The result: gates accepted in isolation that do not form a coherent picture. BDD scenarios test flows that do not match process flow branches. API contracts name actors that do not match the actor registry. Data contracts diverge from entity model attributes.

## What needs to change

### Change 1 — `skills/4-engineering-readiness/quality-gates/create-bdd-scenarios.md`

**Add to the Inputs section:**

```
- `business-analysis/process-flows.md` — if exists: PF-NNN flows with decision points and alternative paths; use these to derive alternative flow scenarios and branch-condition scenarios; do not invent branching logic that is not in the process flows
- `business-intake/business-rules.md` — if exists: BR-NNN rules; every scenario that exercises a decision point must cite the BR-NNN that drives it in the scenario title or a comment
```

**Add to the generation rules (new subsection):**

```
### Process flow traceability

For every feature file (`F-NNN.md`), identify the corresponding PF-NNN process flow from `business-analysis/process-flows.md`.

- If a PF-NNN exists for this epic: the feature file must include at least one scenario per decision point in that process flow. Each such scenario title must reference the PF-NNN and the decision point (e.g. `Scenario: PF-001 Step 4 — application rejected when DTI exceeds 43% (BR-005)`)
- If a PF-NNN does not exist yet: note the gap in the acceptance-checklist.md coverage table with `<!-- Process flow PF-NNN not yet authored — scenarios cover BRS narrative only -->`

For every decision-point scenario (Given/When/Then where the outcome differs based on a business rule):
- Add a comment line above the scenario: `# BR-NNN: <rule text excerpt>`
- This makes the business rule driving the branch explicit and reviewable by the PO
```

**Add to the Self-review checklist:**

```
- [ ] Every decision-point scenario cites a BR-NNN in a comment — no invented branch conditions
- [ ] Every feature file notes its corresponding PF-NNN or explicitly records the gap
```

---

### Change 2 — `skills/4-engineering-readiness/quality-gates/create-api-contract.md`

**Add to the Inputs section (or create it if absent):**

```
- `business-analysis/actors-and-personas.md` — if exists: ACT-NNN IDs and authorization profiles; every API endpoint must name its caller(s) using ACT-NNN IDs
```

**Add to the endpoint definition rules (new requirement):**

```
### Actor-endpoint traceability

For every endpoint defined in the API contract:
- The "Consumers" or "Callers" field must reference the `ACT-NNN` ID(s) from `business-analysis/actors-and-personas.md`, not a free-text role name
- The authorization level must be consistent with the authorization boundary defined for that ACT-NNN in actors-and-personas.md
- Example: `Caller: ACT-001 Applicant (unauthenticated — public endpoint)`; `Caller: ACT-003 Underwriter (requires role: underwriter-role)`

If `business-analysis/actors-and-personas.md` does not exist yet: use free-text role names but add a note: `<!-- ACT-NNN reference to be added when actors-and-personas.md is authored -->`
```

**Add to the Self-review checklist:**

```
- [ ] Every endpoint names its caller(s) using ACT-NNN IDs from actors-and-personas.md (or notes the gap)
- [ ] Authorization level per endpoint is consistent with the actor's permission profile
```

---

### Change 3 — `skills/4-engineering-readiness/quality-gates/create-data-contract.md`

**Add to the Inputs section (or create it if absent):**

```
- `business-analysis/entity-model.md` — if exists: ER diagram and attribute tables are the authoritative domain view; schema tables in the data contract must be consistent with entity model attribute tables for the same entity; flag any divergence explicitly
```

**Add to the schema table rules (new requirement):**

```
### Entity model consistency

If `business-analysis/entity-model.md` exists:
- For every entity whose data contract schema is defined in this gate: compare the attribute table with the entity model attribute table for the same entity
- If they are consistent: add a traceability note in the schema section: `<!-- Consistent with entity-model.md: <EntityName> -->`
- If they diverge (e.g. different field names, different types, missing fields): flag the divergence explicitly: `<!-- DIVERGENCE from entity-model.md: field X is VARCHAR(100) here but VARCHAR(255) in entity-model — resolve before handoff -->`
- Do not silently choose one over the other — surface the divergence so it can be resolved

If `business-analysis/entity-model.md` does not exist yet: note it in the gate metadata: `<!-- Entity model not yet authored — schema tables inferred from BRS; validate against entity model when created -->`
```

**Add to the Self-review checklist:**

```
- [ ] Every schema table has been checked against entity-model.md (or gap noted)
- [ ] Any divergence between data contract and entity model is flagged explicitly — not silently resolved
```

## Implementation steps

1. Open `.brs2spec/skills/4-engineering-readiness/quality-gates/create-bdd-scenarios.md`
   - Add `business-analysis/process-flows.md` and `business-intake/business-rules.md` to Inputs
   - Add the "Process flow traceability" subsection to generation rules
   - Add two items to Self-review checklist

2. Open `.brs2spec/skills/4-engineering-readiness/quality-gates/create-api-contract.md` (or equivalent path)
   - Add `business-analysis/actors-and-personas.md` to Inputs
   - Add the "Actor-endpoint traceability" subsection
   - Add two items to Self-review checklist

3. Open `.brs2spec/skills/4-engineering-readiness/quality-gates/create-data-contract.md` (or equivalent path)
   - Add `business-analysis/entity-model.md` to Inputs
   - Add the "Entity model consistency" subsection
   - Add two items to Self-review checklist

## Quality bar

After this change:
- A BDD feature file with no PF-NNN reference and no gap note fails its self-review
- A BDD decision-point scenario with no BR-NNN comment fails its self-review
- An API contract endpoint that names "applicant" (free text) instead of "ACT-001 Applicant" fails its self-review (when actors-and-personas.md exists)
- A data contract with schema tables that diverge from entity-model.md without an explicit divergence flag fails its self-review
