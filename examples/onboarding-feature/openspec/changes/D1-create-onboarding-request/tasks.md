# Tasks — D1 Create Onboarding Request

## Task 1 — Add request creation model

- Objective: Define the create request input model and validation rules.
- Files likely to change: request DTO/model files.
- Implementation notes: Keep mandatory field rules aligned with D1 scope.
- Validation sub-task: Add unit tests for valid and invalid input.
- Completion criteria: Validation tests pass.

## Task 2 — Add create request API endpoint

- Objective: Expose an endpoint to create onboarding requests.
- Files likely to change: API controller/route, service interface.
- Implementation notes: Call workflow module; do not implement approval logic in D1.
- Validation sub-task: Add API test for successful request creation.
- Completion criteria: API test passes and response contains request ID.
