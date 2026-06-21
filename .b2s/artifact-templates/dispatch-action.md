# Dispatch: Next Action

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by | orchestrator |
| Status | Draft |

---

## Recommended Action

| Field | Value |
|---|---|
| Action Type | REQUEST_BUSINESS_CLARIFICATION / REQUEST_ARCHITECTURE_DECISION / REFINE_REQUIREMENTS / REFINE_EPIC / REFINE_FEATURE / REFINE_STORY / GENERATE_MISSING_BDD / GENERATE_HANDOFF / READY_FOR_AI_IMPLEMENTATION / READY_FOR_HUMAN_REVIEW / STOP_BLOCKED |
| Target Artifact | {{artifact path or story ID}} |
| Assigned Persona | {{persona who should act}} |
| Reason | {{why this action was selected}} |
| Required Input | {{artifacts needed}} |
| Expected Output | {{what the action should produce}} |
| Blocking Condition | {{what blocks this action, if anything}} |
| Recommended Prompt | {{skill or prompt to run next}} |

---

## Dispatch Rationale

{{2–4 sentences explaining why this is the smallest useful next action and why alternatives were not selected.}}

---

## Dispatch Log Entry

| Field | Value |
|---|---|
| Timestamp | {{ISO timestamp}} |
| Previous Phase | {{phase that just completed}} |
| Decision | {{action type selected}} |
| Reason | {{one sentence}} |
| Next Persona | {{persona}} |
| Next Artifact | {{target artifact}} |

---

## Persona Message

### To: {{Persona Name}}

### Context

{{Brief context about the initiative state and what has been completed.}}

### Task

{{Specific task to perform.}}

### Inputs

{{List of artifacts to read before acting.}}

### Expected Output

{{What artifact or decision is expected.}}

### Constraints

{{Rules from the delivery constitution or architecture that apply.}}

---
*This artifact routes workflow progression. The dispatcher selects the smallest useful next action. Set Status: Accepted automatically on dispatch. Do not self-accept if blocked.*
