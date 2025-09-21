#test_main.py
import pytest
from fastapi.testclient import TestClient
from main import api   # Import your FastAPI instance

client = TestClient(api)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Book Management System"}

def test_add_book():
    book_data = {
        "id": 1,
        "name": "Book One",
        "description": "First test book",
        "isAvailable": True
    }
    response = client.post("/book", json=book_data)
    assert response.status_code == 200
    assert any(book["id"] == 1 for book in response.json())

def test_get_books():
    response = client.get("/book")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  # since we added a book

def test_update_book():
    updated_data = {
        "id": 1,
        "name": "Updated Book One",
        "description": "Updated description",
        "isAvailable": False
    }
    response = client.put("/book/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Book One"

def test_delete_book():
    response = client.delete("/book/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_delete_nonexistent_book():
    response = client.delete("/book/999")
    assert response.status_code == 200
    assert response.json() == {"error": "Book not found, deletion failed"}