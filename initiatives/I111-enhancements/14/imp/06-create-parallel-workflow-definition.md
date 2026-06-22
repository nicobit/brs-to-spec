# Prompt 06 - Create the Parallel Workflow Definition

## Context

The new workflow type needs its own `workflow-definition.yaml`, not just a
copied stage-action file. This is where the stage graph for the parallel
workflow becomes explicit.

Before making changes, read these files in full:

- `.b2s/workflow-types/enterprise-modular/workflow-definition.yaml`
- `.b2s/workflow-types/fast-path/workflow-definition.yaml`
- `framework_enhancement/14/plan.md`

## Goal

Create the workflow-definition file for the new workflow type.

## Design principle

The new workflow should be parallel to the existing workflow types, but it
should reuse the same broad delivery lifecycle wherever possible:

- routing
- business intake
- business analysis
- planning
- engineering readiness
- quality or technical specification stages
- handoff
- review package

## Recommended stage model

Prefer adding a dedicated stage for technical specifications rather than
smuggling all such actions into the existing quality-gates stage.

Recommended shape:

```text
0-routing
2-business-intake
2b-business-analysis
3-planning
4-engineering-readiness
4c-technical-specifications
4d-quality-gates
5-handoff
6-review-package
```

or an equivalent stage graph with the same semantic clarity.

## Important rule

Technical specifications are not just another quality gate. They are
design-detail artifacts consumed by descendant delivery steps.

## Done criteria

- [ ] New workflow definition exists under the new workflow-type directory
- [ ] Stage graph is explicit and readable
- [ ] Technical specifications have a dedicated semantic place in the workflow
- [ ] Existing workflow definitions remain unchanged unless explicitly required
