# Phase to Prompt Family Map

This table is guidance for maintainers. It is not a hardcoded restriction.

| Phase area | Default family direction | Notes |
|---|---|---|
| business intake | `b2s` | enterprise intake context is framework-native |
| requirements | `speckit` | strongest fit for specification-first clarity and traceability |
| architecture | `b2s` with `arc42` / `ADR` influence | keep the current skill tree; use family strategy as guidance |
| epics and features | `bmad` | product grouping and prioritization bias |
| stories | `hve` | implementation-ready decomposition bias |
| AI coding handoff | `hve` | strongest fit for coding-agent-ready packages |
| BDD and test artifacts | `b2s` with targeted external influence | keep pragmatic unless a stronger artifact-specific family emerges |

Guidance:

- choose the family that best serves the artifact, not the whole framework
- do not force every phase into one universal prompt style
- prefer additive family metadata over prompt-tree rewrites
