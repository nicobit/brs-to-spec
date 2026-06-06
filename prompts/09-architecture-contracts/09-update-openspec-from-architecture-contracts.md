# Prompt — Update OpenSpec from Architecture & Contract Extensions

Input:
Read all relevant files under:

```text
features/<feature-name>/architecture-contracts/
```

Task:
Update OpenSpec proposal, design, and tasks so architecture-contract findings are not lost.

Rules:
- Important decisions must appear in proposal/design.
- API/OpenAPI contract changes must produce implementation and validation tasks.
- Data model changes must produce migration and validation tasks.
- Event contracts must produce producer/consumer/test tasks.
- Threat model mitigations must produce implementation or validation tasks.
- Quality scenarios must affect testing/validation tasks.
- Do not duplicate tasks unnecessarily.
