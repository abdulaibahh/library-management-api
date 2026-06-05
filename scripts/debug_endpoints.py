#!/usr/bin/env python3
"""Debug script to test endpoints individually and check responses."""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# First, register and login
print("1. Registering user...")
register_payload = {
    "first_name": "Debug",
    "last_name": "User",
    "email": "debug@example.com",
    "phone": "1234567890",
    "password": "TestPass123!"
}
r = requests.post(f"{BASE_URL}/api/v1/auth/register", json=register_payload)
print(f"Status: {r.status_code}")
print(f"Response: {r.text}\n")
user_data = r.json()
user_id = user_data.get("id")

print("2. Logging in...")
login_payload = {"email": "debug@example.com", "password": "TestPass123!"}
r = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_payload)
print(f"Status: {r.status_code}")
print(f"Response: {r.text}\n")
token = r.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

print("3. Testing /api/v1/users (no auth)...")
r = requests.get(f"{BASE_URL}/api/v1/users")
print(f"Status: {r.status_code}")
print(f"Headers: {r.headers}")
print(f"Content-Length: {r.headers.get('content-length')}")
print(f"Response: '{r.text}'\n")

print("4. Testing /api/v1/users (with auth)...")
r = requests.get(f"{BASE_URL}/api/v1/users", headers=headers)
print(f"Status: {r.status_code}")
print(f"Response: '{r.text}'\n")

print("5. Testing /api/v1/categories POST (with auth)...")
category_payload = {"name": "Test Category", "description": "Test"}
r = requests.post(f"{BASE_URL}/api/v1/categories", json=category_payload, headers=headers)
print(f"Status: {r.status_code}")
print(f"Response: '{r.text}'\n")

print("6. Testing /api/v1/books GET...")
r = requests.get(f"{BASE_URL}/api/v1/books", headers=headers)
print(f"Status: {r.status_code}")
print(f"Response: {r.json() if r.text else 'Empty'}\n")

print("7. Testing /api/v1/dashboard/stats...")
r = requests.get(f"{BASE_URL}/api/v1/dashboard/stats", headers=headers)
print(f"Status: {r.status_code}")
print(f"Response: {r.text}\n")
