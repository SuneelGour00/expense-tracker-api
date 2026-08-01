"""Tests for the Smart Expense Tracker API.

Run with: pytest
"""

import pytest
from fastapi.testclient import TestClient

from src import storage
from src.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def isolate_data_file(tmp_path, monkeypatch):
    """Point storage at a temp file so tests never touch the real data/expenses.json."""
    temp_file = tmp_path / "expenses.json"
    temp_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(storage, "DATA_FILE", temp_file)
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    yield


def _create_expense(**overrides):
    payload = {
        "title": "Coffee",
        "amount": 4.5,
        "category": "Food",
        "date": "2026-07-01",
    }
    payload.update(overrides)
    return client.post("/expenses", json=payload)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_create_expense():
    response = _create_expense()
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Coffee"
    assert body["amount"] == 4.5


def test_create_expense_rejects_non_positive_amount():
    response = _create_expense(amount=-5)
    assert response.status_code == 422


def test_list_expenses():
    _create_expense()
    _create_expense(title="Bus ticket", amount=2.0, category="Travel")
    response = client.get("/expenses")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_filter_by_category_case_insensitive():
    _create_expense()
    _create_expense(title="Bus ticket", amount=2.0, category="Travel")
    response = client.get("/expenses", params={"category": "travel"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "Travel"


def test_total_overall_and_by_category():
    _create_expense(amount=4.5, category="Food")
    _create_expense(title="Lunch", amount=10.5, category="Food")
    _create_expense(title="Bus ticket", amount=2.0, category="Travel")

    overall = client.get("/expenses/total").json()
    assert overall["total"] == 17.0

    food_only = client.get("/expenses/total", params={"category": "Food"}).json()
    assert food_only["total"] == 15.0


def test_delete_expense():
    created = _create_expense().json()
    expense_id = created["id"]

    delete_response = client.delete(f"/expenses/{expense_id}")
    assert delete_response.status_code == 204

    list_response = client.get("/expenses")
    assert list_response.json() == []


def test_delete_nonexistent_expense_returns_404():
    response = client.delete("/expenses/9999")
    assert response.status_code == 404
