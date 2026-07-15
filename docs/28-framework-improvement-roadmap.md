# Framework Improvement Roadmap

## Purpose

This roadmap turns the current improvement direction into a practical sequence.
The goal is not to make the framework bigger. The goal is to make it:

- easier to start
- harder to misuse
- smoother on the happy path
- clearer when it must stop
- stronger when requirements or architecture are incomplete

The framework should feel lighter to use while becoming more trustworthy.

A core rule for every improvement in this roadmap is:

**extract more, stop less, and make sourced vs. inferred content highly
visible.**

Without that third condition, Phase 1 would optimize for hidden guesswork
instead of safer delivery.

---

## Strategic Position

brs-to-spec should not try to beat every adjacent framework by copying all of
their strengths into one larger system.

It should instead be very clear about its own role:

- **BMAD-style methods** are strong when agent personas drive implementation
  workflows and coding momentum.
- **OpenSpec-style approaches** are strong when teams want a code-adjacent,
  spec-driven implementation loop.
- **Spekit-style approaches** are strong when the main problem is knowledge
  distribution, enablement, and keeping operational guidance easy to consume.
- **Open-SPDD-style approaches** are strong when the team wants a strict
  software-product-definition discipline with formal artifacts.

brs-to-spec is strongest when the problem is:

- enterprise BRS input is ambiguous or uneven
- architecture impact must be made explicit before implementation
- stories should not be written until technical boundaries are understood
- AI output must remain traceable and reviewable
- teams want both structure and proportionality

In other words:

**brs-to-spec should win on governed clarity with low friction, not on maximum
artifact volume.**

---

## Design Direction

The framework should evolve around four layers:

1. **`b2s-flow` as the outer control plane**
   - deterministic, staged, reviewable
   - best when teams want predictable progression
2. **`b2s-dynamic` as the adaptive inner loop**
   - gap-closing, uncertainty-friendly
   - best when the AI must choose the next useful artifact
3. **validators and gates as the verification plane**
   - protect quality without forcing extra ceremony
4. **skills and templates as execution assets**
   - do the specialist work with strong local rules

This keeps the architecture simple:

- one predictable staged path
- one adaptive path
- one shared quality philosophy

---

## What "Better" Means

Improvement should be judged against these questions:

1. Can a new user start without reading too much?
2. Can the workflow continue safely when the BRS is imperfect?
3. Does the framework stop only for real blockers?
4. Are open questions classified by urgency instead of treated equally?
5. Does the user understand why a stage advanced, paused, or failed?
6. Does the framework produce only the artifacts that improve delivery quality?

If a change increases theory, branching, or prompt complexity without improving
those outcomes, it is probably the wrong change.

---

## Current Improvement Priorities

### 1. Preserve complete extraction from imperfect BRS input

The framework should assume the BRS is often incomplete, inconsistent, or not
written in a clean requirements format.

Desired behavior:

- extract every explicit requirement that can be grounded in source text
- decompose compound requirements into atomic children when useful
- mark inferred requirements clearly instead of silently inventing them
- keep source traceability even when the original BRS is messy
- make sourced vs. inferred content visually obvious in downstream artifacts
  that depend on requirement interpretation

This is the correct foundation because users will not always have well-written
FR/NFR sections.

### 2. Distinguish blockers from deferred detail

Not every open question should stop progress.

The framework should classify questions into:

- **required before delivery planning**
- **required before epic elaboration**
- **required before coding handoff**
- **informational / monitor only**

This allows the workflow to continue when uncertainty is real but not yet
critical.

### 3. Make stop conditions narrower and more explicit

A stop should happen only when the missing information would make the next
artifact misleading, unsafe, or structurally wrong.

This means:

- do not stop just because some detail is missing
- stop when repository ownership, boundary choice, compliance obligations, or
  user-flow intent are still unresolved at the stage that depends on them

### 4. Reduce visible ceremony while keeping hidden rigor

The user should experience fewer interruptions, fewer manual decisions, and
clearer next steps.

The framework should do more of this internally:

- auto-classify open questions
- auto-decide whether a UI artifact is needed
- auto-detect whether the current gap is architectural, planning, or coding
- auto-route to the smallest safe next action

### 5. Clarify product positioning

The framework should be easy to explain in one sentence:

