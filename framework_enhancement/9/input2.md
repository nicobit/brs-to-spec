Yes, understood. You are not thinking about a generic web app or CLI used by a separate user. You are thinking:

```text
The user is already inside VS Code
using GitHub Copilot Chat or Claude Code Chat
and wants the workflow to run from there.
```

In that case, the best solution is different.

## The realistic answer

Inside **VS Code Chat**, Copilot or Claude will not automatically behave like a permanent workflow engine that watches your folder and wakes up personas when a file appears.

But they can be used very well if you structure your repo so the user can say something like:

```text
Run the next BRS-to-Spec event.
```

or:

```text
Read .workflow/events/pending and execute the next event.
```

Then Copilot/Claude reads the event, follows the instructions, creates/updates the expected artifact, and possibly moves the event to done/failed if you instruct it.

So the best model is:

```text
Your framework does not need to call the LLM.
The user calls Copilot/Claude Chat.
Copilot/Claude becomes the action runner.
Your files tell Copilot/Claude exactly what to do.
```

That is important.

## Recommended design for VS Code Chat

You can create a framework that is **chat-driven**, not API-driven.

The repository contains:

```text
.workflow/
  events/
    pending/
    processing/
    done/
    failed/

  personas/
    product-owner.md
    architect.md
    delivery-lead.md
    engineering-lead.md
    qa-analyst.md
    security-reviewer.md
    repository-analyst.md

  instructions/
    dispatcher.md
    event-execution-rules.md
    artifact-validation-rules.md

.github/
  copilot-instructions.md

.claude/
  CLAUDE.md
```

Then the user opens Copilot Chat or Claude Code and says:

```text
Follow .workflow/instructions/dispatcher.md and execute the next pending event.
```

That is enough for a first version.

## How the dispatch works without your own LLM call

Instead of your code doing this:

```text
dispatcher → calls LLM API
```

you make Copilot/Claude do this:

```text
User prompt → Copilot/Claude reads dispatcher.md
→ Copilot/Claude reads next event YAML
→ Copilot/Claude applies the persona prompt
→ Copilot/Claude reads input files
→ Copilot/Claude writes output artifact
→ Copilot/Claude updates event status
```

So the “LLM/action runner” becomes:

```text
GitHub Copilot Chat or Claude Code Chat
```

You are not calling it programmatically.

You are giving it a deterministic file-based protocol.

## Example user command

For Copilot Chat or Claude Code:

```text
Execute the next pending BRS-to-Spec workflow event.

Use:
- .workflow/instructions/dispatcher.md
- .workflow/events/pending/
- .workflow/personas/
- .workflow/state/workflow-state.json

Follow the event exactly:
- read only the files listed in read_from
- write only the files listed in write_to
- validate the artifact using validation rules
- move the event to done or failed
- update event-log.jsonl
```

This is the simplest no-install model.

## Even better: use prompt files / custom instructions

VS Code supports custom instructions for Copilot Chat through instruction files, so you can put common guidance in the repository instead of repeating everything in the prompt. Microsoft’s VS Code docs describe custom instructions as Markdown files that influence Copilot responses and keep coding practices/project rules consistent. ([Visual Studio Code][1])

GitHub Copilot Chat also supports slash commands in the IDE for common tasks, but those are not the same as your custom workflow dispatcher. ([GitHub Docs][2])

So for Copilot, I would generate:

```text
.github/copilot-instructions.md
.workflow/prompts/dispatch-next.prompt.md
.workflow/prompts/execute-event.prompt.md
```

The user can open the prompt file, run it in Copilot Chat, or paste:

```text
Run .workflow/prompts/dispatch-next.prompt.md
```

For Claude Code, you can use:

```text
CLAUDE.md
.workflow/prompts/dispatch-next.md
```

Claude Code also supports hooks, but those are lifecycle hooks inside Claude Code, not a full folder-watching workflow engine. ([Claude Code][3])

## Can hooks help inside VS Code?

Yes, but mostly as a convenience.

