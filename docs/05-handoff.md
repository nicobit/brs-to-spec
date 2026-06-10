# Handoff

The handoff is the engineering contract for one active deliverable.

It is generated after the readiness check and any triggered quality gates are complete.

## Two execution modes

### OpenSpec handoff

Use when OpenSpec is the downstream engineering source of truth.

Output location:

```text
openspec/changes/D1-<deliverable-name>/
  proposal.md
  design.md
  tasks.md
  dependency-graph.md
```

Prompt:

```text
.github/prompts/create-openspec-handoff.prompt.md
```

### Standalone handoff

Use when OpenSpec is not available or not appropriate.

Output location:

```text
standalone-delivery/D1-<deliverable-name>/
  delivery-spec.md
  tasks.md
```

Prompt:

```text
.github/prompts/create-standalone-handoff.prompt.md
```

## Multi-repository handoff (optional)

When the initiative spans multiple repositories (API, UI, DB, etc.), place repository descriptor files in:

```text
input/repositories/<alias>.md
```

The file name without `.md` becomes the subfolder name in the handoff output.

With repo descriptors present, each story folder gains subfolders per repository:

```text
openspec/changes/
  F-001.1/
    api/
      proposal.md
      tasks.md
    ui/
      proposal.md
      tasks.md
  dependency-graph.md
```

Without repo descriptors, the handoff is flat (one folder per story, no subfolders):

```text
openspec/changes/
  F-001.1/
    proposal.md
    tasks.md
  dependency-graph.md
```

To generate a repository descriptor automatically, run:

```text
.github/prompts/describe-repository.prompt.md
```

inside the target repository, then save the output as `input/repositories/<alias>.md`.

## Handoff structure rule

Each handoff artifact is scoped to exactly one active deliverable.

The handoff should derive clearly from:

- approved delivery structure
- initiative-specific architecture refinement
- readiness decisions
- triggered quality gates

If those upstream artifacts are weak, improve them before handoff — do not let the handoff reconstruct them implicitly.

## Important rule

Do not generate a handoff if:

- readiness is not complete
- triggered quality gates are incomplete
- the delivery structure has not been confirmed

## See also

- [Delivery & Execution Modes](02-delivery-and-execution-modes.md)
- [Conditional Quality Gates](06-conditional-quality-gates.md)
- [Prompt Execution Environments](16-prompt-execution-environments.md)
