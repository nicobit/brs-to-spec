# Prompt - Create Compact Handoff Package

## Role

You are an engineering lead creating a lightweight summary of an already-prepared handoff package.

## Context

This is an optional summary helper.

It does not replace the real downstream handoff artifacts under:

```text
specs/...
or
standalone-delivery/...
```

## Purpose

Create a compact summary for engineering review, stakeholder briefings, or downstream coordination after the real handoff package already exists.

## Official Inputs

Use normalized artifacts when available:

```text
input/brs.md or input/brs/*.md
input/architecture.md or input/architecture/*.md
input/input-package.md
engineering-readiness/readiness-check.md
quality-gates/*.md
specs/<active-deliverable>/*
standalone-delivery/<active-deliverable>/*
```

## Output path

```text
handoff/compact-handoff-summary.md
```

## Rules

- Include active deliverable, architecture constraints, quality gates, and execution mode.
- Do not create a second source of truth.
- Do not invent missing tasks, requirements, or decisions.
- Treat this file as a summary-only projection of approved source artifacts.
