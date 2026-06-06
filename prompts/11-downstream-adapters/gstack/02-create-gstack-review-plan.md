# Adapter Prompt — Create gstack Review Plan

Use this after creating `handoff/gstack-brief.md`.

Input files:
- `features/<feature-name>/handoff/gstack-brief.md`
- `features/<feature-name>/handoff/spec-driven-handoff.md`
- Downstream artifacts if available, such as OpenSpec / Spec Kit / Kiro / standalone tasks
- PR diff or implementation plan if available

Task:
Create a role-based review plan for gstack.

Output:
Create:

```text
features/<feature-name>/handoff/gstack-review-plan.md
```

Use this structure:

```markdown
# gstack Review Plan

## 1. Review Objective

## 2. Review Sequence

| Order | Role / gstack skill | Review focus | Required context | Blocks shipping? |
|---|---|---|---|---|

## 3. CEO / Product Review

Questions:
- Does the proposed implementation match the business objective?
- Is scope controlled?
- Are risks acceptable?

## 4. Engineering Review

Questions:
- Is the design implementable?
- Are dependencies clear?
- Are tasks correctly sliced?
- Are architecture contracts respected?

## 5. Design / UX Review

Questions:
- Are user interactions clear?
- Are edge cases covered?
- Are error states defined?

## 6. QA Review

Questions:
- Are acceptance criteria testable?
- Are negative paths covered?
- Are integration and regression risks covered?

## 7. Security Review

Questions:
- Are authorization and data protection requirements implemented?
- Are threat-model mitigations covered?
- Are secrets and credentials handled safely?

## 8. Release / Shipping Review

Questions:
- Is rollout clear?
- Is rollback clear?
- Are operational checks ready?
- Are docs/release notes ready?

## 9. Final Go / No-Go Criteria
```

Rules:
- Keep reviews tied to actual source artifacts.
- Do not create generic review questions only.
- Mark which review findings block shipping.
