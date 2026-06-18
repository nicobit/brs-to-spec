# Feature {{F-NNN.N}} — {{Feature name}}

> Parent epic: {{E-NNN}} — {{epic title}}
> Source requirements: {{FR-NNN, FR-NNN}}
> Business value: {{one sentence}}

## Feature description

{{2–3 sentences: what this feature delivers, who uses it, what problem it solves.}}

## User stories

<!-- Draft stage: stories may be stubs. Confirmed stage: every story must be fully formed per the done criteria below. -->

### {{F-NNN.N}}-1 — {{Story title}}

**As a** `ACT-NNN <persona name>`, **I want** {{capability}}, **so that** {{business value}}.

| Field | Value |
|---|---|
| Story ID | F-NNN.N-1 |
| Source requirement | FR-NNN |
| Business rules | BR-NNN — {{rule summary}}; or "Business rules: none apply — [reason]" |
| Acceptance criteria | See below |
| Architecture constraints | {{AR-NNN or component name}} |
| Likely quality gates | BDD / Security / API contract / Data contract |

#### Acceptance criteria

<!-- Copy verbatim from input/brs.md — do not paraphrase. One row per testable statement. -->
<!-- Complex / regulated / SLA / integration stories require at least 3 ACs. -->

| AC ID | Criterion |
|---|---|
| AC-NNN | {{verbatim text from BRS}} |
| AC-NNN | {{verbatim text from BRS}} |

---

<!-- Add more stories using the same structure above. -->
<!-- If this feature has only one story, add a justification: -->
<!-- > Single-story justification: {{reason why further splitting is not needed at this stage}} -->

## Existing-system impact

Include only if this feature changes or depends on an existing component.

| Area | Impact | Validation expectation |
|---|---|---|
| {{component}} | {{impact}} | {{test or contract needed}} |

## Notes

{{Constraints, open questions, or risks specific to this feature.}}
