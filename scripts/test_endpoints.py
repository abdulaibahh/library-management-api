#!/usr/bin/env python3
""" 
Comprehensive endpoint testing script for Library Management API.
Tests all routes and displays results in a clear format.

Notes:
- This script is designed to work even when some operations are forbidden due to RBAC.
- It avoids crashing if earlier steps (e.g., category/book creation) fail.
"""

import requests
from typing import Any
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

results: list[dict[str, Any]] = []


def test_endpoint(method: str, endpoint: str, description: str, **kwargs) -> dict[str, Any]:
    """Test an endpoint and return result."""
    url = f"{BASE_URL}{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, **kwargs)
        elif method == "POST":
            response = requests.post(url, **kwargs)
        elif method == "PUT":
            response = requests.put(url, **kwargs)
        elif method == "DELETE":
            response = requests.delete(url, **kwargs)
        else:
            raise ValueError(f"Unsupported method: {method}")

        status = "✓ PASS" if 200 <= response.status_code < 300 else "✗ FAIL"
        payload = response.json() if response.text else None

        result = {
            "method": method,
            "endpoint": endpoint,
            "description": description,
            "status_code": response.status_code,
            "status": status,
            "response": payload,
        }
        print(f"{status} | {method:6} | {endpoint:45} | {description:40} | [{response.status_code}]")
        return result

    except Exception as e:
        print(f"✗ ERROR | {method:6} | {endpoint:45} | {description:40} | {str(e)}")
        return {
            "method": method,
            "endpoint": endpoint,
            "description": description,
            "error": str(e),
            "status": "✗ ERROR",
        }


print("=" * 150)
print("Library Management API - Comprehensive Endpoint Test")
print("=" * 150)

# 1. Health Check
print("\n[HEALTH CHECK]")
r1 = test_endpoint("GET", "/health", "Health check endpoint")
results.append(r1)

# 2. Authentication Endpoints
print("\n[AUTHENTICATION]")
health_env = r1.get("response", {}).get("status", "ok") if isinstance(r1.get("response"), dict) else "ok"
unique = abs(hash(str(health_env) + str(datetime.utcnow().timestamp()))) % 1_000_000
email = f"testuser_{unique}@example.com"

register_payload = {
    "first_name": "Test",
    "last_name": "User",
    "email": email,
    "phone": "1234567890",
    "password": "TestPass123!",
}

r2 = test_endpoint("POST", "/api/v1/auth/register", "Register new user", json=register_payload)
results.append(r2)

token = None
user_id = None
if isinstance(r2.get("response"), dict):
    user_id = r2["response"].get("id")
    email = r2["response"].get("email", email)

if email:
    login_payload = {"email": email, "password": "TestPass123!"}
    r_login = test_endpoint("POST", "/api/v1/auth/login", "Login user", json=login_payload)
    results.append(r_login)
    if isinstance(r_login.get("response"), dict):
        token = r_login["response"].get("access_token")

headers = {"Authorization": f"Bearer {token}"} if token else {}

# 3. Users Endpoints
print("\n[USERS]")
test_endpoint("GET", "/api/v1/users", "Get all users", headers=headers)
if user_id:
    test_endpoint("GET", f"/api/v1/users/{user_id}", "Get user by ID", headers=headers)
    test_endpoint("PUT", f"/api/v1/users/{user_id}", "Update user", json={"first_name": "Updated"}, headers=headers)

# 4. Categories Endpoints
print("\n[CATEGORIES]")
category_payload = {"name": "Fiction", "description": "Fiction books"}

r_cat = test_endpoint("POST", "/api/v1/categories", "Create category", json=category_payload, headers=headers)
results.append(r_cat)

category_id = None
if isinstance(r_cat.get("response"), dict):
    category_id = r_cat["response"].get("id")

test_endpoint("GET", "/api/v1/categories", "Get all categories", headers=headers)
if category_id:
    test_endpoint("GET", f"/api/v1/categories/{category_id}", "Get category by ID", headers=headers)
    test_endpoint("PUT", f"/api/v1/categories/{category_id}", "Update category", json={"name": "Updated Fiction"}, headers=headers)

# 5. Books Endpoints
print("\n[BOOKS]")
book_id = None

# Books create requires admin/librarian per API code; script handles forbidden responses.
if category_id:
    book_payload = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "978-0-123456-78-9",
        "publisher": "Test Publisher",
        "publication_year": 2024,
        "description": "A test book",
        "quantity": 5,
        "available_quantity": 5,
        "category_id": category_id,
    }
    r_book = test_endpoint("POST", "/api/v1/books", "Create book", json=book_payload, headers=headers)
    results.append(r_book)

    if isinstance(r_book.get("response"), dict):
        book_id = r_book["response"].get("id")

# Read-only operations

test_endpoint("GET", "/api/v1/books", "Get all books", headers=headers)
if book_id:
    test_endpoint("GET", f"/api/v1/books/{book_id}", "Get book by ID", headers=headers)
    test_endpoint("PUT", f"/api/v1/books/{book_id}", "Update book", json={"title": "Updated Book"}, headers=headers)

# 6. Borrowings Endpoints
print("\n[BORROWINGS]")
borrow_id = None
if user_id and book_id:
    due_date = (datetime.utcnow() + timedelta(days=14)).isoformat()
    borrow_payload = {"book_id": book_id, "due_date": due_date}
    r_borrow = test_endpoint("POST", "/api/v1/borrowings", "Create borrowing", json=borrow_payload, headers=headers)
    results.append(r_borrow)

    if isinstance(r_borrow.get("response"), dict):
        borrow_id = r_borrow["response"].get("id")

# Reads

test_endpoint("GET", "/api/v1/borrowings", "Get all borrowings", headers=headers)
if borrow_id:
    test_endpoint("GET", f"/api/v1/borrowings/{borrow_id}", "Get borrowing by ID", headers=headers)

# 7. Reservations Endpoints
print("\n[RESERVATIONS]")
reserve_id = None
if user_id and book_id:
    reserve_payload = {"book_id": book_id}
    r_reserve = test_endpoint("POST", "/api/v1/reservations", "Create reservation", json=reserve_payload, headers=headers)
    results.append(r_reserve)

    if isinstance(r_reserve.get("response"), dict):
        reserve_id = r_reserve["response"].get("id")

# Reads

test_endpoint("GET", "/api/v1/reservations", "Get all reservations", headers=headers)
if reserve_id:
    test_endpoint("GET", f"/api/v1/reservations/{reserve_id}", "Get reservation by ID", headers=headers)

# 8. Dashboard Endpoints
print("\n[DASHBOARD]")
# App defines /summary (admin/librarian only)
# (The old script used /stats and /overdue, which do not exist.)
test_endpoint("GET", "/api/v1/dashboard/summary", "Get dashboard summary", headers=headers)

print("\n" + "=" * 150)
print("Test Summary")
print("=" * 150)

passed = sum(1 for r in results if "PASS" in r.get("status", ""))
failed = sum(1 for r in results if "FAIL" in r.get("status", "") or "ERROR" in r.get("status", ""))

print(f"Total tests: {len(results)} | Passed: {passed} | Failed: {failed}")
print("=" * 150)

