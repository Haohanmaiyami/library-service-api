from django.conf import settings
from django.db import models
from django.utils import timezone

class Author(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120, db_index=True)
    birth_year = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        unique_together = [("first_name", "last_name", "birth_year")]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()

class Book(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="books")
    book_id = models.CharField(max_length=50, unique=True, db_index=True)  # внутренний ID
    published_year = models.PositiveIntegerField(null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    genre = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["title"]
        indexes = [models.Index(fields=["title", "genre", "book_id"])]

    def __str__(self):
        return f"{self.title} ({self.book_id})"

class Borrow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrows")
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="borrows")
    borrowed_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-borrowed_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["book"],
                condition=models.Q(returned_at__isnull=True),
                name="uniq_active_borrow_per_book",
            )
        ]

    def __str__(self):
        return f"{self.user} -> {self.book} ({'returned' if self.returned_at else 'active'})"
