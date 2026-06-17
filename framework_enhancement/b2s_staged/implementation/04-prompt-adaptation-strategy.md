# Prompt Adaptation Strategy

## Main rule

Reuse `.brs2spec2` prompts for artifact generation, but adapt them to staged
execution.

## Keep

Keep from `.brs2spec2` prompts:

- role/persona framing
- artifact-generation instructions
- stronger completeness requirements
- business-analysis quality bar
- use of modern artifact templates

## Remove or rewrite

Remove or rewrite:

- event identity assumptions
- result-file writing instructions
- queue-state references
- dispatcher-step references tied to `.flow/events/`
- EVT-specific failure/result semantics

## Replace with `.b2s` assumptions

Prompts should assume:

- a selected `stage action`
- a machine-prepared input bundle
- one target output artifact
- validation handled by scripts after artifact generation

## Adaptation pattern

For each reused `.brs2spec2` skill prompt:

1. keep the artifact-writing content
2. remove event/result-file coupling
3. replace `read_from` wording with `current-inputs.json` wording where needed
4. replace `.brs2spec2/...` references with `.b2s/...`
5. preserve output path and output shape
