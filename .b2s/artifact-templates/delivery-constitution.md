# Delivery Constitution

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by | governance-architect |
| Status | Draft |

---

## 1. Purpose

{{One paragraph: what this initiative delivers and why this constitution exists.}}

---

## 2. Delivery Principles

| # | Principle | Rationale |
|---|---|---|
| 1 | | |

---

## 3. Requirement Handling Rules

| Rule | Description | Consequence of Violation |
|---|---|---|
| | | |

---

## 4. Architecture Alignment Rules

| Rule | Description | Applies To |
|---|---|---|
| | | |

---

## 5. Story Quality Rules

| Rule | Description | Check Method |
|---|---|---|
| | | |

---

## 6. BDD and Testability Rules

| Rule | Description | Applies To |
|---|---|---|
| | | |

---

## 7. Security and Compliance Rules

| Rule | Description | Source | Blocking? |
|---|---|---|---|
| | | | |

---

## 8. Documentation Rules

| Rule | Description | Applies To |
|---|---|---|
| | | |

---

## 9. AI Implementation Safety Rules

| Rule | Description | Rationale |
|---|---|---|
| Do not change architecture without an ADR | | |
| Do not make product decisions | | |
| Do not cross governed boundaries | | |
| Include do-not-touch rules in every handoff | | |

---

## 10. Definition of Ready

A story is ready for implementation when:

- [ ] Business goal is clear and specific
- [ ] Acceptance criteria are testable
- [ ] Architecture impact is understood
- [ ] Dependencies are explicit
- [ ] Security and compliance concerns are addressed
- [ ] BDD scenarios exist for happy path and negative cases
- [ ] Impacted files or areas are identified

---

## 11. Definition of Done

A story is done when:

- [ ] All acceptance criteria are implemented and verified
- [ ] All BDD scenarios pass
- [ ] Architecture constraints are respected
- [ ] No blocking open questions remain
- [ ] Regression risks are addressed
- [ ] Code review is complete

---

## 12. Blocking Conditions

Implementation must stop if:

| Condition | Resolution Path |
|---|---|
| Unresolved blocking gap | Escalate to product owner |
| Missing architecture decision | Create ADR |
| Security risk not assessed | Escalate to security reviewer |
| Story failed quality gate | Rewrite story |

---

## 13. Human Review Checkpoints

| Checkpoint | After Phase | Owner | Purpose |
|---|---|---|---|
| Requirements review | 1-requirements | product-owner | Validate requirement completeness and accuracy |
| Architecture review | 3-architecture-context | architect | Validate architecture fit and constraints |
| Story quality review | 6-story-quality-gate | qa-analyst | Validate stories are implementation-ready |
| Readiness review | 9-readiness-review | engineering-lead | Validate initiative is ready for AI implementation |

---

## 14. Advisory Reviews

Advisory reviews provide optional expert perspectives on artifacts before gate review. When enabled, each configured persona reviews the artifact through its specific lens (testability, infrastructure, security, architecture, UI) and produces structured findings. Findings are appended to the artifact but do not block the gate.

| Setting | Value |
|---|---|
| Advisory reviews enabled | Yes / No |

### Enabled Personas

| Persona | Lens | Activates when |
|---|---|---|
| qa-analyst | Testability, edge cases, AC quality | Always (if enabled) |
| devops-engineer | Infrastructure gaps, pipeline needs, enablers | Always (if enabled) |
| security-reviewer | Auth, encryption, data boundaries | Always (if enabled) |
| architect | Coupling, architecture rules, NFRs | Always (if enabled) |
| ui-ux-expert | UI states, validation UX, navigation, accessibility | Epic has Frontend stories |

To disable a specific persona, remove its row from the table above. To disable all advisory reviews, set "Advisory reviews enabled" to "No".

---
*This constitution governs all downstream phases. Every artifact must be validated against it. Set Status: Accepted only by human approval. Never self-accept.*
