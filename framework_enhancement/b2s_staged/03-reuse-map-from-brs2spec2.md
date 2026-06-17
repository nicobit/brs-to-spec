# Reuse Map From `.brs2spec2`

## Reuse directly

These assets are strong candidates for direct or near-direct reuse in `.b2s/`:

### Workflow structure

- `.brs2spec2/workflow/workflow-definition.yaml`

Use as the baseline stage graph, but convert event-driven nodes into staged
action definitions.

### Skill prompts

Most skill prompts under `.brs2spec2/skills/` are reusable because they are
about artifact generation, not queue mechanics.

High-value examples:

- `skills/product-owner/create-business-intake-summary.md`
- `skills/product-owner/create-requirements.md`
- `skills/product-owner/create-use-case-diagram.md`
- `skills/delivery-lead/create-delivery-structure.md`
- `skills/engineering-lead/check-engineering-readiness.md`
- `skills/engineering-lead/create-openspec-handoff.md`

### Artifact templates

Most `.brs2spec2/artifact-templates/` should be reused because they define the
target artifact shape you want `.b2s` to produce.

### Validation intent

The stronger `must_include` and `natural_language` logic in `.brs2spec2`
templates should be reused as validation requirements, but not necessarily as
event-template metadata.

## Reuse with adaptation

### Event templates

`.brs2spec2/workflow/event-templates/` should not be reused as runtime event
templates in `.b2s`.

Instead, they should be mined for:

- action identity
- required inputs
- optional inputs
- primary output path
- stage placement
- validation expectations
- human gate behavior

Those fields should become `.b2s` **stage action definitions**.

### Orchestrator prompts

`.brs2spec2` dispatcher prompts should not be reused as-is.

Their artifact-generation references are useful, but their queue/event language
does not fit a staged engine.

### Review gates

WAIT_HUMAN-style gates should become stage-state transitions in `.b2s`, not
event files.

For example:

- artifact status: `draft` -> `ai_validated` -> `accepted`
- action status: `waiting_human`

## Do not reuse directly

These parts of `.brs2spec2` should not be copied into `.b2s` as-is:

- runtime event objects
- `pending/processing/done/failed` queue semantics
- result-file-per-event flow
- event-log logic tied to EVT IDs
- chain-repair based on event templates

## Mapping pattern

Recommended transformation:

| `.brs2spec2` concept | `.b2s` replacement |
|---|---|
| Event template | Stage action definition |
| Runtime event file | Current action in `next-step.json` |
| Result file | Validation report + state update report |
| Queue state | `next_action` + artifact statuses |
| `on_success.create_events` | stage graph next-actions |
| `WAIT_HUMAN` event | artifact/action state waiting for acceptance |