VS Code Copilot Agent hooks can run shell commands at key lifecycle points during agent sessions. ([Visual Studio Code][4]) GitHub Copilot cloud agent hooks can also execute shell commands during agent execution. ([GitHub Docs][5]) Claude Code hooks can execute shell commands, HTTP endpoints, LLM prompts, or MCP tools at lifecycle points. ([Claude Code][3])

But for your exact case:

```text
file appears in .workflow/events/pending
→ automatically start Product Owner persona
```

that is still better handled by your own dispatcher/watch process or by an explicit chat command. Hooks are not the clean core solution.

## Best solution if you want no install and use VS Code Chat

Use a **pure file/protocol approach**:

```text
1. Your framework creates the workflow files.
2. Copilot/Claude is instructed by repo-level instruction files.
3. The user runs a prompt in chat: "execute next event".
4. The agent reads the event and writes the artifact.
5. The agent updates the workflow status.
```

No Python.
No Node.
No VS Code extension.
No local tool.

The cost is that the user must explicitly start the action in chat.

## Proposed minimal structure

```text
.workflow/
  README.md

  instructions/
    dispatcher.md
    event-schema.md
    validation-rules.md

  events/
    pending/
      EVT-0023-create-business-rules.yaml
    processing/
    done/
    failed/

  personas/
    product-owner.md
    architect.md
    delivery-lead.md
    engineering-lead.md
    qa-analyst.md
    security-reviewer.md
    repository-analyst.md

  prompts/
    dispatch-next.md
    dispatch-all.md
    validate-current-event.md

  state/
    workflow-state.json
    event-log.jsonl
    open-decisions.md
```

## Example `dispatch-next.md`

```markdown
# Dispatch next BRS-to-Spec event

You are the BRS-to-Spec orchestrator.

1. Read `.workflow/instructions/dispatcher.md`.
2. Inspect `.workflow/events/pending/`.
3. Select the next executable event.
4. Read the persona specified by the event from `.workflow/personas/`.
5. Read only the files listed in `read_from`.
6. Produce or update only the files listed in `write_to`.
7. Validate the output using the event validation rules.
8. Move the event file to `.workflow/events/done/` if successful.
9. Move the event file to `.workflow/events/failed/` if validation fails.
10. Append a short entry to `.workflow/state/event-log.jsonl`.
11. If the event defines `on_success`, create the next pending event files.
```

The user tells Copilot/Claude:

```text
Execute .workflow/prompts/dispatch-next.md
```

## My recommendation

For your case, I would support three levels:

### Level 1 — No install, chat-driven

Use Copilot/Claude directly.

```text
User: Execute next event
Agent: reads files and writes artifacts
```

Best for immediate use.

### Level 2 — Optional CLI

Later, add:

```text
brs-to-spec dispatch
```

Best for repeatability and validation.

### Level 3 — Optional VS Code extension

Later, add buttons:

```text
Run next event
Run all
Show workflow status
Validate artifacts
```

Best for user experience.

## Final answer

Because you are using **VS Code Chat with GitHub Copilot or Claude**, the no-install solution is:

> **Do not programmatically call the LLM. Make Copilot/Claude the runner by giving them a file-based workflow protocol and prompt files.**

The user action becomes:

```text
Execute the next pending workflow event.
```

And the agent does the dispatch by reading:

```text
.workflow/prompts/dispatch-next.md
.workflow/events/pending/*.yaml
.workflow/personas/*.md
```

This is the simplest and most coherent solution for your current way of working.

[1]: https://code.visualstudio.com/docs/copilot/customization/custom-instructions?utm_source=chatgpt.com "Use custom instructions in VS Code"
[2]: https://docs.github.com/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide?utm_source=chatgpt.com "Asking GitHub Copilot questions in your IDE"
[3]: https://code.claude.com/docs/en/hooks?utm_source=chatgpt.com "Hooks reference - Claude Code Docs"
[4]: https://code.visualstudio.com/docs/copilot/customization/hooks?utm_source=chatgpt.com "Agent hooks in Visual Studio Code (Preview)"
[5]: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks?utm_source=chatgpt.com "Customize agent workflows with hooks"
