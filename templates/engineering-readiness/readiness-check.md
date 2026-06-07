# Engineering Readiness Check

## Metadata

| Field | Value |
|---|---|
| Initiative / Feature |  |
| Active deliverable |  |
| Delivery mode |  |
| Execution mode |  |
| Reviewer |  |
| Review date |  |
| Source BRS version |  |
| Architecture version |  |

## Readiness Decision

| Decision | Value |
|---|---|
| Status | Ready / Ready with risks / Not ready |
| Decision owner |  |
| Decision date |  |
| Conditions / caveats |  |

## Decision Rationale

## Core Checklist

| Area | Status | Evidence | Gap / Risk | Required action | Owner | Required before |
|---|---|---|---|---|---|---|
| Business scope clear |  |  |  |  |  | Handoff |
| Requirements traceable |  |  |  |  |  | Handoff |
| Initial architecture reviewed |  |  |  |  |  | Handoff |
| Architecture constraints applied |  |  |  |  |  | Implementation |
| Architecture conflicts resolved or accepted |  |  |  |  |  | Implementation |
| Governed service / API boundaries identified |  |  |  |  |  | Handoff |
| Governed data boundaries identified |  |  |  |  |  | Handoff |
| Governed event boundaries identified |  |  |  |  |  | Handoff |
| Impacted modules known |  |  |  |  |  | Implementation |
| Acceptance expectations clear |  |  |  |  |  | Implementation |
| Validation approach clear |  |  |  |  |  | Implementation |
| Dependencies known |  |  |  |  |  | Implementation |
| Open questions assigned |  |  |  |  |  | Handoff |

## Governed Boundary Assessment

| Boundary ID | Boundary type | Producer / Owner | Consumer(s) | Created / Changed? | External or cross-team? | Governed contract needed? | Expected gate |
|---|---|---|---|---|---|---|---|

Use this section to make contract boundaries explicit.

Typical expectation:

- governed service / API boundary -> `API contract`
- governed data ownership or schema boundary -> `Data contract`
- governed asynchronous event boundary -> `Event contract`

## Conditional Quality Gates

| Quality Gate | Triggered? | Required? | Trigger evidence | Risk if skipped | Owner | Required before | Output |
|---|---|---|---|---|---|---|---|
| BDD scenarios |  |  |  |  | PO/QA | Implementation | `quality-gates/bdd-scenarios.md` |
| Test strategy |  |  |  |  | QA | Implementation | `quality-gates/test-strategy.md` |
| QA review |  |  |  |  | QA | Merge | `quality-gates/qa-review.md` |
| Architecture review |  |  |  |  | Architect | Implementation | `quality-gates/architecture-review.md` |
| Security review |  |  |  |  | Security/Architect | Implementation/Merge | `quality-gates/security-review.md` |
| Release readiness review |  |  |  |  | Dev/QA/SRE | Release | `quality-gates/release-readiness-review.md` |
| API contract |  |  |  |  | Engineering | Implementation | `quality-gates/api-contract.md` |
| Data contract |  |  |  |  | Engineering/DB | Implementation | `quality-gates/data-contract.md` |
| Event contract |  |  |  |  | Engineering | Implementation | `quality-gates/event-contract.md` |
| Threat model |  |  |  |  | Security/Architect | Implementation | `quality-gates/threat-model.md` |
| Observability plan |  |  |  |  | SRE/Engineering | Release | `quality-gates/observability-plan.md` |

When a governed boundary exists in the section above, the matching contract gate should normally be triggered unless an explicit justification says otherwise.

## Blocking Issues

| Issue ID | Severity | Description | Evidence | Owner | Required action | Required before |
|---|---|---|---|---|---|---|

## Accepted Risks

| Risk ID | Risk | Impact | Mitigation | Accepted by | Expiry / Review date |
|---|---|---|---|---|---|

## Required Actions Before Handoff

| Action ID | Action | Owner | Required before | Status |
|---|---|---|---|---|

## Recommended Handoff

| Field | Value |
|---|---|
| Execution mode | OpenSpec / Standalone / Business Copilot |
| Reason |  |
| Active deliverable only? | Yes / No |
