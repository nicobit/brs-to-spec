# Prompt 02 - Add Policy-Aware Input Collection

## Context

The workflow already resolves required and optional inputs. This enhancement
adds first-class policy resolution so prompts receive not only business inputs,
but also the policy context that governs artifact generation.

## Step 1 - Read the current input flow

Read these files in full:

- `.b2s/scripts/b2s_engine/inputs.py`
- `.b2s/scripts/b2s_engine/workspace.py`
- `.b2s/prompts/run-workflow.md`

Identify the current output shape of:

- `.b2s/tmp/current-inputs.json`

## Step 2 - Extend current-inputs.json

Update the input collection flow so the machine-written input payload can carry:

```json
{
  "resolved_policy_inputs": [],
  "resolved_required_inputs": [],
  "resolved_optional_inputs": [],
  "prompt_family": "b2s",
  "template_mode": "strict"
}
```

Rules:

- `resolved_policy_inputs` comes from `policy_refs`
- preserve existing keys
- do not rename current keys that prompts already depend on

## Step 3 - Extend the placeholder contract

Update `.b2s/agent-instructions.md` and `.b2s/prompts/run-workflow.md` so the
prompt-facing placeholder contract includes:

- `{resolved_policy_inputs}`
- `{prompt_family}`
- `{template_mode}`

Be explicit that policy files must be read in full before generating an
artifact, just like required inputs.

## Step 4 - Implement policy resolution rules

In `inputs.py`, resolve `policy_refs` using the same disciplined path handling
used for normal inputs.

Policy behavior:

- for actions explicitly migrated in the same change set, missing policy files
  should fail collection
- for old actions with no `policy_refs`, behavior must remain unchanged
- do not mass-annotate actions with `policy_refs` until the referenced policy
  files exist and tests or fixtures are updated accordingly
- optional business inputs remain optional
- policy files are not treated as output artifacts

## Step 5 - Make the contract visible to prompts

Update one or two representative skill prompts to mention policy inputs
explicitly. Keep the change additive. Do not rewrite every skill.

Examples:

- `.b2s/skills/product-owner/create-requirements.md`
- `.b2s/skills/architect/review-initial-architecture.md`

## Step 6 - Verify

Produce or update a small example of `current-inputs.json` if the repo already
keeps test fixtures for engine payloads.

## Done criteria

- [ ] policy files are resolved by the engine
- [ ] `current-inputs.json` contains resolved policy paths
- [ ] workflow docs require policy files to be read before generation
- [ ] at least one real prompt is updated to reference policy context
