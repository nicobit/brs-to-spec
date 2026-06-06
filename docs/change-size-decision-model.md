# Change Size Decision Model

Use this guide to decide how much of the framework to apply.

The goal is to avoid unnecessary bureaucracy while keeping enough control for risky changes.

## Summary

```text
Small change  → Minimal flow
Medium change → Add BDD + test strategy
Large/risky change → Full framework
```

## Small Change — Minimal Flow

Use this for:

```text
small UI text changes
simple validation rule
small API change with no integration impact
minor bug fix with clear expected behavior
small configuration change
low-risk internal improvement
```

Use these artifacts:

```text
business-intake/
  brs-summary.md                optional if input is already clear
  requirements.md
  epics-and-features.md          lightweight, can contain one feature only
  user-stories.md
  gaps-and-questions.md

engineering-contracts/
  technical-spec.md             lightweight

openspec-change/
  proposal.md
  design.md                     lightweight
  tasks.md
```

Optional:

```text
business-test-expectations.md
```

Do not force:

```text
full test strategy
full test plan
full traceability matrix
formal architecture contract
formal API/event contracts
```

## Medium Change — BDD + Test Strategy Flow

Use this for:

```text
new feature in an existing module
moderate backend + frontend change
new workflow step
changes with role-based behavior
changes with non-trivial validation
changes that need QA planning
```

Use all small-change artifacts plus:

```text
engineering-contracts/
  bdd-scenarios.md
  test-strategy.md
```

Optional depending on risk:

```text
test-plan.md
traceability-matrix.md
```

## Large / Risky Change — Full Framework

Use this for:

```text
regulated feature
client-data-impacting feature
audit/compliance-heavy feature
security-sensitive change
cross-system integration
database migration with risk
new service / major architecture change
external API/event contract
performance-sensitive change
multi-team delivery
high business impact
```

Use the full artifact set:

```text
business-intake/
  brs-summary.md
  requirements.md
  epics-and-features.md
  user-stories.md
  gaps-and-questions.md
  business-test-expectations.md

engineering-contracts/
  technical-spec.md
  bdd-scenarios.md
  test-strategy.md
  test-plan.md
  traceability-matrix.md

openspec-change/
  proposal.md
  design.md
  tasks.md

quality-gates/
  business-ready-checklist.md
  engineering-ready-checklist.md
  ready-for-copilot-checklist.md

reviews/
  code-review.md
  qa-review.md
  architecture-review.md
```

Add specific security or release reviews where required.

## Decision Questions

Answer these before choosing the flow.

| Question | If yes |
|---|---|
| Does it affect client/customer data? | Large/risky |
| Does it affect authorization or roles? | Medium or Large |
| Does it affect audit/compliance/regulatory evidence? | Large/risky |
| Does it add or change integrations? | Medium or Large |
| Does it require database migration? | Medium or Large |
| Does it affect multiple teams or systems? | Large/risky |
| Is expected behavior already very clear? | Small possible |
| Is QA/UAT needed beyond developer testing? | Medium or Large |
| Could a mistake cause financial, regulatory, security, or client impact? | Large/risky |

## Default rule

If unsure, choose **Medium**.

Use **Large/Risky** only when the additional artifacts genuinely reduce risk.

Use **Small** only when the change is genuinely low risk and well understood.

## Anti-pattern

Do not apply the full framework to every small change.

That creates process fatigue and people will stop using the system.

## Recommended adoption

Start with:

```text
1 real small change
1 real medium feature
1 real risky feature
```

Then adjust the artifact set based on what actually helped.
