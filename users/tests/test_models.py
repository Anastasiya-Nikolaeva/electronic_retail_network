from django.db import IntegrityError
from django.test import TestCase

from users.models import CustomUser


class CustomUserManagerTests(TestCase):
    """
    Тестовый класс для менеджера CustomUserManager.

    Этот класс содержит тесты для проверки функциональности создания
    обычных пользователей и суперпользователей.
    """

    def setUp(self):
        """
        Настройка тестового окружения.

        Создает тестовые данные для использования в тестах.
        """
        self.email = "testuser@example.com"
        self.username = "testuser"
        self.password = "testpassword"

    def test_create_user(self):
        """
        Тестирование создания обычного пользователя.

        Проверяет, что менеджер корректно создает нового пользователя
        с указанными данными и что пароль хешируется правильно.
        """
        user = CustomUser.objects.create_user(
            email=self.email, username=self.username, password=self.password
        )
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.username, self.username)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        """
        Тестирование создания суперпользователя.

        Проверяет, что менеджер корректно создает суперпользователя
        с указанными данными и что все соответствующие поля установлены.
        """
        superuser = CustomUser.objects.create_superuser(
            email=self.email, username=self.username, password=self.password
        )
        self.assertEqual(superuser.email, self.email)
        self.assertEqual(superuser.username, self.username)
        self.assertTrue(superuser.check_password(self.password))
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_user_without_email(self):
        """
        Тестирование создания пользователя без адреса электронной почты.

        Проверяет, что менеджер выдает ошибку, если адрес электронной почты не указан.
        """
        with self.assertRaises(ValueError) as context:
            CustomUser.objects.create_user(
                email="", username=self.username, password=self.password
            )
        self.assertEqual(
            str(context.exception), "Поле электронной почты должно быть заполнено"
        )

    def test_create_user_without_username(self):
        """
        Тестирование создания пользователя без имени пользователя.

        Проверяет, что менеджер выдает ошибку, если имя пользователя не указано.
        """
        with self.assertRaises(ValueError) as context:
            CustomUser.objects.create_user(
                email=self.email, username="", password=self.password
            )
        self.assertEqual(
            str(context.exception), "Поле имени пользователя должно быть заполнено"
        )

    def test_create_user_without_password(self):
        """
        Тестирование создания пользователя без пароля.

        Проверяет, что менеджер выдает ошибку, если пароль не установлен.
        """
        with self.assertRaises(ValueError) as context:
            CustomUser.objects.create_user(
                email=self.email, username=self.username, password=None
            )
        self.assertEqual(str(context.exception), "Пароль должен быть установлен")

    def test_str_method(self):
        """
        Тестирование метода __str__.

        Проверяет, что метод __str__ возвращает адрес электронной почты пользователя.
        """
        user = CustomUser.objects.create_user(
            email=self.email, username=self.username, password=self.password
        )
        self.assertEqual(str(user), self.email)


class CustomUserModelTests(TestCase):
    """
    Тестовый класс для модели CustomUser.

    Этот класс содержит тесты для проверки функциональности модели
    CustomUser, включая уникальность полей и обновление данных.
    """

    def setUp(self):
        """
        Настройка тестового окружения.

        Создает тестового пользователя для использования в тестах.
        """
        self.email = "testuser@example.com"
        self.username = "testuser"
        self.password = "testpassword"
        self.user = CustomUser.objects.create_user(
            email=self.email, username=self.username, password=self.password
        )

    def test_user_fields(self):
        """
        Тестирование полей пользователя.

        Проверяет, что поля phone, city и avatar инициализируются как None
        при создании нового пользователя.
        """
        self.assertEqual(self.user.phone, None)
        self.assertEqual(self.user.city, None)
        self.assertEqual(self.user.avatar, None)

    def test_unique_email(self):
        """
        Тестирование уникальности адреса электронной почты.

        Проверяет, что при попытке создать пользователя с уже существующим
        адресом электронной почты возникает ошибка IntegrityError.
        """
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                email=self.email, username="anotheruser", password="anotherpassword"
            )

    def test_unique_username(self):
        """
        Тестирование уникальности имени пользователя.

        Проверяет, что при попытке создать пользователя с уже существующим
        именем пользователя возникает ошибка IntegrityError.
        """
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                email="anotheruser@example.com",
                username=self.username,
                password="anotherpassword",
            )

    def test_update_user(self):
        """
        Тестирование обновления данных пользователя.

        Проверяет, что можно обновить поля phone и city у существующего
        пользователя и что изменения сохраняются в базе данных.
        """
        self.user.phone = "1234567890"
        self.user.city = "Москва"
        self.user.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, "1234567890")
        self.assertEqual(self.user.city, "Москва")

    def test_user_authentication(self):
        """
        Тестирование аутентификации пользователя.

        Проверяет, что метод check_password возвращает True для правильного пароля.
        """
        self.assertTrue(self.user.check_password(self.password))

    def test_inactive_user(self):
        """
        Тестирование состояния неактивного пользователя.

        Проверяет, что поле is_active можно установить в False и что
        это изменение сохраняется в базе данных.
        """
        self.user.is_active = False
        self.user.save()
        self.assertFalse(self.user.is_active)
