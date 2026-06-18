# Business Test Expectations

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by event | {{event_id}} |
| Status | Draft |

## BTE Catalog

| BTE-NNN | Title | Actor | Priority | FR Source | AC Source |
|---|---|---|---|---|---|
| BTE-001 | | {{role}} / ACT-NNN | Must / Should / Could | FR-NNN | AC-NNN |

---

## BTE-001: {{Title}}

**Actor:** {{business role name or ACT-NNN}}  
**Priority:** Must / Should / Could  
**FR source:** FR-NNN  
**AC source:** AC-NNN

**Pre-state:** {{what state the system must be in before the test}}

**Action:** {{what the actor does — business language, no technical steps}}

**Expected outcome:** {{what is observable after the action — what you see, receive, or state that changes}}

**Failure signal:** {{what would indicate this expectation is NOT met}}

---

## Coverage Map

| FR-NNN | BTE-NNN(s) | Coverage type |
|---|---|---|
| FR-001 | BTE-001, BTE-002 | Happy path + failure |
| FR-002 | BTE-003 | Happy path |

---
*Set Status: Accepted after product owner or business stakeholder sign-off. Do not self-accept.*
