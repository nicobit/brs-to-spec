---
description: Show help for the brs-to-spec framework — entry points, phases, or a specific action.
---

## How to use this prompt

Read the user's request and apply exactly one of the three modes below. Do not run the workflow. Do not write any files.

---

## Mode 1 — General help (no argument, or "help")

Output this text verbatim, substituting nothing:

---

**brs-to-spec framework — quick reference**

**Starting out**

| Say | What happens |
|---|---|
| `new initiative` / `create initiative` | Scaffold a new initiative workspace via CLI |
| `b2s-dispatch-next` / `next` | Run exactly one staged action and stop |
| `b2s-dispatch-all` / `continue` | Run staged actions until a stop condition is reached |
| `status` / `what is next` | Show current stage, next action, and any blockers |

**Repair and recovery**

| Say | What happens |
|---|---|
| `repair chain` / `fix processing` | Repair a broken or inconsistent action chain |
| `reset to <phase>` / `rewind to <phase>` | Rewind state to a previous phase and re-run from there |
| `resume` / `resume from <phase>` | Guided decision: repair, retry, or reset — then continue |

**Help**

| Say | What happens |
|---|---|
| `b2s-help` | This screen |
| `b2s-help <phase>` | Explain a phase: what it does, its actions, stop condition |
| `b2s-help <action-id>` | Explain one action: inputs, output, blockers, gate |

**Phases (in order)**

| Phase ID | Name |
|---|---|
| `0-routing` | Route initiative — determine delivery and execution mode |
| `2-business-intake` | Business intake — summarize the BRS; human gate required |
| `2b-business-analysis` | Business analysis — requirements, use cases, rules, flows |
| `3-planning` | Planning — architecture, delivery structure, modules, increments |
| `4-engineering-readiness` | Engineering readiness — readiness check, initiative context; human gate required |
| `5-quality-gates` | Quality gates — BDD scenarios, test strategy, security, API/data/event contracts |
| `6-handoff` | Handoff — OpenSpec, standalone, compact, or agile handoff packages |

---

## Mode 2 — Phase help (argument matches a phase ID or phase name)

Recognized phase IDs: `0-routing`, `2-business-intake`, `2b-business-analysis`, `3-planning`, `4-engineering-readiness`, `5-quality-gates`, `6-handoff`.

Also accept loose matches: "routing", "intake", "business analysis", "planning", "engineering", "readiness", "quality", "handoff".

**Steps:**

1. Read `.b2s/workflow/stage-actions.yaml`.
2. Filter actions whose `stage_id` matches the requested phase.
3. Read `.b2s/state/workflow-state.json` in the active initiative workspace (if it exists) to report current position.
4. Output a structured summary:

```
Phase: <stage_id> — <human name>

Actions in this phase (in serial order):
  <action_id> — <title>
    Outputs: <primary output path>
    Human gate: yes / no
    Blocked by: <blocked_by_action list, or "nothing — runs first">

Current position: <last_completed_action or "not started">
Next action: <next_action from workflow-state.json, or "unknown — run status">
Stop condition: <human gate action id if present, otherwise "phase complete when all actions pass">
```

---

## Mode 3 — Action help (argument matches an action_id)

Recognized action IDs are any `action_id` value in `.b2s/workflow/stage-actions.yaml`.

**Steps:**

1. Read `.b2s/workflow/stage-actions.yaml`.
2. Find the action whose `action_id` matches the argument (exact match; also accept partial unambiguous prefix).
3. Read the skill file at `skill_ref` — only the first 40 lines (enough to get Step 1 and the purpose).
4. Output a structured summary:

```
Action: <action_id> — <title>
Stage: <stage_id>
Persona: <persona>

Inputs
  Required: <required list>
  Optional: <optional list>

Output
  Primary: <primary>
  Secondary: <secondary list, or "none">

Blockers
  Blocked by stage: <list, or "none">
  Blocked by action: <list, or "none">

Human gate: <yes — gate_id: <id> / no>

Skill: <skill_ref>
Purpose: <first sentence of the skill file's purpose or Step 1 description>
```

---

## Error cases

- Argument given but matches neither a phase nor an action ID → output: `Unknown phase or action: "<argument>". Run b2s-help for the full list.`
- Multiple actions match a partial action ID → list the matches and ask the user to be more specific.
- `.b2s/workflow/stage-actions.yaml` cannot be read → output: `Cannot read stage-actions.yaml. Check that you are in the brs-to-spec repository root.`
