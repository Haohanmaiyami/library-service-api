# 📚 Library — API DRF дипломная работа (DF1)

**Задача:** REST API для управления библиотекой: книги, авторы, пользователи и выдачи.  
**Стек:** Django 5, DRF, SimpleJWT, PostgreSQL, drf-spectacular, Docker Compose.
---

## Запуск через Docker

1) Сгенерировать `requirements.txt` из Poetry:
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```
Собрать и запустить:
```bash
docker compose up --build
```

Доступы:

Приложение: http://localhost:8000

Swagger UI: http://localhost:8000/api/docs/

Redoc: http://localhost:8000/api/redoc/

OpenAPI JSON: http://localhost:8000/api/schema/

## Локальный запуск (без Docker)

```
poetry install
poetry run python manage.py migrate
poetry run python manage.py createsuperuser   # по желанию
poetry run python manage.py runserver
```

## Аутентификация (JWT)

Эндпоинты:

POST /api/auth/jwt/create/ — получить access/refresh

POST /api/auth/jwt/refresh/ — обновить access


# Эндпоинты
## Авторы

- GET /api/authors/?search=tolstoy&ordering=last_name

- POST /api/authors/ (только staff)

- GET /api/authors/{id}/

- PUT/PATCH/DELETE /api/authors/{id}/ (только staff)

## Книги

- GET /api/books/?title=&author=&genre=&book_id= (поиск/фильтры)

- POST /api/books/ (только staff)

- GET /api/books/{id}/

- PUT/PATCH/DELETE /api/books/{id}/ (только staff)

```
Поля книги: title, author, book_id (уникальный), published_year, pages, genre, description.
```

## Выдачи (Borrow)

- GET /api/borrows/ — staff видит всё; пользователь — только свои

- POST /api/borrows/?target_user=<id> — выдать книгу пользователю <id> (только staff)

- POST /api/borrows/{id}/return_book/ — закрыть выдачу (только staff)

## Права доступа (Permissions)

- IsAdminOrReadOnly — для авторов и книг (мутации — только staff, чтение — всем).

- IsStaffForMutationOrOwnerRead — для выдач (управляет staff; пользователь читает только свои записи).

## Валидация (Serializers)

- book_id — непустой и уникальный.

- published_year — разумные границы.

- pages > 0.

- due_at — только будущее время.

- запрет второй активной выдачи одной и той же книги.

## OpenAPI (Swagger/Redoc)

- Схема: /api/schema/

- Swagger UI: /api/docs/

- Redoc: /api/redoc/

## PEP8

- Поддерживается с помощью flake8 (проверка) и black (форматирование).

## База данных

PostgreSQL поднимается через docker-compose (сервис db).
Переменные окружения в docker-compose.yml:

```
POSTGRES_DB=library_db
POSTGRES_USER=library_user
POSTGRES_PASSWORD=library_pass
```

Имя пользователя  admin
Адрес электронной почты: admin@mail.ru
Password: admin


{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2Mjc0MjMzMSwiaWF0IjoxNzYwMTUwMzMxLCJqdGkiOiJhMDA3M2U4NTIzOGY0ZjlmYTZhYTFlYzY3MWIwZDczMCIsInVzZXJfaWQiOiIxIn0.s3TWCGdFj1ULmBrN6nPofvJdYZQ0h0aV06nNWbs643Y",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYwMTY5NTMxLCJpYXQiOjE3NjAxNTAzMzEsImp0aSI6IjhhZDg2ZWNlNmYzYzQyZTNiZWI2YzkwZjhiZDY5Njg3IiwidXNlcl9pZCI6IjEifQ.guRP9mdKdtOldEZw_4hbMHmQldX7QDb9Nlg-UbwUBRA"
}


{
    "username": "ayan",
    "email": "ayan@example.com",
    "first_name": "Ayan",
    "last_name": "Kharitonov"
}
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MjgxNTQxNywiaWF0IjoxNzYwMjIzNDE3LCJqdGkiOiI1ZGQ3MDhhZTc0YzI0ZjEwOTEwNDViZjA5MTlmMDY4MyIsInVzZXJfaWQiOiI0In0.P0_xkytqMgZXm_0qBw9YJs-L5M9UOtas85PqCKctrCY",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYwMjQyNjE3LCJpYXQiOjE3NjAyMjM0MTcsImp0aSI6Ijk2NDBmNGFmMGI4ZjQxNjZhMTJlYzg3MDc1NjU1YjQ4IiwidXNlcl9pZCI6IjQifQ.CZ9_iblgeuAcOqfupawnCxjYghwKz_Qw24vyG18r5GA"
}

{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYwMjQyODIzLCJpYXQiOjE3NjAyMjM2MjMsImp0aSI6IjIzNDBhNmYxMzQ3ZjRmOWJiZTcwMGYwOTVlYmI0MTUyIiwidXNlcl9pZCI6IjQifQ.bGAyBUVWY81l1jvrHHpRVmnrl2oG29RPt_8BINkLjLs"
}

{
    "id": 4,
    "username": "ayan",
    "email": "ayan@example.com",
    "first_name": "Ayan",
    "last_name": "Kharitonov",
    "is_staff": true
}