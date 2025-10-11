import pytest
from django.utils import timezone
from conftest import login_and_get_headers

@pytest.mark.django_db
def test_staff_can_create_author(api, staff):
    headers = login_and_get_headers(api, "librarian", "Pass123456!")
    r = api.post("/api/authors/", {
        "first_name": "Лев", "last_name": "Толстой", "birth_year": 1828
    }, format="json", **headers)
    assert r.status_code == 201, r.content
    # листинг доступен всем
    r2 = api.get("/api/authors/")
    assert r2.status_code == 200
    assert r2.json()["count"] >= 1

@pytest.mark.django_db
def test_non_staff_cannot_create_author(api, user):
    headers = login_and_get_headers(api, "user1", "Pass123456!")
    r = api.post("/api/authors/", {"first_name": "A", "last_name": "B"}, format="json", **headers)
    assert r.status_code == 403

@pytest.mark.django_db
def test_book_validation_and_unique_book_id(api, staff):
    headers = login_and_get_headers(api, "librarian", "Pass123456!")
    # сначала создадим автора
    a = api.post("/api/authors/", {
        "first_name": "Leo", "last_name": "Tolstoy", "birth_year": 1828
    }, format="json", **headers).json()["id"]

    # валидный кейс
    r = api.post("/api/books/", {
        "title": "War and Peace", "author": a, "book_id": "WAR-PEACE-001",
        "published_year": 1869, "pages": 1225, "genre": "novel", "description": "Epic"
    }, format="json", **headers)
    assert r.status_code == 201, r.content

    # дубликат book_id
    r2 = api.post("/api/books/", {
        "title": "War and Peace 2", "author": a, "book_id": "WAR-PEACE-001",
        "published_year": 1869, "pages": 100, "genre": "novel"
    }, format="json", **headers)
    assert r2.status_code == 400
    assert "book_id" in r2.json()

    # страницы <= 0
    r3 = api.post("/api/books/", {
        "title": "Bad", "author": a, "book_id": "B-2",
        "published_year": 1869, "pages": 0
    }, format="json", **headers)
    assert r3.status_code == 400
    assert "pages" in r3.json()

    # год в будущем
    r4 = api.post("/api/books/", {
        "title": "Future", "author": a, "book_id": "B-3",
        "published_year": timezone.now().year + 5, "pages": 10
    }, format="json", **headers)
    assert r4.status_code == 400
    assert "published_year" in r4.json()


@pytest.mark.django_db
def test_search_and_ordering(api, staff):
    headers = login_and_get_headers(api, "librarian", "Pass123456!")
    a = api.post("/api/authors/", {"first_name":"Лев","last_name":"Толстой","birth_year":1828},
                 format="json", **headers).json()["id"]
    api.post("/api/books/", {"title":"BBB","author":a,"book_id":"S1","published_year":1900,"pages":10},
             format="json", **headers)
    api.post("/api/books/", {"title":"AAA","author":a,"book_id":"S2","published_year":1900,"pages":10},
             format="json", **headers)

    r1 = api.get("/api/authors/?search=Толстой")
    assert r1.status_code == 200 and r1.json()["count"] >= 1

    r2 = api.get("/api/books/?ordering=title")
    titles = [b["title"] for b in r2.json()["results"]]
    assert titles == sorted(titles)
