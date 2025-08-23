from django.test import TestCase

from users.models import CustomUser
from users.serializers import CustomUserSerializer


class CustomUserSerializerTestCase(TestCase):
    """
    Тестовый класс для сериализатора CustomUserSerializer.

    Этот класс содержит тесты для проверки функциональности создания и обновления
    экземпляров модели CustomUser через сериализатор.
    """

    def setUp(self):
        """
        Настройка тестового окружения.

        Создает тестового пользователя, который будет использоваться в тестах.
        """
        self.user = CustomUser.objects.create_user(
            email="test@example.com", username="testuser", password="securepassword"
        )

    def test_create_user_valid_data(self):
        """
        Тестирование создания пользователя с валидными данными.

        Проверяет, что сериализатор корректно создает нового пользователя
        с указанными данными и что пароль хешируется правильно.
        """
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newsecurepassword",
            "phone": "1234567890",
            "city": "New City",
            "avatar": None,  # или путь к тестовому изображению
        }
        serializer = CustomUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.email, data["email"])
        self.assertTrue(
            user.check_password(data["password"])
        )  # Проверка хеширования пароля

    def test_create_user_missing_password(self):
        """
        Тестирование создания пользователя без пароля.

        Проверяет, что сериализатор выдает ошибку, если пароль не указан
        в данных для создания пользователя.
        """
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "phone": "1234567890",
            "city": "New City",
        }
        serializer = CustomUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_update_user_valid_data(self):
        """
        Тестирование обновления пользователя с валидными данными.

        Проверяет, что сериализатор корректно обновляет данные существующего
        пользователя, включая изменение пароля, и что новый пароль хешируется правильно.
        """
        data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "phone": "0987654321",
            "city": "Updated City",
            "password": "newsecurepassword",  # Убедитесь, что новый пароль указан
        }
        serializer = CustomUserSerializer(instance=self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.username, data["username"])
        self.assertEqual(updated_user.email, data["email"])
        self.assertTrue(
            updated_user.check_password(data["password"])
        )  # Проверка нового пароля

    def test_update_user_email_taken(self):
        """
        Тестирование обновления пользователя с занятым адресом электронной почты.

        Проверяет, что сериализатор выдает ошибку, если новый адрес электронной почты
        уже занят другим пользователем.
        """
        CustomUser.objects.create_user(
            email="taken@example.com", username="takenuser", password="securepassword"
        )
        data = {
            "email": "taken@example.com",  # email уже занят
            "username": "updateduser",
        }
        serializer = CustomUserSerializer(instance=self.user, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_update_user_username_taken(self):
        """
        Тестирование обновления пользователя с занятым именем пользователя.

        Проверяет, что сериализатор выдает ошибку, если новое имя пользователя
        уже занято другим пользователем.
        """
        CustomUser.objects.create_user(
            email="another@example.com", username="takenuser", password="securepassword"
        )
        data = {
            "username": "takenuser",  # username уже занят
        }
        serializer = CustomUserSerializer(instance=self.user, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)
