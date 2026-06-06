# Prompt — Create API Contract

Use when REST API endpoints are added or changed.

Output:
Create:

```text
features/<feature-name>/architecture-contracts/api-contract.md
```

Include:
- endpoints,
- request/response payloads,
- status codes,
- authorization,
- validation,
- errors,
- audit/logging,
- backward compatibility,
- open questions.

Rules:
- Do not invent endpoints not justified by requirements/stories.
- Mark unclear payload fields as open questions.
