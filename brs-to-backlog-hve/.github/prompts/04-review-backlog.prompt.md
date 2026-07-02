# 04 — Review Backlog Quality

You are a delivery lead, QA lead, product owner, and solution architect reviewing backlog quality.

## Input

Read:

- `/input/brs.md`
- `/input/architecture.md` if available
- `/output/01-extracted-capabilities.md`
- `/output/02-candidate-epics.md`
- `/output/03-candidate-stories.md`
- `.github/instructions/backlog-governance.instructions.md`
- `.github/instructions/story-quality.instructions.md`
- `.github/instructions/brs-traceability.instructions.md`

## Goal

Review the generated backlog before it is moved to GitHub.

## Check For

1. Missing BRS requirements
2. Requirements not mapped to capabilities, epics, or stories
3. Duplicated epics or stories
4. Epics that are too broad
5. Stories that are too large
6. Stories that are too vague
7. Stories that are too technical
8. Missing personas
9. Missing business rules
10. Missing exception flows
11. Missing acceptance criteria
12. Missing NFRs
13. Missing integration requirements
14. Missing audit, security, compliance, and reporting requirements
15. Weak traceability
16. Open questions that block delivery
17. Architecture constraints not reflected in stories
18. Testability problems

## Output

Create:

```text
/output/04-backlog-review.md
```

Use this structure:

# Backlog Review

## 1. Overall Assessment

Give one decision:

- Ready for GitHub backlog creation
- Needs minor fixes
- Needs major fixes
- Not ready

Explain why.

## 2. Coverage Review

| BRS Area | Covered by Capability | Covered by Epic | Covered by Story | Gap |
|---|---|---|---|---|

## 3. Issues Found

For each issue include:

- Issue ID
- Severity: High / Medium / Low
- Description
- Affected epic/story
- Recommendation

## 4. Missing Epics

List any missing epics.

## 5. Missing Stories

List any missing stories.

## 6. Stories to Split

List stories that are too large and suggest a better split.

## 7. Stories to Merge

List duplicated or overlapping stories.

## 8. Acceptance Criteria Improvements

List stories with weak or incomplete acceptance criteria.

## 9. Traceability Problems

List missing or weak BRS references.

## 10. Security / Audit / Compliance Gaps

List any missing security, audit, compliance, privacy, regulatory, or evidence requirements.

## 11. Integration and Architecture Gaps

List missing integration, architecture, deployment, operations, monitoring, or support requirements.

## 12. Final Recommended Backlog Changes

Create a clear action list.

## 13. Final Decision

Say whether the backlog is ready to move into GitHub.
