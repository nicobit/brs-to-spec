# API Specs — F-001.1 Inventory API

## GET /inventory

- Query params: `tenantId` (required), `stage` (optional), `page` (optional), `pageSize` (optional)
- Response: 200 OK

```json
{
  "items": [ { "resourceId": "...", "resourceType": "...", "lastUpdated": "..." } ],
  "page": 1,
  "pageSize": 50,
  "total": 1234
}
```

Security: Bearer token (Azure AD). Validate group membership per tenant.
