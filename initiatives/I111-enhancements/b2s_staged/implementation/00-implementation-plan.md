# `.b2s` Implementation Plan

## Goal

Create a new `.b2s/` framework that:

- uses stage/state orchestration instead of persistent event queues
- produces artifacts compatible with `.brs2spec2`
- reuses adapted `.brs2spec2` skill prompts and artifact templates
- moves deterministic orchestration mechanics into scripts

## Design decision

The `.b2s` engine should not emulate `.brs2spec2` event files.

Instead, it should operate on:

- stage graph
- stage actions
- compact workflow state
- script-generated input/validation/state files

## Build slices

### Slice A - foundation

Implement first:

1. `.b2s/` folder structure
2. workflow/state templates
3. stage-action definitions
4. base CLI and script package
5. output-file and gate/state contracts

### Slice B - artifact layer

Implement next:

1. port artifact templates from `.brs2spec2`
2. port and adapt skill prompts from `.brs2spec2`
3. remove event/result-file assumptions from prompts

### Slice C - engine mechanics

Implement next:

1. `next-step`
2. `collect-inputs`
3. `validate-artifact`
4. `update-state`

### Slice D - orchestration

Implement next:

1. `.b2s/prompts/run-workflow.md`
2. gate handling
3. repair/reset

### Slice E - verification

Implement last:

1. staged fixtures
2. command-level tests
3. end-to-end dry run against a sample initiative

## Main implementation principle

Prompts should generate business artifacts.
Scripts should decide what to run, what to read, whether validation passed, and
how state changes.

## Required contracts before implementation

Do not start coding until these are explicit:

- stage-action schema
- script output-file schemas
- workflow-state gate/state model
- fixture root and sample workspace layout

## Recommendation

Do not attempt full artifact coverage on day one.

The first thin slice should prove:

- routing
- business intake
- requirements catalog
- one planning artifact
- readiness check

Once those work, scale the rest of the action graph.
