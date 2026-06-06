# Large Feature / Multi-Quarter Planning Track

This track is for large BRS-driven initiatives that may span more than one quarter.

It prevents the framework from becoming a story factory for an entire large BRS.

## Core principle

For a large BRS:

```text
Decompose the whole BRS.
Align the whole BRS with architecture.
Plan and slice the whole BRS.
Detail only the next increment.
```

Do **not** create detailed user stories for the entire multi-quarter scope too early.

## Why this track exists

Large BRS documents often contain:

```text
multiple business objectives
many requirements
multiple capabilities
several epics/features
architecture dependencies
infrastructure and CI/CD needs
business and regulatory constraints
multi-quarter delivery scope
```

If the full BRS is converted directly into detailed user stories, the result can be noisy, unstable, and wasteful.

The right approach is:

```text
Full BRS
  ↓
requirements
  ↓
architecture alignment
  ↓
delivery structure
  ↓
delivery slicing / roadmap
  ↓
selected next increment
  ↓
detailed stories and engineering contracts only for selected increment
```

## When to use this track

Use it when:

```text
the BRS is large
the feature spans more than one quarter
multiple teams are involved
multiple epics/features are expected
architecture decisions are not fully resolved
infrastructure or enablement work is significant
business priority is not fully clear
not everything should be built in the first increment
```

Skip it when:

```text
the change is small
the feature fits in one sprint or one small release
scope is already clear
there is only one feature/capability
```

## Where it fits

The normal business intake remains stable:

```text
00a Extract BRS from Word
00b Extract architecture from Word
01 Summarize BRS
02 Extract requirements
03 Review BRS + requirements against architecture
04 Create delivery structure
```

Then, for large/multi-quarter BRS initiatives, run:

```text
prompts/06-planning/01-create-delivery-slicing-and-roadmap.md
prompts/06-planning/02-select-next-increment-scope.md
prompts/06-planning/03-create-increment-handoff.md
```

After that, run detailed user-story generation and engineering contracts only for the selected increment.

## Recommended flow for large BRS

```text
Whole BRS:
  00a extract BRS
  00b extract architecture
  01 summarize BRS
  02 extract requirements
  03 architecture alignment
  04 delivery structure
  06-planning/01 delivery slicing and roadmap

Selected next increment:
  06-planning/02 select next increment scope
  05 create user stories for selected increment
  07 business test expectations for selected increment
  technical spec
  architecture contracts as needed
  enablement as needed
  handoff package
```

## Outputs

```text
planning/delivery-slicing.md
planning/next-increment-scope.md
planning/increment-handoff.md
```

## Important rule

For a multi-quarter BRS, `05-create-user-stories.md` should not be run against the entire BRS unless explicitly intended.

Use it against the selected next increment.
