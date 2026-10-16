from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Employee(BaseModel):
    id: int
    name: str
    department: str
    status: str


class EmployeeCreate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None


class StatusUpdate(BaseModel):
    status: Optional[str] = None


SEED_EMPLOYEES = [
    Employee(id=1, name="Rahul Sharma", department="Engineering", status="Active"),
    Employee(id=2, name="Priya Patel", department="HR", status="Active"),
    Employee(id=3, name="Amit Verma", department="Engineering", status="Inactive"),
]

_employees: list[Employee] = []
_next_id = 1


def reset_store() -> None:
    """Restore seed data; used by tests and when the module starts."""
    global _employees, _next_id
    _employees = [employee.model_copy() for employee in SEED_EMPLOYEES]
    _next_id = max(employee.id for employee in _employees) + 1


def _find_employee(employee_id: int) -> Employee:
    for employee in _employees:
        if employee.id == employee_id:
            return employee
    raise HTTPException(status_code=404, detail="Employee not found")


def _error(error: str, detail: str, status_code: int) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"error": error, "detail": detail})


app = FastAPI(title="Employee API", version="1.0.0")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    detail = str(exc.detail)
    return _error("Request failed", detail, exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return _error("Invalid request", "Request body or parameters are invalid", 400)


@app.get("/employees", response_model=list[Employee])
def list_employees(department: Optional[str] = Query(default=None)) -> list[Employee]:
    if department is None:
        return [employee.model_copy() for employee in _employees]
    requested_department = department.strip().casefold()
    return [
        employee.model_copy()
        for employee in _employees
        if employee.department.casefold() == requested_department
    ]


@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: int) -> Employee:
    return _find_employee(employee_id).model_copy()


@app.post("/employees", response_model=Employee, status_code=201)
def create_employee(payload: EmployeeCreate) -> Employee:
    if not isinstance(payload.name, str) or not payload.name.strip():
        return _error("Invalid employee", "name is required and cannot be blank", 400)  # type: ignore[return-value]
    if not isinstance(payload.department, str) or not payload.department.strip():
        return _error("Invalid employee", "department is required and cannot be blank", 400)  # type: ignore[return-value]

    global _next_id
    employee = Employee(
        id=_next_id,
        name=payload.name.strip(),
        department=payload.department.strip(),
        status="Active",
    )
    _employees.append(employee)
    _next_id += 1
    return employee.model_copy()


@app.patch("/employees/{employee_id}/status", response_model=Employee)
def update_status(employee_id: int, payload: StatusUpdate) -> Employee:
    employee = _find_employee(employee_id)
    if payload.status not in {"Active", "Inactive"}:
        return _error("Invalid status", "status must be exactly Active or Inactive", 400)  # type: ignore[return-value]
    employee.status = payload.status
    return employee.model_copy()


reset_store()
