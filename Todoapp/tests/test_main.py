from fastapi.testclient import TestClient
from todoapp.main import app

def test_read_all_todos():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_create_todo():
    client = TestClient(app)
    todo = {"title": "My first todo", "completed": False}
    response = client.post("/create-todo", json=todo)
    assert response.status_code == 201
    assert response.json()["title"] == "My first todo"
    assert response.json()["completed"] == False

def test_get_todo():
    client = TestClient(app)
    response = client.get("/get-todo/1")
    assert response.status_code == 200
    assert response.json()["title"] == "My first todo"

def test_update_todo():
    client = TestClient(app)
    todo = {"id": 1, "title": "Updated title", "completed": True}
    response = client.put("/update-todo/1", json=todo)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["completed"] == True

def test_delete_todo():
    client = TestClient(app)
    response = client.delete("/delete-todo/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Todo deleted"
