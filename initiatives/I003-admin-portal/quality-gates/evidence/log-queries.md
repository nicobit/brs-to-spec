# Log Analytics Sample Queries

## Job failures for a resource

```
AzureDiagnostics
| where ResourceId == "{resourceId}"
| where TimeGenerated > ago(24h)
| where Level == "Error" or Level == "Critical"
| where OperationName == "AdminPortalAction"
| sort by TimeGenerated desc
```

## Recent traces for correlation id

```
traces
| where customDimensions.correlation_id == "{correlationId}"
| order by timestamp desc
```

## Audit events for a tenant

```
AuditLogs
| where TenantId == '{tenantId}'
| where TimeGenerated > ago(30d)
| order by TimeGenerated desc
```
