# Action Contract v2

This note describes the current additive action model used by `.b2s`.

## Mental model

An action definition is the executable workflow contract for one artifact step:

```text
Phase -> Inputs -> Policies -> Prompt Family -> Skill Prompt -> Template -> Artifact -> Validation -> Gate
```

## Core fields

| Field group | Purpose |
|---|---|
| `action_id`, `stage_id`, `title`, `persona` | identity and routing |
| `inputs.required`, `inputs.optional` | artifact and source prerequisites |
| `policy_refs` | policy files resolved as governing inputs |
| `prompt_family` | strategy label such as `b2s`, `speckit`, `bmad`, `hve` |
| `skill_ref` | exactly one skill prompt loaded for execution |
| `artifact_template_ref` | output structure contract |
| `outputs.primary`, `outputs.secondary` | artifact targets |
| `validation_profile` | validator family |
| `validation_rules.required`, `validation_rules.optional` | named rule checks |
| `blocked_by_stage`, `blocked_by_action`, `conditions` | workflow sequencing |
| `human_gate` | optional post-generation review gate |
| `compatibility.fallback_skill_ref` | fallback when non-native family routing cannot resolve the primary skill |

## Resolution rules

- missing v2 metadata is defaulted by the engine
- `prompt_family` is routing metadata, not a reason to load multiple prompts
- `policy_refs` are resolved during `collect-inputs` and surfaced through
  `{resolved_policy_inputs}`
- templates define the output shape; policies define the governing rules
- required named validation rules fail the action when they fail
- optional named validation rules become advisories

## Compatibility

Older actions can stay unchanged.

The engine will default:

- `prompt_family` -> `b2s`
- `policy_refs` -> `[]`
- `template_mode` -> `strict`
- `validation_rules.required` -> `[]`
- `validation_rules.optional` -> `[]`
- `compatibility` -> `{}`
