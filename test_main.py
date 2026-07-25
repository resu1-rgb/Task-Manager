from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_tasks():
    login_response = client.post(
        "/login",
        json={"email": "vova@gmail.com", "password": "12345678", "username": "vova"},
    )
    token = login_response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/read_tasks_deadline", headers=headers)
    assert response.status_code == 200


def test_add_tasks():
    login_response = client.post(
        "/login",
        json={"email": "vova@gmail.com", "password": "12345678", "username": "vova"},
    )
    token = login_response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    test_add_task = client.post(
        "/add_tasks",
        json={"task": "Task_add", "deadline": "2024-06-30T12:00:00"},
        headers=headers,
    )
    assert test_add_task.status_code == 200

def test_del_tasks():
    login_response = client.post('/login', json={'username': 'vova', 'email': 'vova@gmail.com', 'password': '12345678'})
    token = login_response.json()['token']
    headers = {'Authorization': f'Bearer {token}'}
    test_add_task = client.post('add_tasks', json={"task": "Task_add", "deadline": "2024-06-30T12:00:00"}, headers=headers)
    assert test_add_task.status_code == 200
    
    test_read_task = client.get('/read_tasks_deadline', headers=headers)
    tasks = test_read_task.json()
    assert tasks

    task_id = tasks[-1]['id']
    test_del_task = client.delete(f'/del_tasks/{task_id}', headers=headers)
    assert test_del_task.status_code == 200

def test_wrong_password():
    wrong_response = client.post('/login', json={'username': 'vova', 'email': 'vova@gmail.com', 'password': '123456789'})
    assert wrong_response.status_code == 401