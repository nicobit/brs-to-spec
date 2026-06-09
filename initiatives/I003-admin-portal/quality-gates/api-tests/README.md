API contract test harness

Run tests:

```bash
cd initiatives/I003-admin-portal/quality-gates/api-tests
npm install
npm test
```

What it does:
- Starts a lightweight Express mock server in-process for tests.
- Validates short (200) and long-running (202 + job status) paths.
