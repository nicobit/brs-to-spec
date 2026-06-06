# Adapter Prompt — Create OpenSpec Artifacts from Handoff

Use this when OpenSpec will own the engineering execution workflow.

Input:
- `features/<feature-name>/handoff/spec-driven-handoff.md`
- Referenced source artifacts

Task:
Create OpenSpec-native artifacts from the handoff package.

Output:

```text
features/<feature-name>/openspec-change/proposal.md
features/<feature-name>/openspec-change/design.md
features/<feature-name>/openspec-change/tasks.md
```

Rules:
- Treat the handoff package as the final upstream input.
- Carry forward architecture decisions, contracts, risks, and open questions.
- If OpenSpec becomes the source of truth, do not maintain a second competing task plan outside OpenSpec.
