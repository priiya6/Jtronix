def test_patch_status_to_inactive_and_active_persists(client):
    inactive = client.patch("/employees/1/status", json={"status": "Inactive"})
    assert inactive.status_code == 200
    assert inactive.json()["status"] == "Inactive"
    assert client.get("/employees/1").json()["status"] == "Inactive"

    active = client.patch("/employees/1/status", json={"status": "Active"})
    assert active.status_code == 200
    assert client.get("/employees/1").json()["status"] == "Active"


def test_invalid_status_returns_error_and_does_not_change_data(client):
    before = client.get("/employees/1").json()
    response = client.patch("/employees/1/status", json={"status": "active"})
    assert 400 <= response.status_code < 500
    assert set(response.json()) == {"error", "detail"}
    assert client.get("/employees/1").json() == before


def test_patch_unknown_employee_returns_json_404(client):
    response = client.patch("/employees/999/status", json={"status": "Inactive"})
    assert response.status_code == 404
    assert set(response.json()) == {"error", "detail"}


def test_department_filter_is_case_insensitive_and_non_mutating(client):
    before = client.get("/employees").json()
    response = client.get("/employees", params={"department": "engineering"})
    assert response.status_code == 200
    assert [employee["id"] for employee in response.json()] == [1, 3]
    assert client.get("/employees").json() == before


def test_unknown_department_returns_empty_list(client):
    response = client.get("/employees", params={"department": "Legal"})
    assert response.status_code == 200
    assert response.json() == []


def test_q1_and_q2_still_work_after_q3_operations(client):
    client.patch("/employees/3/status", json={"status": "Active"})
    created = client.post("/employees", json={"name": "After Patch", "department": "HR"})
    assert created.status_code == 201
    assert client.get("/employees/3").status_code == 200
    assert any(employee["id"] == created.json()["id"] for employee in client.get("/employees").json())
