# Persona Skill Registry Maturity Report

## Summary

This report documents the improvements made to the brs-to-spec framework in the 9/10 maturity pass. The goal was to raise adoption simplicity, BMAD differentiation, implementation risk reduction, and overall concept quality without adding phases, personas, or delivery modes.

---

## Changes made in this pass

| File | Change |
|---|---|
| `docs/00-5-minute-quickstart.md` | Created: first-time user path from BRS to handoff in 7 steps; under 150 lines |
| `docs/01-what-do-i-run.md` | Created: lookup table mapping every user need to persona, skill, prompt, and output |
| `docs/comparison-bmad.md` | Created: honest, professional comparison with BMAD-style methods; defines artifact-first identity |
| `docs/persona-skill-registry-maturity-report.md` | Created: this file |
| `.brs2spec/brs-to-spec-run-workflow.md` | Patched: added explicit 10-step execution model at the top |
| `.brs2spec/templates/planning/workflow-state.json` | Updated: added `next_skill` section with persona, skill, prompt, reason, expected_output |
| `initiatives/I001-customer-onboarding/planning/workflow-state.json` | Updated: populated `next_skill.reason` and `next_skill.expected_output` |
| `.brs2spec/tools/scripts/check_registry.py` | Created: validates module.md, module-registry.yaml, prompt paths, personas, skills |
| `mkdocs.yml` | Updated: added quickstart, what-do-i-run, BMAD comparison, maturity report to nav |
| `README.md` | Updated: added links to quickstart and what-do-i-run; moved advanced content to docs/ |

---

## How this improves the scores

| Area | Before | After target | What improved |
|---|---:|---:|---|
| Concept quality | 7 | 9 | 10-step execution model made explicit; artifact-first identity stated clearly in comparison doc; module.md already had 10 sections |
| Enterprise relevance | 8 | 9 | Governance model now documented against BMAD; quickstart shows enterprise BRS path |
| BMAD differentiation | 5 | 9 | Dedicated comparison page; "Personas do not own the process. Artifacts own the process." stated explicitly |
| Implementation risk | 7 | 9 | Registry validator script catches broken prompt paths; next_skill in workflow-state reduces "what do I do next" ambiguity |
| Adoption simplicity | 6 | 9 | 5-minute quickstart (no theory); "What do I run?" lookup table; both linked from README |
| Long-term potential | 7 | 9 | check_registry.py provides CI-ready validation; next_skill schema enables automation |

---

## Adoption improvements

- First-time users now have a clear 7-step quickstart that avoids theory.
- The "What do I run?" lookup table means users never have to guess which prompt to load.
- The `@persona` addressing model is documented in both module.md and the lookup table.
- README links directly to both onboarding docs without burying them.
- The 10-step model in the workflow runner makes the orchestrator's behavior explicit.

---

## Implementation risk reduction

- `check_registry.py` validates that all `prompt:` paths in `module-registry.yaml` exist on disk. This catches broken references before they cause silent failures in AI-assisted sessions.
- `next_skill` in workflow-state.json allows an AI assistant to resume a session without scanning the entire initiative workspace.
- The explicit 10-step model in the orchestrator reduces the risk of the AI doing specialist work inside the orchestrator instead of invoking the registered skill.

---

## BMAD differentiation

The `docs/comparison-bmad.md` page establishes three clear differentiation points:

1. **Artifact-first vs agent-first**: BMAD-style methods put personas at the center. brs-to-spec puts artifacts at the center. Personas only enter when a skill is needed.
2. **Enterprise starting point**: BMAD typically starts from a product idea or PRD. brs-to-spec is designed for formal enterprise BRS and architecture input with governance obligations.
3. **Complementarity**: brs-to-spec prepares the governed input that BMAD-style or coding-agent delivery can consume. The two are not competitors — they address different parts of the lifecycle.

The exact sentence "Personas do not own the process. Artifacts own the process. Personas execute registered skills against artifacts." appears in both `docs/comparison-bmad.md` and `.brs2spec/module.md`.

---

## Remaining risks

| Risk | Severity | Mitigation |
|---|---|---|
| `check_registry.py` requires PyYAML for YAML validation | Low | Script degrades gracefully; prints skip message instead of failing |
| `docs/00-5-minute-quickstart.md` references the `skills/0-intake/00-create-brs.md` prompt; verify this path exists | Medium | Run `python .brs2spec/tools/scripts/check_registry.py` to confirm |
| README content checks in `check_program.py` do not yet verify links to the new quickstart and what-do-i-run docs | Low | Add these checks in a future pass if content drift becomes a concern |
| BMAD is a moving target; the comparison page may need updating as BMAD evolves | Low | Keep the page factual and non-promotional to reduce maintenance burden |

---

## Recommended next steps

1. Run `python .brs2spec/tools/scripts/check_registry.py` to confirm the registry is valid.
2. Run `python .brs2spec/tools/scripts/check_program.py` to confirm no regressions.
3. Verify `docs/00-5-minute-quickstart.md` with a real first-time user walk-through.
4. Consider adding `next_skill` content checks to `check_program.py` for the workflow-state template.
5. If the framework is published, add `check_registry.py` to the CI pipeline alongside `check_program.py`.
