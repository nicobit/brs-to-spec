# Downstream Framework Selection

After the handoff package is created, decide whether to use OpenSpec, GitHub Spec Kit, Kiro, or standalone mode.

| Situation | Recommended mode |
|---|---|
| Team already uses OpenSpec | Handoff to OpenSpec |
| Team uses GitHub Spec Kit | Handoff to Spec Kit |
| Team uses Kiro | Handoff to Kiro |
| No downstream SDD framework is available | Standalone mode |
| Need quick pilot without new tooling | Standalone mode |
| Need enterprise BRS normalization only | Handoff mode |
| Need full local process and prompts | Standalone mode |

## Important rule

Do not duplicate execution ownership.

After handoff:
- downstream framework owns implementation tasks and execution,
- this framework remains the upstream evidence and decision trail.

# gstack Selection

Use gstack when the team wants role-based challenge and review around:
- product/CEO view,
- engineering plan,
- design/UX,
- QA,
- security,
- documentation,
- release/shipping.

gstack can be used as:
- the downstream execution/review layer,
- or a reviewer around OpenSpec / Spec Kit / Kiro / standalone mode.

Updated decision table:

| Situation | Recommended mode |
|---|---|
| Need formal spec/task framework | OpenSpec or GitHub Spec Kit |
| Need productized IDE spec workflow | Kiro |
| Need role-based review, QA, security, release challenge | gstack |
| Need no external framework | Standalone |
| Need both formal tasks and strong review | OpenSpec/Spec Kit/Kiro + gstack review |
