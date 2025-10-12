import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_register_success(api):
    payload = {
        "username": "ayan",
        "email": "ayan@example.com",
        "first_name": "Ayan",
        "last_name": "Kharitonov",
        "password": "StrongPass123!",
        "password2": "StrongPass123!",
    }
    r = api.post("/api/auth/register/", payload, format="json")
    assert r.status_code == 201, r.content
    assert User.objects.filter(username="ayan").exists()


@pytest.mark.django_db
def test_register_password_mismatch(api):
    r = api.post(
        "/api/auth/register/",
        {"username": "x", "password": "Pass123456!", "password2": "zzz"},
        format="json",
    )
    assert r.status_code == 400
    assert "password2" in r.json()


@pytest.mark.django_db
def test_jwt_login_and_me(api, user):
    # логин
    r = api.post(
        "/api/auth/jwt/create/",
        {"username": "user1", "password": "Pass123456!"},
        format="json",
    )
    assert r.status_code == 200
    access = r.json()["access"]

    # без токена 401
    r2 = api.get("/api/auth/me/")
    assert r2.status_code == 401

    # с токеном 200
    r3 = api.get("/api/auth/me/", HTTP_AUTHORIZATION=f"Bearer {access}")
    assert r3.status_code == 200
    assert r3.json()["username"] == "user1"


@pytest.mark.django_db
def test_register_duplicate_username(api, user):
    r = api.post(
        "/api/auth/register/",
        {"username": "user1", "password": "Pass123456!", "password2": "Pass123456!"},
        format="json",
    )
    assert r.status_code == 400


@pytest.mark.django_db
def test_protected_without_token(api):
    r = api.post("/api/books/", {}, format="json")
    assert r.status_code == 401
