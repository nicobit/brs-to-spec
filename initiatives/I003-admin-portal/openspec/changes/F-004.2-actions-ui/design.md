# Design — F-004.2 Actions UI (frontend)

What this story touches:
- Action confirmation modal, dry-run preview, job status UI and polling

Integration points:
- Calls `POST /actions/{actionId}/run` and polls `GET /jobs/{jobId}`
