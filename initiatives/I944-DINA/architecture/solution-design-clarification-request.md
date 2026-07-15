 # Solution Design Clarification Request

## Summary

The following unresolved, delivery-planning-blocking question must be answered before we can finalize repository-level decisions and proceed with delivery planning.

This clarifies whether the onchain registry is ever intended to be the legal source-of-truth or if the offchain investor registry remains authoritative. Legal confirmation or product policy is required because the answer affects data residency, evidence capture, reconciliation responsibilities, and contractual language that must be embedded in delivery artifacts.

Please provide a concise, authoritative decision (yes/no/conditional) and any constraints or timelines that affect implementation choices.

## Blocking Questions

| ID | Component / Boundary | Decision Area | Question | Why It Matters | Required For |
|---|---|---|---|---|---|
| SDQ-001 | Investor Registry / Onchain registry | Source-of-truth | Does the onchain registry ever become the legal source-of-truth? | If onchain becomes legal source, data residency, ownership, reconciliation, and legal controls change significantly; contracts and evidence strategies must be adapted. | delivery-planning |

## Answer Instructions

Record answers in:

```text
input/clarifications/solution-design.yaml
```


Provide concise, authoritative responses including any legal guidance, acceptance criteria, and timelines for changes if applicable.

Suggested respondents: Legal, Product, Head of Operations. Suggested deadline: 5 business days to avoid blocking delivery planning.
Contact the architect (architect) if clarification on wording is needed.
Thank you for responding promptly.

## Resolution Rule

After answers are captured, rerun `create-solution-decisions` so the architecture decisions incorporate the clarifications before delivery planning continues.
