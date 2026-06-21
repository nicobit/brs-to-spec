# Implementation Contract — E-005 Platform, Non-functional & Reporting

## Non-Functional Constraints

| Constraint | Target | Source |
|---|---|---|
| P95 response time < 500ms for core read APIs | API Gateway / Backend | REQ-014 |
| Data residency: UK-only for personal data | Storage / Backups | REQ-015 |
| Encryption: at-rest + in-transit, keys in Key Vault | Storage / Secrets | REQ-015 |

## Monitoring & Reporting

- Admin metrics: API latencies, queue depths, reconciliation failures, screening latencies
- Dashboards and alerts for thresholds defined in NFRs

## Open Questions

- Which tenancy model (single-tenant vs multi-tenant) determines encryption key scoping?

## API Surface

### GET /api/v1/platform/metrics

```yaml
openapi: 3.0.3
info:
	title: Platform API
	version: 1.0.0
paths:
	/api/v1/platform/metrics:
		get:
			summary: Retrieve platform metrics
			parameters:
				- in: query
					name: metric
					schema:
						type: string
			responses:
				'200':
					description: Metrics payload
```

## Events

- `platform.metric_emitted` — payload: { name, value, tags, timestamp }

## Business Rules

| Rule | Condition | Effect | Source |
|---|---|---|---|
| BR-100 | If API latency > threshold | Emit `platform.metric_emitted` with alert flag | FR-014 |
