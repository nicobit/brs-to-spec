# Agile Delivery Light Flow - UI Action Trigger Plan

## Purpose

Define when `agile-delivery-light-flow` should take explicit UI-focused action, what artifact it should create, and where that action should sit in the current phased flow.

This plan assumes the current framework direction remains:
- planning-first by default
- epic elaboration before coding prep
- implementation contracts and coding handoff generated on demand

---

## Problem Statement

The current light flow is much stronger for:
- requirement traceability
- business rules
- story slicing
- data and API implementation prep

It is weaker for UI-bearing change because UI intent is still too implicit.

Without a UI-specific contract, a coding agent can still invent:
- screen behavior
- component changes
- validation messages
- loading, empty, success, and error states
- navigation behavior
- accessibility behavior
- design-system interpretation

So the issue is not only "missing UX expertise." The issue is that the workflow does not yet make UI change intent explicit enough before coding.

---

## Recommendation

Do not make UI artifacts mandatory for every initiative.

Instead:

- Keep the current default light-flow path for non-UI work
- Add a conditional UI-specific action for UI-bearing epics
- Trigger that action during epic elaboration / pre-handoff, not at routing and not only at coding time

---

## Trigger Principle

The framework should take UI-specific action only when all of the following are true:

1. The initiative includes a real frontend/UI layer
2. A specific epic or story actually changes user-facing behavior
3. The UI behavior is important enough that silent inference by a coding agent would be risky

This keeps the light flow lightweight while still protecting UI-heavy changes.

---

## Trigger Timing

### Do not trigger at routing

Reason:
- too early
- not enough detail about actual screen/component changes

### Do not wait until coding handoff

Reason:
- by then story boundaries are already fixed
- vague UI intent will already have propagated into the coding package

### Trigger during epic elaboration / pre-handoff

Best point in the current light flow:
- after `create-delivery-skeleton`
- during or immediately after `create-epic-folders`
- before `create-epic-coding-handoffs`

This is the point where the framework already knows:
- the epic scope
- the story set
- the layers touched
- the dependencies

That is enough to define UI change intent properly.

---

## Trigger Rule for Agile Delivery Light Flow

The UI-specific action should become mandatory for an epic when:

- `planning/delivery-skeleton.md` marks `Frontend` as present in `## Application Layers`
- and the epic has at least one story whose `Layers` includes `Frontend`
- and at least one of the following is true:
  - new screen, page, modal, wizard, or form
  - change to navigation or flow order
  - new or changed field validation behavior
  - new or changed empty/loading/error/success states
  - new or changed visibility/permission behavior in UI
  - accessibility-sensitive interaction
  - responsive/mobile-specific behavior matters

It should remain optional when:
- the UI is touched only cosmetically
- the work is pure content swap with no behavior change
- the frontend layer is present but not materially changed in the selected epic

It should not trigger when:
- the epic is backend-only
- the epic is integration-only
- the epic changes only persistence/API behavior

---

## Proposed New Action

Suggested action ID:

`create-ui-change-spec`

Suggested stage placement:

- Stage `3-epic-elaboration`, after `create-epic-folders`
- or a narrow pre-handoff step between epic review and coding handoff

Preferred behavior:
- conditional per epic
- generated only for UI-bearing epics

---

## Proposed Artifact

Suggested artifact name:

`epics/E-NNN-<slug>/ui-change-spec.md`

This should not be a full design document. It should be a compact implementation-facing UI contract.

### Required sections

1. Affected Screens and Components
- which screens, views, dialogs, forms, tables, or widgets change

2. User Interaction Changes
- what the user can now do
- what changes in flow or sequence

3. Field-Level Behavior
- input fields
- defaults
- validation rules
- formatting
- visibility conditions

4. UI States
- loading
- empty
- success
- validation error
- system error
- unauthorized/forbidden

5. Navigation and Entry/Exit Behavior
- where the user comes from
- where the user goes next
- cancel/back behavior

6. Permission and Visibility Rules
- who can see the control
- who can use the control
- disabled vs hidden behavior

7. Accessibility and Responsiveness Constraints
- keyboard behavior
- labels/announcements
- focus management
- mobile/tablet expectations if relevant

8. Design-System / Existing Pattern References
- exact existing components or screens to follow

---

## Relationship to Existing Artifacts

### Story

The story should still contain:
- user intent
- business context
- linked requirements
- Gherkin acceptance criteria
- dependencies
- open questions

The story should not carry the full UI contract when that would make it bloated.

### Implementation contract

The implementation contract should remain focused on:
- data entities
- API surface
- events
- business rules
- non-functional constraints

UI detail should not be forced into the implementation contract unless directly relevant.

### Coding handoff

The coding handoff should reference:
- stories
- implementation contract
- UI change spec, when present

---

## Why This Is Better Than "Add a UX Agent"

A UX agent may help generate the artifact, but the important thing is the artifact contract itself.

Without a required UI output:
- the UX agent becomes optional advice
- coding still drifts
- review still lacks a stable UI checklist

So the correct design is:

- define the conditional UI artifact first
- optionally introduce a UX persona/agent to produce it

Artifact first, agent second.

---

## Other Similar Gaps to Watch

UI is the clearest current gap, but it is not the only one.

Other artifact families that may need similar treatment later:
- rollout / migration / feature-flag contract
- authorization / policy behavior contract
- content / messaging / localization contract
- operational support / runbook impact

These should not be added now unless they become recurring delivery failures.

---

## Suggested Implementation Sequence

1. Add the decision rule for when UI action is mandatory
2. Add `create-ui-change-spec` as a conditional light-flow action
3. Add a compact `ui-change-spec.md` template
4. Update story prompts so frontend stories reference the UI spec when present
5. Update coding handoff to consume the UI spec
6. Add validation so UI-bearing epics fail if the UI artifact is required but missing

---

## Decision Summary

For `agile-delivery-light-flow`, the framework should take explicit UI-focused action:
- only when `Frontend` is truly in scope
- at epic elaboration / pre-handoff time
- through a conditional UI-specific artifact
- not merely by adding a UX agent without a contract

This preserves the light-flow philosophy while making UI-heavy change safer for AI coding.
