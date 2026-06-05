import asyncio
from types import SimpleNamespace

from app.services.auth_service import AuthService
from app.core.security import decode_access_token


def test_hash_and_verify():
    pw = "secret"
    hashed = asyncio.run(AuthService.hash_password(pw))
    assert asyncio.run(AuthService.verify_password(pw, hashed)) is True


def test_create_and_decode_token():
    user = SimpleNamespace(id=1, email="user@example.com")
    token = asyncio.run(AuthService.create_token(user))
    payload = decode_access_token(token)
    assert payload is not None
    assert payload.get("sub") == "user@example.com"
