# Skill: Traceability Matrix

Use this skill to connect the BRS to the generated backlog.

## Required Mapping

Each BRS item should map to one or more of:

```text
BRS item → capability → epic → story → acceptance criteria → test note
```

## Status Values

Use:

- Covered
- Partially covered
- Not covered
- Needs clarification

## Gap Types

Use these gap types:

- Missing capability
- Missing epic
- Missing story
- Missing acceptance criteria
- Missing NFR coverage
- Missing security/audit/compliance coverage
- Missing integration coverage
- Ambiguous BRS source
- Conflicting requirements

## Quality Rules

- Do not mark an item covered unless there is clear evidence.
- If coverage is only implied, mark as partially covered.
- If mapping depends on an assumption, mark as needs clarification.
- Do not merge unrelated BRS items into one vague backlog item.
