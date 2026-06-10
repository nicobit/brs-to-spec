# Tasks — F-001.1 Inventory API (backend)

OS-F-001.1-001: Implement `GET /inventory` endpoint
- Requirement: FR-001
- AC: AC-004
- AR: Authentication rule (Azure AD)
- Evidence: integration test hitting sample subscription IDs returning paginated results

OS-F-001.1-002: Add inventory data model & ingestion job
- Requirement: FR-001
- Evidence: ingestion job populates `inventory_items` for sample subscription IDs

OS-F-001.1-003: Add API integration tests
- Validate pagination, filters by `tenantId` and `stage`, auth enforcement

Done criteria:
- AC-004 verified by integration tests
- BDD scenarios: SCN-001, SCN-002, SCN-003, SCN-004 pass in CI
