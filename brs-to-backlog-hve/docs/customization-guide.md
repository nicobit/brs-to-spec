# Customization Guide

This project is intentionally generic. Customize it for your organization and delivery model.

## Add Your Own Labels

Edit:

```text
.github/prompts/05-create-github-issues.prompt.md
```

Add labels such as:

- domain name
- platform
- cloud
- data
- regulatory
- frontend
- backend
- api
- database
- test-automation

## Add Your Definition of Ready

Edit:

```text
.github/instructions/backlog-governance.instructions.md
```

Add criteria used by your delivery organization.

## Add Your Story Template

Edit:

```text
.github/instructions/story-quality.instructions.md
```

For example, add:

- Figma link
- API contract link
- data model link
- logging requirement
- support model
- rollout notes

## Add Your Compliance Requirements

Edit:

```text
.github/instructions/brs-traceability.instructions.md
```

Add required controls for:

- audit evidence
- access control
- data retention
- privacy
- segregation of duties
- regulatory reporting

## Add Your Architecture Constraints

Edit:

```text
input/architecture.md
```

The better the architecture context, the more precise the stories and dependencies will be.
