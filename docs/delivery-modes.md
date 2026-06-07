# Delivery Modes

This framework is adaptive. It should not be used with the same level of ceremony for every change.

Use one of these modes:

```text
Fast Path
Standard Path
Enterprise Path
Enterprise + Modular Delivery
```

## Fast Path

Use when the request is small and already clear.

Recommended flow:

```text
request / short BRS
  ↓
OpenSpec directly
  ↓
proposal.md / design.md / tasks.md
  ↓
implementation
```

Do not run the full BRS intake.

## Standard Path

Use when there is a BRS or business request that needs clarification, but the delivery remains limited.

```text
BRS
  ↓
business intake summary
  ↓
requirements / gaps
  ↓
next increment
  ↓
OpenSpec change
```

## Enterprise Path

Use when the initiative is large, formal, or business-critical.

```text
BRS
  ↓
business intake
  ↓
requirements review
  ↓
gaps/questions
  ↓
architecture alignment
  ↓
delivery slicing
  ↓
next increment
  ↓
OpenSpec handoff
```

## Enterprise + Modular Delivery

Use when the BRS is large enough that a linear Epic → Feature → User Story decomposition becomes too abstract or too large for AI coding agents.

Typical triggers:
- effort greater than 12-15 person-months,
- delivery longer than one quarter,
- several systems or teams involved,
- high context-saturation risk for downstream AI coding tools,
- multiple vertical increments needed.

```text
BRS
  ↓
business intake summary
  ↓
business capabilities
  ↓
global architecture rules
  ↓
software modules
  ↓
capability-to-module map
  ↓
delivery increments D1/D2/D3
  ↓
OpenSpec change for the active deliverable only
```

## Principle

The framework should be smaller in front of the Product Owner and more modular in front of AI coding agents.
