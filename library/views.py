from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Author, Book, Borrow
from .serializers import AuthorSerializer, BookSerializer, BorrowSerializer
from .permissions import IsAdminOrReadOnly, IsStaffForMutationOrOwnerRead

User = get_user_model()

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by("last_name", "first_name")
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["last_name", "birth_year", "first_name"]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("author").all().order_by("title")
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["title", "genre", "book_id", "author__last_name", "author__first_name"]
    ordering_fields = ["title", "published_year", "pages"]

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params
        if title := q.get("title"):
            qs = qs.filter(title__icontains=title)
        if author := q.get("author"):   # ID автора
            qs = qs.filter(author_id=author)
        if genre := q.get("genre"):
            qs = qs.filter(genre__icontains=genre)
        if book_id := q.get("book_id"):
            qs = qs.filter(book_id__icontains=book_id)
        return qs

class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.select_related("book", "user").all()
    serializer_class = BorrowSerializer
    permission_classes = [IsStaffForMutationOrOwnerRead]
    search_fields = ["book__title", "user__username"]
    ordering_fields = ["borrowed_at", "due_at", "returned_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user and user.is_staff:
            return qs
        return qs.filter(user=user)

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionError("Только персонал может создавать выдачи.")
        target_user_id = self.request.query_params.get("target_user")
        target_user = get_object_or_404(User, id=target_user_id)
        serializer.save(user=target_user)

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        if not request.user.is_staff:
            return Response({"detail": "Только персонал может закрывать выдачу."}, status=status.HTTP_403_FORBIDDEN)
        borrow = self.get_object()
        if borrow.returned_at:
            return Response({"detail": "Книга уже возвращена."}, status=status.HTTP_400_BAD_REQUEST)
        from django.utils import timezone
        borrow.returned_at = timezone.now()
        borrow.save(update_fields=["returned_at"])
        return Response(BorrowSerializer(borrow).data, status=status.HTTP_200_OK)
