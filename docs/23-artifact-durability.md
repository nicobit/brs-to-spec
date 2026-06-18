# Artifact Durability

The framework produces two fundamentally different types of artifact. Understanding the
distinction determines which artifacts need attention after a model upgrade and which
are stable regardless of model changes.

## The two types

### Human artifacts

Consumed by humans making decisions. A human reads, interprets, and validates them
before they drive any downstream work. Model variance in how they were generated does
not invalidate them — the human review is the validation.

Examples: business summary, gap analysis, epics and features, architecture review,
delivery spec, readiness check, BDD scenarios (as reviewed documents), handoff packages.

**Durability strategy:**

- Write in structured format — tables and defined sections, not free prose
- Always validate with a human reviewer before they drive downstream work
- They survive model upgrades because humans re-read and re-validate them
- Review them when an initiative resumes after a long pause, not when the model upgrades

### Execution artifacts

Fed into LLMs or CI to drive automated action. These are sensitive to model upgrades —
a long prose instruction fed to a new model version may produce structurally different output.
The longer and more narrative the artifact, the more interpretation variance accumulates.

Examples: `.github/prompts/*.prompt.md`, `.brs2spec/skills/8-copilot-implementation/*.md`,
BDD scenarios wired to a test runner, CI gate configs.

**Durability strategy:**

- Keep them short and constraint-based — prefer constraint lists over narrative paragraphs
- Put the quality bar and hard rules at the top — the model reads top-down
- Anchor outputs to machine-verifiable IDs (SCN-NNN, FR-NNN, REQ-NNN) not prose descriptions
- Treat a model upgrade as a change of interpreter — run a smoke test after upgrading
- Version them explicitly alongside the model version used

## Classification table

| Artifact | Type | Durability strategy |
|---|---|---|
| Business summary | Human | Structured tables, human review |
| Gap analysis | Human | Structured tables, human review |
| Epics and features | Human | Structured tables, human review |
| Architecture review | Human | Structured tables, human review |
| Delivery spec | Human | Structured prose, human review |
| Readiness check | Human | Structured tables, human review |
| Test strategy | Human | Structured tables, human review |
| Security review | Human | Structured tables, human review |
| BDD scenarios (unexecuted markdown) | Human | Gherkin structure, human review |
| Handoff package (proposal, design, tasks) | Human | Structured prose + tables, human review |
| API contract | Human → Execution | Structured tables reviewed by human; wire to contract test for CI |
| Data contract | Human → Execution | Structured tables reviewed by human; wire to schema validation for CI |
| Event contract | Human → Execution | Structured tables reviewed by human; wire to schema registry check for CI |
| BDD scenarios (wired to CI) | Execution | Machine-verifiable, model-agnostic, survives model upgrades |
| `.github/prompts/*.prompt.md` | Execution | Keep short and constraint-based; smoke test after model upgrade |
| `.brs2spec/skills/8-copilot-implementation/*.md` | Execution | Keep short and constraint-based; smoke test after model upgrade |
| CI gate configs | Execution | Machine-verifiable, model-agnostic |

## The boundary in practice

The same artifact can be in both categories depending on how it is used:

- **BDD scenarios as a markdown file** reviewed by QA and the PO → Human artifact
- **BDD scenarios wired to pytest-bdd and run in CI** → Execution artifact

The transition from human to execution artifact is the act of wiring to a test runner.
That transition is the most valuable step in the framework — it converts a reviewed
human decision into a durable machine-verifiable fact.

See [Wiring Quality Gates to CI](22-wiring-quality-gates-to-ci.md) for how to make
that transition for each artifact type.

## What to do after a model upgrade

| Artifact type | Action |
|---|---|
| Human artifacts | None — they are validated by human review, not by the model |
| Execution artifacts (wired to CI) | Run CI — if it passes, the upgrade had no effect |
| Execution artifacts (prompts) | Run smoke test — compare output structure to previous run |
| Long narrative prompts | Review top-to-bottom — shorten and constrain if output drifts |

See [Model Upgrade Guide](24-model-upgrade-guide.md) for the full smoke test procedure.
