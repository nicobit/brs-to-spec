# Skill: Backlog Splitting

Use this skill when turning epics or large story groups into implementable user stories.

## Split by Persona

If different users receive different value or perform different actions, split the story.

Example:

- Client advisor submits onboarding request
- Compliance officer reviews onboarding request
- Operations user corrects onboarding data

## Split by Workflow Step

Split long processes into independently testable steps.

Example:

- Capture request
- Validate request
- Submit request
- Review request
- Approve request
- Notify user

## Split by Business Rule

If rules can be tested independently, split them.

Example:

- Validate mandatory fields
- Validate eligibility
- Validate limits
- Validate jurisdiction-specific constraints

## Split by System Boundary

If multiple systems are involved, split by integration boundary where possible.

Example:

- Prepare outbound payload
- Send payload to external system
- Receive response
- Handle rejection
- Reconcile status

## Split by UI and API Only When Useful

Do not automatically split frontend and backend if business value becomes unclear.

Good split:

- User can submit request through UI
- System validates and persists request through API

Weak split:

- Create frontend component
- Create backend endpoint

## Split by Risk

Separate risky, unknown, or dependency-heavy stories from simpler stories.

## Warning Signs a Story Is Too Large

- Many personas
- More than 8-10 acceptance criteria
- Multiple external systems
- Multiple business outcomes
- Multiple independent workflows
- Large UI and large backend in one story
- Hard to test in isolation
