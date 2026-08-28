import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def registered_user():
    client.post("/register", json={
        "email": "test@gmail.com",
        "password": "testpass1",
        "username": "testuser"
    })
    return {"email": "test@gmail.com", "password": "testpass1"}


@pytest.fixture
def auth_token(registered_user):
    response = client.post("/login", json=registered_user)
    return response.json()["token"]


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


# --- регистрация ---

def test_register():
    response = client.post("/register", json={
        "email": "new@gmail.com",
        "password": "testpass1",
        "username": "newuser"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}


def test_register_existing_user(registered_user):
    response = client.post("/register", json={
        "email": "test@gmail.com",
        "password": "testpass1",
        "username": "testuser"
    })
    assert response.status_code == 409


# --- логин ---

def test_login(registered_user):
    response = client.post("/login", json=registered_user)
    assert response.status_code == 200
    assert "token" in response.json()


def test_wrong_password(registered_user):
    response = client.post("/login", json={
        "email": "test@gmail.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401


# --- задачи ---

def test_add_task(auth_headers):
    response = client.post("/add_tasks",
        json={"task": "купить молоко", "deadline": "2025-06-30T12:00:00"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Task added"}


def test_add_task_without_token():
    response = client.post("/add_tasks", json={"task": "test", "deadline": None})
    assert response.status_code == 401


def test_read_tasks(auth_headers):
    client.post("/add_tasks", json={"task": "задача 1", "deadline": None}, headers=auth_headers)
    client.post("/add_tasks", json={"task": "задача 2", "deadline": None}, headers=auth_headers)
    response = client.get("/read_tasks", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_read_task_by_id(auth_headers):
    client.post("/add_tasks", json={"task": "задача", "deadline": None}, headers=auth_headers)
    response = client.get("/read_tasks/1", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["task"] == "задача"


def test_read_task_by_id_not_found(auth_headers):
    response = client.get("/read_tasks/999", headers=auth_headers)
    assert response.status_code == 404


def test_mark_task_done(auth_headers):
    client.post("/add_tasks", json={"task": "задача", "deadline": None}, headers=auth_headers)
    response = client.patch("/tasks/1/done", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["is_done"] == True


def test_update_task(auth_headers):
    client.post("/add_tasks", json={"task": "старое название", "deadline": None}, headers=auth_headers)
    response = client.patch("/tasks/1", json={"task": "новое название"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["task"] == "новое название"


def test_delete_task(auth_headers):
    client.post("/add_tasks", json={"task": "задача", "deadline": None}, headers=auth_headers)
    response = client.delete("/del_tasks/1", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted"}


def test_delete_task_not_found(auth_headers):
    response = client.delete("/del_tasks/999", headers=auth_headers)
    assert response.status_code == 404


def test_task_search(auth_headers):
    client.post("/add_tasks", json={"task": "купить молоко", "deadline": None}, headers=auth_headers)
    client.post("/add_tasks", json={"task": "сделать уроки", "deadline": None}, headers=auth_headers)
    response = client.get("/task_search?q=молоко", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_task_sort(auth_headers):
    client.post("/add_tasks", json={"task": "задача 1", "deadline": None}, headers=auth_headers)
    client.post("/add_tasks", json={"task": "задача 2", "deadline": None}, headers=auth_headers)
    response = client.get("/task_sort", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2
