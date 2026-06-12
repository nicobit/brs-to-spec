# Gap Assessment Matrix: Context-Driven AI Maturity

This matrix translates the initial analysis into a practical assessment of where the framework is already strong and where further enhancement would most improve AI-safe delivery.

| Gap area | Current strength | Current gap | Risk if unchanged | Potential impact if improved | Suggested priority |
|---|---|---|---|---|---|
| Context packaging per task | Strong artifact set and stage outputs | No explicit per-task context bundle definition | Agents may receive too much, too little, or mixed-priority context | Higher implementation accuracy and lower prompt ambiguity | High |
| Context freshness and drift detection | Good stage and artifact completion flow | Weak visibility into stale downstream handoff after upstream changes | Agents may implement from outdated assumptions or superseded rules | Safer execution and fewer invalid handoffs | High |
| Explicit context hierarchy | Implied hierarchy across artifacts | No clear precedence model when artifacts conflict | Conflicting guidance can produce inconsistent agent behavior | More deterministic AI decisions | High |
| Retrieval strategy | Clear artifact inventory | Limited guidance on what to load by task type, risk, or role | Context windows may fill with low-value material while critical context is missed | Better signal-to-noise ratio in AI interactions | High |
| Feedback from implementation back into context | Strong upstream-to-downstream governance | Weak downstream learning loop into readiness, rules, and templates | Repeated mistakes remain local and framework maturity plateaus | Continuous improvement of prompts and artifacts | Medium-High |
| Context suitability scoring | Strong governance readiness concept | No explicit scoring for AI consumability | Approved artifacts may still be poor AI inputs | Better handoff quality for coding agents | Medium-High |
| Live system context for brownfield work | Brownfield concerns are explicitly recognized | Operational and repository reality is not yet first-class context | Agents may miss implementation conventions and real impact surfaces | Better brownfield accuracy and fewer regressions | High |
| Examples as context objects | Good templates and workflow guidance | Limited use of approved exemplar-based context | Agents may understand rules but miss the intended pattern quality | Faster, more consistent artifact generation | Medium |
| Role-specific context views | Clear artifact consumers | Context is not yet systematically projected by audience | Each consumer must manually reinterpret the same material | Better usability across PO, architect, reviewer, and coding-agent flows | Medium |
| Context loss controls across stage transitions | Strong traceability intent | Limited preservation of assumptions, rationale, and unresolved tensions | Important nuance may be lost before implementation or review | Better continuity and fewer downstream misunderstandings | Medium-High |

## Priority interpretation

The highest-value gaps are the ones that affect whether an AI agent receives the right context at the right time in the right form.

These are:

- context packaging per task
- context freshness and drift detection
- explicit context hierarchy
- retrieval strategy
- live system context for brownfield work

These areas most directly influence whether the framework behaves as a truly context-driven system instead of a well-structured document workflow.

## Maturity reading

The framework appears strong in:

- creating context
- sequencing context
- governing context

The framework appears less mature in:

- dynamically selecting context
- validating context freshness
- optimizing context for specific AI consumers
- learning from downstream execution outcomes

## Recommended next focus

If these gaps are addressed in order, the most practical first wave would be:

1. Define a per-task context packaging model.
2. Add explicit artifact precedence and conflict-resolution rules.
3. Introduce drift detection for handoff artifacts after upstream changes.
4. Define retrieval guidance by task type, role, and delivery mode.
5. Enrich brownfield mode with live system context inputs in addition to narrative documents.

That sequence would improve the framework's context-driven behavior without requiring a full redesign of the existing artifact model.
