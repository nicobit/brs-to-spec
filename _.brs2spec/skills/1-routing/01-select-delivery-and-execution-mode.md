# Prompt - Select Delivery and Execution Mode

## Hard constraints

- Select the **smallest safe workflow** — do not default to Enterprise or Enterprise + Modular without score evidence
- Do not make OpenSpec the default — only select it when it is actually available and in use
- Do not treat Fast Path as permission to skip readiness or triggered quality gates
- Do not give a decision without evidence for each criterion
- Do not recommend all prompts by default — explicitly exclude those not needed
- Do not hide uncertainty — state it with impact

## Execution mode selection rules

Select **OpenSpec** when ALL of the following are true:
- The initiative has ≥5 functional requirements OR spans more than one team / service boundary
- The BRS has identifiable user-facing features that can be broken into `F-XXX.X` user stories
- The output will be consumed by engineers or AI coding agents implementing discrete stories

Select **Standalone** only when:
- The initiative is a single-team, single-service change with fewer than 5 FRs, OR
- The team explicitly does not use OpenSpec tooling and needs a flat task list

Select **Business Copilot** only when:
- The output is for a business user or non-technical stakeholder, not for engineers

**Default for a new initiative with a real BRS (≥5 FRs, multiple features): OpenSpec.**
The constraint "do not make OpenSpec the default" means do not blindly apply it to trivial changes — it does not mean prefer Standalone for substantial initiatives.

## Stop conditions

- If required inputs are missing, do not invent content
- List missing inputs, explain the impact, and continue only for sections supported by available inputs

## Role

You are a delivery architect deciding the minimum safe process for an enterprise initiative.

## Inputs

```text
input/brs.md or input/brs/*.md
input/architecture.md or input/architecture/*.md   (optional)
input/input-package.md
```

## Output path

```text
state/routing-decision.md
```

## Required output structure

```markdown
# Routing Decision

## Decision Summary

| Decision | Selected value | Reason | Confidence |
|---|---|---|---|
| Delivery mode | Fast / Standard / Enterprise / Enterprise + Modular |  |  |
| Execution mode | OpenSpec / Standalone / Business Copilot |  |  |
| Small-change path applicable? | Yes / No |  |  |

## Delivery Mode Assessment

| Criterion | Low / Medium / High | Evidence | Impact |
|---|---|---|---|
| Requirement ambiguity |  |  |  |
| Architecture impact |  |  |  |
| Compliance / audit relevance |  |  |  |
| Business criticality |  |  |  |
| Number of teams |  |  |  |
| Delivery size |  |  |  |
| AI context saturation risk |  |  |  |
| Change narrow enough for small-change path |  |  |  |
| Regression / contract sensitivity despite small scope |  |  |  |

## Execution Mode Assessment

| Criterion | OpenSpec | Standalone | Business Copilot |
|---|---|---|---|
| Available in project? |  |  |  |
| Recommended? |  |  |  |
| Reason |  |  |  |

## Required Next Prompts

| Step | Prompt | Required? | Reason |
|---|---|---|---|

## Prompts Not Needed

| Prompt | Reason not needed |
|---|---|

## Risks of Under-Processing

## Risks of Over-Processing

## Small-Change Path Notes

| Item | Decision / note |
|---|---|
| Is Fast Path acceptable? |  |
| Minimum required artifacts |  |
| Readiness still required? |  |
| Gates that still may trigger |  |
```

## Quality bar

- Delivery mode and execution mode are both selected with evidence
- Each criterion includes specific evidence from the BRS or architecture input — not generic statements
- Unnecessary prompts are explicitly excluded with a reason
- Small-change applicability is stated explicitly
- Under-processing and over-processing risks are both described
- The recommendation is practical for a real project

## Self-review checklist

- [ ] Delivery mode and execution mode are both selected
- [ ] Each major criterion includes evidence from the inputs
- [ ] Unnecessary prompts are explicitly excluded
- [ ] Small-change applicability is stated explicitly
- [ ] Under-processing and over-processing risks are both described
- [ ] No criterion is left blank without a reason
