# Enhancement 3 — Document the Human vs Execution Artifact Boundary

## Context

The BRS to Spec framework produces two fundamentally different types of artifact, but
never names the distinction:

**Human artifacts** — consumed by humans making decisions:
- Business summary, gap analysis, epics and features (Business Copilot)
- Architecture review, delivery spec, readiness check
- BDD scenarios, test strategy, security review (as review documents)
- Handoff packages (OpenSpec proposal, design, tasks)

These are stable. A human reads them, interprets them, makes a decision. Model variance
in how they were generated does not invalidate them — a human validates them before use.

**Execution artifacts** — fed into LLMs or CI to drive automated action:
- `.github/prompts/*.prompt.md` — instructions to GitHub Copilot
- `.brs2spec/skills/8-copilot-implementation/*.md` — code generation prompts
- BDD scenarios when wired to a test runner (transition from human to execution artifact)
- CI gate configs

These are fragile relative to model upgrades. A long prose prompt fed to a new model
version may produce different output. The longer and more narrative the prompt, the
more variance accumulates.

The article "Stop Writing Specs. Start Writing Facts." attacks execution artifacts
used as if they were human artifacts — specs fed to LLMs and expected to produce
deterministic code. The framework needs to name this boundary so teams understand
which artifacts need which durability strategy.

## What needs to change

### 1. Create a new doc: `docs/23-artifact-durability.md`

A reference page that names the two categories and explains the durability strategy for each.

**Human artifacts — durability strategy:**
- Write them in structured format (tables, defined sections) not free prose
- Validate them with a human reviewer before they drive any downstream work
- They survive model upgrades because humans re-read and re-validate them
- Review them when the initiative resumes after a long pause, not when the model upgrades

**Execution artifacts — durability strategy:**
- Keep them short and constraint-based — less prose means less interpretation variance
- Anchor them to machine-verifiable IDs (SCN-NNN, FR-NNN, REQ-NNN) not prose descriptions
- Version them explicitly — treat a model upgrade as a change of interpreter
- After a model upgrade, run a smoke test on the 2-3 most-used execution artifacts
  and compare output structure to previous runs

Include a classification table for every artifact type in the framework:

| Artifact | Type | Durability strategy |
|---|---|---|
| Business summary | Human | Structured tables, human review |
| Gap analysis | Human | Structured tables, human review |
| Epics and features | Human | Structured tables, human review |
| Architecture review | Human | Structured tables, human review |
| BDD scenarios (unexecuted) | Human | Gherkin structure, human review |
| BDD scenarios (wired to CI) | Execution | Machine-verifiable, model-agnostic |
| API contract | Human → Execution | Structured tables → contract test |
| Delivery spec | Human | Structured prose, human review |
| `.github/prompts/*.prompt.md` | Execution | Keep short, constraint-based, version |
| Implementation prompts | Execution | Keep short, constraint-based, version |
| CI gate configs | Execution | Machine-verifiable, model-agnostic |

### 2. Add a callout to `docs/01-overview.md`

Add a short note in the overview that the framework produces two types of artifact
and link to the durability page. One paragraph is enough — this is orientation,
not deep explanation.

### 3. Add a note to `docs/12-prompt-quality-guidelines.md`

Add a section: "Execution artifact guidelines"
- Keep prompts short — prefer constraint lists over narrative paragraphs
- Put quality bar and anti-patterns at the top, not the bottom
- Anchor outputs to structured IDs (SCN-NNN, FR-NNN) not prose
- Treat a model upgrade as a prompt regression test trigger

### 4. Update `mkdocs.yml` nav

Add `23-artifact-durability.md` under the Reference section.

## Implementation steps

1. Create `docs/23-artifact-durability.md` with the full classification table and strategies
2. Update `docs/01-overview.md` — add one-paragraph callout with link
3. Read and update `docs/12-prompt-quality-guidelines.md` — add execution artifact section
4. Update `mkdocs.yml` nav

## Quality bar for this enhancement

- A developer new to the framework can read one page and understand which artifacts
  are stable and which need attention after a model upgrade
- The classification table covers every artifact type the framework produces
- The prompt quality guidelines include concrete rules for execution artifacts
- The boundary between human and execution artifacts is named and explained, not assumed
