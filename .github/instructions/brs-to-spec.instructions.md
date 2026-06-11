---
applyTo: "initiatives/**,examples/**/initiatives/**"
---

## Persona skill registry — load first

**Load `.brs2spec/module-index.md` at the start of every session.** It contains the Skill Index, persona quick-reference, trigger-to-skill lookup, Hard Rules 1-7, workspace rules, intent triggers, loading rules, and stop rules (~4,200 tokens).

Load `.brs2spec/module-full.md` only when you need: persona definitions (`must_read`, `must_not_do`, `handoff_to`), per-skill `required_inputs`, `done_criteria`, or `stop_conditions`.

After loading `module-index.md`, follow all rules found there. The rules in that file are the authoritative behavioral contract for this framework.
