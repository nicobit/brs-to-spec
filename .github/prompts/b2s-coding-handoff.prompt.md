---
description: Generate a self-contained coding handoff for one or all epics of an initiative. The handoff bundles data model, API spec, events, business rules, and all acceptance criteria into a single file a coding agent can implement from.
---

**You** are the executor. Follow `.b2s/prompts/run-workflow.md` for CLI commands.

## What this does

Runs `create-epic-coding-handoffs` for the specified initiative. This produces `coding-handoff.md` inside each selected epic folder — a self-contained coding package.

## User input

The user provides:
- **Initiative ID** (required): e.g., `I093-I3`, `I025-N5`
- **Epic ID** (optional): e.g., `E-001`, `E-002`. If omitted, generate handoffs for ALL epics that have an `implementation-contract.md`.

## Steps

1. Identify the workspace root: `initiatives/{initiative-id}/`

2. If the user specified an epic ID, create `input/selected-epics.md` in the workspace:
   ```markdown
   # Selected Epics
   - {epic-id}
   ```
   If no epic specified, skip this step (all epics with contracts will be selected).

3. Run:
   ```
   python .b2s/scripts/b2s_cli.py run-action --workspace-root initiatives/{initiative-id} --action-id create-epic-coding-handoffs
   ```

4. Run:
   ```
   python .b2s/scripts/b2s_cli.py collect-inputs --workspace-root initiatives/{initiative-id}
   ```

5. Read `.b2s/tmp/current-inputs.json`. Read all resolved inputs.

6. Read the skill prompt: `.b2s/skills/engineering-lead/create-epic-coding-handoffs.md`
   Read the template: `.b2s/artifact-templates/epic-coding-handoff.md`

7. For each selected epic, read:
   - `epics/E-NNN-<slug>/epic.md`
   - `epics/E-NNN-<slug>/implementation-contract.md`
   - All story files in `epics/E-NNN-<slug>/stories/`
   - `architecture/architecture-rules.md`
   - `requirements/atomic-requirements.md`
   - `input/brs.md`

8. Generate `coding-handoff.md` for each selected epic following the skill prompt exactly.
   The handoff must be **self-contained** — all content inline, no "see other file" references.

9. Run:
   ```
   python .b2s/scripts/b2s_cli.py validate-artifact --workspace-root initiatives/{initiative-id}
   ```

10. If validation fails, fix and re-validate (up to 3 attempts).

11. Run:
    ```
    python .b2s/scripts/b2s_cli.py update-state --workspace-root initiatives/{initiative-id}
    ```

12. If `input/selected-epics.md` was created in step 2, delete it after completion.

## Examples

```
/b2s-coding-handoff I025-N5
/b2s-coding-handoff I025-N5 E-002
/b2s-coding-handoff I093-I3 E-001
```
