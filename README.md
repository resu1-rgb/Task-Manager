# Task Manager

REST API для управления задачами с JWT авторизацией.

## Стек

- **FastAPI** — веб фреймворк
- **PostgreSQL** — база данных
- **SQLAlchemy** — ORM
- **Alembic** — миграции
- **AuthX** — JWT авторизация
- **Docker** — контейнеризация

## Запуск через Docker

```bash
git clone https://github.com/resu1-rgb/pet_project.git
cd pet_project
docker compose up --build
```

API будет доступен на `http://localhost:8000`

Документация: `http://localhost:8000/docs`

## Запуск локально

**1. Создай виртуальное окружение**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**2. Установи зависимости**
```bash
pip install -r requirements.txt
```

**3. Создай `.env` файл**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
JWT_SECRET_KEY=your_secret_key
```

**4. Примени миграции**
```bash
alembic upgrade head
```

**5. Запусти сервер**
```bash
uvicorn main:app --reload
```

## Эндпоинты

### Авторизация
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/register` | Регистрация |
| POST | `/login` | Логин, возвращает JWT токен |

### Задачи
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/add_tasks` | Создать задачу |
| GET | `/read_tasks` | Все задачи |
| GET | `/read_tasks/{id}` | Задача по ID |
| PATCH | `/tasks/{id}` | Редактировать задачу |
| PATCH | `/tasks/{id}/done` | Отметить выполненной/невыполненной |
| DELETE | `/del_tasks/{id}` | Удалить задачу |
| GET | `/task_search?q=текст` | Поиск по тексту |
| GET | `/task_sort` | Задачи отсортированные по дате |

## Тесты

```bash
pytest test_main.py -v
```

15 тестов покрывают: регистрацию, логин, создание/чтение/редактирование/удаление задач, поиск и сортировку.
