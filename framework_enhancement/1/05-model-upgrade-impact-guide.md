# Enhancement 5 — Model Upgrade Impact Guide

## Context

The BRS to Spec framework uses LLMs at every stage — from business intake through
engineering handoff to implementation. When a model is upgraded (e.g. Copilot switches
from Sonnet 3.7 to Sonnet 4, or a team migrates from one model to another), there is
currently no guidance on:

- which framework artifacts are at risk of producing different output
- which artifacts are stable and need no review
- what to do to validate that the framework still works correctly after a model change

The article "Stop Writing Specs. Start Writing Facts." documents exactly this problem:
a 1,500-word specification required four reinterpretations across four model versions,
while an executable test survived unchanged. The framework needs to make this risk
visible and manageable.

## What needs to change

### 1. Create a new doc: `docs/24-model-upgrade-guide.md`

A practical reference page for teams upgrading their AI model. Structure:

#### What changes when a model upgrades

A model upgrade is a change of interpreter — the same prompt may produce different
output structure, different level of detail, different interpretation of ambiguous rules.
This is not a bug. It is the mechanism.

#### Artifact risk classification

| Artifact type | Risk on model upgrade | Action required |
|---|---|---|
| BDD scenarios (wired to CI) | None — machine-verifiable | None |
| BDD scenarios (unexecuted markdown) | Low — structure is explicit | Spot-check one scenario |
| API / data / event contracts (structured tables) | Low — structure is explicit | Spot-check one contract |
| Business summary, gap analysis | Low — human-reviewed before use | None unless re-running |
| Architecture review, delivery spec | Low — human-reviewed before use | None unless re-running |
| `.github/prompts/*.prompt.md` | Medium — execution artifacts | Run smoke test |
| `.brs2spec/skills/8-copilot-implementation/*.md` | Medium-High — long narrative | Run smoke test |
| `.brs2spec/skills/1-routing/*.md` | Medium — routing decisions affect everything downstream | Run smoke test |
| Free-form prose prompts | High — most sensitive to model variance | Review and tighten |

#### Smoke test procedure

After a model upgrade, run the following smoke tests before using the framework on
a live initiative:

1. **Routing smoke test** — run `00-start.md` against a known BRS fixture. Verify the
   routing recommendation matches the expected output. If it differs materially, review
   the routing prompt.

2. **Implementation smoke test** — run `01-implement-one-task.md` against a trivial
   known task. Verify the output structure matches the required template. If sections
   are missing or reordered, tighten the prompt.

3. **BDD scenario smoke test** — run the BDD scenario generation prompt against a
   known set of requirements. Verify SCN-NNN IDs are present, Gherkin blocks are complete,
   and the coverage summary matches the scenario count.

4. **CI gate check** — if BDD scenarios are wired to CI, run the test suite. All
   previously passing tests must still pass. If any fail due to output format changes,
   update the test stubs.

#### What NOT to do after a model upgrade

- Do not re-run all prompts on existing initiatives and overwrite completed artifacts.
  Human-reviewed artifacts are stable regardless of model version.
- Do not assume the new model is "better" and regenerate specs. The existing artifacts
  were human-validated — their value is the human review, not the model that generated them.
- Do not change the model mid-initiative. Pick a model at initiative start and stick with it
  until the initiative completes.

#### Recommended model pinning strategy

For long-running initiatives (more than 4 weeks):
- Pin the model version in `.github/copilot-instructions.md` if your platform supports it
- Note the model version in `engineering-readiness/initiative-context.md`
- Only upgrade the model between initiatives, not during one

### 2. Add a callout to `docs/16-prompt-execution-environments.md`

Add a section: "Model upgrades" with a one-paragraph note and a link to the new guide.
The note: "Treat a model upgrade as a change of interpreter. Human artifacts are stable.
Execution artifacts (prompts that drive code generation) require a smoke test.
See [Model Upgrade Guide](24-model-upgrade-guide.md)."

### 3. Add model version field to `engineering-readiness/initiative-context.md` template

Add one row to the metadata table:

```
| AI model version | (e.g. claude-sonnet-4, gpt-4o) |
```

This makes the model version part of the initiative record, so if output changes are
noticed later, the team knows which model produced the original artifacts.

### 4. Update `mkdocs.yml` nav

Add `24-model-upgrade-guide.md` under the Reference section.

## Implementation steps

1. Create `docs/24-model-upgrade-guide.md` with the full guide
2. Read `docs/16-prompt-execution-environments.md` — add model upgrade callout
3. Read `.brs2spec/templates/templates/engineering-readiness/initiative-context.md`
   — add model version field to metadata table
4. Update `mkdocs.yml` nav

## Quality bar for this enhancement

- A developer can read one page and know exactly what to check after a model upgrade
- The artifact risk table covers every artifact type the framework produces
- The smoke test procedure is concrete — specific prompts, specific verification steps
- The model pinning recommendation is clear and actionable
- The guide does not recommend re-running prompts on completed initiatives
