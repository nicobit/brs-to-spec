# Architecture-Aware Flow

## Rule

Architecture input is a first-class input. It is propagated end-to-end through the initiative workspace.

## Two phases of architecture use

### Early phase: context framing

At the start of an initiative, `input/architecture.md` (or `input/architecture/*.md`) provides high-level solution architecture context:

```text
system landscape
software systems
containers
major integrations
major platform boundaries
high-level constraints
```

Use that early input to understand the world the initiative lives in.

Do not assume it already resolves all initiative-specific delivery questions.

### Later phase: initiative-specific refinement

After the delivery structure is confirmed, use `architecture/architecture-review.md` and `architecture/architecture-rules.md` to refine architecture implications for this specific initiative:

```text
impacted components
interface and contract impact
governed boundaries
rollout / rollback constraints
validation implications
delivery-shaping rules
```

## Governed boundaries

When the architecture review reveals a governed boundary, surface it explicitly:

- governed service or API boundary → usually trigger `API contract`
- governed data ownership or schema boundary → usually trigger `Data contract`
- governed asynchronous event boundary → usually trigger `Event contract`

These decisions feed the readiness check and quality gate triggers.

## Multi-repository signal

When the architecture spans multiple repositories (separate API service, UI, DB, etc.), the architecture review should surface this explicitly.

The workflow runner will ask whether `input/repositories/` descriptors are needed before handoff generation.

Descriptor setup:

```text
input/repositories/<alias>.md
```

Use `.github/prompts/describe-repository.prompt.md` to generate a descriptor from a target repository automatically.

## Important rules

- Do not imply that architecture is optional when it exists.
- Do not over-claim that early architecture input resolves all delivery questions.
- Do not allow the handoff to reconstruct architecture decisions that belong in the architecture review artifacts.

## See also

- [Brownfield / Existing-System Mode](19-brownfield-existing-system-mode.md)
- [Handoff](05-handoff.md)
