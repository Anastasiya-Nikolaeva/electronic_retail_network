from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Менеджер для модели CustomUser.

    Этот менеджер предоставляет методы для создания обычных пользователей и суперпользователей.
    """

    def create_user(self, email, username, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя с указанным адресом электронной почты и паролем.

        Параметры:
        email (str): Адрес электронной почты пользователя. Обязательное поле.
        username (str): Имя пользователя. Обязательное поле.
        password (str, optional): Пароль для пользователя. Обязательное поле; вызывает исключение, если не указано.
        **extra_fields: Дополнительные поля для пользователя.

        Возвращает:
        CustomUser: Созданный пользователь.

        Исключения:
        ValueError: Если адрес электронной почты или имя пользователя не указаны, или если пароль не установлен.
        """
        if not email:
            raise ValueError("Поле электронной почты должно быть заполнено")
        if not username:
            raise ValueError("Поле имени пользователя должно быть заполнено")
        if password is None:
            raise ValueError("Пароль должен быть установлен")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя (администратора) с указанным адресом электронной почты и паролем.

        Параметры:
        email (str): Адрес электронной почты суперпользователя. Обязательное поле.
        username (str): Имя пользователя суперпользователя. Обязательное поле.
        password (str, optional): Пароль для суперпользователя. Обязательное поле.
        **extra_fields: Дополнительные поля для суперпользователя.

        Возвращает:
        CustomUser: Созданный суперпользователь.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Пользовательская модель.

    Эта модель расширяет стандартную модель пользователя, добавляя дополнительные поля,
    такие как номер телефона, город и аватар.
    """

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Телефон"
    )
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Фото"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        """
        Возвращает строковое представление пользователя, используя его адрес электронной почты.

        Возвращает:
        str: Адрес электронной почты пользователя.
        """
        return self.email
