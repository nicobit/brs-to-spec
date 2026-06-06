# Prompt — Assess Handoff Readiness

Input:
- `features/<feature-name>/handoff/spec-driven-handoff.md`
- All referenced source artifacts

Task:
Assess whether the feature is ready to hand over to a downstream spec-driven engineering framework.

Output:

```text
features/<feature-name>/handoff/handoff-readiness.md
```

Use this structure:

```markdown
# Handoff Readiness Assessment

## 1. Readiness Result
Ready / Ready with risks / Not ready

## 2. Blocking Issues

| ID | Issue | Owner | Required action |
|---|---|---|---|

## 3. Non-Blocking Risks

## 4. Required Source Artifacts

## 5. Downstream Recommendation
OpenSpec / GitHub Spec Kit / Kiro / Standalone

## 6. Final Recommendation
```

Rules:
- Be strict.
- Do not mark ready if architecture decisions that block implementation are unresolved.
- Do not mark ready if mandatory contracts are missing.