**brs-to-spec is the low-friction governance layer that turns uneven enterprise
requirements into implementation-safe delivery packages.**

That positioning is more durable than trying to compete directly as:

- a coding method
- a knowledge base
- a documentation wiki
- a universal spec language

---

## Recommended Roadmap

### Phase 1 - Friction removal

Focus on the parts that improve user trust immediately.

- strengthen extraction from weak BRS input
- continue downstream when open questions are not yet stage-blocking
- improve stop messages so they explain exactly what is missing and why it
  matters now
- make the "next action" explanation short and concrete

Expected result:

- fewer unnecessary stops
- better artifact completeness from real-world BRS documents
- lower anxiety for users who are unsure whether their input is "good enough"

### Phase 2 - Smarter orchestration

Make the framework adapt without becoming vague.

- give each stage explicit blocker criteria
- add bounded retry/repair behavior before escalation
- let the workflow propose a provisional path when certainty is partial but
  sufficient
- keep a strong distinction between "draft with flagged assumptions" and
  "accepted decision"

Expected result:

- better resilience
- fewer dead ends
- more predictable behavior when artifacts are incomplete

### Cross-cutting workstream - Validator hardening

Prompt and skill improvements are not enough on their own.

The framework also needs a parallel validator-hardening workstream so that
safer behavior is enforced consistently rather than depending on prompt
compliance.

Priority areas:

- validate that inferred requirements are explicitly labeled and remain
  distinguishable from source-backed requirements
- validate that stage-blocking open questions include a correct
  `required-before` classification
- validate that downstream artifacts do not silently upgrade assumptions into
  accepted facts
- validate that stop reasons clearly explain what is missing and which next
  artifact depends on it
- validate that requirement decomposition preserves parent-child traceability

Expected result:

- less prompt drift
- more trustworthy continuation behavior
- better protection against "extract more" becoming "invent more"

### Phase 3 - Productization and differentiation

Once the inner behavior is smoother, sharpen how the framework presents itself.

- document `b2s-flow` and `b2s-dynamic` as complementary, not competing
- show a simple workflow selector with examples
- document when to use brs-to-spec before BMAD or before coding-agent flows
- explain how governance quality is preserved without forcing heavyweight
  process on every initiative

Expected result:

- clearer adoption story
- stronger differentiation
- less confusion about which workflow type to choose

---

## What To Avoid

The easiest way to damage the framework is to improve it by adding more visible
process.

Avoid:

- new phases unless an existing phase is structurally overloaded
- new artifacts that only restate information already present elsewhere
- mandatory human gates for low-risk clarification
- broad "AI loop" behavior that makes outputs less predictable
- framework language that sounds impressive but hides decision rules

The framework should feel more opinionated and more helpful, not more complex.

---

## Concrete Near-Term Changes

These are the highest-value changes to prioritize next:

1. **Atomic requirement robustness**
   - complete extraction from imperfect BRS prose
   - explicit decomposition and source grounding
   - visually obvious explicit vs. inferred labeling
2. **Stage-aware open-question handling**
   - continue when questions are relevant later but not now
   - stop only when the current stage truly depends on the answer
3. **Blocker taxonomy**
   - distinguish missing evidence, missing decision, missing ownership, and
     missing user-intent detail
4. **Bounded repair loop**
   - retry once or twice with a focused clarification artifact before hard stop
5. **Validator hardening**
   - enforce inference labeling, traceability, and correct blocker staging
   - catch silent assumption upgrades before they propagate
6. **Cleaner workflow messaging**
   - every pause should say: what is missing, why it matters now, what artifact
     depends on it, and how to resume

---

## Success Criteria

The roadmap is working if the framework becomes:

- easier to run on imperfect enterprise input
- less likely to stop prematurely
- more complete in requirement extraction
- clearer in its stop reasons
- easier to explain against BMAD, OpenSpec, Spekit, and Open-SPDD
- more trusted by users who do not want extra ceremony

---

## Summary

The best next version of brs-to-spec is not the most elaborate version.

It is the version that:

- extracts more from weak input
- blocks less often for non-critical uncertainty
- makes sourced vs. inferred interpretation impossible to miss
- makes its decisions easier to understand
- keeps governance strong without making the user feel governed

That is the path to becoming easier to use and stronger than the adjacent
frameworks for this specific problem space.
