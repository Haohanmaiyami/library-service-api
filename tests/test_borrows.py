import pytest
from django.utils import timezone
from conftest import login_and_get_headers

def _mk_author(api, headers):
    return api.post("/api/authors/", {
        "first_name": "Лев", "last_name": "Толстой", "birth_year": 1828
    }, format="json", **headers).json()["id"]

def _mk_book(api, headers, author_id, book_id="BK-1"):
    return api.post("/api/books/", {
        "title": "Книга №1", "author": author_id, "book_id": book_id,
        "published_year": 1869, "pages": 100
    }, format="json", **headers).json()["id"]

@pytest.mark.django_db
def test_non_staff_cannot_borrow(api, user):
    headers_user = login_and_get_headers(api, "user1", "Pass123456!")
    r = api.post("/api/borrows/", {
        "book": 1, "due_at": "2099-12-31T23:59:00Z"
    }, format="json", **headers_user)
    assert r.status_code == 403

@pytest.mark.django_db
def test_staff_borrow_return_and_no_double_borrow(api, staff):
    headers = login_and_get_headers(api, "librarian", "Pass123456!")
    author_id = _mk_author(api, headers)
    book_id = _mk_book(api, headers, author_id, book_id="UNIQUE-42")

    # borrow (оформим на себя — user не передаём)
    r1 = api.post("/api/borrows/", {
        "book": book_id, "due_at": "2099-12-31T23:59:00Z"
    }, format="json", **headers)
    assert r1.status_code == 201, r1.content
    borrow_id = r1.json()["id"]

    # повторная выдача той же книги до возврата запрещена
    r2 = api.post("/api/borrows/", {
        "book": book_id, "due_at": "2099-12-31T23:59:00Z"
    }, format="json", **headers)
    assert r2.status_code == 400
    assert "book" in r2.json()

    # возврат
    r3 = api.post(f"/api/borrows/{borrow_id}/return_book/", format="json", **headers)
    assert r3.status_code == 200
    assert r3.json()["returned_at"] is not None

    # второй возврат запрещён
    r4 = api.post(f"/api/borrows/{borrow_id}/return_book/", format="json", **headers)
    assert r4.status_code == 400

    # теперь книгу можно снова выдать
    r5 = api.post("/api/borrows/", {
        "book": book_id, "due_at": "2099-12-31T23:59:00Z"
    }, format="json", **headers)
    assert r5.status_code == 201

@pytest.mark.django_db
def test_borrow_visibility(api, staff, user):
    h_staff = login_and_get_headers(api, "librarian", "Pass123456!")
    h_user = login_and_get_headers(api, "user1", "Pass123456!")
    a = api.post("/api/authors/", {"first_name":"A","last_name":"B"}, format="json", **h_staff).json()["id"]
    b = api.post("/api/books/", {"title":"T","author":a,"book_id":"X1","published_year":1900,"pages":10},
                 format="json", **h_staff).json()["id"]
    # staff выдаёт на себя (user не передаём)
    borrow_id = api.post("/api/borrows/", {"book": b, "due_at": "2099-01-01T00:00:00Z"},
                         format="json", **h_staff).json()["id"]

    # обычный юзер не видит чужую выдачу
    r = api.get("/api/borrows/", **h_user)
    assert r.status_code == 200 and all(x["id"] != borrow_id for x in r.json()["results"])

    # повторный возврат запрещён
    assert api.post(f"/api/borrows/{borrow_id}/return_book/", **h_staff).status_code == 200
    assert api.post(f"/api/borrows/{borrow_id}/return_book/", **h_staff).status_code == 400
