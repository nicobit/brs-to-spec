# Template Quality Guidelines

v1.0.2 improves output quality by strengthening templates.

## Quality rule

Every important artifact should answer:

```text
What decision was made?
What evidence supports it?
What risk remains?
Who owns the action?
Before which delivery stage is the action required?
Which requirement or architecture constraint is affected?
```

## Required fields for review artifacts

Use these fields in review outputs:

| Field | Why it matters |
|---|---|
| Decision | Prevents vague review outcomes |
| Evidence | Prevents unsupported AI conclusions |
| Gap / Risk | Makes unresolved concerns visible |
| Required action | Turns review comments into work |
| Owner | Prevents orphaned actions |
| Required before | Clarifies whether action blocks implementation, merge, or release |
| Traceability | Links output back to BRS, architecture, and deliverable |

## Avoid

```text
Looks good.
No major issues.
Add tests.
Architecture is aligned.
```

## Prefer

```text
Control area | Status | Evidence | Gap / Risk | Required action | Owner | Required before
```

## Keep templates compact

Do not add more documents unless the readiness check triggers them.
Improve the quality of the generated document, not the number of documents.
