# Action Migration Guide

This guide is for maintainers evolving `stage-actions.yaml`.

## 1. Leave an old action unchanged

You can keep an old action in its minimal form.

The engine will default missing metadata such as:
- `prompt_family: b2s`
- `policy_refs: []`
- `template_mode: strict`
- empty named validation rules

## 2. Upgrade an action to v2 metadata

Add only the fields you need:

```yaml
prompt_family: speckit
policy_refs:
  - ".b2s/policies/requirements/definition-of-ready.md"
validation_rules:
  required:
    - "requirement_has_id"
  optional: []
```

Do not rewrite the whole action if the rest is already correct.

## 3. Add policies

- create or reuse a short file under `.b2s/policies/`
- add it to `policy_refs`
- make sure the skill prompt tells the model to read `{resolved_policy_inputs}`

Use policies for governing rules, not for output structure.

## 4. Add a named validation rule

- implement the rule in `.b2s/scripts/b2s_engine/validation.py`
- register it in `NAMED_RULES`
- reference it under `validation_rules.required` or `.optional`
- add or update tests

Use required rules for must-pass checks. Use optional rules for advisories.

## 5. Opt into a non-native prompt family

Set `prompt_family` to a guidance family such as `speckit`, `bmad`, or `hve`.

Keep the existing skill tree unless you truly need a different skill file. If
the selected non-`b2s` skill path may not exist yet, add:

```yaml
compatibility:
  fallback_skill_ref: ".b2s/skills/engineering-lead/create-openspec-handoff.md"
```

This keeps family strategy additive instead of forcing a filesystem migration.
