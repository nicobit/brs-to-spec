# gstack Brief

## 1. Purpose

Use gstack to challenge the onboarding feature plan and review implementation readiness.

## 2. Recommended gstack Usage Mode

gstack as reviewer around standalone mode.

## 3. Context Files to Provide

| File | Why gstack needs it |
|---|---|
| `handoff/spec-driven-handoff.md` | Primary context |
| `business-intake/requirements.md` | Business and system requirements |
| `business-intake/brs-architecture-alignment.md` | Architecture constraints and missing decisions |
| `architecture-contracts/api-contract.md` | API expectations |
| `architecture-contracts/domain-model.md` | Status workflow and business invariants |
| `architecture-contracts/threat-model.md` | Authorization and audit risks |

## 8. Risks and Open Questions

- Initial onboarding status must be confirmed.
- Audit payload fields must be confirmed.

## 9. Suggested gstack Skill Sequence

| Step | Suggested gstack skill | Purpose | Input context | Expected output |
|---|---|---|---|---|
| 1 | `/plan-eng-review` | Challenge implementation plan | Handoff + contracts | Engineering review findings |
| 2 | `/plan-design-review` | Challenge workflow/user interaction | User stories + API contract | Design review findings |
| 3 | `/cso` | Security challenge | Threat model + requirements | Security findings |
| 4 | `/qa` | Test readiness | Stories + acceptance criteria | QA gaps |
| 5 | `/ship` | Release readiness | Enablement + handoff | Ship/no-ship view |
