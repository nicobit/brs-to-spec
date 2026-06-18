# BDD Scenarios - F-{{NNN}}: {{Feature Name}}

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Feature | F-{{NNN}} |
| Story count | N |
| Scenario count | N |
| Created at | {{date}} |
| Created by | qa-analyst |
| Status | In progress |

## Story-to-Scenario Mapping

| Story | Scenarios |
|---|---|
| F-{{NNN}}.1 | SCN-NNN, SCN-NNN |

---

## SCN-NNN - Scenario Name

| Field | Value |
|---|---|
| ID | SCN-NNN |
| Story | F-XXX.X |
| Requirement | FR-NNN |
| AC | AC-NNN |
| Type | Happy path / Failure / Authorization / State transition / Async / Dry-run |
| Priority | Must / Should / Could |

```gherkin
Scenario: Scenario name
  Given system state before the action
  When one specific action occurs
  Then an observable outcome is produced
  And any additional observable outcome is verified
```

---

## Scenario Quality Checklist

Before marking this file complete, verify each scenario:

- [ ] Written in valid Given/When/Then Gherkin
- [ ] Scenario name describes the business situation, not the implementation
- [ ] Then clause is observable and specific (not "it works" or "it succeeds")
- [ ] Linked to AC-NNN
- [ ] Linked to story ID (F-XXX.X)
- [ ] Happy path covered per story
- [ ] Negative/validation path covered per story
- [ ] Authorization scenario present where roles exist
- [ ] State transition scenario present where workflow states exist
- [ ] Integration failure scenario present where external calls exist
- [ ] Audit scenario present where compliance is required

---
*Status: In progress - set to Accepted by the QA gate owner. Never self-accept.*
