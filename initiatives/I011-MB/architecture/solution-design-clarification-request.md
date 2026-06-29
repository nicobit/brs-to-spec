# Solution Design Clarification Request

## Summary

Delivery planning is blocked by a small set of unresolved repository, CI, and API contract questions. Answers are required to assign target repositories, CI pipelines, and to finalize API contracts before work can be split into implementation tasks.

## Blocking Questions

| ID | Component / Boundary | Decision Area | Question | Why It Matters | Required For |
|---|---|---|---|---|---|
| SDQ-001 | Repository mapping | repository / ownership | Please provide the canonical repository names and CI pipeline identifiers for: Intake API, Scoring Service, Underwriter UI, Offer Generator, Notification pipeline, Payment orchestration adapter | Required to populate Repository Summary and to plan delivery (scoping, owners, pipelines) | delivery-planning / repository inventory |
| SDQ-002 | Scoring explainability contract | contract / schema | Confirm the API contract for `/scores/{id}` explainability payload (fields, storage reference, retention) | Required to mark the explainability bindings as `confirmed` and to implement storage schema and UI rendering | SD-002, D-002, UI-002 |
| SDQ-003 | Temenos T24 integration | integration / protocol | Confirm Temenos T24 integration contract (SOAP vs REST) and expected transaction semantics | Required to design the adapter and ensure operational bindings and retry semantics | SD-006, SD-004 |

## Answer Instructions

Record answers in:

```text
input/clarifications/solution-design.yaml
```

Use the clarification input schema expected by the framework. Do not edit this request artifact manually.

## Resolution Rule

After answers are captured in `input/clarifications/solution-design.yaml`, rerun solution decision generation so the architecture decisions incorporate the clarifications before delivery planning continues.

## No other blockers

The items above are the only blocking solution-design questions identified. Once answered, the architecture decisions can be finalized and delivery planning can proceed.

Contact: Delivery Lead
