# config/test_settings.py
from .settings import *

# Тесты гоняем на SQLite (в памяти)
DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": ":memory:",
}