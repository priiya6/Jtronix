def test_create_employee_returns_201_trimmed_and_active(client):
    response = client.post("/employees", json={"name": "  Neha Singh ", "department": " Finance "})
    assert response.status_code == 201
    assert response.json() == {
        "id": 4,
        "name": "Neha Singh",
        "department": "Finance",
        "status": "Active",
    }
    assert client.get("/employees/4").json()["name"] == "Neha Singh"


def test_second_create_gets_different_id(client):
    first = client.post("/employees", json={"name": "One", "department": "Engineering"})
    second = client.post("/employees", json={"name": "Two", "department": "Engineering"})
    assert first.status_code == 201
    assert second.status_code == 201
    assert second.json()["id"] != first.json()["id"]


def test_blank_or_missing_create_fields_are_rejected_without_mutation(client):
    before = client.get("/employees").json()
    invalid_payloads = [
        {"name": "", "department": "Engineering"},
        {"name": "   ", "department": "Engineering"},
        {"name": "Valid", "department": ""},
        {"name": "Valid", "department": "   "},
        {"name": "Valid"},
        {"department": "Engineering"},
        {},
    ]
    for payload in invalid_payloads:
        response = client.post("/employees", json=payload)
        assert 400 <= response.status_code < 500
        assert set(response.json()) == {"error", "detail"}
    assert client.get("/employees").json() == before
