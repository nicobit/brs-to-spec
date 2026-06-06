# Prompt — Create Domain Model / DDD Model

Use only when the feature has non-trivial business rules, workflows, state transitions, business invariants, domain events, or ambiguous business terminology.

Output:
Create:

```text
features/<feature-name>/architecture-contracts/domain-model.md
```

Include:
- ubiquitous language,
- bounded context,
- entities,
- value objects,
- aggregates,
- domain services,
- domain events,
- state model,
- business invariants,
- validation rules,
- domain exceptions,
- mapping to requirements and user stories.

Rules:
- Keep it lightweight.
- Do not force DDD jargon if the feature is simple.
