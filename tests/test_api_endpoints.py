import asyncio
from collections.abc import AsyncGenerator, Generator
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.roles import UserRole
from app.core.security import hash_password
from app.database.base import Base
from app.dependencies.database import get_db
from app.main import app
from app.models.book import Book
from app.models.borrowing import Borrowing
from app.models.category import Category
from app.models.reservation import Reservation
from app.models.role import Role
from app.models.user import User


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def setup_database() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with testing_session() as session:
            admin_role = Role(name=UserRole.admin.value)
            librarian_role = Role(name=UserRole.librarian.value)
            student_role = Role(name=UserRole.student.value)
            session.add_all([admin_role, librarian_role, student_role])
            await session.flush()
            session.add_all(
                [
                    User(
                        first_name="Admin",
                        last_name="User",
                        email="admin@example.com",
                        phone="1000000000",
                        password_hash=hash_password("AdminPass123!"),
                        role=admin_role,
                    ),
                    User(
                        first_name="Student",
                        last_name="User",
                        email="student@example.com",
                        phone="2000000000",
                        password_hash=hash_password("StudentPass123!"),
                        role=student_role,
                    ),
                ]
            )
            await session.commit()

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with testing_session() as session:
            yield session

    asyncio.run(setup_database())
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    asyncio.run(engine.dispose())


