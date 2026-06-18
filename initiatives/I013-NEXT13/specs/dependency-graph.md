# Dependency Graph

- F-001.1 -> F-001.2 -> F-001.3
- F-001.1 -> F-002.1 -> F-002.2
- F-001.1 -> F-003.1 -> F-003.2
- F-002.2 -> F-004.1 -> F-004.2
# Dependency Graph

This document maps story dependencies for I013-NEXT13.

- F-001.1 -> none
- F-001.2 -> F-001.1
- F-001.3 -> F-001.1
- F-002.1 -> F-001.1
- F-002.2 -> F-002.1
- F-003.1 -> F-001.1
- F-003.2 -> F-003.1
- F-004.1 -> F-002.2
- F-004.2 -> F-004.1
- F-005.1 -> F-002.2
- F-005.2 -> F-005.1
- F-006.1 -> F-001.1

Notes:
- Payment/disbursement stories depend on payment provider contract (external).
