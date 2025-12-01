# 📚 Library Management API — DRF Diploma Project (DF1)

**Goal:** REST API for library management: books, authors, users and borrows.  
**Stack:** Django 5, Django REST Framework, SimpleJWT, PostgreSQL, drf-spectacular, Docker Compose.

---

## 🚀 Run with Docker

1) Generate `requirements.txt` from Poetry:

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

2) Build and start containers:

```bash
docker compose up --build
```

---

## 🌐 URLs

Application:  
http://localhost:8000  

Swagger UI:  
http://localhost:8000/api/docs/  

Redoc:  
http://localhost:8000/api/redoc/  

OpenAPI JSON:  
http://localhost:8000/api/schema/  

---

## 💻 Local run (without Docker)

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
```

---

## 👤 Creating a superuser in the container

```bash
# after the first container start
docker compose exec web python manage.py createsuperuser
# then get admin JWT via /api/auth/jwt/create/
```

---

## 🔐 Authentication (JWT)

### Endpoints

- `POST /api/auth/jwt/create/` — get access/refresh tokens  
- `POST /api/auth/jwt/refresh/` — refresh access token  

All protected endpoints require a valid **access** token in the `Authorization: Bearer <token>` header.

---

# 📡 API Endpoints

## 👥 Authors

- `GET /api/authors/?search=tolstoy&ordering=last_name` — list with search and ordering  
- `POST /api/authors/` — create (staff only)  
- `GET /api/authors/{id}/` — retrieve  
- `PUT /api/authors/{id}/` — full update (staff only)  
- `PATCH /api/authors/{id}/` — partial update (staff only)  
- `DELETE /api/authors/{id}/` — delete (staff only)  

---

## 📘 Books

- `GET /api/books/?title=&author=&genre=&book_id=` — list with filters/search  
- `POST /api/books/` — create (staff only)  
- `GET /api/books/{id}/` — retrieve  
- `PUT /api/books/{id}/` — full update (staff only)  
- `PATCH /api/books/{id}/` — partial update (staff only)  
- `DELETE /api/books/{id}/` — delete (staff only)  

```text
Book fields:
- title
- author
- book_id (unique)
- published_year
- pages
- genre
- description
```

---

## 📚 Borrows

- `GET /api/borrows/`  
  - staff users see **all** borrows  
  - regular users see **only their own** records  

- `POST /api/borrows/?target_user=<id>` — issue a book to user `<id>` (staff only)  

- `POST /api/borrows/{id}/return_book/` — close a borrow / mark as returned (staff only)  

---

## 🛡️ Permissions

- **IsAdminOrReadOnly** — used for authors and books  
  - safe methods (GET, HEAD, OPTIONS) — available to everyone  
  - write operations (POST, PUT, PATCH, DELETE) — **staff only**

- **IsStaffForMutationOrOwnerRead** — used for borrows  
  - staff can create and modify any borrow  
  - regular user can **only read** their own borrows  

---

## ✅ Validation (Serializers)

- `book_id` — required and unique  
- `published_year` — must be within a reasonable range  
- `pages` — must be `> 0`  
- `due_at` — must be in the future  
- second active borrow of the **same book** for the same user is forbidden  

---

## 🧹 Code style (PEP8)

PEP8 is enforced with:

- **flake8** — linting  
- **black** — formatting  

---

## 🗄️ Database

PostgreSQL is started via `docker-compose` (service `db`).  
Environment variables are configured via `.env` file and used in `docker-compose.yml`.

---

## ⚙️ Environment variables (`.env.example`)

### Django

```bash
SECRET_KEY=change_me
DEBUG=1
ALLOWED_HOSTS=*
```

### Database (PostgreSQL)

```bash
POSTGRES_DB=library_db
POSTGRES_USER=library_user
POSTGRES_PASSWORD=library_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

---

## 👨‍💻 Default admin credentials (for testing)

- Username: `admin`  
- Email: `admin@mail.ru`  
- Password: `admin`




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

## Доступы:

Приложение: http://localhost:8000

Swagger UI: http://localhost:8000/api/docs/

Redoc: http://localhost:8000/api/redoc/

OpenAPI JSON: http://localhost:8000/api/schema/

## Локальный запуск (без Docker)

```
poetry install
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
```

## Создание суперпользователя в контейнере

```
# после первого запуска контейнеров
docker compose exec web python manage.py createsuperuser
# затем получи JWT админа через /api/auth/jwt/create/
```


## Аутентификация (JWT)

#### Эндпоинты:

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


## PEP8

- Поддерживается с помощью flake8 (проверка) и black (форматирование).

## База данных

PostgreSQL поднимается через docker-compose (сервис db).
Переменные окружения в docker-compose.yml:

# .env.example

## Django
```commandline
SECRET_KEY=change_me
DEBUG=1
ALLOWED_HOSTS=*
```


## Database (PostgreSQL)
```
POSTGRES_DB=library_db
POSTGRES_USER=library_user
POSTGRES_PASSWORD=library_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
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

done
