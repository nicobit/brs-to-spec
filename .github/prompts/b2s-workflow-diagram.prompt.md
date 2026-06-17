---
description: Show the workflow diagram for the active initiative as a Mermaid flowchart rendered inline in VS Code Copilot chat.
---

1. Identify the active initiative workspace from the user's message (e.g. `I021` → `initiatives/I021-NEXT21/`).
2. Run:
   ```
   python .b2s/scripts/b2s_cli.py list-actions --workspace-root <WORKSPACE_ROOT> --diagram
   ```
3. Output the result verbatim — the Mermaid code block will render as a diagram in VS Code Copilot chat.
4. Do not summarise, paraphrase, or add commentary. Stop after the output.

If the user also passes a stage filter (e.g. "diagram for planning"), add `--stage-id <stage_id>` to the command.
