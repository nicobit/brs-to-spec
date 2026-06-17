# Current State Comparison

## `_.brs2spec` model

Primary characteristics:

- staged workflow
- compact `state/workflow-state.json`
- `next_action` and `next_skill`
- skill registry and prompt lookup
- no persistent per-action queue folders
- repair flow based on artifact scan and state rebuild

Strengths:

- lighter mental model
- lower orchestration overhead
- easier to understand in one session
- token discipline is explicitly built into the orchestrator

Weaknesses:

- still relies on the model to execute deterministic steps faithfully
- state updates are prompt-governed
- validation is weaker and more prose-driven
- artifact outputs are older and less strict than `.brs2spec2`

## `.brs2spec2` model

Primary characteristics:

- event-template-driven workflow
- runtime event files
- queue buckets: `pending`, `processing`, `done`, `failed`
- result files per event
- explicit on-success chaining
- stronger must-include and validation rules

Strengths:

- explicit traceability
- better chaining and repair potential
- stronger artifact-generation prompts
- cleaner mapping between workflow definition and generated artifacts

Weaknesses:

- high orchestration overhead
- more files and more state surfaces
- more token cost if rules remain in prompts
- the LLM can still bypass or fake mechanics unless scripts enforce them

## What `.b2s` should borrow from each

From `_.brs2spec`:

- compact state
- stage-driven orchestration
- skill registry / prompt lookup discipline
- "load only the active prompt" behavior
- repair by scanning artifact truth

From `.brs2spec2`:

- workflow stage graph
- modern skill prompts
- artifact templates
- stronger completeness rules
- clearer business-analysis split

## Conclusion

The right target is not a copy of either framework.

`.b2s` should be:

- staged like `_.brs2spec`
- output-strict like `.brs2spec2`
- script-enforced where both older approaches were still prompt-dependent
