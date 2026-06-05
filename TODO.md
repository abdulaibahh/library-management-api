# TODO

- [ ] Add root endpoint handler for GET `/` to avoid 404.
- [ ] Keep existing API routes unchanged.
- [ ] Re-run server and verify:
  - GET `/` returns 200 (or redirect).
  - GET `/health` still returns 200.
  - `/api/v1/*` endpoints still work with RBAC.
