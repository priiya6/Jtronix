# Assessment Status

The Employee REST API implementation is complete and covers all three assessment questions:

- Employee listing, lookup, department filtering, and consistent JSON errors.
- Validated employee creation with trimmed fields, unique IDs, and an `Active` default.
- Employee status updates restricted to `Active` and `Inactive`.

## Verification

- Full pytest suite: **13 passed**.
- Postman collection: valid JSON at `postman/Employee_API.postman_collection.json`.
- Runtime data is intentionally in-memory and resets when the API restarts.

See `README.md` and `RUN_PROJECT.md` for setup, test, API, and Postman instructions.
