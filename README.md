# Limkokwing Library Management API

A production-style library management REST API built with FastAPI, SQLAlchemy, PostgreSQL, and JWT authentication.

## Features

- User registration and login with JWT
- Role-based access control for admin, librarian, and student
- CRUD operations for users, books, categories
- Borrowing and reservation workflows
- Dashboard summary endpoint
- Async database access with SQLAlchemy and Alembic migrations
- Pytest-based test suite and GitHub Actions CI

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy 2.0
- Alembic
- PostgreSQL
- JWT Authentication
- Passlib bcrypt
- Pytest

## Getting Started

### Setup

1. Clone the repo
2. Create and activate a Python virtual environment
3. Install dependencies

```bash
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Environment

Copy the example env file and customize values:

```bash
copy .env.example .env
```

Example values:

```env
APP_NAME=Limkokwing Library Management API
ENVIRONMENT=development
DEBUG=True
DATABASE_URL=postgresql+asyncpg://user:password@localhost/library_db
JWT_SECRET_KEY=CHANGE_ME
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
```

### Database

Run Alembic migrations:

```bash
alembic upgrade head
```

Seed initial data:

```bash
python -m app.database.run_seed
```

### Run the application

```bash
uvicorn app.main:app --reload
```

Swagger UI is available at `http://127.0.0.1:8000/docs`.
ReDoc is available at `http://127.0.0.1:8000/redoc`.

### Testing

```bash
python -m pytest -q
```

## Project Structure

- `app/api/v1/` - API routes
- `app/core/` - configuration and security utilities
- `app/database/` - session, base model, and seed data
- `app/models/` - SQLAlchemy ORM models
- `app/schemas/` - Pydantic request and response schemas
- `app/services/` - business logic services
- `app/dependencies/` - FastAPI dependencies
- `app/utils/` - shared utilities

## License

MIT License
