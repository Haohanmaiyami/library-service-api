from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers

from .models import Author, Book, Borrow


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "birth_year"]

    def validate_birth_year(self, value):
        if value and (value < 1000 or value > timezone.now().year):
            raise serializers.ValidationError("Год рождения вне допустимого диапазона.")
        return value


class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "book_id",
            "published_year",
            "pages",
            "genre",
            "description",
        ]

    def validate_book_id(self, value):
        v = value.strip()
        if not v:
            raise serializers.ValidationError("Book ID не может быть пустым.")
        qs = Book.objects.filter(book_id=v)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Книга с таким Book ID уже существует.")
        return v

    def validate_published_year(self, value):
        if value and (value < 1400 or value > timezone.now().year + 1):
            raise serializers.ValidationError(
                "Год публикации вне допустимого диапазона."
            )
        return value

    def validate_pages(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Количество страниц должно быть > 0.")
        return value


class BorrowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Borrow
        fields = ["id", "user", "book", "borrowed_at", "due_at", "returned_at"]
        read_only_fields = ["borrowed_at", "returned_at"]

    def validate(self, attrs):
        book = attrs.get("book")
        due_at = attrs.get("due_at")
        if due_at is None:
            raise serializers.ValidationError(
                {"due_at": "Нужно указать срок возврата."}
            )
        if due_at <= timezone.now():
            raise serializers.ValidationError(
                {"due_at": "Срок возврата должен быть в будущем."}
            )
        if Borrow.objects.filter(book=book, returned_at__isnull=True).exists():
            raise serializers.ValidationError(
                {"book": "Книга уже выдана (есть активный Borrow)."}
            )
        return attrs


User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    """Безопасные поля профиля для ответа наружу."""

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "is_staff")


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Регистрация: принимает пароль дважды, валидирует по Django validators,
    создаёт пользователя через create_user (пароль хэшируется).
    """

    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
        )
        # делаем нефундаментальные поля необязательными
        extra_kwargs = {
            "email": {"required": False, "allow_blank": True},
            "first_name": {"required": False, "allow_blank": True},
            "last_name": {"required": False, "allow_blank": True},
        }

    def validate_username(self, value: str) -> str:
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким username уже существует."
            )
        return value

    def validate_email(self, value: str) -> str:
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует."
            )
        return value

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError({"password2": "Пароли не совпадают."})
        # Стандартные валидаторы Django
        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user
