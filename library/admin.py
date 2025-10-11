from django.contrib import admin
from .models import Author, Book, Borrow


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "birth_year")
    search_fields = ("first_name", "last_name")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "book_id", "genre", "published_year")
    list_filter = ("genre", "published_year")
    search_fields = ("title", "book_id")


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "borrowed_at", "due_at", "returned_at")
    list_filter = ("returned_at",)
    search_fields = ("book__title", "user__username")
