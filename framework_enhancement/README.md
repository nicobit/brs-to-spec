# Framework Enhancement Plan

These prompts define a set of targeted improvements to the BRS to Spec framework,
motivated by the analysis of "Stop Writing Specs. Start Writing Facts." (Wasowski, 2026).

## Background

The article distinguishes between two types of artifact:
- **Specs** — prose interpreted by LLMs, fragile across model upgrades
- **Facts** — executable assertions verified by machines, model-agnostic and durable

The BRS to Spec framework is largely immune to this critique because its artifacts are
primarily consumed by humans, not fed back into LLMs to generate code. However, five
specific gaps were identified where the framework can be strengthened.

## Enhancements — priority order

| # | File | Area | Effort | Value |
|---|---|---|---|---|
| 1 | [01-elevate-bdd-as-primary-artifact.md](01-elevate-bdd-as-primary-artifact.md) | Elevate BDD scenarios as the primary durable artifact | Low | High |
| 2 | [02-ci-wiring-for-quality-gates.md](02-ci-wiring-for-quality-gates.md) | Add CI wiring guidance for quality gates | Medium | High |
| 3 | [03-human-vs-execution-artifact-boundary.md](03-human-vs-execution-artifact-boundary.md) | Document human vs execution artifact boundary | Low | Medium |
| 4 | [04-tighten-implementation-prompt.md](04-tighten-implementation-prompt.md) | Tighten implementation prompt to be constraint-based | Medium | Medium |
| 5 | [05-model-upgrade-impact-guide.md](05-model-upgrade-impact-guide.md) | Add model upgrade impact guide | Low | Medium |

## How to use these prompts

Each file is a self-contained implementation prompt. To implement an enhancement:

1. Open the enhancement file and read the full context and "What needs to change" section
2. Follow the "Implementation steps" in order
3. Use the "Quality bar" section to verify the implementation is complete
4. Enhancements 1, 3, and 5 are documentation-only — low risk, implement first
5. Enhancements 2 and 4 modify existing prompts and templates — review carefully before saving

## Recommended implementation order

Start with 1 → 3 → 5 (documentation only, low risk).
Then 4 (prompt restructuring, medium risk).
Then 2 (new doc + new prompt + template changes, most effort).

Enhancements are independent — each can be implemented without the others,
but 1 and 2 are complementary and work best together.
