# What Keeps The Framework From 9.5

This document captures the main reasons the framework does not yet score at the very top tier.

## 1. Stronger as a framework than as a product

The ideas are better than the packaging.

A strong architect, engineering lead, or delivery lead will see the value quickly, but broader audiences may experience the weight of the framework before they experience the payoff.

This is a productization issue more than a strategy issue.

## 2. Artifact-rich, but not yet fully context-orchestrated

The framework is strong at defining:

- what artifacts should exist
- when they should exist
- who should consume them
- what stage should happen next

It is less mature, today, at defining:

- exactly what context should be loaded for each downstream AI action
- how context should be prioritized dynamically
- how context freshness should be surfaced operationally
- how context should be preserved and reused role by role

This is the largest structural reason it does not yet feel like a fully context-driven system.

## 3. Adoption friction is still real

The framework asks users to operate with discipline.

That is often the correct choice, especially in enterprise environments, but it creates a real adoption hurdle compared with lighter spec-to-code or repo-native agent workflows.

Some teams will initially interpret the framework as heavier than necessary before they understand the risk it is protecting against.

## 4. Developer ergonomics lag behind governance quality

The framework is better at controlling engineering entry conditions than at making everyday execution feel easy and natural.

That means:

- the upstream story is stronger than the in-repo story
- the governance model is stronger than the execution ergonomics
- the architect and delivery-lead value is more immediately obvious than the developer value

This is fixable, but it matters.

## 5. Value proposition is powerful, but not yet maximally compressed

The framework has a strong core idea:

transform raw business and architecture input into AI-safe, implementation-ready engineering context

But this idea still needs sharper packaging so that external readers and first-time adopters grasp it quickly.

At the moment, the value often becomes clearer after reading multiple documents instead of one immediately compelling message.

## 6. Still early on learning loops and adaptive behavior

The framework is already strong at structured flow and controlled handoff.

It is less mature, today, at:

- learning from repeated downstream issues
- adapting context selection based on task patterns
- using examples as first-class pattern guidance
- reshaping context by role without losing source-of-truth discipline

That is why the Wave 3 work matters so much.

## Summary

The framework is not held back by lack of rigor, intelligence, or structure.

It is held back mainly by:

- productization
- usability
- context orchestration maturity
- execution ergonomics

Those are good problems to have, because they are signs that the core framework idea is already strong.
