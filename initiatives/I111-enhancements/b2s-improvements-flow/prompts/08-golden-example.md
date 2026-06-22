# Prompt 8 — Golden Example Generation

Create a complete golden example for `.b2s`.

Purpose:

The framework currently has good structure, but it needs proof that it can generate deep, specific, non-generic, implementation-ready output.

Create a realistic enterprise BRS example and run it through the full `.b2s` flow.

The example should be complex enough to test the framework properly.

Suggested domain:
Enterprise subscription approval workflow, loan origination, client onboarding, payment approval, digital asset subscription/redemption, or another regulated enterprise process.

The BRS should include:

- business objective
- actors
- process steps
- business rules
- role-based permissions
- validation rules
- state transitions
- integration with at least one external/internal system
- audit requirement
- error cases
- reporting or notification requirement
- at least one ambiguity/open question

Generate the complete output:

- business intake
- requirements
- business rules
- architecture review
- delivery structure
- epic packages
- feature packages
- story packages
- acceptance criteria
- BDD scenarios
- traceability matrix
- readiness check
- test strategy
- handoff package
- review package

The golden example must prove that the framework creates:

1. specific epics
2. coherent features
3. implementation-ready stories
4. testable acceptance criteria
5. meaningful BDD scenarios
6. traceability from BRS to stories and tests
7. architecture-aware implementation context
8. coding-agent prompts that can be used by Copilot/Codex/Claude/Devin

Do not use toy content such as "Story 1", "Feature 1", or "Implement functionality".

Add the golden example under:

```text
examples/golden-enterprise-b2s/
```

Include a README explaining:

- input BRS
- selected delivery mode
- generated artifacts
- how to evaluate output quality
- known limitations
