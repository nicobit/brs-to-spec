# BDD Scenarios — Feature {{F-NNN}}: {{Feature name}}

> Gherkin scenarios for all user stories in feature {{F-NNN}}.
> One file per feature. Full scenario set: happy path, failure, boundary, authorization.
> Primary consumer: QA, engineering lead, coding agent (`/opsx:apply`)
> SCN-NNN IDs are sequential across the entire initiative — check `acceptance-checklist.md` for the global sequence.

## Coverage summary — Feature {{F-NNN}}

| Scenario ID | Story ID | Requirement ID | Business rule | Scenario type | Priority | Status |
|---|---|---|---|---|---|---|
| SCN-NNN | F-NNN.X | FR-NNN | | Happy path | Must | Draft |

---

## Scenarios by user story

---

### F-NNN.X — {{User story name}}

> As a {{role}}, I want {{capability}}, so that {{outcome}}.
> Requirement: {{FR-NNN}}
> AC location: `input/brs.md` § {{section}} or inline below

#### SCN-NNN — {{Scenario name}} (Happy path)

| Field | Value |
|---|---|
| Story | F-NNN.X |
| Requirement | FR-NNN |
| AC | AC-NNN |
| Scenario type | Happy path |
| Priority | Must |

```gherkin
Given ...
When ...
Then ...
```

#### SCN-NNN — {{Scenario name}} (Failure / negative)

| Field | Value |
|---|---|
| Story | F-NNN.X |
| Requirement | FR-NNN |
| AC | AC-NNN |
| Scenario type | Negative |
| Priority | Must |

```gherkin
Given ...
When ...
Then ...
```

#### SCN-NNN — {{Scenario name}} (Authorization / boundary)

| Field | Value |
|---|---|
| Story | F-NNN.X |
| Requirement | FR-NNN |
| AC | AC-NNN |
| Scenario type | Authorization |
| Priority | Should |

```gherkin
Given ...
When ...
Then ...
```

---

## Coverage gaps and open questions — Feature {{F-NNN}}

| Question ID | Story | Question | Impact | Owner | Answer |
|---|---|---|---|---|---|
