# BDD Scenarios — F-{{NNN}}: {{Feature Name}}

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Feature | F-{{NNN}} |
| Story count | N |
| Scenario count | N |
| Created at | {{date}} |
| Created by event | {{event_id}} |
| Status | In progress |

## Story-to-Scenario Mapping

| Story | Scenarios |
|---|---|
| F-{{NNN}}.1 | SCN-NNN, SCN-NNN |
| F-{{NNN}}.2 | SCN-NNN |

---

## SCN-NNN — {{Scenario Name}}

| Field | Value |
|---|---|
| ID | SCN-NNN |
| Story | F-XXX.X |
| Requirement | FR-NNN |
| AC | AC-NNN |
| Type | Happy path / Failure / Authorization / State transition / Async / Dry-run |
| Priority | Must / Should / Could |

```gherkin
Scenario: {{Scenario name}}
  Given {{system state before the action}}
  When {{one specific action}}
  Then {{observable outcome}}
  And {{additional observable outcome if needed}}
```

---

## SCN-NNN — {{Scenario Name}}

| Field | Value |
|---|---|
| ID | SCN-NNN |
| Story | F-XXX.X |
| Requirement | FR-NNN |
| AC | AC-NNN |
| Type | Failure |
| Priority | Must |

```gherkin
Scenario: {{Scenario name — failure case}}
  Given {{system state before the action}}
  When {{action that triggers the failure}}
  Then {{observable failure outcome}}
```

---
*Status: In progress — set to Accepted by QA gate owner after review. Never self-accept.*