def auth_headers(client: TestClient, email: str, password: str) -> dict[str, str]:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_all_endpoints_success_paths(client: TestClient) -> None:
    assert client.get("/").status_code == 200
    assert client.get("/health").status_code == 200

    admin_headers = auth_headers(client, "admin@example.com", "AdminPass123!")
    student_headers = auth_headers(client, "student@example.com", "StudentPass123!")

    unauthorized_response = client.get("/api/v1/users/me")
    assert unauthorized_response.status_code == 401

    registered_response = client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Registered",
            "last_name": "Student",
            "email": "registered@example.com",
            "phone": "3000000000",
            "password": "RegisteredPass123!",
        },
    )
    assert registered_response.status_code == 201
    registered_user = registered_response.json()

    duplicate_register_response = client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Registered",
            "last_name": "Student",
            "email": "registered@example.com",
            "phone": "3000000000",
            "password": "RegisteredPass123!",
        },
    )
    assert duplicate_register_response.status_code == 400

    assert client.get("/api/v1/users/me", headers=student_headers).status_code == 200
    assert client.get("/api/v1/users/", headers=student_headers).status_code == 403

    users_response = client.get("/api/v1/users/", headers=admin_headers)
    assert users_response.status_code == 200
    assert len(users_response.json()) >= 3

    user_response = client.get(f"/api/v1/users/{registered_user['id']}", headers=admin_headers)
    assert user_response.status_code == 200

    update_user_response = client.put(
        f"/api/v1/users/{registered_user['id']}",
        headers=admin_headers,
        json={
            "first_name": "Updated",
            "last_name": "Student",
            "email": "registered.updated@example.com",
            "phone": "4000000000",
            "is_active": True,
            "password": "UpdatedPass123!",
            "role_id": registered_user["role_id"],
        },
    )
    assert update_user_response.status_code == 200
    assert update_user_response.json()["email"] == "registered.updated@example.com"

    login_updated_user_response = client.post(
        "/api/v1/auth/login",
        json={"email": "registered.updated@example.com", "password": "UpdatedPass123!"},
    )
    assert login_updated_user_response.status_code == 200

    delete_user_response = client.delete(f"/api/v1/users/{registered_user['id']}", headers=admin_headers)
    assert delete_user_response.status_code == 204

    category_response = client.post(
        "/api/v1/categories/",
        headers=admin_headers,
        json={"name": "Fiction", "description": "Fiction books"},
    )
    assert category_response.status_code == 200
    category = category_response.json()

    assert client.get("/api/v1/categories/").status_code == 200
    assert client.get(f"/api/v1/categories/{category['id']}").status_code == 200

    update_category_response = client.put(
        f"/api/v1/categories/{category['id']}",
        headers=admin_headers,
        json={"name": "Modern Fiction", "description": "Updated fiction books"},
    )
    assert update_category_response.status_code == 200
    category = update_category_response.json()

    delete_category_response = client.post(
        "/api/v1/categories/",
        headers=admin_headers,
        json={"name": "Delete Me", "description": None},
    )
    assert delete_category_response.status_code == 200
    delete_category = delete_category_response.json()
    assert client.delete(f"/api/v1/categories/{delete_category['id']}", headers=admin_headers).status_code == 204

    book_response = client.post(
        "/api/v1/books/",
        headers=admin_headers,
        json={
            "title": "API Testing",
            "author": "Test Author",
            "isbn": "978-0-000000-00-1",
            "publisher": "Test Publisher",
            "publication_year": 2026,
            "description": "A book used for endpoint tests",
            "quantity": 3,
            "available_quantity": 3,
            "category_id": category["id"],
        },
    )
    assert book_response.status_code == 200
    book = book_response.json()

    assert client.get("/api/v1/books/").status_code == 200
    assert client.get(f"/api/v1/books/{book['id']}").status_code == 200

    update_book_response = client.put(
        f"/api/v1/books/{book['id']}",
        headers=admin_headers,
        json={
            "title": "API Testing Updated",
            "author": "Test Author",
            "isbn": "978-0-000000-00-1",
            "publisher": "Test Publisher",
            "publication_year": 2026,
            "description": "Updated test book",
            "quantity": 3,
            "available_quantity": 3,
            "category_id": category["id"],
        },
    )
    assert update_book_response.status_code == 200

    disposable_book_response = client.post(
        "/api/v1/books/",
        headers=admin_headers,
        json={
            "title": "Disposable",
            "author": "Test Author",
            "isbn": "978-0-000000-00-2",
            "publisher": None,
            "publication_year": 2026,
            "description": None,
            "quantity": 1,
            "available_quantity": 1,
            "category_id": category["id"],
        },
    )
    assert disposable_book_response.status_code == 200
    disposable_book = disposable_book_response.json()
    assert client.delete(f"/api/v1/books/{disposable_book['id']}", headers=admin_headers).status_code == 204

    due_date = (datetime.now(UTC).replace(tzinfo=None) + timedelta(days=14)).isoformat()
    borrowing_response = client.post(
        "/api/v1/borrowings/",
        headers=student_headers,
        json={"book_id": book["id"], "due_date": due_date},
    )
    assert borrowing_response.status_code == 201
    borrowing = borrowing_response.json()

    assert client.get("/api/v1/borrowings/", headers=admin_headers).status_code == 200
    assert client.get("/api/v1/borrowings/me", headers=student_headers).status_code == 200
    assert client.get(f"/api/v1/borrowings/{borrowing['id']}", headers=student_headers).status_code == 200

    return_response = client.post(f"/api/v1/borrowings/{borrowing['id']}/return", headers=student_headers)
    assert return_response.status_code == 200
    assert return_response.json()["status"] == "returned"

    reservation_response = client.post(
        "/api/v1/reservations/",
        headers=student_headers,
        json={"book_id": book["id"]},
    )
    assert reservation_response.status_code == 201
    reservation = reservation_response.json()

    assert client.get("/api/v1/reservations/", headers=admin_headers).status_code == 200
    assert client.get("/api/v1/reservations/me", headers=student_headers).status_code == 200
    assert client.get(f"/api/v1/reservations/{reservation['id']}", headers=student_headers).status_code == 200

    cancel_response = client.post(f"/api/v1/reservations/{reservation['id']}/cancel", headers=student_headers)
    assert cancel_response.status_code == 200
    assert cancel_response.json()["status"] == "cancelled"

    dashboard_response = client.get("/api/v1/dashboard/summary", headers=admin_headers)
    assert dashboard_response.status_code == 200
    assert dashboard_response.json()["total_users"] >= 2
