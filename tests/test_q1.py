def test_seed_data_present(client):
    response = client.get("/employees")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Rahul Sharma", "department": "Engineering", "status": "Active"},
        {"id": 2, "name": "Priya Patel", "department": "HR", "status": "Active"},
        {"id": 3, "name": "Amit Verma", "department": "Engineering", "status": "Inactive"},
    ]


def test_list_all_employees(client):
    response = client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_employee_by_id(client):
    response = client.get("/employees/2")
    assert response.status_code == 200
    assert response.json()["name"] == "Priya Patel"


def test_get_missing_employee_returns_consistent_json_error(client):
    response = client.get("/employees/999")
    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/json")
    assert set(response.json()) == {"error", "detail"}
