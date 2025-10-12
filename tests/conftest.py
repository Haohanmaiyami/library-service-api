import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture(autouse=True)
def fast_password_hashers(settings):
    # ускоряем хэш паролей в тестах
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="user1", email="user1@example.com", password="Pass123456!"
    )


@pytest.fixture
def staff(db):
    return User.objects.create_user(
        username="librarian",
        email="lib@example.com",
        password="Pass123456!",
        is_staff=True,
    )


def login_and_get_headers(api: APIClient, username: str, password: str):
    resp = api.post(
        "/api/auth/jwt/create/",
        {"username": username, "password": password},
        format="json",
    )
    assert resp.status_code == 200, resp.content
    access = resp.json()["access"]
    return {"HTTP_AUTHORIZATION": f"Bearer {access}"}
