# Solution Design Clarification Request

## Summary

{{Write one short paragraph explaining whether delivery-planning-blocking solution-design questions must be answered before delivery planning can proceed safely.}}

## Blocking Questions

| ID | Component / Boundary | Decision Area | Blocker Type | Question | Why It Matters Now | Blocks Next Artifact | Required For |
|---|---|---|---|---|---|---|---|
| {{SDQ-NNN}} | {{component or boundary}} | {{repository / ownership / contract / integration / UI ownership}} | {{missing-evidence / missing-decision / missing-ownership / missing-user-intent}} | {{question}} | {{why delivery planning is unsafe without the answer now}} | {{solution-decisions refresh / delivery-skeleton.md}} | {{solution decisions refresh / delivery planning}} |

If no delivery-planning-blocking questions remain, write:

```text
No blocking solution design questions require clarification.
```

## Answer Instructions

Record answers in:

```text
input/clarifications/solution-design.yaml
```

Use the clarification input schema expected by the framework. Do not edit this request artifact manually.

## Resolution Rule

After answers are captured, rerun solution decision generation so the architecture decisions incorporate the clarifications before delivery planning continues. Questions deferred to epic elaboration or coding handoff should remain traceable in the source artifacts and must not be silently treated as resolved.
