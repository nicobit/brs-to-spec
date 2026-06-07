# Prompt — Identify Required Conditional Quality Gates

Use this prompt only after the engineering readiness check.

Read the **Conditional Quality Gates** table in
`engineering-readiness/readiness-check.md` and return only the gates that are
**Triggered**.

For each triggered gate:
- confirm it is marked `Required? = Yes`,
- name the owner,
- point to the prompt that produces it under
  `prompts/4-engineering-readiness/quality-gates/`,
- point to the output under `quality-gates/`.

Rules:
- Do not generate gates that are not triggered.
- A triggered gate is mandatory before implementation, merge, or release
  (depending on the gate).
- Do not turn this into the default workflow — gates are a controlled escalation.
