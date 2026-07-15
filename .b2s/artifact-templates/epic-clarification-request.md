# Epic Clarification Request - {{epic_id}}

## Summary

{{Write one short paragraph explaining whether this epic has blocking questions that must be resolved before story generation can proceed safely.}}

## Blocking Questions

| ID | Route | Page | Blocker Type | Question | Why It Matters Now | Blocks Next Artifact | Required For |
|---|---|---|---|---|---|---|---|
| {{UIQ-NNN}} | {{/route}} | {{Page Name}} | {{missing-evidence / missing-decision / missing-ownership / missing-user-intent}} | {{question}} | {{why story generation is unsafe without the answer now}} | {{implementation-contract refresh / S-NNN.N story generation}} | {{story generation / contract refresh}} |

If no blocking questions remain, write:

```text
No blocking questions require clarification for this epic.
```

## Answer Instructions

Record answers in:

```text
input/clarifications/{{epic_id}}.yaml
```

Use the clarification input schema expected by the framework. Do not edit this request artifact manually.

## Resolution Rule

After answers are captured, rerun the current epic shell generation so the implementation contract can incorporate the clarifications before story generation continues.
