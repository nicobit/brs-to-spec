# Data Specs — F-001.1 Inventory API

Table: `inventory_items`

- Columns: `tenant_id`, `subscription_id`, `resource_id`, `resource_type`, `display_name`, `last_updated`
- Indexing: partition by `tenant_id`, cluster by `subscription_id`

Retention: follow inventory TTL guidelines in readiness doc.
