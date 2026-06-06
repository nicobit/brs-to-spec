# Prompt — Decide Architecture & Contract Artifacts

Recommended environment:
- VS Code Copilot Chat
- Approved engineering LLM with repository context

Owner:
- Architect / Tech Lead

Input files:
- `features/<feature-name>/business-intake/requirements.md`
- `features/<feature-name>/business-intake/brs-architecture-alignment.md`
- `features/<feature-name>/business-intake/user-stories.md`
- `features/<feature-name>/engineering-contracts/technical-spec.md` if available
- `features/<feature-name>/input/architecture-draft.md`

Task:
Decide which optional architecture and contract artifacts are needed.

Output:
Create:

```text
features/<feature-name>/architecture-contracts/artifact-decision.md
```

Use this structure:

```markdown
# Architecture & Contract Artifact Decision

## 1. Summary

## 2. Artifact Decision Matrix

| Artifact | Needed? | Reason | Owner | Mandatory before implementation? |
|---|---|---|---|---|
| Architecture decisions / ADRs |  |  |  |  |
| API contract |  |  |  |  |
| OpenAPI contract |  |  |  |  |
| Domain model / DDD |  |  |  |  |
| Data model |  |  |  |  |
| Event contracts |  |  |  |  |
| Quality attribute scenarios |  |  |  |  |
| Threat model |  |  |  |  |

## 3. Recommended Next Prompts

## 4. Explicitly Skipped Artifacts
```

Rules:
- Do not make all artifacts mandatory.
- Recommend only artifacts that reduce real ambiguity or risk.
- Use DDD only if domain complexity justifies it.
- Use OpenAPI when REST APIs are created or changed.
