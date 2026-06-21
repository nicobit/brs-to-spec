# Stories for {{Feature ID}} — {{Feature Title}}

## Metadata

| Field | Value |
|---|---|
| Feature | {{feature_id}} — {{feature_title}} |
| Parent Epic | {{epic_id}} — {{epic_title}} |
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by | delivery-lead |
| Status | Draft |

---

## Summary

| Metric | Value |
|---|---|
| Total stories | N |
| Must | N |
| Should | N |
| Could | N |

---

## Story Catalogue

### {{Story ID}} — {{Story Title}}

| Field | Value |
|---|---|
| User Story | As a {{actor}}, I want to {{action}}, so that {{outcome}}. |
| Business Context | {{2–3 sentences: why this story matters}} |
| Linked Requirements | REQ-NNN, REQ-NNN |
| Linked Business Rules | BR-NNN, BR-NNN |
| Linked Capability | CAP-NNN |
| Actor | {{actor name — specific role, not "user"}} |
| Primary Component | {{component name from architecture review}} |
| Impacted API | {{endpoint or API surface, if applicable}} |
| Impacted Data / Entity | {{entity or table, if applicable}} |
| Impacted Integration | {{external system, if applicable}} |
| Architecture Constraints | AR-NNN |
| Priority | Must / Should / Could |
| Increment | D1 / D2 |
| Out of Scope | {{one sentence: what a developer might assume is included but is not}} |
| Dependencies | {{story or external dependency}} |
| Open Questions | {{questions specific to this story}} |
| Readiness | Ready / Not Ready |

#### Acceptance Criteria

- **AC-001:** Given {{precondition}}, When {{action}}, Then {{outcome}}
- **AC-002:** Given {{precondition}}, When {{action}}, Then {{outcome}}

#### Notes

{{Additional context for implementation.}}

---

## Story Traceability

| Story | Requirements | Business Rules | Capability | Component | Readiness |
|---|---|---|---|---|---|
| {{story_id}} | REQ-NNN | BR-NNN | CAP-NNN | {{component}} | Ready / Not Ready |

---

## Not Ready Stories

| Story | Reason | Required Action |
|---|---|---|
| | | |

---
*Generate one file per feature. Each story must be independently testable and sized for one focused implementation session. Set Status: Accepted only after story quality gate. Never self-accept.*
