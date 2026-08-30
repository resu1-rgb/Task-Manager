# Task Manager

REST API for task management with JWT authentication.

## Stack

- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy** — ORM
- **Alembic** — migrations
- **AuthX** — JWT authentication
- **Docker** — containerization

## Run with Docker

```bash
git clone https://github.com/resu1-rgb/pet_project.git
cd pet_project
docker compose up --build
```

API available at `http://localhost:8000`

Documentation: `http://localhost:8000/docs`

## Run locally

**1. Create virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create `.env` file**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
JWT_SECRET_KEY=your_secret_key
```

**4. Apply migrations**
```bash
alembic upgrade head
```

**5. Start server**
```bash
uvicorn main:app --reload
```

## Endpoints

### Auth
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login, returns JWT token |

### Tasks
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/add_tasks` | Create a task |
| GET | `/read_tasks` | List all tasks |
| GET | `/read_tasks/{id}` | Task by ID |
| PATCH | `/tasks/{id}` | Update task text or deadline |
| PATCH | `/tasks/{id}/done` | Toggle task done/undone |
| DELETE | `/del_tasks/{id}` | Delete a task |
| GET | `/task_search?q=text` | Search tasks by text |
| GET | `/task_sort` | Tasks sorted by creation date |

## Tests

```bash
pytest test_main.py -v
```

15 tests covering: registration, login, create/read/update/delete tasks, search and sort.
