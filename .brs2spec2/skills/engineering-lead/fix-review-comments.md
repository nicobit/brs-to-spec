# Skill — Fix Review Comments

## Identity

| Field | Value |
|---|---|
| skill_id | eng-fix-review-comments |
| persona | engineering-lead |
| event_types | FIX_REVIEW_COMMENTS |
| produces | code changes + reviews/implementation/task-{task-id}-review-fix-summary.md |

## When this skill is used

Post-review, when an engineer is implementing approved fixes for review findings on one already-implemented task. Tightens the implementation — does not reopen the feature or create new source-of-truth requirements.

## Hard constraints

- Address only the review findings approved for the current task — do not expand scope
- Do not reopen unrelated design decisions unless a finding explicitly requires it
- Do not implement future tasks
- Do not silently ignore a blocking review issue — surface it explicitly
- Do not remove tests without replacing the coverage
- Do not introduce new scope because a reviewer mentioned a broader idea
- If a finding conflicts with active source artifacts: stop and surface the conflict
- If a finding would expand scope beyond the approved task: stop and propose escalation

## Prerequisites check

Before starting, verify:
- Review findings are documented (from `reviews/implementation/*.md`)
- The task's implementation exists and is accessible
- The active source artifacts are accessible

## Instructions

### Step 1 — Load context

Load only what this fix needs:
- `engineering-readiness/initiative-context.md`
- The specific review file with findings
- The implemented files being fixed
- Relevant quality gate artifacts only if a finding references them

### Step 2 — Group findings

1. **Blocking / approve-blocking**: must fix before merge
2. **Non-blocking**: should fix, can defer with justification
3. **Outside current scope**: acknowledge but do not implement

### Step 3 — Implement approved fixes

For each approved finding:
1. Make the smallest safe change to address it
2. Update tests where behaviour or coverage changes
3. Do not expand scope while fixing

If a finding conflicts with an authoritative constraint (AR-NNN or Accepted gate): do not implement — surface the conflict instead.

### Step 4 — Write fix summary

Output structure:
```markdown
## Findings Addressed
## Files Changed
## Validation Evidence
## Tests Added or Updated
## Deferred Findings
## Remaining Risks
## Open Questions
```

Deferred findings must be kept visible — never silently dropped.

## Done criteria

- [ ] Only approved findings addressed
- [ ] No blocking finding silently ignored
- [ ] Validation evidence visible for every fix
- [ ] Deferred findings listed explicitly
- [ ] Scope not expanded accidentally
- [ ] Tests updated where behaviour changed
- [ ] Result file written with `status: pass`

## Stop conditions

- Finding conflicts with active source artifacts → stop, surface the conflict
- Finding expands task beyond approved scope → stop, propose escalation
- Required test or validation evidence cannot be produced → stop, explain why
