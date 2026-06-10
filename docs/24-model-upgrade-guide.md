# Model Upgrade Guide

A model upgrade is a change of interpreter. The same prompt may produce different output
structure, different level of detail, or a different interpretation of ambiguous rules.
This is not a bug — it is the mechanism. This page tells you what to check and what to ignore.

## What is and is not at risk

| Artifact type | Risk | Reason | Action required |
|---|---|---|---|
| BDD scenarios wired to CI | None | Machine-verifiable — exit code, not model output | Run CI — if it passes, upgrade had no effect |
| API / data / event contracts (structured tables) | Low | Stable structure; human-reviewed before use | None unless re-running the prompt |
| Business summary, gap analysis, epics | Low | Human-reviewed before use | None unless re-running the prompt |
| Architecture review, delivery spec | Low | Human-reviewed before use | None unless re-running the prompt |
| BDD scenarios (unexecuted markdown) | Low | Gherkin structure is explicit | Spot-check one scenario if re-running |
| `.github/prompts/*.prompt.md` | Medium | Execution artifacts — model interprets them | Run smoke test after upgrade |
| `.brs2spec/1-routing/*.md` | Medium | Routing affects everything downstream | Run smoke test after upgrade |
| `.brs2spec/8-copilot-implementation/*.md` | Medium | Code generation prompts — long prose | Run smoke test after upgrade |
| Long narrative prompts (any) | High | Most sensitive to model interpretation variance | Review and tighten if output drifts |

The key principle: **human artifacts are validated by human review, not by the model.**
A business summary that a PO signed off on is valid regardless of which model generated it.
Execution artifacts are validated by their output structure — that is what changes with the model.

## Smoke test procedure

Run these checks after any model upgrade before using the framework on a live initiative.

### 1. Routing smoke test

Run `.brs2spec/1-routing/01-select-delivery-and-execution-mode.md` against a simple known
BRS fixture (one or two requirements, no architecture input).

**Verify:**
- Output contains a Decision Summary table with delivery mode and execution mode selected
- Each criterion in the Delivery Mode Assessment table has an evidence value
- No blank fields in required sections

If the output structure differs materially from a previous run, review the routing prompt
and tighten any narrative sections.

### 2. Workflow prompt smoke test

Run `.github/prompts/brs-to-spec-run-workflow.prompt.md` against the same simple fixture.

**Verify:**
- The prompt detects the correct current stage (routing, if nothing else exists)
- It produces a Stage Completed / Next Stage response in the correct format
- It does not skip the stage sequence or jump to handoff

### 3. Implementation prompt smoke test

Run `.brs2spec/8-copilot-implementation/01-implement-one-task.md` against a trivial
known task with a clear SCN-NNN reference.

**Verify:**
- Output contains all required sections: Task Implemented, Files Changed, Requirements Covered,
  Validation Evidence, Tests Added or Updated, Assumptions, Risks, Remaining Open Questions
- At least one SCN-NNN is referenced as the done criterion
- No sections are missing or reordered

### 4. CI gate check

If BDD scenarios are wired to a test runner, run the test suite.

**Verify:**
- All previously passing tests still pass
- If any fail due to output format changes, update the test stubs — do not change the scenarios

## What NOT to do after a model upgrade

- Do not re-run all prompts on existing initiatives and overwrite completed artifacts.
  Human-reviewed artifacts are valid regardless of model version — their value is the human review.
- Do not assume the new model is "better" and regenerate specs without a human re-review.
- Do not upgrade the model mid-initiative. Pick a model at initiative start and stay with it
  until the initiative completes. Upgrade between initiatives only.
- Do not treat a changed output as a bug. Compare the structure, not the wording.
  If the required sections are present and the quality bar is met, the output is acceptable.

## Model pinning

For initiatives longer than 4 weeks, pin the model version:

- Note it in `engineering-readiness/initiative-context.md` → AI model version field
- If your platform supports model pinning, configure it in `.github/copilot-instructions.md`
- Only upgrade the model between initiatives, not during one

If you cannot pin the model (platform-managed upgrade), run the smoke tests above at the
start of each working session until the initiative is complete.

## See also

- [Artifact Durability](23-artifact-durability.md)
- [Prompt Quality Guidelines](12-prompt-quality-guidelines.md)
- [Prompt Execution Environments](16-prompt-execution-environments.md)
