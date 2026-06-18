# Test Strategy

## Metadata

| **Field** | **Value** |
|---|---|
| **Status** | **In progress** |
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by event | {{event_id}} |

## Test Levels

| Level | Required | Framework | Coverage Target | Trigger |
|---|---|---|---|---|
| Unit | Required / Recommended / N/A | | | |
| Integration | | | | |
| API/Contract | | | | |
| BDD/Acceptance | | | | |
| E2E | | | | |
| Performance | | | | |
| Security | | | | |

## Technology Stack

| Area | Language | Framework | Test Runner |
|---|---|---|---|
| Backend | | | |
| Frontend | | | |
| BDD | | | |

## Coverage Targets

| Level | Minimum % | Critical Path (100%) | Exclusions |
|---|---|---|---|
| Unit | | FR-NNN, BR-NNN | |
| Integration | | | |

## Test Data Strategy

| Concern | Approach |
|---|---|
| Test data seeding | Factory / Fixture / Migration |
| PII handling in tests | {{how PII is anonymized or excluded}} |
| Test environment | Dedicated / Shared / In-memory |

## Quality Gate to Test Mapping

| Gate | Test level | SCN-NNN / TC-NNN | CI pipeline stage |
|---|---|---|---|
| BDD Scenarios | Acceptance | SCN-NNN range | post-build |
| Security Review | Security scan + manual | | pre-merge |

## CI Pipeline Integration

| Stage | What runs | Pass criteria |
|---|---|---|
| pre-commit | Unit tests | All pass |
| post-build | Integration + BDD | All SCN-NNN pass |
| pre-merge | All levels | All pass |

## Accepted Risks

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|

---
*Status: In progress — set to Accepted by QA gate owner. Never self-accept.*
