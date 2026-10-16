# Employee REST API

This is a small in-memory Employee REST API built with FastAPI. It implements all three assessment questions in one service.

## Assessment coverage

- **Question 1:** list employees, retrieve an employee by ID, and return consistent JSON errors for missing IDs.
- **Question 2:** create employees with validation, trimmed fields, unique IDs, and an `Active` default status; filter by department.
- **Question 3:** update an employee status to exactly `Active` or `Inactive`, with validation and persistence during the process lifetime.

## Features

- Seeded employees: Rahul Sharma (Engineering, Active), Priya Patel (HR, Active), and Amit Verma (Engineering, Inactive).
- List all employees or filter by department.
- Get one employee by ID with a JSON 404 error when missing.
- Create employees with trimmed, non-blank name and department values.
- Automatically assign a unique, never-reused ID and default new employees to Active.
- Update an employee's status to Active or Inactive.
- In-memory storage only; restarting the API restores the three seed employees.

## Endpoints

| Method | Path | Success |
|---|---|---|
| GET | `/employees` | 200, all employees |
| GET | `/employees?department=Engineering` | 200, matching employees or `[]` |
| GET | `/employees/{id}` | 200, one employee |
| POST | `/employees` | 201, created employee |
| PATCH | `/employees/{id}/status` | 200, updated employee |

POST body: `{"name": "Neha Singh", "department": "Finance"}`

PATCH body: `{"status": "Inactive"}`

## Setup and run

Use Python 3.11 or another version with compatible dependency wheels. The complete Windows PowerShell setup and demo procedure is in [RUN_PROJECT.md](RUN_PROJECT.md).

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`; interactive documentation is at `/docs`.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Postman

Import `postman\Employee_API.postman_collection.json` into Postman. Its `baseUrl` variable defaults to `http://127.0.0.1:8000`. Run the requests in collection order against a freshly started API.

## Design choices and limitations

- Status values are exact-case: only `Active` and `Inactive` are accepted.
- Department filtering is case-insensitive and does not modify stored data.
- Errors consistently use `{"error": "...", "detail": "..."}`.
- Data is process-local and resets on restart; authentication, database persistence, pagination, and concurrency controls are outside the assessment scope.
