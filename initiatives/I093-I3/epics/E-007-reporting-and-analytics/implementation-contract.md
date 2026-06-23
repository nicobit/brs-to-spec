# Implementation Contract

## Data Entities

- Report (id, name, parameters)

```mermaid
erDiagram
		REPORT ||--o{ REPORTPARAM : has
		REPORT {
			string id
			string name
		}
		REPORTPARAM {
			string id
			string report_id
			string name
		}
```

## API Surface

### GET /reports/{id}
Returns generated report data.

```yaml
openapi: 3.0.0
info:
	title: Reporting API
	version: 1.0.0
paths:
	/reports/{id}:
		get:
			summary: Get report
			parameters:
				- in: path
					name: id
					required: true
			responses:
				'200':
					description: OK
```

## Events

- report.generated (ReportId, GeneratedAt)
