from .settings import *  # noqa: F401,F403

# Тесты гоняем на SQLite (в памяти)
DATABASES["default"] = {  # noqa: F405
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": ":memory:",
}
