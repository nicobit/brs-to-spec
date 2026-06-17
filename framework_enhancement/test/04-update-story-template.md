# Enhancement Prompt 04 — Update story.md Template

## What this prompt does

Edits `.brs2spec/templates/openspec-handoff/story.md` to:
1. Replace the inline BDD Gherkin section with a pointer to `quality-gates/bdd/`
2. Add a "Test plan" section pointing to `quality-gates/test-plans/`
3. Keep all other sections unchanged

## File to edit

```
.brs2spec/templates/openspec-handoff/story.md
```

## Change 1 — Replace the BDD scenarios section

Find this section in `story.md`:

```markdown
## BDD scenarios

<!-- Full Gherkin here — not a pointer to another file. -->
<!-- Minimum: one happy-path + one failure per story. -->
<!-- Add boundary and authorization scenarios where the AC implies them. -->
<!-- High-risk stories (async, RBAC, dry-run, state transitions, export): see authoring rules in create-bdd-scenarios.md for minimum counts. -->

### SCN-NNN — {{Scenario name}} (Happy path)

| Field | Value |
|---|---|
| Requirement | FR-NNN |
| AC | AC-NNN |
| Scenario type | Happy path |
| Priority | Must |

```gherkin
Given {{pre-condition: who is authenticated, what data exists, what the system state is}}
When {{one action the user or system takes}}
Then {{observable outcome — what the user sees or what the system records}}
And {{additional observable outcome if needed}}
```

### SCN-NNN — {{Scenario name}} (Failure / negative)

| Field | Value |
|---|---|
| Requirement | FR-NNN |
| AC | AC-NNN |
| Scenario type | Negative |
| Priority | Must |

```gherkin
Given ...
When ...
Then ...
```

### SCN-NNN — {{Scenario name}} (Boundary / authorization)

| Field | Value |
|---|---|
| Requirement | FR-NNN |
| AC | AC-NNN |
| Scenario type | Authorization |
| Priority | Should |

```gherkin
Given ...
When ...
Then ...
```
```

Replace it with:

```markdown
## BDD scenarios

<!-- BDD scenarios are authored in quality-gates/bdd/ — the single source of truth. -->
<!-- Do not copy Gherkin into this file — reference the scenarios below. -->
<!-- The coding-prompt.md and test-plan.md for this story reference the same SCN-NNN IDs. -->

**Canonical source:** `quality-gates/bdd/F-NNN.md` — section "F-XXX.X — {{User Story Name}}"

Scenarios in scope for this story:

| SCN-ID | Scenario name | Type | Priority | AC |
|---|---|---|---|---|
| SCN-NNN | {{scenario name}} | Happy path | Must | AC-NNN |
| SCN-NNN | {{scenario name}} | Failure / negative | Must | AC-NNN |
| SCN-NNN | {{scenario name}} | Boundary | Should | AC-NNN |
| SCN-NNN | {{scenario name}} | Authorization | Must | AC-NNN |

<!-- Fill the table from quality-gates/bdd/F-NNN.md coverage summary for this story. -->
<!-- Do not add rows that are not in the BDD file. Do not write Gherkin here. -->
```

## Change 2 — Add a "Test plan" section after BDD scenarios

After the new BDD scenarios section, insert:

```markdown
## Test plan

<!-- The test plan defines what will be tested, at what level, and with what priority for this story. -->
<!-- It is the output of the three-amigos session and is the contract the developer implements against. -->

**Full test plan:** `quality-gates/test-plans/{{F-XXX.X}}-test-plan.md`

### C1 — Critical (blocks merge)

<!-- Copy the C1 rows from quality-gates/test-plans/{{F-XXX.X}}-test-plan.md -->

| TC-ID | Test type | Condition | Expected outcome |
|---|---|---|---|
| TC-NNN | {{Unit / Integration / Security}} | {{condition}} | {{expected outcome}} |

### C2 — High (blocks sprint done)

| TC-ID | Test type | Condition | Expected outcome |
|---|---|---|---|
| TC-NNN | {{test type}} | {{condition}} | {{expected outcome}} |

<!-- C3 and C4 test cases are tracked in the full test plan — not repeated here. -->
<!-- Overall story risk: {{C1 / C2 / C3 / C4}} — see full test plan for rationale. -->
```

## Change 3 — Update the Acceptance criteria section comment

Find:
```markdown
<!-- Every AC must have at least one BDD scenario below, or an explicit note that it is verified by manual review. -->
```

Replace with:
```markdown
<!-- Every AC must have at least one BDD scenario (see BDD scenarios section) and at least one TC-NNN test case (see Test plan section), or an explicit note that it is verified by manual review. -->
```

## Self-review after applying

Verify:
- [ ] `## BDD scenarios` section no longer contains inline Gherkin blocks
- [ ] `## BDD scenarios` section has a canonical source pointer and a summary table (SCN-NNN, name, type, priority, AC)
- [ ] `## Test plan` section exists after BDD scenarios
- [ ] Test plan section has C1 and C2 tables with TC-NNN, test type, condition, expected outcome
- [ ] Test plan section has a pointer to the full `quality-gates/test-plans/` file
- [ ] AC section comment references both BDD scenarios and test plan
- [ ] No inline Gherkin remains in the template
